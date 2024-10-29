from django import forms
from store.models import Product, Category
from .models import StockProduct
# from .tasks import add_stock

class AddProductForm(forms.ModelForm):
    name = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    description = forms.TextInput()
    image = forms.ImageField(required=True)
    price = forms.DecimalField(required=True)
    is_sale = forms.CheckboxInput(attrs={'class': 'form-check-input'})
    discount_percentage = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'value': '0'}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=True)
    class Meta:
        model = Product
        fields = ('name', 'image', 'description', 'price', 'is_sale', 'discount_percentage', 'category',)

class AddStockForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects.all())
    quantity = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'value': '0'}))
    
    def save(self):
        product = self.cleaned_data['product']
        quantity = self.cleaned_data['quantity']

        # add_stock(product=product, amount=quantity)