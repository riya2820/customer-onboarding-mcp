from fastmcp import FastMCP

mcp = FastMCP("customer-onboarding")

@mcp.tool
def get_target_schema() -> dict:
    # Show expected fields for customer records
    return {
        "external_id": "text, required",
        "company_name": "text, required",
        "contact_email": "email, required",
        "signup_date": "date YYYY-MM-DD, required",
    }

if __name__ == "__main__":
    mcp.run()