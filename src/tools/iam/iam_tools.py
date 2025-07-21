import boto3
from util.table_util import format_markdown_table

# ----------------------------
# IAM
# ----------------------------
def register(server):

    @server.tool()
    def list_iam_users() -> str:
        iam = boto3.client("iam")
        paginator = iam.get_paginator("list_users")
        rows = []
        for page in paginator.paginate():
            for user in page["Users"]:
                rows.append([user["UserName"], user["CreateDate"].strftime("%Y-%m-%d")])
        return format_markdown_table(["User", "Created"], rows)