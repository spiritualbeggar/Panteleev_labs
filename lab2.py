class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    def evaluate(self, variables):
        raise NotImplementedError("Метод evaluate должен быть переопределен в подклассах")

    def to_string(self):
        raise NotImplementedError("Метод to_string должен быть переопределен в подклассах")

class NumberNode(Node):
    def evaluate(self, variables):
        return self.value

    def to_string(self):
        return str(self.value)

class VariableNode(Node):
    def evaluate(self, variables):
        if self.value in variables:
            return variables[self.value]
        else:
            raise ValueError(f"Переменная {self.value} не определена")

    def to_string(self):
        return self.value

class OperationNode(Node):
    def evaluate(self, variables):
        left_value = self.left.evaluate(variables)
        right_value = self.right.evaluate(variables)
        if self.value == '+':
            return left_value + right_value
        elif self.value == '-':
            return left_value - right_value
        elif self.value == '*':
            return left_value * right_value
        elif self.value == '/':
            if right_value == 0:
                raise ZeroDivisionError("Деление на ноль")
            return left_value / right_value
        else:
            raise ValueError(f"Неизвестная операция: {self.value}")

    def to_string(self):
        return f"({self.left.to_string()} {self.value} {self.right.to_string()})"

# Пример создания дерева арифметического выражения
# (x + 2) * (y - 3)
x = VariableNode('x')
y = VariableNode('y')
two = NumberNode(2)
three = NumberNode(3)

add = OperationNode('+')
add.left = x
add.right = two

sub = OperationNode('-')
sub.left = y
sub.right = three

mul = OperationNode('*')
mul.left = add
mul.right = sub

# Вычисление выражения с подстановкой значений переменных
variables = {'x': 5, 'y': 7}

# Вывод значений переменных
print(f"Значения переменных: x = {variables['x']}, y = {variables['y']}")

# Вывод выражения
expression = mul.to_string()
print(f"Выражение: {expression}")

# Вычисление и вывод результата
result = mul.evaluate(variables)
print(f"Результат: {result}")  # Результат: 20