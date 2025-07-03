# Overview

The Email Drafting Agent converts minimal bullet-point inputs into professional, multilingual email drafts. Leveraging the GenAI AgentOS platform, it streamlines email creation by generating:

A clear, context-aware subject line

Natural greetings and closings in English or Spanish

Concise, well-structured body paragraphs

All outputs are logged as MLflow artifacts for auditability and version control.

## Key Features

- Bullet-to-Email Transformation: Automatically map bullet inputs (recipient, purpose, details) to a formatted email.
- Multilingual Capabilities: Support for English (en) and Spanish (es) with automated greeting normalization.
- Customizable Tone: Adjust the email’s tone (e.g., formal, friendly) via a simple CLI flag.
- Instant Console Output: Render the full email (subject + body) directly in the terminal.
- Persistent Artifacts: Log the complete email as email.txt in MLflow under each run’s artifacts.
- Extensible Architecture: Modular codebase designed for easy addition of languages, templates, or output formats.

