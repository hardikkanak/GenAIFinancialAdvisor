from django import forms
from django.contrib.auth import authenticate
from .models import CustomUser

class FinancialAdviceForm(forms.Form):
    AGE_CHOICES = [
        ('18-24', '18-24'),
        ('25-35', '25-35'),
        ('36-45', '36-45'),
        ('46-55', '46-55'),
        ('56+', '56+'),
    ]
    
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    
    OBJECTIVE_CHOICES = [
        ('Capital Appreciation', 'Capital Appreciation'),
        ('Income', 'Income'),
        ('Growth', 'Growth'),
        ('Wealth Preservation', 'Wealth Preservation'),
    ]
    
    FACTOR_CHOICES = [
        ('Returns', 'Returns'),
        ('Risk', 'Risk'),
        ('Liquidity', 'Liquidity'),
        ('Tax Benefits', 'Tax Benefits'),
    ]
    
    DURATION_CHOICES = [
        ('<1 year', '<1 year'),
        ('1-3 years', '1-3 years'),
        ('3-5 years', '3-5 years'),
        ('5+ years', '5+ years'),
    ]
    
    EXPECT_CHOICES = [
        ('<10%', '<10%'),
        ('10%-20%', '10%-20%'),
        ('20%-30%', '20%-30%'),
        ('30%+', '30%+'),
    ]
    
    AVENUE_CHOICES = [
        ('Mutual Fund', 'Mutual Fund'),
        ('Equity', 'Equity'),
        ('Fixed Deposits', 'Fixed Deposits'),
        ('Government Bonds', 'Government Bonds'),
        ('Gold', 'Gold'),
    ]
    
    age = forms.ChoiceField(choices=AGE_CHOICES, initial='25-35')
    gender = forms.ChoiceField(choices=GENDER_CHOICES, initial='Male')
    objective = forms.ChoiceField(choices=OBJECTIVE_CHOICES, initial='Capital Appreciation')
    factor = forms.ChoiceField(choices=FACTOR_CHOICES, initial='Returns')
    duration = forms.ChoiceField(choices=DURATION_CHOICES, initial='3-5 years')
    expect = forms.ChoiceField(choices=EXPECT_CHOICES, initial='20%-30%')
    avenue = forms.ChoiceField(choices=AVENUE_CHOICES, initial='Mutual Fund')
class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        user = authenticate(email=self.cleaned_data['email'], password=self.cleaned_data['password'])
        if not user:
            raise forms.ValidationError("Invalid email or password")
        return self.cleaned_data
class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email']

    def clean(self):
        cd = self.cleaned_data
        if cd['password'] != cd['confirm_password']:
            raise forms.ValidationError("Passwords do not match")
        return cd