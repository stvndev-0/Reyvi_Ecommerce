from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate

class LoginForm(AuthenticationForm):
	def __init__(self, *args, **kwargs):
		super(LoginForm, self).__init__(*args, **kwargs)
		self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Username'
        })
		self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password'
        })

	def clean_username(self):
		user = self.cleaned_data.get('username')
		if not User.objects.filter(username=user).exists():
			raise ValidationError('The user does not exist.')
		return user
	
	def clean_password(self):
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')
		if username:
			user = User.objects.filter(username=username).first()
			if user:
				# Intentar autenticar al usuario
				user = authenticate(username=username, password=password)
				if user is None:
					raise ValidationError('The password is incorrect.')
		return password

class SignUpForm(UserCreationForm):
	email = forms.EmailField(label="", required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Email'}))

	class Meta:
		model = User
		fields = ('username', 'email', 'password1', 'password2')

	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'Username'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted-white"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['placeholder'] = 'Password'
		self.fields['password1'].label = ''
		self.fields['password1'].help_text = '<ul class="form-text small text-muted-white"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

		self.fields['password2'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['placeholder'] = 'Confirm password'
		self.fields['password2'].label = ''
		self.fields['password2'].help_text = '<span class="form-text text-muted-white"><small>Enter the same password as before, for verification.</small></span>'

	def clean_email(self):
		email = self.cleaned_data.get('email')
		
		if not email.endswith('@gmail.com'):
			raise ValidationError('Only Gmail emails are allowed.')
		else:
			client_email = User.objects.filter(email=email)
			if client_email.exists():
				raise ValidationError('The email is already registered, please enter another one.')
			return email
	
class UpdateUserForm(UserChangeForm):
	# Ocultar el campo password
	password = None
	# Obtener otros campos
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}), required=True)

	class Meta:
		model = User
		fields = ('email',)