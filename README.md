# Email Drafting Agent

The Email Drafting Agent transforms concise bullet‑point inputs into polished, professional emails in English or Spanish. Built on the GenAI AgentOS platform, it generates context‑aware subjects, natural greetings and closings, and well‑structured body content, with all outputs logged via MLflow for auditability.

## Key Features

- **Bullet‑to‑Email Transformation**: Map bullet points (recipient, purpose, details) to a formatted email.
- **Multilingual Support**: Automatic greetings, body rewriting, and closings in English (`en`) or Spanish (`es`).
- **Customizable Tone**: Specify tone (`formal`, `friendly`, `urgent`, technical) via CLI flag.
- **Robust Parsing**: Accepts bullets marked with `•`, `-`, `*`, numbered lists, and continuations.
- **Style‑Guide Enforcement**: Oxford commas, parallel list structure, title‑case subjects, and proper punctuation.
- **JSON/Code Payloads**: Includes sample payloads or code snippets verbatim.
- **CI/CD and Observability**: Linted, type‑checked, unit‑tested, and logged to MLflow.

## Architecture

1. AgentOS Entry Point: `compose_email` function (AgentOS CLI).
2. Agent Logic: `EmailDraftingAgent` in `agent.py` parses input and applies NLG rules.
3. NLG Helpers: `rewrite_purpose` and `rewrite_detail` in `nlg.py` produce natural sentences.
4. Output:
- STDOUT: Immediate email preview.
- MLflow: Saves `email.txt` artifact under each run.

## Prerequisites

- Python 3.9 or later
- Virtual environment (`venv`, `virtualenv`)
- GenAI AgentOS CLI
- MLflow installed

## Installation

```bash
git clone https://github.com/<your-username>/email-drafting-agent.git
cd email-drafting-agent
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## AgentOS Component Registration

Register the email agent with a descriptive name and entry point:

```bash
agentos register email_agent \
  --entry-point compose_email \
  -r components.yaml \
  --description "Generate professional emails from bullets (en/es)"
```

## Usage

Execute the agent using the CLI:

```bash
agentos run email_agent \
  --use-outer-env \
  --entry-point compose_email \
  -r components.yaml \
  -A bullets=$'• Recipient: María\n• Purpose: Seguimiento\n• Completed the task' \
  -A sender_name="Ana" \
  -A tone="friendly" \
  -A language="es"
```

- Output: The terminal displays the formatted email.
- Artifact: Retrieve `email.txt` from `mlruns/<experiment>/0/<run-id>/artifacts/email.txt`.

## Configuration Options

| Flag          | Description                                            | Example                |
| ------------- | ------------------------------------------------------ | ---------------------- |
| `bullets`     | Bullet points with recipient, purpose, and key details | `-A bullets="$..."`    |
| `sender_name` | Name to appear in the closing                          | `-A sender_name="Ana"` |
| `tone`        | Tone of the email (`formal`, `friendly`, etc.)         | `-A tone="friendly"`   |
| `language`    | Output language (`en` or `es`)                         | `-A language="es"`     |


## Example Output

English

```bash
Subject: Follow-Up

Hello Maria,

I wanted to follow up on your request. I have completed the task.

Best regards,
Ana
```

Spanish

```bash
Subject: Seguimiento

Hola María,

Quería darle seguimiento a tu solicitud. Ya he completado la tarea.

Saludos,
Ana
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