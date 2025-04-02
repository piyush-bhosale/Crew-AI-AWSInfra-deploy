#!/usr/bin/env python
import sys
import warnings
import re
import json
from datetime import datetime
from flask import Flask, request, jsonify
from crew import AwsAd

# Initialize Flask App
app = Flask(__name__)
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# Prepare input payload
def getinputs(data):
    action = data.get("action", "").strip().lower()
    inputs = {"action": action}
    if action == "create":
        inputs.update({
            "aws_region": data.get("aws_region"),
            "vpc_id": data.get("vpc_id"),
            "subnet_ids": data.get("subnet_ids"),
            "directory_name": data.get("directory_name")
        })
    elif action == "delete":
        inputs.update({
            "aws_region": data.get("aws_region"),
            "directory_id": data.get("directory_id")
        })
    return inputs

# Route to trigger CrewAI flow
@app.route("/run", methods=["POST"])
def run():
    try:
        data = request.get_json()
        inputs = getinputs(data)
        crew = AwsAd().crew()
        result = crew.kickoff(inputs={"topic": inputs})
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)
