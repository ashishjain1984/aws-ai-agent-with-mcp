import boto3
from util.table_util import format_markdown_table

# ----------------------------
# Lambda (Region-Aware)
# ----------------------------
def register(server):

    @server.tool()
    def list_lambda_functions(region: str = "us-east-1") -> str:
        client = boto3.client("lambda", region_name=region)
        functions = client.list_functions().get("Functions", [])
        rows = [[f["FunctionName"], f["Runtime"]] for f in functions]
        return format_markdown_table(["Function Name", "Runtime"], rows)