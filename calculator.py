import re

class Calculator:
    def evaluate(self, expression):
        try:
            # Only allow safe mathematical operations
            allowed_chars = set('0123456789+-*/.() ')
            if not all(c in allowed_chars for c in expression):
                return "Invalid characters in expression!"
            
            # Prevent code injection by checking for dangerous patterns
            if '__' in expression or 'import' in expression:
                return "Invalid expression!"
            
            result = eval(expression)
            return f"Result: {result}"
        except ZeroDivisionError:
            return "Cannot divide by zero!"
        except SyntaxError:
            return "Invalid mathematical expression!"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def calculate_simple(self, num1, operator, num2):
        try:
            num1 = float(num1)
            num2 = float(num2)
            
            if operator == '+':
                return f"{num1} + {num2} = {num1 + num2}"
            elif operator == '-':
                return f"{num1} - {num2} = {num1 - num2}"
            elif operator == '*':
                return f"{num1} * {num2} = {num1 * num2}"
            elif operator == '/':
                if num2 == 0:
                    return "Cannot divide by zero!"
                return f"{num1} / {num2} = {num1 / num2}"
            else:
                return "Invalid operator!"
        except ValueError:
            return "Invalid numbers!"
