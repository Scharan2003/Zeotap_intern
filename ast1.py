class Node:
    def __init__(self, node_type, value=None, left=None, right=None):
        self.node_type = node_type  # "operator" or "operand"
        self.value = value  # For operands, this could be a comparison value
        self.left = left  # Left child
        self.right = right  # Right child


def create_rule(rule_string):
    rule_string = rule_string.strip()

    # Handle top-level parentheses
    if rule_string.startswith('(') and rule_string.endswith(')'):
        rule_string = rule_string[1:-1].strip()

    # Handle AND and OR operators at the top level
    depth = 0
    operator_position = -1
    operator = None

    for i, char in enumerate(rule_string):
        if char == '(':
            depth += 1
        elif char == ')':
            depth -= 1
        elif depth == 0:
            # Only look for AND/OR when not inside parentheses
            if rule_string[i:i + 3] == "AND":
                operator = "AND"
                operator_position = i
                break
            elif rule_string[i:i + 2] == "OR":
                operator = "OR"
                operator_position = i
                break

    if operator_position != -1:
        # Split the rule into left and right parts based on the operator
        left_part = rule_string[:operator_position].strip()
        right_part = rule_string[operator_position + len(operator):].strip()
        left_node = create_rule(left_part)
        right_node = create_rule(right_part)
        return Node("operator", operator, left_node, right_node)

    # If no operator is found, it's an operand
    return Node("operand", rule_string.strip())


def evaluate_rule(node, data):
    if node.node_type == "operand":
        # Simple evaluation logic for the operand
        parts = node.value.split()
        if len(parts) != 3:
            raise ValueError(f"Invalid operand format: {node.value}")
        attribute, operator, value = parts
        value = int(value) if value.isdigit() else value.strip("'")
        if operator == ">":
            return data[attribute] > value
        elif operator == "<":
            return data[attribute] < value
        elif operator == "=":
            return data[attribute] == value
        else:
            raise ValueError(f"Unknown operator: {operator}")
    elif node.node_type == "operator":
        left_result = evaluate_rule(node.left, data)
        right_result = evaluate_rule(node.right, data)
        if node.value == "AND":
            return left_result and right_result
        elif node.value == "OR":
            return left_result or right_result


def combine_rules(rule1, rule2, operator):
    """
    Combines two rule trees using the given operator ("AND" or "OR").
    Returns a new rule tree Node representing the combined rule.
    """
    if operator not in ["AND", "OR"]:
        raise ValueError(f"Invalid operator: {operator}. Use 'AND' or 'OR'.")

    return Node("operator", operator, rule1, rule2)


# Example usage
if __name__ == "__main__":
    rule1 = "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing'))"
    rule2 = "(experience > 5 AND salary < 100000)"

    # Create abstract syntax trees for both rules
    ast1 = create_rule(rule1)
    ast2 = create_rule(rule2)

    # Combine both rules with an AND operator
    combined_rule_ast = combine_rules(ast1, ast2, "AND")

    # Example data to evaluate the combined rule
    data = {"age": 35, "department": "Sales", "experience": 7, "salary": 90000}
    result = evaluate_rule(combined_rule_ast, data)

    print("Is user eligible based on combined rule?", result)  # Expected Output: True
