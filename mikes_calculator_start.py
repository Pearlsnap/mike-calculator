# goal is to build a calculator that works with postfix notation
import operator
from collections import deque

operations_map = {
    '+': operator.add,
    '-': operator.sub,
    '/': operator.truediv
}

class PostfixCalculator:
    def __init__(self):
        self.stack = deque()

    def operation_right_side(self, operator, num_operands):
        numbers = deque()
        for i in range(num_operands):
            numbers.appendleft(self.stack.pop())
        return operator(*numbers)

    def calculate(self, input_string):
        for item in input_string:
            if item.isdigit():
                self.stack.append(float(item))
            elif item in operations_map.keys():
                operator = operations_map[item]
                self.stack.append(self.operation_right_side(operator, 2))
            else:
                pass
        return self.stack

operations_map['-'](1,2)

if __name__ == '__main__':
    calculator = PostfixCalculator()
    result = calculator.calculate('6 2 1 + / 2 +')
    print(result)
