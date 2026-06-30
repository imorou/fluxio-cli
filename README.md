# Fluxio-CLI — DevOps AI Assistant for Terminal 

**Version:** 1.0.0
**Status:** Deployment Validated

`fluxio-cli` is a command-line automation tool designed to run directly within a Linux Virtual Machine environment (Ubuntu Server). It allows system and DevOps engineers to interact with the power of the **DeepSeek V3** large language model (via the **OpenRouter** API architecture) without ever leaving their working terminal.

Instead of constantly switching between the terminal and a web browser to look up complex syntaxes (Docker, Terraform, Bash scripts, or PL/SQL), Fluxio-CLI brings AI directly into the engineer's workflow. The tool eliminates visual noise to return only clean, accurate, and immediately actionable technical code.

---

##  Key Features

- **100% Terminal Interface**: Instant translation of natural language queries into system commands or infrastructure scripts.
- **Secrets Security**: Complete isolation of authentication tokens and private keys using the Linux environment variable system (`.env` excluded from version control).
- **Ultra-Lightweight Architecture**: A minimalist Python 3 structure that avoids overloading VM resources.

---

##  Installation & Deployment

### 1. Environment Preparation & Isolation

Create the working directory and set up a Python isolated environment:

```bash
# Create project directory
mkdir -p ~/fluxio-cli && cd ~/fluxio-cli

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install openai python-dotenv

```

2. Secure Secrets Management

Fluxio uses environment variables to securely manage API credentials.

Create a .env file at the root of the project:

```bash
touch .env

Add your OpenRouter API key inside:

```env
OPENROUTER_API_KEY=your_private_api_key_here

```
 Important:
The .env file must be excluded from Git tracking using .gitignore to prevent accidental exposure of sensitive credentials.

3. Setting Up a Global CLI Alias

To run Fluxio from anywhere in your Linux system, add a permanent alias to your shell configuration:

```bash
echo "alias fluxio='/home/sandda/fluxio-cli/venv/bin/python3 /home/sandda/fluxio-cli/main.py'" >> ~/.bashrc
source ~/.bashrc

```
Now you can run Fluxio globally:

```bash
fluxio "Generate a Docker command to run PostgreSQL with persistent storage"
```
Usage

Once installed, you can interact with Fluxio directly from your terminal:

```bash
fluxio "Write a Docker Compose file for PostgreSQL with persistent volume"

```
Example use cases:
Generate Docker commands
Write Terraform infrastructure
Debug Bash scripts
Create Kubernetes manifests
Query SQL structures
 Roadmap & Upcoming Modules
[ ] Fluxio-Log (Analyzer Module)

AI-powered log analysis system that reads local error logs (error.log) and suggests fixes.

[ ] Fluxio-Memo (Documentation Module)

Automatically stores generated commands and builds a deployment history.

[ ] Future Enhancements
Kubernetes deep integration
Cloud provider support (AWS / OCI / Azure)
Interactive shell mode
Autocompletion for DevOps commands

---

**Author:** Imorou TOURE (DevOps & Cloud Engineer)
##  Professional Certifications

- **[Oracle Cloud Infrastructure (OCI) Multicloud Architect Professional](https://drive.google.com/file/d/11EB7Y8uym9LAPtdWyshftYeTdYAxxuap/view?usp=drive_link)**
- **[Oracle Cloud Infrastructure 2025 AI Foundations Associate](https://drive.google.com/file/d/1SMFyPhzabimOnQzK1D5Iu9aZb-HNGlrl/view?usp=drive_link)**


