import json
import requests
import re
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

def parse_user_input(input_sentence: str) -> Dict[str, Any]:
    """
    Parse the user's input sentence and extract relevant parameters for CVE search.

    Args:
        input_sentence (str): The user's input sentence.

    Returns:
        Dict[str, Any]: Extracted parameters for CVE search.
    """
    params = {}

    # Extract keyword
    keyword_match = re.search(r'(?:about|related to|concerning)\s+(["\w\s]+)', input_sentence, re.IGNORECASE)
    if keyword_match:
        params['keyword'] = keyword_match.group(1).strip('"')

    # Extract CVE ID
    cve_match = re.search(r'CVE-\d{4}-\d{4,7}', input_sentence, re.IGNORECASE)
    if cve_match:
        params['cve_id'] = cve_match.group(0)

    # Extract CVSS v3 severity
    severity_match = re.search(r'(CRITICAL|HIGH|MEDIUM|LOW)\s+severity', input_sentence, re.IGNORECASE)
    if severity_match:
        params['cvss_v3_severity'] = severity_match.group(1).upper()

    # Extract date range
    date_match = re.search(r'(in the last|from)\s+(\d+)\s+(days?|weeks?|months?)', input_sentence, re.IGNORECASE)
    if date_match:
        end_date = datetime.utcnow()
        number = int(date_match.group(2))
        unit = date_match.group(3).lower()
        if 'day' in unit:
            start_date = end_date - timedelta(days=number)
        elif 'week' in unit:
            start_date = end_date - timedelta(weeks=number)
        elif 'month' in unit:
            start_date = end_date - timedelta(days=number * 30)  # Approximation
        params['pub_start_date'] = start_date.isoformat() + "Z"
        params['pub_end_date'] = end_date.isoformat() + "Z"

    return params

def search_cve(
    keyword: Optional[str] = None,
    cpe_name: Optional[str] = None,
    cve_id: Optional[str] = None,
    cvss_v3_severity: Optional[str] = None,
    pub_start_date: Optional[str] = None,
    pub_end_date: Optional[str] = None,
    results_per_page: int = 2000,
    start_index: int = 0
) -> Dict[str, Any]:
    """
    Search for CVE threats using the NIST NVD API.

    Args:
        keyword (str, optional): Keyword to search in CVE descriptions.
        cpe_name (str, optional): CPE name to filter vulnerabilities.
        cve_id (str, optional): Specific CVE ID to retrieve.
        cvss_v3_severity (str, optional): CVSS v3 severity rating (LOW, MEDIUM, HIGH, CRITICAL).
        pub_start_date (str, optional): Start date for publication date range (ISO format).
        pub_end_date (str, optional): End date for publication date range (ISO format).
        results_per_page (int, optional): Number of results per page (default 2000, max 2000).
        start_index (int, optional): Starting index for pagination (default 0).

    Returns:
        Dict[str, Any]: API response containing CVE information.
    """
    base_url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
    params = {
        "resultsPerPage": results_per_page,
        "startIndex": start_index
    }

    if keyword:
        params["keywordSearch"] = keyword
    if cpe_name:
        params["cpeName"] = cpe_name
    if cve_id:
        params["cveId"] = cve_id
    if cvss_v3_severity:
        params["cvssV3Severity"] = cvss_v3_severity.upper()
    
    if pub_start_date and pub_end_date:
        params["pubStartDate"] = pub_start_date
        params["pubEndDate"] = pub_end_date

    response = requests.get(base_url, params=params)
    response.raise_for_status()
    return response.json()

def parse_cve_results(api_response: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Parse the API response and extract relevant CVE information.

    Args:
        api_response (Dict[str, Any]): The raw API response.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing parsed CVE information.
    """
    parsed_results = []
    for vuln in api_response.get("vulnerabilities", []):
        cve = vuln.get("cve", {})
        parsed_results.append({
            "id": cve.get("id"),
            "description": cve.get("descriptions", [{}])[0].get("value"),
            "published": cve.get("published"),
            "lastModified": cve.get("lastModified"),
            "cvssV3": cve.get("metrics", {}).get("cvssMetricV31", [{}])[0].get("cvssData"),
            "references": [ref.get("url") for ref in cve.get("references", [])]
        })
    return parsed_results

def lambda_handler(event, context):
    """
    AWS Lambda function handler for CVE search.

    Args:
        event (dict): The event dict containing the user's input sentence.
        context (object): The context object provided by AWS Lambda.

    Returns:
        dict: The Lambda function result containing CVE information.
    """
    try:
        # Extract the user's input sentence from the event
        user_input = event.get('body', '')
        
        # Parse the user's input to extract search parameters
        params = parse_user_input(user_input)
        
        # Call the CVE search function with extracted parameters
        results = search_cve(**params)

        # Parse the results
        parsed_results = parse_cve_results(results)

        # Prepare the response
        response = {
            "statusCode": 200,
            "body": json.dumps({
                "totalResults": results['totalResults'],
                "resultsPerPage": results['resultsPerPage'],
                "startIndex": results['startIndex'],
                "cveList": parsed_results
            }),
            "headers": {
                "Content-Type": "application/json"
            }
        }

        return response

    except Exception as e:
        # Handle any errors
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
            "headers": {
                "Content-Type": "application/json"
            }
        }

# The following code is for local testing and should be removed when deploying to Lambda
if __name__ == "__main__":
    # Simulate a Lambda event with a user's input sentence
    test_event = {
        "body": "Show me HIGH severity CVEs related to log4j in the last 30 days"
    }
    
    # Call the Lambda handler with the test event
    result = lambda_handler(test_event, None)
    
    # Print the result
    print(json.dumps(json.loads(result["body"]), indent=2))