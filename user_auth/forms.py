from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django import forms
# Create your forms here.

# define the forbidden usernames validator
def forbidden_usernames_validator(value):
    forbidden_usernames = ['admin', 'settings', 'news', 'about', 'help', 'signin', 'signup',
        'signout', 'terms', 'privacy', 'cookie', 'new', 'login', 'logout', 'administrator',
        'join', 'account', 'username', 'root', 'blog', 'user', 'users', 'billing', 'subscribe',
        'reviews', 'review', 'blog', 'blogs', 'edit', 'mail', 'email', 'home', 'job', 'jobs',
        'contribute', 'newsletter', 'shop', 'profile', 'register', 'auth', 'authentication',
        'campaign', 'config', 'delete', 'remove', 'forum', 'forums', 'download', 'downloads',
        'contact', 'blogs', 'feed', 'faq', 'intranet', 'log', 'registration', 'search',
        'explore', 'rss', 'support', 'status', 'static', 'media', 'setting', 'css', 'js',
        'follow', 'activity']

    if value.lower() in forbidden_usernames:
        raise ValidationError('The username is a reserved word')

def invalid_username_validator(value):
    if '@' in value or '+' in value or '-' in value:
        raise ValidationError('Enter a valid username.')

def unique_email_validator(value):
    if User.objects.filter(email__iexact=value).exists():
        raise ValidationError('User with this email already taken')

def unique_username_ignore_case_validator(value):
    if User.objects.filter(username__iexact=value).exists():
        raise ValidationError('Sorry! Username already taken by another user')


class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    email = forms.CharField(required=True)

    class Meta:
        model = User
        include = ['email']
        exclude = ['last_login', 'date_joined']

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].validators.append(forbidden_usernames_validator)
        self.fields['username'].validators.append(invalid_username_validator)
        self.fields['username'].validators.append(unique_username_ignore_case_validator)
        self.fields['email'].validators.append(unique_email_validator)


    def clean(self):
        super(SignUpForm, self).clean()
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and password != confirm_password:
            self._errors['password'] = self.error_class(['Passwords don\'t match'])
        return self.cleaned_data
