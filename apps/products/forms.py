from django import forms
from .models import Category, Brand

class ProductFilterForm(forms.Form):
    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), required=False)
    brand = forms.ModelMultipleChoiceField(queryset=Brand.objects.all(), required=False)
    min_price = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    max_price = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    sort_by = forms.ChoiceField(choices=[('price_asc', 'Giá tăng dần'), ('price_desc', 'Giá giảm dần')], required=False)
    items_per_page = forms.ChoiceField(choices=[(10, '10'), (20, '20')], required=False, initial=10)
