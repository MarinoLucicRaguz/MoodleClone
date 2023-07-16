from django import forms
from django.contrib.auth.forms import UserChangeForm, AuthenticationForm
from django.core.validators import MaxValueValidator, MinValueValidator
from app1.models import *

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class SubjectForm(forms.ModelForm):
    ects = forms.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    sem_red = forms.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    sem_izv = forms.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nositelj'].queryset = Professor.objects.exclude(role__name__in=['STUDENT', 'ADMIN'])

    class Meta:
        model = Predmeti
        fields = '__all__'
 
class UserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ['username', 'password', 'role', 'status', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].queryset = Role.objects.exclude(name='ADMIN')

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        status = cleaned_data.get('status')

        if role and status:
            if role.name == 'PROFESSOR' and status != 'none':
                self.add_error('status', "Status must be 'none' for a professor.")
            elif role.name == 'STUDENT' and status == 'none':
                self.add_error('status', "Status cannot be 'none' for a student.")


from django.contrib.auth.hashers import make_password

class CustomUserChangeForm(UserChangeForm):
    password = forms.CharField(widget=forms.PasswordInput)

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.password = make_password(password)

        if commit:
            user.save()
        return user

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')

        if status:
            role = self.instance.role
            if role.name == 'PROFESSOR' and status != 'none':
                self.add_error('status', "Status must be 'none' for a professor.")
            elif role.name == 'STUDENT' and status == 'none':
                self.add_error('status', "Status cannot be 'none' for a student.")

    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email', 'status')

class EnrollmentForm(forms.Form):
    subjects = forms.ModelMultipleChoiceField(queryset=Predmeti.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)

