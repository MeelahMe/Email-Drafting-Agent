from setuptools import setup, find_packages

setup(
    name="email_drafting_agent",
    version="0.1.0",
    packages=find_packages(),            # finds the email_agent package
    install_requires=[
        "agentos",
        "mlflow",
    ],
    entry_points={
        "agentos.components": [
            "email_agent = entrypoint:compose_email",
        ]
    },
)
