# AWS MCP Server POC

## Overview
This POC demonstrates how to create a basic AWS MCP Server using Python, allowing interaction with AWS Services via the Model Context Protocol.

## Setup
```bash
python -m venv aws-mcp-env
source aws-mcp-env/bin/activate
pip install -r requirements.txt


Windows:

python -m venv aws-mcp-env
.\aws-mcp-env\Scripts\activate
pip install -r requirement.txt


Set the local environment:
$env:PYTHONPATH="src"
$env:FASTMCP_PORT = "8000"

## 🗣️ Multilingual Support (New!)

You can now interact with AWS in **Hindi or any language** using natural language!

### ✅ To use:

1. Install the additional dependency:
    ```bash
    pip install deep-translator
    ```

2. Run the multilingual client:
    ```bash
    python src/client/awc_iam_mcp_client_multilingual.py
    ```

3. Type your questions or commands in Hindi (or other languages). For example:
    ```
    मेरे EC2 इंस्टेंस क्या हैं?
    ```

The agent will detect your language, translate it, execute the AWS command, and return the response **back in your language** using MCP + LangChain + Groq.
