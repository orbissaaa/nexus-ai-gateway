# Universal Multi-Provider AI Gateway

هذا المشروع عبارة عن بوابة FastAPI متوافقة مع واجهة OpenAI، وتستخدم تدويرًا دائريًا بين مزودين متوافقين مع OpenAI تم إعدادهم بواسطة مالك النظام. عند استقبال HTTP 429، تُدخل البوابة المفتاح في فترة تهدئة، ثم تنتقل تلقائيًا إلى المفتاح التالي.

> استخدم فقط مفاتيح API التي تملكها أو لديك تفويض صريح لاستخدامها، والتزم بشروط كل مزود وحدود الخطط المجانية. التدوير لا يتجاوز حدود الحصة ولا يلغيها؛ هو آلية توفر واستمرارية لخدمة مصرح بها.

## الملفات

| الملف | الغرض |
|---|---|
| `core/config.py` | قراءة إعدادات `.env` حتى 100 مزود |
| `core/quota_tracker.py` | تسجيل 429 وفترة التهدئة وإعادة التفعيل |
| `core/rotator.py` | Round-robin وfailover باستخدام `httpx.AsyncClient` |
| `api/routes.py` | مسارا `/v1/chat/completions` و`/v1/health` |
| `main.py` | إنشاء تطبيق FastAPI وتشغيل Uvicorn |
| `test_client.py` | عميل اختبار محلي |

## التشغيل

1. أنشئ بيئة افتراضية وثبّت المتطلبات:

```bash
cd ai_gateway
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. انسخ ملف البيئة وعدّله:

```bash
cp .env.example .env
```

يجب أن يحتوي كل مزود على `NAME` و`KEY` و`MODEL`. الحقل `BASE_URL` اختياري، وقيمته الافتراضية `https://api.openai.com/v1`.

3. شغّل الخدمة:

```bash
python main.py
```

أو:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

4. افحص الحالة:

```bash
curl http://127.0.0.1:8000/v1/health
```

5. اختبر طلب محادثة:

```bash
python test_client.py --message "اكتب تحية قصيرة"
```

إذا تم ضبط `GATEWAY_API_KEY` في `.env`، فسيضيف `test_client.py` المفتاح تلقائيًا عند وجود المتغير نفسه في بيئة جلسة الاختبار.

## مثال عميل OpenAI

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://127.0.0.1:8000/v1",
    api_key="replace-with-your-gateway-key",
)

response = client.chat.completions.create(
    model="gateway-default",
    messages=[{"role": "user", "content": "Hello"}],
)
print(response.choices[0].message.content)
```

## ملاحظات سلوكية

- الطلب الوارد يُرسل إلى المزود باستخدام `PROVIDER_X_MODEL`، لذلك لا يُفترض أن يتطابق اسم النموذج الوارد مع نماذج جميع المزودين.
- تستمر البوابة في تجربة المزود التالي عند أخطاء الشبكة و429 و5xx.
- أخطاء 4xx الأخرى تُعاد للعميل لأنها غالبًا أخطاء طلب أو تفويض وليست إشارة آمنة للتدوير.
- الإصدار الحالي يعيد JSON غير متدفق؛ الطلبات التي تحتوي `stream: true` تُرفض برسالة واضحة بدل إعطاء سلوك غير متوافق.
- سجل التهدئة محفوظ في الذاكرة، ويُعاد ضبطه عند إعادة تشغيل العملية.
- لا تُسجّل مفاتيح API في السجلات أو استجابات HTTP.
