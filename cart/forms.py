from django import forms

PRODUCT_QTY_CHOICE = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QTY_CHOICE, coerce=int)
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
