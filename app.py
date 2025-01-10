from flask import Flask, render_template, request, jsonify
import sympy as sm
import re  
import json
from mangum import Mangum

# Existing code setup
app = Flask(__name__)
a, b, d, t, x, y, z = sm.symbols('a b d t x y z')

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    expression = ''
    operation = ''
    latex_result = ''

    if request.method == 'POST':
        expression = request.form['expression']
        operation = request.form['operation']
        
        # Replace e**x with exp(x) to make sure SymPy interprets it correctly
        expression = re.sub(r'e\*\*([a-zA-Z0-9_]+)', r'exp(\1)', expression)

        # Insert an asterisk between numbers and letters using regex
        expression = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', expression)

        try:
            expr = sm.sympify(expression)
            if operation == 'diff':
                result = sm.diff(expr, x)
            elif operation == 'expand':
                result = sm.expand(expr)
            elif operation == 'solve':
                result = sm.solve(expr, x)
            elif operation == 'simplify':
                result = sm.simplify(expr)
            elif operation == 'factor':
                result = sm.factor(expr)
            elif operation == 'rationalize':
                result = sm.together(expr)
            elif operation == 'diffx':
                result = sm.diff(expr, x)
            elif operation == 'diffy':
                result = sm.diff(expr, y)
            elif operation == 'diffz':
                result = sm.diff(expr, z)
            elif operation == 'integratex':
                integral_result = sm.integrate(expr, x)
                result = integral_result + sm.Symbol('C') if integral_result != 0 else sm.Symbol('C')
            elif operation == 'integratey':
                integral_result = sm.integrate(expr, y)
                result = integral_result + sm.Symbol('C') if integral_result != 0 else sm.Symbol('C')
            elif operation == 'integratez':
                integral_result = sm.integrate(expr, z)
                result = integral_result + sm.Symbol('C') if integral_result != 0 else sm.Symbol('C')
            elif operation == 'limit':
                # Assuming limit as x approaches 0, you can modify as needed
                limit_point = float(request.form['limit_point'])
                result = sm.limit(expr, x, limit_point)
            elif operation == 'ode':
                # Solving the ODE expr with respect to t
                result = sm.dsolve(expr, x)
            elif operation == 'series':
                # Compute the series expansion around a point (e.g., x=0)
                expansion_point = float(request.form['expansion_point'])
                result = sm.series(expr, x, expansion_point, n=6)  # n is the number of terms
                
            latex_result = sm.latex(result)
            
        except Exception as e:
            result = f"Error: {str(e)}"
            latex_result = None

    return render_template('index.html', result=result, expression=expression, latex_result=latex_result)

handler = Mangum(app)

# Chatbot integration

# Define the model class

if __name__ == '__main__':
    app.run(port=5000, debug=True)
