from mcp.server.fastmcp import FastMCP

from tools.cloudwatch import cloudwatch_tools
from tools.dynamodb import dynamodb_tools
from tools.ec2 import ec2_tools
from tools.finops import finops_tools
from tools.iam import iam_tools
from tools.aws_lambda import lambda_tools; 
from tools.s3 import s3_tools; 



# Create MCP server instance
server = FastMCP(name="AWS-MCP-POC")

#register tools
cloudwatch_tools.register(server)
dynamodb_tools.register(server)
ec2_tools.register(server)
finops_tools.register(server)
iam_tools.register(server)
lambda_tools.register(server)
s3_tools.register(server)

                         
if __name__ == "__main__":
    print("🚀 MCP Server running at http://localhost:8000/mcp")
    server.run(transport="streamable-http")
