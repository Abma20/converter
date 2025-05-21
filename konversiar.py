import tkinter as tk
from tkinter import ttk

class Conversion:
    def __init__(self):
        self.top = -1
        self.stack = []
        self.output = []
        self.precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}

    def is_empty(self):
        return True if self.top == -1 else False

    def peek(self):
        return self.stack[-1]

    def pop(self):
        if not self.is_empty():
            self.top -= 1
            return self.stack.pop()
        else:
            return '$'

    def push(self, op):
        self.top += 1
        self.stack.append(op)

    def is_operand(self, ch):
        return ch.isalpha() or ch.isdigit()

    def not_greater(self, i):
        try:
            a = self.precedence[i]
            b = self.precedence[self.peek()]
            if i == '^':
                return True if a < b else False
            else:
                return True if a <= b else False
        except KeyError:
            return False

    def infix_to_postfix(self, exp):
        for char in exp:
            if self.is_operand(char):
                self.output.append(char)
            elif char == '(':
                self.push(char)
            elif char == ')':
                while not self.is_empty() and self.peek() != '(':
                    a = self.pop()
                    self.output.append(a)
                if not self.is_empty() and self.peek() != '(':
                    return -1
                else:
                    self.pop()
            else:
                while not self.is_empty() and self.not_greater(char):
                    self.output.append(self.pop())
                self.push(char)
        
        while not self.is_empty():
            self.output.append(self.pop())
        
        return "".join(self.output)

    def infix_to_prefix(self, exp):
        exp = exp[::-1]
        exp = list(exp)
        
        for i in range(len(exp)):
            if exp[i] == '(':
                exp[i] = ')'
            elif exp[i] == ')':
                exp[i] = '('

        exp = "".join(exp)
        exp = self.infix_to_postfix(exp)
        exp = exp[::-1]

        return exp

    def postfix_to_infix(self, exp):
        stack = []
        for char in exp:
            if self.is_operand(char):
                stack.append(char)
            else:
                op1 = stack.pop()
                op2 = stack.pop()
                stack.append(f'({op2}{char}{op1})')

        return stack.pop()

    def prefix_to_infix(self, exp):
        stack = []
        exp = exp[::-1]
        
        for char in exp:
            if self.is_operand(char):
                stack.append(char)
            else:
                op1 = stack.pop()
                op2 = stack.pop()
                stack.append(f'({op1}{char}{op2})')

        return stack.pop()

    def postfix_to_prefix(self, exp):
        return self.infix_to_prefix(self.postfix_to_infix(exp))

    def prefix_to_postfix(self, exp):
        return self.infix_to_postfix(self.prefix_to_infix(exp))


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Expression Converter")
        
        # Maksimalkan jendela
        self.root.state('zoomed')

        # Buat frame untuk memusatkan widget
        self.frame = ttk.Frame(root, padding=20)  # Menambahkan padding di frame
        self.frame.pack(expand=True, anchor='center')

        # Pengaturan font yang lebih besar
        font_large = ('Arial', 18)  # Ukuran font yang lebih besar

        # Pengaturan widget dengan font lebih besar
        self.exp_label = ttk.Label(self.frame, text="Enter Expression:", font=font_large)
        self.exp_label.pack(pady=10)  # Padding vertikal lebih besar

        self.exp_entry = ttk.Entry(self.frame, width=40, font=font_large)  # Lebih lebar
        self.exp_entry.pack(pady=10)

        self.result_label = ttk.Label(self.frame, text="Result:", font=font_large)
        self.result_label.pack(pady=10)

        self.result_display = ttk.Label(self.frame, text="", width=40, font=font_large)  # Lebih besar
        self.result_display.pack(pady=10)

        self.options = ["Infix to Postfix", "Infix to Prefix", "Postfix to Infix",
                        "Prefix to Infix", "Postfix to Prefix", "Prefix to Postfix"]
        
        self.option_var = tk.StringVar(value=self.options[0])
        self.option_menu = ttk.OptionMenu(self.frame, self.option_var, *self.options)
        self.option_menu.config(width=30)  # Lebih lebar
        self.option_menu.pack(pady=10)

        self.convert_button = ttk.Button(self.frame, text="Convert", command=self.convert_expression, style="TButton")
        self.convert_button.pack(pady=10)

        # Menambahkan styling untuk tombol
        style = ttk.Style()
        style.configure('TButton', font=font_large)  # Menambah font besar untuk tombol

    def convert_expression(self):
        exp = self.exp_entry.get()
        choice = self.options.index(self.option_var.get()) + 1
        converter = Conversion()
        
        if choice == 1:
            result = converter.infix_to_postfix(exp)
        elif choice == 2:
            result = converter.infix_to_prefix(exp)
        elif choice == 3:
            result = converter.postfix_to_infix(exp)
        elif choice == 4:
            result = converter.prefix_to_infix(exp)
        elif choice == 5:
            result = converter.postfix_to_prefix(exp)
        elif choice == 6:
            result = converter.prefix_to_postfix(exp)
        
        self.result_display.config(text=result)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
