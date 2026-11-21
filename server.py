from fastmcp import FastMCP
from pathlib import Path
import csv
from collections import Counter

mcp = FastMCP("customer-onboarding")
INCOMING = Path(__file__).parent / "data" / "incoming"

@mcp.tool
def get_target_schema() -> dict:
    # Shows expected fields for customer records
    return {
        "external_id": "text, required",
        "company_name": "text, required",
        "contact_email": "email, required",
        "signup_date": "date YYYY-MM-DD, required",
    }

# List incoming files 
@mcp.tool
def list_incoming_files() -> list[str]:
    result = []
 
    for item in INCOMING.iterdir():
        if item.is_file():
            # print(f"File: {item.name}")
            result.append(item.name)
    return ','.join(sorted(result))


# Read file and returns one dict per row
@mcp.tool
def read_file(filename: str) -> list[dict]:
    result = []
    with open(safe_path(filename), mode="r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            result.append(row)
    return result


# Profile Source
@mcp.tool
def profile_source(filename: str) -> dict:
   pass


def safe_path(filename: str) -> Path:
    # Return the full path to a file inside INCOMING, or raise an error if file not found
    path = (INCOMING / filename).resolve()
    if not path.is_relative_to(INCOMING.resolve()): # file not in folder
        raise PermissionError(f"{filename} is outside the incoming folder")
    if not path.is_file(): # file not in folder
        raise FileNotFoundError(f"{filename} not found")
    return path


if __name__ == "__main__":
    mcp.run()