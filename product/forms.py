from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(
        label="Nom",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=True,
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control"}),
        required=True,
    )


class QueryForm(forms.Form):
    query = forms.CharField(
        label="Query",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=True,
    )


class FavoriteForm(forms.Form):
    code = forms.IntegerField(
        label="Code",
        min_value=0,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        # widget=forms.NumberInput(attrs={'class': 'form-control'}),
        required=True,
    )
    is_favorite = forms.BooleanField(
        label="Favorite state",
        widget=forms.CheckboxInput(attrs={"class": "form-control"}),
        required=False,
    )
