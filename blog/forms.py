from django import forms


class CommentForm(forms.Form):
    comment = forms.CharField(required=True, max_length=1024, label='Comment')


class SignInForm(forms.Form):
    email = forms.EmailField(required=True, label='email', max_length=255)
    password = forms.CharField(max_length=25, required=True, label='password')


class SignUpForm(SignInForm):
    fn = forms.CharField(max_length=35, required=True, label='fn')
    ln = forms.CharField(max_length=35, required=True, label='ln')
