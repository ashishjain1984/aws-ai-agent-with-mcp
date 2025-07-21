import boto3
from util.table_util import format_markdown_table


# ----------------------------
# S3
# ----------------------------
def register(server):

    @server.tool()
    def list_s3_buckets() -> str:
        s3 = boto3.client("s3")
        buckets = s3.list_buckets().get("Buckets", [])
        print("I am here: ", buckets)
        rows = [[b["Name"]] for b in buckets]
        return format_markdown_table(["Bucket Name"], rows)