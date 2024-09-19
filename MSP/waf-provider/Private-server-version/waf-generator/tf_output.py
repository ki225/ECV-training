import re

def filter_content(log_line):
    creating_pattern = r'([\w.-]+)\.([\w.-]+): Still creating\.\.\.'
    still_creating_pattern = r'([\w.-]+)\.([\w.-]+): Still creating\.\.\.'
    apply_complete_pattern = r'Apply complete! Resources: (\d+) added, (\d+) changed, (\d+) destroyed\.'
    completed_pattern = r'([\w.-]+)\.([\w.-]+): Creation complete'
    
    match = re.search(creating_pattern, log_line) or re.search(still_creating_pattern, log_line)
    if match:
        return f"{match.group(1)}.{match.group(2)} is creating"
    
    match = re.search(completed_pattern, log_line)
    if match:
        return f"{match.group(1)}.{match.group(2)}: Creation complete"
    
    match = re.search(apply_complete_pattern, log_line)
    if match:
        return f"Apply complete! Resources: {match.group(1)} added, {match.group(2)} changed, {match.group(3)} destroyed"
    return None

def filter_terraform_output(original_output):
    filtered_output = filter_content(original_output)
    return filtered_output