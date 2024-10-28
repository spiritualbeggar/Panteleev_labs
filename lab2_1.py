class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    def is_operator(self):
        return self.value in ['+', '-', '*', '/']


class ExpressionTree:
    def __init__(self, root=None):
        self.root = root

    def evaluate(self, variables={}):
        return self._evaluate_node(self.root, variables)

    def _evaluate_node(self, node, variables):
        if node is None:
            return 0
        # Если узел - число или переменная, вернем значение
        if not node.is_operator():
            if isinstance(node.value, (int, float)):
                return node.value
            return variables.get(node.value, 0)  # подставляем значение переменной

        # Если узел - оператор, рекурсивно вычислим левое и правое поддеревья
        left_val = self._evaluate_node(node.left, variables)
        right_val = self._evaluate_node(node.right, variables)

        # Выполняем соответствующую операцию
        if node.value == '+':
            return left_val + right_val
        elif node.value == '-':
            return left_val - right_val
        elif node.value == '*':
            return left_val * right_val
        elif node.value == '/':
            return left_val / right_val

    def to_string(self):
        return self._node_to_string(self.root)

    def _node_to_string(self, node):
        if node is None:
            return ""
        # Если узел - число или переменная, вернем её значение
        if not node.is_operator():
            return str(node.value)

        # Если узел - оператор, добавим скобки для группировки
        left_expr = self._node_to_string(node.left)
        right_expr = self._node_to_string(node.right)
        return f"({left_expr} {node.value} {right_expr})"

    @staticmethod
    def from_postfix(expression):
        stack = []
        for token in expression:
            if token in ['+', '-', '*', '/']:
                right = stack.pop()
                left = stack.pop()
                node = Node(token)
                node.left = left
                node.right = right
                stack.append(node)
            else:
                stack.append(Node(token))
        return ExpressionTree(stack.pop())

# Пример использования
# Выражение: a b + c * (в постфиксной записи: "a b + c *")
expression = ['a', 'b', '+', 'c', '*']
tree = ExpressionTree.from_postfix(expression)

# Подстановка значений переменных
variables = {'a': 3, 'b': 4, 'c': 2}

# Вывод выражения и его результата
equation = tree.to_string()
result = tree.evaluate(variables)
print("Уравнение:", equation)
print("Результат:", result)  # Должен вывести 14, так как (3 + 4) * 2 = 14
