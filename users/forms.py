from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class LoginForm(AuthenticationForm):
	username = forms.CharField(label="Email", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
	password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class SignUpForm(UserCreationForm):
	email = forms.EmailField(label="", required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Email'}))
	terms_agreement = forms.BooleanField(required=True, error_messages={'required': 'You must agree to the terms to register.'})

	class Meta:
		model = User
		fields = ('email', 'password1', 'password2')

	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)

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
		
		if User.objects.filter(email=email).exists():
			raise ValidationError('The email is already registered, please enter another one.')
		
		return email
	
	def clean_password2(self):
		# Incluir mas validaciones
		pass

class UpdateUserForm(UserChangeForm):
	# Ocultar el campo password
	password = None
	# Obtener otros campos
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}), required=True)

	class Meta:
		model = User
		fields = ('email',)