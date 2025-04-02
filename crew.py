import os
import boto3
from crewai.tools import tool
from dotenv import load_dotenv
from crewai import Agent, Crew, Process, LLM, Task
from crewai.project import CrewBase, agent, crew, task

# Load environment variables from .env file
load_dotenv()

# Tool to create an AWS Directory
@tool("create_ad")
def create_ad(aws_region: str, directory_name: str, vpc_id: str, subnet_ids: list):
    """
    Create an AWS Managed Active Directory in the specified region and VPC.
    """
    password = os.getenv("AWS_PASSWORD")
    client = boto3.client("ds", region_name=aws_region)
    try:
        # Create Active Directory
        response = client.create_microsoft_ad(
            Name=directory_name,
            ShortName=directory_name.replace(" ", "")[:4],
            Password=password,
            VpcSettings={
                "VpcId": vpc_id,
                "SubnetIds": subnet_ids
            },
            Edition="Standard"  # Change to "Enterprise" if required
        )
        # Extract Directory ID
        directory_id = response["DirectoryId"]
        print(f"** AWS Managed Active Directory is being created. Directory ID: {directory_id} Subnet IDs: {subnet_ids}")
        return {"status": "created", "directory_id": directory_id}
    except Exception as e:
        print(f"** Error: {str(e)}")
        return {"error": str(e)}

# Tool to delete an AWS Directory
@tool("delete_ad")
def delete_ad(aws_region: str, directory_id: str):
    """
    Deletes an existing AWS Managed Active Directory.
    """
    client = boto3.client("ds", region_name=aws_region)
    try:
        client.delete_directory(DirectoryId=directory_id)
        print(f"** AWS Managed Active Directory (directory_id) Deleted Successfully.")
        return {"status": "deleted", "directory_id": directory_id}
    except Exception as e:
        print(f"** Error deleting directory: {str(e)}")
        return {"error": str(e)}

# Define the Crew class
class AwsAd(CrewBase):
    # YAML Configuration file paths
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # Large Language Model config
    llm = LLM(
        model="openai/llama3.3-70b",
        base_url="https://llm-proxy.kpit.com",
        api_key=os.getenv("OPENAI_API_KEY")
    )

    # Agent initialization
    @agent
    def aws_expert(self) -> Agent:
        return Agent(
            config=self.agents_config["aws_expert"],
            verbose=True,
            llm=self.llm,
            tools=[create_ad, delete_ad]
        )

    # Task initialization
    @task
    def create_ad_task(self) -> Task:
        return Task(
            config=self.tasks_config["create_ad_task"]
        )

    # Crew composition
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
