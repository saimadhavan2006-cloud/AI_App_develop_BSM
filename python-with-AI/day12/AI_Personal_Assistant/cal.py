import ast
import operator


# Allowed mathematical operations
operators = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg
}


def calculate(expression):

    try:
        tree = ast.parse(expression, mode="eval")

        def evaluate(node):

            # Number
            if isinstance(node, ast.Constant):
                if isinstance(node.value, (int, float)):
                    return node.value

                raise ValueError("Invalid number")

            # Arithmetic operation
            if isinstance(node, ast.BinOp):
                left = evaluate(node.left)
                right = evaluate(node.right)

                operation = operators.get(type(node.op))

                if operation is None:
                    raise ValueError("Operation not allowed")

                return operation(left, right)

            # Negative number
            if isinstance(node, ast.UnaryOp):
                operation = operators.get(type(node.op))

                if operation is None:
                    raise ValueError("Operation not allowed")

                return operation(evaluate(node.operand))

            raise ValueError("Invalid expression")

        result = evaluate(tree.body)

        return result

    except Exception:
        return None
