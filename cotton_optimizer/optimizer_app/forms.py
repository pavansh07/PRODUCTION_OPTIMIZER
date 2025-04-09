# --- forms.py ---
from django import forms

COTTON_GRADES = [
    ('A', 'Grade A - Premium'),
    ('B', 'Grade B - Standard'),
    ('C', 'Grade C - Economy'),
]

class OptimizationInputForm(forms.Form):
    available_labor = forms.IntegerField(label="Available Labor (persons)")
    machine_hours = forms.FloatField(label="Available Machine Hours (optional)", required=False)
    selling_price = forms.FloatField(label="Selling Price per kg of Yarn (Rs)")
    optimize_for = forms.ChoiceField(
        choices=[('profit', 'Profit'), ('production', 'Production')],
        label="Optimization Goal"
    )
    cotton_grade = forms.ChoiceField(
        choices=COTTON_GRADES,
        label="Cotton Grade"
    )
