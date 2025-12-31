import re
import sympy

class MathEngine:
    def __init__(self):
        self.x = sympy.Symbol('x')
        self.y = sympy.Symbol('y')

    def _preprocess(self, expression: str):
        """Mengubah 2x menjadi 2*x, xy menjadi x*y, dll."""
        # 1. Tambahkan * antara angka dan huruf (misal 2x -> 2*x)
        expr = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', expression)
        # 2. Tambahkan * antara huruf dan angka (misal x2 -> x*2)
        expr = re.sub(r'([a-zA-Z])(\d)', r'\1*\2', expr)
        # 3. Tambahkan * antara x dan y (misal xy -> x*y)
        expr = re.sub(r'([xX])([yY])', r'\1*\2', expr)
        # 4. Tambahkan * antara y dan x (misal yx -> y*x)
        expr = re.sub(r'([yY])([xX])', r'\1*\2', expr)
        # 5. Mengubah ^ menjadi ** (standar Python)
        expr = expr.replace('^', '**')
        return expr

    def evaluate(self, expression: str):
        try:
            clean_expr = self._preprocess(expression)
            expr_obj = sympy.sympify(clean_expr, locals={'x': self.x, 'y': self.y})
            result = expr_obj.evalf() if expr_obj.is_number else expr_obj
            return result
        except Exception as e:
            raise ValueError(f"Invalid Expression: {str(e)}")

    def get_plot_data(self, function_str: str, x_range=(-10, 10), y_range=(-10, 10)):
        try:
            # Preprocess sebelum plotting
            if '=' in function_str:
                lhs, rhs = function_str.split('=')
                clean_str = f"({self._preprocess(lhs)}) - ({self._preprocess(rhs)})"
            else:
                clean_str = self._preprocess(function_str)

            expr = sympy.sympify(clean_str, locals={'x': self.x, 'y': self.y})
            
            import numpy as np
            if 'y' in str(expr):
                x_vals = np.linspace(x_range[0], x_range[1], 200)
                y_vals = np.linspace(y_range[0], y_range[1], 200)
                X, Y = np.meshgrid(x_vals, y_vals)
                f = sympy.lambdify((self.x, self.y), expr, "numpy")
                Z = f(X, Y)
                return (X, Y, Z, True)
            else:
                f = sympy.lambdify(self.x, expr, "numpy")
                x_vals = np.linspace(x_range[0], x_range[1], 400)
                y_vals = f(x_vals)
                return (x_vals, y_vals, None, False)
        except Exception as e:
            raise ValueError(f"Plotting Error: {str(e)}")
    def evaluate(self, expression: str):
        try:
            clean_expr = self._preprocess(expression)
            # Menambahkan transformasi agar 1/0 tidak langsung crash
            expr_obj = sympy.sympify(clean_expr, locals={'x': self.x, 'y': self.y})
            
            # Cek pembagian dengan nol secara simbolik
            if expr_obj.is_infinite:
                return "Error: Division by Zero"
                
            result = expr_obj.evalf()
            return round(float(result), 6) if result.is_number else result
        except ZeroDivisionError:
            return "Error: Division by Zero"
        except Exception as e:
            return f"Error: Syntax Invalid"