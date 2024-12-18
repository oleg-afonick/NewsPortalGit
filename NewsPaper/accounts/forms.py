from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django import forms


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
        ]


class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    username = forms.CharField(label="Имя пользователя")

    def __init__(self, *args, **kwargs):
        super(BaseRegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = 'Имя пользователя'
        self.fields['email'].help_text = 'Email'
        self.fields['password1'].help_text = 'Пароль'
        self.fields['password2'].help_text = 'Повторите пароль'

    class Meta:
        model = User
        fields = ("username",
                  "email",
                  "password1",
                  "password2",)

    def save(self, *args, **kwargs):
        user = super(BaseRegisterForm, self).save(*args, **kwargs)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user


class CommonSignupForm(SignupForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Убираем help_text для полей пароля
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''

    def save(self, request):
        user = super(CommonSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user


class CommonSocialSignupForm(SocialSignupForm):
    def save(self, request):
        user = super(CommonSocialSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user
