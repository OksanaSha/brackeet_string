BRACKET_DICT = {'(': ')', '{': '}', '[': ']'}

class StackItem:
    def __init__(self, value, prev_stack_item):
        self.value = value
        self.prev_stack_item = prev_stack_item



class Stack:
    def __init__(self):
        self.tail = None
        self.stack_len = 0

    def is_empty(self):
        if self.tail:
            return False
        return True

    def push(self, value):
        new_stack_item = StackItem(value, self.tail)
        self.tail = new_stack_item
        self.stack_len += 1

    def pop(self):
        if not self.tail:
            return
        value = self.tail.value
        self.tail = self.tail.prev_stack_item
        self.stack_len -= 1
        return value

    def peek(self):
        return self.tail.value

    def size(self):
        return self.stack_len


def get_key(value, dict_=BRACKET_DICT):
    for key, val in dict_.items():
        if val == value:
            return key


def is_correct_brackets(brackets_str, brackets_dict=BRACKET_DICT):
    bracket_stack = Stack()
    for bracket in brackets_str:
        if bracket in brackets_dict:
            bracket_stack.push(bracket)
        elif bracket in brackets_dict.values():
            open_bracket = get_key(bracket)
            if open_bracket == bracket_stack.peek():
                bracket_stack.pop()
            else:
                return
        else:
            print('Элемент не является скобкой')
            return
    return True

if __name__ == '__main__':
    brackets = '(((([{}]))))'
    if is_correct_brackets(brackets):
        print('Сбалансированно')
    else:
        print('Несбалансированно')



