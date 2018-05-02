import operator
from collections import deque

operations_map = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv
}

def is_float(item):
    try:
        float(item)
        return True
    except ValueError:
        return False

class Calculator:
    """
        This is an Interface, or Abstract Class (the same in Python)
        You can throw errors for each method to force that they be implemented.
    """
    def __init__(self):
        pass
    def get_calculatable(self):
        pass
    def add_input(self, item):
        pass
    def calculate(self):
        pass

class PostfixCalculator(Calculator):
    """
    A specific type of calculator which assumes operators will be to the
    right of the operands on which they operate.
    For example, 2 2 + is equal to 4.
    """
    def __init__(self):
        self.stack = deque()

    def _operation_right_side(self, oper, num_operands):
        numbers = deque()
        for i in range(num_operands):
            numbers.appendleft(self.stack.pop())
        return oper(*numbers)

    def get_calculatable(self):
        return self.stack

    def add_input(self, item):
        if item in operations_map.keys():
            self.stack.append(item)
        elif is_float(item):
            self.stack.append(float(item))
        else:
            pass

    def calculate(self):
        while len(self.stack) > 1:
            next_oper = self.stack.pop()
            num_operands = 2
            # if the stack ends in something other than an operator, remove
            # and do nothing
            if next_oper not in operations_map.keys():
                break
            # if the stack is [3, +], we will remove the + and do nothing
            if len(self.stack) < num_operands:
                break

            oper = operations_map[next_oper]
            self.stack.append(self._operation_right_side(oper, num_operands))

# Below are the actual programs

class InteractiveCalculator:
    """
    Takes an instance of a Calculator as input
    Calculator interface has methods
        get_calculatable()
        add_item(item)
        calculate()
    """
    # Dependency injection
    def __init__(self, calculator):
        if not isinstance(calculator, Calculator):
            raise ValueError('Must pass a valid Calculator')
        self.calculator = calculator

    def run(self):
        while True:
            user_in = str(raw_input('Enter a number or operator (q to quit): '))
            if user_in == 'q':
                break
            elif user_in == '=':
                self.calculator.calculate()
                self.print_screen()
            else:
                self.calculator.add_input(user_in)
                if user_in in operations_map.keys():
                    self.print_screen()

    def print_screen(self):
        stack = self.calculator.get_calculatable()
        if len(stack) > 1:
            print(' '.join(str(item) for item in stack))
        elif len(stack) == 1:
            print(stack[0])
        else:
            print('N/A')

class InteractivePostfixCalculator:
    """
    Not a subclass of InteractiveCalculator.
    Has a similar interface by coincidence.
    """
    def run(self):
        # separating the use and construction
        postfix_calculator = PostfixCalculator()
        interactive_calculator = InteractiveCalculator(postfix_calculator)
        interactive_calculator.run()

if __name__ == '__main__':
    program = InteractivePostfixCalculator()
    program.run()
