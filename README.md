# Fluxio-CLI — DevOps AI Assistant for Terminal 

**Author:** Imorou TOURE (DevOps & Cloud Engineer)
**Version:** 1.0.0
**Status:** Deployment Validated

`fluxio-cli` is a command-line automation tool designed to run directly within a Linux Virtual Machine environment (Ubuntu Server). It allows system and DevOps engineers to interact with the power of the **DeepSeek V3** large language model (via the **OpenRouter** API architecture) without ever leaving their working terminal.

Instead of constantly switching between the terminal and a web browser to look up complex syntaxes (Docker, Terraform, Bash scripts, or PL/SQL), Fluxio-CLI brings AI directly into the engineer's workflow. The tool eliminates visual noise to return only clean, accurate, and immediately actionable technical code.

---

## Key Features

- **100% Terminal Interface**: Instant translation of natural language queries into system commands or infrastructure scripts.
- **Secrets Security**: Complete isolation of authentication tokens and private keys using the Linux environment variable system (`.env` excluded from version control).
- **Ultra-Lightweight Architecture**: A minimalist Python 3 structure that avoids overloading VM resources.

---

##  Installation & Deployment

### 1. Environment Preparation & Isolation
```bash
# Create the working directory
mkdir -p ~/fluxio-cli && cd ~/fluxio-cli

# Software isolation via a Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies (OpenRouter-compatible SDK)
pip install openai python-dotenv
