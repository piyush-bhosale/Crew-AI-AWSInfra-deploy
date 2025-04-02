# AWS Active Directory Deployment using CrewAI

This project demonstrates how to use **CrewAI** to automate the **creation and deletion of AWS Managed Active Directory Services** using conversational agents. It is designed to showcase the power of CrewAI agents, tasks, and tools, and how they can be integrated into a cloud infrastructure automation workflow. This is ideal for DevOps professionals with basic Python knowledge.

---

## What is CrewAI?

**CrewAI** is an open-source framework for building **collaborative AI agent teams** that work together using tasks, tools, and large language models. It enables defining goal-oriented agents that can perform real-world operations like executing Python code, running cloud commands, and working with APIs or databases.

Learn more: [https://docs.crewai.com](https://docs.crewai.com)

---

## What this Project Does

This CrewAI project:
- Defines an **AWS Expert agent**.
- Allows the agent to **create or delete AWS Directory Services** in a specified region.
- Takes structured input from a Flask API endpoint.
- Uses `boto3` to interact with AWS resources securely via environment variables.

---

## Prerequisites

Before running this project, make sure:
- **Python 3.10+** is installed.
- AWS CLI is configured locally with valid credentials:  
  ```bash
  aws configure
  ```
- IAM permissions include:
  - `ds:CreateMicrosoftAD`
  - `ds:DeleteDirectory`
  - VPC and subnet read permissions

---

## File Structure

When CrewAI is installed, it scaffolds the following base structure automatically:
```
your_project/
├── config/
│   ├── agents.yaml      # Define roles, goals, backstory of AI agents
│   └── tasks.yaml       # Define what the agent is supposed to do
├── tools/               # Custom tools and logic used by agents
│   └── __init__.py
├── crew.py              # Main class for creating crew, agents, and task logic
├── main.py              # Flask API to trigger the agent process
├── .env                 # Stores credentials and sensitive data (ignored in .gitignore)
├── .gitignore
├── pyproject.toml       # Project metadata and build system for hatch/crew
├── requirement.txt      # Required Python libraries
```

---

## How it Works

1. You send a POST request to `/run` with a payload like:
```json
{
  "action": "create",
  "aws_region": "ap-south-1",
  "vpc_id": "vpc-xxxxxxxx",
  "subnet_ids": ["subnet-abc", "subnet-def"],
  "directory_name": "corp-directory"
}
```

2. The `main.py` reads this input and maps it to either a **create** or **delete** task.

3. The `crew.py` file builds the CrewAI environment:
   - Initializes the LLM
   - Loads the `aws_expert` agent
   - Attaches tools like `create_ad`, `delete_ad`
   - Binds the task `create_ad_task` from the YAML config

4. Agent `aws_expert` uses these tools to invoke AWS APIs via `boto3`.

---

## Detailed Explanation of Key Files

### 1. `config/agents.yaml`
Defines your agent:
```yaml
aws_expert:
  role: "{topic} AWS Expert"
  goal: "Create or delete Directory Service in AWS"
  backstory: "You are an AWS cloud expert who assists in cloud automation."
```

### 2. `config/tasks.yaml`
Describes what your agent will do:
```yaml
create_ad_task:
  description: "Create or delete Directory Service in a region"
  expected_output: "Successful AWS Directory operation"
  agent: aws_expert
```

### 3. `crew.py`
Contains:
- `@tool` decorated Python functions (`create_ad`, `delete_ad`)
- Agent and task constructors
- LLM setup
- Final `crew()` method that assembles everything

### 4. `main.py`
Handles HTTP request input using Flask and maps it to crew execution:
```python
@app.route("/run", methods=["POST"])
def run():
    # Parses JSON, kicks off crew
```

---

## Environment Variables (`.env`)

```env
MODEL=gpt-4
OPENAI_API_KEY="your-openai-key"
AWS_REGION="ap-south-1"
AWS_PASSWORD="your-ad-password"
```

Do **not** commit your `.env` file to GitHub. It is listed in `.gitignore`.

---

## Dependencies

List of required Python libraries (`requirement.txt`):
```
boto3
crewai
python-dotenv
```

Install with:
```bash
pip install -r requirement.txt
```

---

## Getting Started

```bash
# Clone the repository
git clone https://github.com/your-username/aws_ad_crewai.git
cd aws_ad_crewai

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirement.txt

# Set environment variables in .env file

# Run the Flask app
python main.py
```

---

## Why This Project?

This project showcases:
- CrewAI agent orchestration
- Real-world AWS automation
- Clean Python design
- Ideal for DevOps/Cloud/AI engineering roles

It’s a perfect example to demonstrate **automation skills**, **agent development**, and **cloud integration** to recruiters or hiring managers.

---

## License

This project is licensed under the MIT License.
