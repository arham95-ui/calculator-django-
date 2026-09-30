from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django import forms
from .models import CalculationHistory
import ast
import re

# Define form inside views.py as a fallback
class CalculatorForm(forms.Form):
    expression = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter expression (e.g., 2+3*4)',
            'id': 'expression-input'
        })
    )

def calculate(expression):
    """
    Safe calculator function that evaluates mathematical expressions
    """
    expression = expression.replace(' ', '')
    allowed_chars = re.compile(r'^[\d+\-*/.()%^ ]+$')
    if not allowed_chars.match(expression):
        return "Error: Invalid characters in expression"
    
    try:
        def safe_eval(node):
            if isinstance(node, ast.BinOp):
                left = safe_eval(node.left)
                right = safe_eval(node.right)
                
                if isinstance(node.op, ast.Add):
                    return left + right
                elif isinstance(node.op, ast.Sub):
                    return left - right
                elif isinstance(node.op, ast.Mult):
                    return left * right
                elif isinstance(node.op, ast.Div):
                    if right == 0:
                        return "Error: Division by zero"
                    return left / right
                elif isinstance(node.op, ast.Pow):
                    return left ** right
                elif isinstance(node.op, ast.Mod):
                    return left % right
                elif isinstance(node.op, ast.FloorDiv):
                    if right == 0:
                        return "Error: Division by zero"
                    return left // right
            elif isinstance(node, ast.UnaryOp):
                operand = safe_eval(node.operand)
                if isinstance(node.op, ast.USub):
                    return -operand
                return operand
            elif isinstance(node, ast.Constant):
                return node.value
            else:
                return "Error: Unsupported operation"
        
        tree = ast.parse(expression, mode='eval')
        result = safe_eval(tree.body)
        
        if isinstance(result, float) and result.is_integer():
            result = int(result)
        
        return str(result)
    
    except ZeroDivisionError:
        return "Error: Division by zero"
    except Exception as e:
        return f"Error: Invalid expression"

def calculator_view(request):
    result = None
    expression = ''
    
    if request.method == 'POST':
        form = CalculatorForm(request.POST)
        if form.is_valid():
            expression = form.cleaned_data['expression']
            result = calculate(expression)
            
            if request.user.is_authenticated:
                CalculationHistory.objects.create(
                    user=request.user,
                    expression=expression,
                    result=result
                )
    else:
        form = CalculatorForm()
    
    history = None
    if request.user.is_authenticated:
        history = CalculationHistory.objects.filter(user=request.user)[:10]
    
    context = {
        'form': form,
        'result': result,
        'expression': expression,
        'history': history,
    }
    
    return render(request, 'calculator_app/calculator.html', context)

@login_required
def history_view(request):
    history = CalculationHistory.objects.filter(user=request.user)
    return render(request, 'calculator_app/history.html', {'history': history})