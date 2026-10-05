import boto3
import json

bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")

def get_model_id() -> str:
    account_id = boto3.client("sts").get_caller_identity()["Account"]
    return f"arn:aws:bedrock:us-east-1:{account_id}:inference-profile/us.anthropic.claude-sonnet-4-6"

def ask_claude(prompt, system=None, max_tokens=500):
    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": prompt}]
    }
    if system:
        body["system"] = system

    response = bedrock.invoke_model(modelId=get_model_id(), body=json.dumps(body))
    result = json.loads(response["body"].read())
    return result["content"][0]["text"]
