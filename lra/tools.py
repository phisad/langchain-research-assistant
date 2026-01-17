from pathlib import Path
from fastmcp import FastMCP
from langchain_mcp_adapters.client import MultiServerMCPClient
from pypdf import PdfReader

multi_tool_server = MultiServerMCPClient(
    {
        "pdf-server": {
            "url": "http://localhost:8000/mcp",
            "transport": "streamable_http",
        }
    }
)

mcp_pdf = FastMCP("PDF")


@mcp_pdf.tool
def list_pdfs() -> list[str]:
    return [f.name for f in Path.cwd().glob("*.pdf")]


@mcp_pdf.tool
def read_pdf(file_name: str):
    path = Path.cwd() / file_name
    if not path.exists():
        return f"Error: File '{file_name}' not found"
    if not path.suffix.lower() == ".pdf":
        return f"Error: '{file_name}' is not a PDF file"
    reader = PdfReader(path)
    text = []
    for page in reader.pages:
        text.append(page.extract_text() or "")
    return "\n\n".join(text)


def start(server_name: str):
    if server_name == "pdf":
        mcp_pdf.run(transport="streamable-http")
