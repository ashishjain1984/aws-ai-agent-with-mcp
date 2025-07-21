import boto3
from util.table_util import format_markdown_table

# ----------------------------
# EC2 
# ----------------------------
def register(server):
   
    # Running Instances with Tags 
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


    # All EC2 Instances with Tags
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