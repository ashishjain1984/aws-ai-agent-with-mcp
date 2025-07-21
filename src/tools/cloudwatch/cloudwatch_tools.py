import boto3
from util.table_util import format_markdown_table

# ----------------------------
# CloudWatch (Recent Alarms)
# ----------------------------
def register(server):

    @server.tool()
    def list_cloudwatch_alarms(region: str = "us-east-1") -> str:
        cw = boto3.client("cloudwatch", region_name=region)
        alarms = cw.describe_alarms(StateValue="ALARM").get("MetricAlarms", [])
        rows = [[a["AlarmName"], a["MetricName"], a["StateUpdatedTimestamp"].strftime("%Y-%m-%d %H:%M")[:16]] for a in alarms]
        return format_markdown_table(["Alarm", "Metric", "Updated"], rows)

