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


@mcp.tool
def profile_source(filename: str) -> dict:
    """Summarize each column so a human (or AI) can see what the data looks like.
    Example:
        Input:  "acme.csv"
        Output: {
            "file": "acme.csv",
            "row_count": 12,
            "columns": [
                {"column": "Cust #", "fill_rate": 0.92, "distinct": 10,
                 "samples": ["A-1003", "A-1001", "A-1002"]},
                ...one dict per column
            ]
        }
    fill_rate: rows with a non-blank value ÷ total rows, rounded to 2 decimals
    "" and " " both count as blank
    distinct: how many different non-blank values there are
    samples: up to 3 of the most common non-blank values
    """
    count = 0
    rows = read_file(filename)                
    columns = []

    for col in rows[0].keys():
        values = [] # reset 
        for row in rows:
            if row[col].strip():
                values.append(row[col].strip())
        count = Counter(values)

        columns.append({
            "column": col,
            "fill_rate": round(len(values) / len(rows), 2),
            "distinct": len(count),
            "samples": [value for value, _ in count.most_common(3)],
        })

    return {"file": filename, "row_count": len(rows), "columns": columns}



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