# Email Drafting Agent

**Transform bullet-point inputs into polished, professional emails**—in English or Spanish—using a GenAI-powered AgentOS component. Outputs are type-checked, linted, unit-tested, and logged via MLflow for full auditability.

---

## 📝 Key Features

- **Bullet→Email Transformation**  
  Converts concise bullets (`Recipient:…`, `Purpose:…`, `Changes:…`, etc.) into full emails with subject, greeting, body, and closing.

- **Multilingual & Tone Control**  
  English (`en`) or Spanish (`es`), with tones: `formal`, `friendly`, `urgent`, or `technical`.

- **Style-Guide Enforcement**  
  Oxford commas, parallel lists, title-case subjects, proper sentence casing, and punctuation.

- **Code & JSON Payloads**  
  Preserves fenced code/JSON blocks verbatim (indented for readability).

- **CI/CD & Observability**  
  — Linted (`flake8`), type-checked (`mypy`), unit-tested (`pytest`), and logged to MLflow.

---

## 🚀 Architecture

1. **Entry Point**: `compose_email` (AgentOS CLI)  
2. **Core Logic**:  
   - **`agent.py`**: `EmailDraftingAgent` parses bullets, builds subject & body.  
   - **`nlg.py`**: `rewrite_purpose` & `rewrite_detail` craft natural sentences.  
   - **`subject_transformer.py`**: Title-cases & Oxford-comma-joins subjects.  
3. **Outputs**:  
   - **STDOUT**: Immediate email preview.  
   - **MLflow**: `email.txt` artifact per run.

---

## 🛠 Prerequisites & Installation

```bash
# Clone & set up venv
git clone https://github.com/<you>/email-drafting-agent.git
cd email-drafting-agent
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

```

## 📦 Register with AgentOS

Register the email agent with a descriptive name and entry point:

```bash
agentos register email_agent \
  --entry-point compose_email \
  -r components.yaml \
  --description "Generate professional emails from bullets (en/es)"
```

## 💻 Usage

Run from the CLI with your bullets. Here’s the example we tested:

```bash
## Usage

Run the agent via AgentOS CLI with your bullet input:

```bash
agentos run email_agent \
  --use-outer-env \
  -r components.yaml \
  --entry-point compose_email \
  -A bullets=$'• Recipients: Backend Team; QA & DevOps\n• Purpose: Review API changes, share sample payload, and update docs\n• Changes:\n  1. Added `POST /v2/users` endpoint\n     - Request body now requires `email_verified: boolean`\n       * Must log timestamp in ISO format\n       * Default to `false` if missing\n     - Deprecates `username` field in response\n  2. Error codes revamped for 400, 401, 403\n  3. Rate limits set to 1000 RPM\n• Sample payload (JSON):\n  ```json\n  {\n    \"email\": \"user@example.com\",\n    \"email_verified\": true,\n    \"roles\": [\"user\",\"admin\"]\n  }\n  ```\n• Docs update: see `docs/api_v2.md` for full spec\n• Deadline: EOD Friday (UTC−07:00)' \
  -A sender_name="Ana" \
  -A tone="technical" \
  -A language="en"
```

- Output: Email printed to console
- Artifact: retrieve from `mlruns/<experiment>/0/<run-id>/artifacts/email.txt`

## Configuration Options

| Flag          | Description                                            | Example                |
| ------------- | ------------------------------------------------------ | ---------------------- |
| `bullets`     | Bullet points with recipient, purpose, and key details | `-A bullets="$..."`    |
| `sender_name` | Name to appear in the closing                          | `-A sender_name="Ana"` |
| `tone`        | Tone of the email (`formal`, `friendly`, etc.)         | `-A tone="friendly"`   |
| `language`    | Output language (`en` or `es`)                         | `-A language="es"`     |


## Example Output

**Command:**

```bash
agentos run email_agent \
  --use-outer-env \
  -r components.yaml \
  --entry-point compose_email \
  -A bullets=$'• Recipients: Backend Team; QA & DevOps\n• Purpose: Review API changes, share sample payload, and update docs\n• Changes:\n  1. Added `POST /v2/users` endpoint\n     - Request body now requires `email_verified: boolean`\n       * Must log timestamp in ISO format\n       * Default to `false` if missing\n     - Deprecates `username` field in response\n  2. Error codes revamped for 400, 401, 403\n  3. Rate limits set to 1000 RPM\n• Sample payload (JSON):\n  ```json\n  {\n    \"email\": \"user@example.com\",\n    \"email_verified\": true,\n    \"roles\": [\"user\",\"admin\"]\n  }\n  ```\n• Docs update: see `docs/api_v2.md` for full spec\n• Deadline: EOD Friday (UTC−07:00)' \
  -A sender_name=\"Ana\" \
  -A tone=\"technical\"
