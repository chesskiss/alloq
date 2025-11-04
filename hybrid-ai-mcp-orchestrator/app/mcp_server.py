import asyncio
from mcp.server import Server
from mcp.types import Tool, ToolList, CallToolRequest, CallToolResult
from app import analyzer, hardware_recommender

server = Server("hybrid-ai-mcp-server")

@server.list_tools()
async def list_tools() -> ToolList:
    return ToolList(
        tools=[
            Tool(
                name="analyze_program",
                description="Analyze code and return detected algorithms.",
                input_schema={
                    "type": "object",
                    "properties": {"code": {"type": "string"}},
                    "required": ["code"],
                },
            ),
            Tool(
                name="recommend_hardware",
                description="Recommend hardware given an algorithm name.",
                input_schema={
                    "type": "object",
                    "properties": {"algorithm": {"type": "string"}},
                    "required": ["algorithm"],
                },
            ),
        ]
    )

@server.call_tool()
async def call_tool(req: CallToolRequest) -> CallToolResult:
    if req.name == "analyze_program":
        code = req.arguments.get("code", "")
        algos = analyzer.detect_algorithms(code)
        return CallToolResult(output={"algorithms": algos})

    if req.name == "recommend_hardware":
        algorithm = req.arguments.get("algorithm", "")
        suggestion = hardware_recommender.recommend_for_algorithm(algorithm)
        return CallToolResult(output=suggestion.dict())

    return CallToolResult(output={"error": f"Unknown tool: {req.name}"})

if __name__ == "__main__":
    asyncio.run(server.run_stdio())
