# from django.shortcuts import render
# from .forms import OptimizationInputForm
# from .lp_solver import optimize_production

# def index(request):
#     result = None
#     if request.method == 'POST':
#         form = OptimizationInputForm(request.POST)
#         if form.is_valid():
#             inputs = form.cleaned_data
#             result = optimize_production(inputs)
#     else:
#         form = OptimizationInputForm()
#     return render(request, 'index.html', {'form': form, 'result': result})
# --- views.py ---


from django.shortcuts import render, redirect
from .forms import OptimizationInputForm
from .lp_solver import optimize_production

def index(request):
    if request.method == 'POST':
        form = OptimizationInputForm(request.POST)
        if form.is_valid():
            inputs = form.cleaned_data
            result = optimize_production(inputs)

            request.session['result'] = {
                'production': result['production'],
                'profit': result['profit'],
                'power_consumed': result['power_consumed'],
                'cost_breakdown': result['cost_breakdown'],
                'optimize_for': inputs['optimize_for'],
            }
            return redirect('results')  # Make sure this URL name is registered in urls.py
    else:
        form = OptimizationInputForm()

    return render(request, 'index.html', {'form': form})


def results(request):
    result = request.session.get('result')
    if not result:
        return redirect('index')

    # Prepare charts
    chart_data = {
        'labels': ['Yarn Production (kg)', 'Power Consumed (units)'],
        'values': [result['production'], result['power_consumed']]
    }

    production_data = {
        'labels': ['Production'],
        'values': [result['production']]
    }

    profit_data = {
        'labels': ['Profit'],
        'values': [result['profit']] if result['profit'] is not None else []
    }

    return render(request, 'results.html', {
        'result': result,
        'chart_data': chart_data,
        'production_data': production_data,
        'profit_data': profit_data
    })
