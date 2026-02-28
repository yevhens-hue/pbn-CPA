import json
import re
import requests
from bs4 import BeautifulSoup

def validate_schema(url_or_html):
    """
    Validates the presence and basic structure of JSON-LD schema in a given URL or HTML string.
    """
    html = ""
    if url_or_html.startswith("http"):
        try:
            resp = requests.get(url_or_html, timeout=15)
            if resp.status_code == 200:
                html = resp.text
            else:
                return {"status": "error", "message": f"Failed to fetch URL: {resp.status_code}"}
        except Exception as e:
            return {"status": "error", "message": f"Request failed: {str(e)}"}
    else:
        html = url_or_html

    soup = BeautifulSoup(html, 'html.parser')
    schemas = soup.find_all('script', type='application/ld+json')
    
    if not schemas:
        return {"status": "fail", "message": "No JSON-LD schema found."}
    
    results = {
        "found_types": [],
        "errors": [],
        "status": "pass"
    }

    for schema in schemas:
        try:
            data = json.loads(schema.string)
            if isinstance(data, dict):
                s_type = data.get("@type")
                if s_type:
                    results["found_types"].append(s_type)
            elif isinstance(data, list):
                for item in data:
                    s_type = item.get("@type")
                    if s_type:
                        results["found_types"].append(s_type)
        except Exception as e:
            results["errors"].append(f"Invalid JSON in schema: {str(e)}")
            results["status"] = "fail"

    # Validation Rules
    essential_types = ["SoftwareApplication", "FAQPage"]
    missing = [t for t in essential_types if t not in results["found_types"]]
    
    if missing:
        results["status"] = "warning"
        results["message"] = f"Missing recommended types: {', '.join(missing)}"
    
    return results

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        target = sys.argv[1]
        print(f"🧐 Validating schema for: {target}")
        report = validate_schema(target)
        print(json.dumps(report, indent=2))
    else:
        print("Usage: python3 schema_validator.py <url_or_html_string>")
