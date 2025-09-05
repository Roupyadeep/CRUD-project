from django import forms

class EmployeeForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=20, required=False)
    position = forms.CharField(max_length=100, required=False)
    salary = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
