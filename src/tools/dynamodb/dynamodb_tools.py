import boto3
from util.table_util import format_markdown_table

# ----------------------------
# DynamoDB
# ----------------------------
def register(server):
    
    @server.tool()
    def list_dynamodb_tables() -> str:
        client = boto3.client("dynamodb")
        tables = client.list_tables().get("TableNames", [])
        rows = [[t] for t in tables]
        return format_markdown_table(["Table Name"], rows)