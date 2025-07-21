import boto3
from datetime import datetime, timedelta
from util.table_util import format_markdown_table


# ----------------------------
# AWS Cloud FinOps 
# ----------------------------
def register(server):

    @server.tool()
    def get_monthly_cost_summary() -> str:
        ce = boto3.client("ce")
        today = datetime.utcnow()
        start = today.replace(day=1).strftime("%Y-%m-%d")
        end = today.strftime("%Y-%m-%d")
        result = ce.get_cost_and_usage(
            TimePeriod={"Start": start, "End": end},
            Granularity="MONTHLY",
            Metrics=["UnblendedCost"],
            GroupBy=[{"Type": "DIMENSION", "Key": "SERVICE"}],
        )
        rows = [
            [g["Keys"][0], f"${float(g['Metrics']['UnblendedCost']['Amount']):.2f}"]
            for g in result["ResultsByTime"][0]["Groups"]
        ]
        return format_markdown_table(["Service", "Cost (MTD)"], rows)


    @server.tool()
    def list_high_cost_services(limit: int = 5) -> str:
        from datetime import datetime
        ce = boto3.client("ce")

        today = datetime.utcnow()
        start_of_month = today.replace(day=1).strftime("%Y-%m-%d")
        end_date = today.strftime("%Y-%m-%d")

        result = ce.get_cost_and_usage(
            TimePeriod={"Start": start_of_month, "End": end_date},
            Granularity="MONTHLY",
            Metrics=["UnblendedCost"],
            GroupBy=[{"Type": "DIMENSION", "Key": "SERVICE"}],
        )

        groups = result["ResultsByTime"][0]["Groups"]
        sorted_groups = sorted(groups, key=lambda g: float(g["Metrics"]["UnblendedCost"]["Amount"]), reverse=True)

        top_services = sorted_groups[:limit]
        rows = [
            [group["Keys"][0], f"${float(group['Metrics']['UnblendedCost']['Amount']):.2f}"]
            for group in top_services
        ]

        return format_markdown_table(["Service", "Cost (MTD)"], rows)


    @server.tool()
    def show_s3_storage_by_bucket() -> str:
        s3 = boto3.client("s3")
        cw = boto3.client("cloudwatch")
        buckets = s3.list_buckets().get("Buckets", [])
        rows = []

        for b in buckets:
            name = b["Name"]
            try:
                metrics = cw.get_metric_statistics(
                    Namespace="AWS/S3",
                    MetricName="BucketSizeBytes",
                    Dimensions=[
                        {"Name": "BucketName", "Value": name},
                        {"Name": "StorageType", "Value": "StandardStorage"},
                    ],
                    StartTime=datetime.utcnow() - timedelta(days=2),
                    EndTime=datetime.utcnow(),
                    Period=86400,
                    Statistics=["Average"],
                )
                datapoints = metrics.get("Datapoints", [])
                if datapoints:
                    size_bytes = datapoints[-1]["Average"]
                    size_gb = size_bytes / (1024**3)
                    estimated_cost = size_gb * 0.023  # Assuming $0.023/GB-month
                    rows.append([name, f"{size_gb:.2f} GB", f"${estimated_cost:.2f}"])
            except Exception as e:
                rows.append([name, "N/A", f"Error: {str(e)}"])

        return format_markdown_table(["Bucket", "Size", "Estimated Cost"], rows)


