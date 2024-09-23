# the CVE information will be parsed from NIST API and returned in the response.
import nvdlib
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import re

def searchCVE(cveId):
    cve = nvdlib.searchCVE(cveId=cveId)[0]
    results = f"""
                {str(cve.v31severity)} - {str(cve.v31score)}\n
                {cve.descriptions[0].value}\n
                """
    return results

# print(r.v31severity + ' - ' + str(r.v31score))
# print(r.descriptions[0].value)
# print(r.v31vector)