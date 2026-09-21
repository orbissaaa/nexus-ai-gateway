# 🚀 NexusAI Gateway

> A lightning-fast, production-ready Multi-Provider AI Gateway & API Rotator built with FastAPI. Features automatic quota tracking, rate-limit handling, and seamless multi-key load balancing.

---

## 🌟 Features

* **Multi-Provider Support:** Seamlessly route requests across various AI providers (Groq, OpenRouter, OpenAI, etc.).
* **Automatic API Key Rotation:** Intelligent `QuotaTracker` automatically rotates keys upon hitting rate limits or quotas.
* **FastAPI Powered:** High-performance asynchronous backend with built-in automatic Swagger documentation (`/docs`).
* **Secure & Clean:** Strict `.env` isolation to keep your secret API keys safe.

---

## ⚙️ Installation & Setup

Choose your operating system below to set up and run the project locally:

### 🪟 Windows

1. **Clone the repository:**
```cmd
git clone https://github.com/orbissaaa/nexus-ai-gateway.git
cd nexus-ai-gateway

```


2. **Create and activate a virtual environment:**
```cmd
python -m venv .venv
.venv\Scripts\activate

```


3. **Install dependencies:**
```cmd
pip install -r requirements.txt

```


4. **Configure environment variables:**
* Copy the example environment file:
```cmd
copy .env.example .env

```


* Open the `.env` file and add your actual API keys.



---

### 🐧 Linux (Ubuntu / Debian / Kali Linux)

1. **Clone the repository:**
```bash
git clone https://github.com/orbissaaa/nexus-ai-gateway.git
cd nexus-ai-gateway

```


2. **Install python3-venv (if not already installed):**
```bash
sudo apt update && sudo apt install python3-venv python3-pip -y

```


3. **Create and activate a virtual environment:**
```bash
python3 -m venv .venv
source .venv/bin/activate

```


4. **Install dependencies:**
```bash
pip install -r requirements.txt

```


5. **Configure environment variables:**
* Copy the example environment file:
```bash
cp .env.example .env

```


* Open the `.env` file using your preferred editor (like `nano .env`) and add your actual API keys.



---

### 🍏 macOS

1. **Clone the repository:**
```bash
git clone https://github.com/orbissaaa/nexus-ai-gateway.git
cd nexus-ai-gateway

```


2. **Create and activate a virtual environment:**
```bash
python3 -m venv .venv
source .venv/bin/activate

```


3. **Install dependencies:**
```bash
pip install -r requirements.txt

```


4. **Configure environment variables:**
* Copy the example environment file:
```bash
cp .env.example .env

```


* Open the `.env` file and add your actual API keys.



---

## 🚀 Running the Server

Start the FastAPI server locally using Uvicorn:

```bash
python main.py

```

*(Or via uvicorn directly: `uvicorn main:app --host 127.0.0.1 --port 8000 --reload`)*

Once running, you can access:

* **Interactive API Docs (Swagger UI):** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs?utm_source=gemini)

---

## 🧪 Testing

Open a second terminal window (with the virtual environment activated) and run the test client:

```bash
python test_client.py

```

---

## 🤝 Support & Connect

If you like this project or find it helpful, please give it a ⭐️ star on GitHub!

* **GitHub:** [orbissaaa](https://github.com/orbissaaa)
* **Issues / Bugs:** If you encounter any issues, please open an [Issue](https://www.google.com/search?q=https://github.com/orbissaaa/nexus-ai-gateway/issues&utm_source=gemini).

---

## 📝 License

This project is open-source and available under the [MIT License](https://www.google.com/search?q=LICENSE&utm_source=gemini).
