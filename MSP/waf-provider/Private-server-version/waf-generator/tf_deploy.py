import re

def parse_terraform_output(output):
    summary = "Terraform Execution Summary:\n"
    plan_match = re.search(r'Plan: (\d+) to add, (\d+) to change, (\d+) to destroy', output)
    if plan_match:
        resources_to_add = int(plan_match.group(1))
        resources_to_change = int(plan_match.group(2))
        resources_to_destroy = int(plan_match.group(3))
        summary += f"Planned changes: {resources_to_add} to add, {resources_to_change} to change, {resources_to_destroy} to destroy\n\n"

    resource_actions = {}
    for line in output.split('\n'):
        create_match = re.search(r'# ([\w\.]+) will be created', line)
        if create_match:
            resource_name = create_match.group(1)
            resource_actions[resource_name] = "To be created"
        
        status_match = re.search(r'([\w\.]+): Creation complete after (\d+[sm])', line)
        if status_match:
            resource_name = status_match.group(1)
            duration = status_match.group(2)
            resource_actions[resource_name] = f"Created in {duration}"

    if resource_actions:
        summary += "Resource actions:\n"
        for resource, status in resource_actions.items():
            summary += f"- {resource}: {status}\n"

    if "Apply complete!" in output:
        completion_match = re.search(r'Apply complete! Resources: (\d+) added, (\d+) changed, (\d+) destroyed', output)
        if completion_match:
            added = completion_match.group(1)
            changed = completion_match.group(2)
            destroyed = completion_match.group(3)
            summary += f"\nExecution completed: {added} added, {changed} changed, {destroyed} destroyed."
    elif "No changes." in output:
        summary += "\nNo changes. Your infrastructure matches the configuration."
    else:
        summary += "\nExecution status: In progress or incomplete."
    return summary

def filter_terraform_output(original_output):
    filtered_output = parse_terraform_output(original_output)
    return filtered_output