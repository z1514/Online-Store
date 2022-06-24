from django import forms

class LoginForm(forms.Form):
    userid = forms.CharField(label="user account",required=True)
    password = forms.CharField(label="password",widget=forms.PasswordInput)

class RegistrationForm(forms.Form):
    userid = forms.CharField(label='user account：', required=True)
    name = forms.CharField(label='name：', required=True)
    password1 = forms.CharField(label='password：', widget=forms.PasswordInput)
    password2 = forms.CharField(label='re-password：', widget=forms.PasswordInput)
    birthday = forms.DateField(label='birthday：', error_messages={'invalid': 'invalid date'})
    address = forms.CharField(label='mailing address：', required=False)
    phone = forms.CharField(label='telephone：', required=False)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('The passwords don\'t match')

        return password2