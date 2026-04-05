def detect_rule_type(prompt):
    if "flow" in prompt.lower():
        return "Flow"
    return "Activity"
