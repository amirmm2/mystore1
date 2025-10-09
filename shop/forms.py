from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django.contrib.auth.models import User
from .models import Profile


class UpdateUserInfo(forms.ModelForm):
    phone = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'تلفن'}),
        required=False
    )
    address1 = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'آدرس'}),
        required=False
    )
    city = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'شهر'}),
        required=False
    )
    state = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'منطقه'}),
        required=False
    )
    zipcode = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'کدپستی'}),
        required=False
    )
    country = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'کشور'}),
        required=False
    )

    class Meta:
        model = Profile
        fields = ['phone', 'address1', 'city', 'state', 'zipcode', 'country']


class UpdatePasswordForm(SetPasswordForm):
    """
    نیازی به Meta نیست، SetPasswordForm خودش فیلدهای لازم را دارد.
    """


class UpdateUserForm(UserChangeForm):
    password = None  # حذف فیلد رمز عبور از فرم

    first_name = forms.CharField(
        max_length=30,
        required=True,
        label="نام",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        label="نام خانوادگی",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام خانوادگی'})
    )
    username = forms.CharField(
        max_length=30,
        required=True,
        label="نام کاربری",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام کاربری'})
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username")


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        label="نام",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        label="نام خانوادگی",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام خانوادگی'})
    )
    username = forms.CharField(
        max_length=30,
        required=True,
        label="نام کاربری",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام کاربری'})
    )
    password1 = forms.CharField(
        label="رمز عبور",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'رمز عبور'})
    )
    password2 = forms.CharField(
        label="تکرار رمز عبور",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'تکرار رمز عبور'})
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "password1", "password2")
