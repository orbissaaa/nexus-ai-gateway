---
name: Bug report
about: Create a report to help us improve
title: "[Bug]:"
labels: bug
assignees: orbissaaa

---

name: Bug report
description: File a bug report to help us improve NexusAI Gateway
title: "[BUG] "
labels: ["bug", "needs-triage"]
body:
  - type: markdown
  - type: input
    id: summary
    attributes:
      label: Bug Summary
      description: A brief, clear summary of what the bug is.
      placeholder: e.g. API Rotator fails when Groq hits rate limit.
    validations:
      required: true
  - type: textarea
    id: reproduce
    attributes:
      label: Steps to Reproduce
      description: How can we reproduce this issue?
      placeholder: |
        1. Run main.py
        2. Send request to endpoint...
        3. See error...
    validations:
      required: true
  - type: textarea
    id: expected
    attributes:
      label: Expected Behavior
      description: What did you expect to happen?
      placeholder: It should automatically rotate to the next active key.
    validations:
      required: true
  - type: textarea
    id: environment
    attributes:
      label: Environment & Version
      description: What OS, Python version, and gateway version are you using?
      placeholder: |
        - OS: Windows 11 / Ubuntu 22.04 / macOS
        - Python version: 3.10
        - Gateway Version: v1.0.0
    validations:
      required: true
  - type: textarea
    id: optional_info
    attributes:
      label: Optional Addition / Extra Information
      description: Add any other context, screenshots, or logs about the problem here.
      placeholder: Paste any error traceback or extra logs here.
    validations:
      required: false
