from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms



User = get_user_model()

# class RegistrationForm(UserCreationForm):
#     first_name = forms.CharField(required=False, label="Имя")
#     last_name = forms.CharField(required=False, label="Фамилия")
#     parent_name = forms.CharField(required=False, label="Отчество")
#     city = forms.CharField(required=False, label="Город")
#     job_title = forms.CharField(required=False, label="Должность")
#     phone = forms.CharField(required=False, label="Телефон", widget=forms.TextInput(attrs={'placeholder': '+7 (999) 000-00-00'}))
#     kpp = forms.IntegerField(required=False, label="КПП")
#     inn = forms.IntegerField(required=False, label="ИНН")
#     organization = forms.CharField(required=False, label="Организация")
#     class Meta(UserCreationForm.Meta):
#         model = User
#         fields = ('first_name', 'last_name', 'parent_name', 'email', 'phone', 'city', 'organization', 'inn', 'kpp', 'job_title')


class RegistrationForm(forms.Form):
    # 1. Объявляем дополнительные поля
    first_name = forms.CharField(required=False, label="Имя", widget=forms.TextInput(attrs={'placeholder': 'Имя (необязательно)'}))
    last_name = forms.CharField(required=False, label="Фамилия", widget=forms.TextInput(attrs={'placeholder': 'Фамилия (необязательно)'}))
    parent_name = forms.CharField(required=False, label="Отчество", widget=forms.TextInput(attrs={'placeholder': 'Отчество (необязательно)'}))    
    city = forms.CharField(required=False, label="Город", widget=forms.TextInput(attrs={'placeholder': 'Город (необязательно)'}))
    job_title = forms.CharField(required=False, label="Должность", widget=forms.TextInput(attrs={'placeholder': 'Должность (необязательно)'}))
    phone = forms.CharField(required=False, label="Телефон", widget=forms.TextInput(attrs={'placeholder': '+7 (999) 000-00-00 (необязательно)'}))
    kpp = forms.IntegerField(required=False, label="КПП", widget=forms.TextInput(attrs={'placeholder': 'КПП (необязательно)'}))
    inn = forms.IntegerField(required=False, label="ИНН", widget=forms.TextInput(attrs={'placeholder': 'ИНН (необязательно)'}))
    organization = forms.CharField(required=False, label="Организация", widget=forms.TextInput(attrs={'placeholder': 'Организация (необязательно)'}))

    agreement = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'style': 'margin-right: 5px; cursor: pointer;',

        })        
    )

    agreement_2 = forms.BooleanField(
        required=True,
                widget=forms.CheckboxInput(attrs={
                    'class': 'form-check-input',
                    'style': 'margin-right: 5px; cursor: pointer;',             
                })  
    )
    
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
                
        self.field_order = [
            'last_name',     
            'first_name',
            'parent_name',   
            'email',       
            'phone',
            'city',
            'organization',
            'inn',
            'kpp',
            'job_title',                       
        ]
    
    def signup(self, request, user):
        user.first_name = self.cleaned_data.get("first_name", "")
        user.last_name = self.cleaned_data.get("last_name", "")
        user.parent_name = self.cleaned_data.get("parent_name", "")
        user.city = self.cleaned_data.get("city", "")
        user.phone = self.cleaned_data.get("phone", "")
        user.organization = self.cleaned_data.get("organization", "")
        user.inn = self.cleaned_data.get("inn")
        user.kpp = self.cleaned_data.get("kpp")
        user.job_title = self.cleaned_data.get("job_title", "")
        user.agreement = self.cleaned_data.get("agreement", False)
        user.agreement_2 = self.cleaned_data.get("agreement_2", False)
        user.save()


class UserForm(forms.ModelForm):
    first_name = forms.CharField(required=False, label="Имя")
    last_name = forms.CharField(required=False, label="Фамилия")
    parent_name = forms.CharField(required=False, label="Отчество")
    city = forms.CharField(required=False, label="Город")
    job_title = forms.CharField(required=False, label="Должность")
    phone = forms.CharField(required=False, label="Телефон", widget=forms.TextInput(attrs={'placeholder': '+7 (999) 000-00-00'}))
    kpp = forms.IntegerField(required=False, label="КПП")
    inn = forms.IntegerField(required=False, label="ИНН")
    organization = forms.CharField(required=False, label="Организация")
    class Meta:
        model = User
        # fields = ('first_name', 'last_name', 'email')
        fields = ('first_name', 'last_name', 'parent_name', 'email', 'phone', 'city', 'organization', 'inn', 'kpp', 'job_title')