```

**Output**:

```bash
Subject: Review API Changes, Share Sample Payload, & Update Docs

Good afternoon, Backend Team and QA & DevOps,

I'm writing to review the API changes, share the sample payload, and update the documentation.

Changes:
- Added `POST /v2/users` endpoint.
- Request body now requires `email_verified: boolean`.
- Must log timestamp in ISO format.
- Default to `false` if missing.
- Deprecates `username` field in response.
- Error codes revamped for 400, 401, 403.
- Rate limits set to 1,000 RPM.

  ```json
  {
    "email": "user@example.com",
    "email_verified": true,
    "roles": ["user", "admin"]
  }
    ```
See docs/api_v2.md for full spec.
Deadline: EOD Friday (UTC-07:00).

Sincerely,
Ana
```

## Live Demo

Expose your agent over HTTP (e.g. ngrok) and test with:

```bash
curl -X POST https://1234abcd.ngrok.io/draft_email \
  -H "Content-Type: application/json" \
  -d '{
    "bullets": "• Recipients: Backend Team; QA & DevOps\n• Purpose: Review API changes, share sample payload, and update docs\n• Changes:\n  1. Added `POST /v2/users` endpoint\n     - Request body now requires `email_verified: boolean`\n       * Must log timestamp in ISO format\n       * Default to `false` if missing\n     - Deprecates `username` field in response\n  2. Error codes revamped for 400, 401, 403\n  3. Rate limits set to 1000 RPM\n• Sample payload (JSON):\n  ```json\n  {\n    \"email\": \"user@example.com\",\n    \"email_verified\": true,\n    \"roles\": [\"user\",\"admin\"]\n  }\n  ```\n• Docs update: see `docs/api_v2.md` for full spec\n• Deadline: EOD Friday (UTC−07:00)'",
    "sender_name": "Ana",
    "tone": "technical",
    "language": "en"
}'
```

Expected JSON response:

```bash
{
  "subject": "Review API Changes, Share Sample Payload, & Update Docs",
  "email": "Good afternoon, Backend Team and QA & DevOps,\n\nI'm writing to review the API changes, share the sample payload, and update the documentation.\n\nChanges:\n- Added `POST /v2/users` endpoint.\n- Request body now requires `email_verified: boolean`.\n- Must log timestamp in ISO format.\n- Default to `false` if missing.\n- Deprecates `username` field in response.\n- Error codes revamped for 400, 401, 403.\n- Rate limits set to 1,000 RPM.\n\n  ```json\n  {\n    \"email\": \"user@example.com\",\n    \"email_verified\": true,\n    \"roles\": [\"user\", \"admin\"]\n  }\n  ```\n\nSee `docs/api_v2.md` for full spec.\n\nDeadline: EOD Friday (UTC−07:00).\n\nSincerely,\nAna"
}
```

## Testing and CI/CD

- Unit Tests: in `email_agent/tests/`, covering parsing and NLG logic.
- CI Pipeline: `.github/workflows/ci.yml` runs flake8, mypy, pytest, and stores results.

## Monitoring and Observability

- **MLflow UI**: Visualize runs, compare outputs, and download artifacts.
- **Structured Logging**: Timestamps, execution metrics, and error tracking.

## Optional Live Demo

Expose a local HTTP endpoint via ngrok for interactive testing:
```bash
ngrok http 8000
```

## Contributing 

Contributions are welcome. Please fork the repository and submit pull requests for enhancements or fixes.