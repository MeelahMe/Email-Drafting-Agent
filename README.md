# Overview

The Email Drafting Agent converts minimal bullet-point inputs into professional, multilingual email drafts. Leveraging the GenAI AgentOS platform, it streamlines email creation by generating:

A clear, context-aware subject line

Natural greetings and closings in English or Spanish

Concise, well-structured body paragraphs

All outputs are logged as MLflow artifacts for auditability and version control.

## Key Features

- **Bullet-to-Email Transformation**: Automatically map bullet inputs (recipient, purpose, details) to a formatted email.
- **Multilingual Capabilities**: Support for English (en) and Spanish (es) with automated greeting normalization.
- **Customizable Tone**: Adjust the email’s tone (e.g., formal, friendly) via a simple CLI flag.
- **Instant Console Output**: Render the full email (subject + body) directly in the terminal.
- **Persistent Artifacts**: Log the complete email as email.txt in MLflow under each run’s artifacts.
- **Extensible Architecture**: Modular codebase designed for easy addition of languages, templates, or output formats.

## Architecture

1. AgentOS Entry Point: compose_email function registers with AgentOS.
2. Core Agent: EmailDraftingAgent encapsulates prompt engineering and template rendering.
3. Output Handling:
- STDOUT: Printed for immediate CLI feedback.
- MLflow: Logged as a plaintext artifact for later retrieval.
4. Language Normalization: Regex-based greeting replacement ensures correct salutations.

## Prerequisites

- Python 3.9 or later
- Virtual environment (`venv` or equivalent)
- GenAI AgentOS CLI
- MLflow

## Installation

1. Clone the repository

```bash
git clone https://github.com/<your-username>/email-drafting-agent.git
cd email-drafting-agent
```

2. Set up the environment

```bash
python3 -m venv .venv
source .venv/bin/activate
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

## --- Configure options---

## Example Output

Engligh

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

- **Unit Tests**: Located in `tests/`, verifying formatting logic and language normalization.
- **CI Pipeline**: `.github/workflows/ci.yml` runs flake8, mypy, pytest, and builds a Docker image.

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