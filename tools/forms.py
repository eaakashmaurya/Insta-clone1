from django import forms

class SandhiForm(forms.Form):
    txt1 = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter the first word','class': 'form-control mt-4 transliterate_input_sn'}))
    txt2 = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter the second word','class': 'form-control transliterate_input_sn'}))


class DictForm(forms.Form):
    choices=[("sans", "Sanskrit-to-English"), ("eng", "English-to-Sanskrit")]
    type = forms.ChoiceField(choices=choices, widget=forms.Select(attrs={'class': 'p-2 w-100 mt-4'}))
    txt = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Input word','class': 'form-control transliterate_input_sn', 'id' : 'textbox'}))

class SandhiSplitterForm(forms.Form):
    choices=[('समासच्छेदः', 'समासच्छेदः'),('पदच्छेदः', 'पदच्छेदः'), ('उभयोरपि', 'उभयोरपि')]
    txt = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Input word','class': 'form-control transliterate_input_sn'}))
    type = forms.ChoiceField(choices=choices, widget=forms.Select(attrs={'class': 'p-2 w-100 mt-4'}))
    
