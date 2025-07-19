from mcp.server.fastmcp import FastMCP
from tabulate import tabulate

import boto3

# Create MCP server instance
server = FastMCP(name="AWS-MCP-POC")

def format_markdown_table(headers, rows):
    return "```\n" + tabulate(rows, headers=headers, tablefmt="github") + "\n```"

# ----------------------------
# S3
# ----------------------------
@server.tool()
def list_s3_buckets() -> str:
    s3 = boto3.client("s3")
    buckets = s3.list_buckets().get("Buckets", [])
    rows = [[b["Name"]] for b in buckets]
    return format_markdown_table(["Bucket Name"], rows)

# ----------------------------
# Lambda (Region-Aware)
# ----------------------------
@server.tool()
def list_lambda_functions(region: str = "us-east-1") -> str:
    client = boto3.client("lambda", region_name=region)
    functions = client.list_functions().get("Functions", [])
    rows = [[f["FunctionName"], f["Runtime"]] for f in functions]
    return format_markdown_table(["Function Name", "Runtime"], rows)

# ----------------------------
# DynamoDB
# ----------------------------
@server.tool()
def list_dynamodb_tables() -> str:
    client = boto3.client("dynamodb")
    tables = client.list_tables().get("TableNames", [])
    rows = [[t] for t in tables]
    return format_markdown_table(["Table Name"], rows)

# ----------------------------
# IAM
# ----------------------------
@server.tool()
def list_iam_users() -> str:
    iam = boto3.client("iam")
    paginator = iam.get_paginator("list_users")
    rows = []
    for page in paginator.paginate():
        for user in page["Users"]:
            rows.append([user["UserName"], user["CreateDate"].strftime("%Y-%m-%d")])
    return format_markdown_table(["User", "Created"], rows)

# ----------------------------
# EC2 (Running Instances with Tags)
# ----------------------------
@server.tool()
def list_running_ec2_instances(region: str = "us-east-1") -> str:
    ec2 = boto3.client("ec2", region_name=region)
    filters = [{"Name": "instance-state-name", "Values": ["running"]}]
    response = ec2.describe_instances(Filters=filters)
    rows = []
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            tags = ", ".join([f'{t["Key"]}:{t["Value"]}' for t in instance.get("Tags", [])])
            rows.append([instance["InstanceId"], instance["InstanceType"], tags])
    return format_markdown_table(["Instance ID", "Type", "Tags"], rows)


# ----------------------------
# EC2 (All Instances with Tags)
# ----------------------------
@server.tool()
def list_all_ec2_instances(region: str = "us-east-1") -> str:
    ec2 = boto3.client("ec2", region_name=region)
    response = ec2.describe_instances()
    rows = []
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            tags = ", ".join([f'{t["Key"]}:{t["Value"]}' for t in instance.get("Tags", [])])
            state = instance['State']['Name']
            rows.append([instance["InstanceId"], instance["InstanceType"], state, tags])
    return format_markdown_table(["Instance ID", "Type", "Tags"], rows)

# ----------------------------
# CloudWatch (Recent Alarms)
# ----------------------------
@server.tool()
def list_cloudwatch_alarms(region: str = "us-east-1") -> str:
    cw = boto3.client("cloudwatch", region_name=region)
    alarms = cw.describe_alarms(StateValue="ALARM").get("MetricAlarms", [])
    rows = [[a["AlarmName"], a["MetricName"], a["StateUpdatedTimestamp"].strftime("%Y-%m-%d %H:%M")[:16]] for a in alarms]
    return format_markdown_table(["Alarm", "Metric", "Updated"], rows)



if __name__ == "__main__":
    print("🚀 MCP Server running at http://localhost:8000/mcp")
    server.run(transport="streamable-http")
