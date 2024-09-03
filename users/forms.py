from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User



# Faltan validaciones
class LoginForm(AuthenticationForm):
	# Ya que estoy extendiendo 'AuthenticationForm' y agregando placeholders a los campos del formulario, tengo
	# que sobrescribir el metodo '__init__'.
	def __init__(self, *args, **kwargs):
		super(LoginForm, self).__init__(*args, **kwargs)
		self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Username'
        })
		self.fields['password'].widget.attrs.update({
            'class': 'form-control rounded-3',
			'id': 'floatingPassword',
            'placeholder': 'Password'
        })

# Faltan validaciones
class SignUpForm(UserCreationForm):
	email = forms.EmailField(label="", required=True, widget=forms.TextInput(attrs={'class':'form-control'}))

	class Meta:
		model = User
		fields = ('username', 'email', 'password1', 'password2')

	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = ''
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted-white"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['placeholder'] = ''
		self.fields['password1'].label = ''
		self.fields['password1'].help_text = '<ul class="form-text small text-muted-white"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

		self.fields['password2'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['placeholder'] = ''
		self.fields['password2'].label = ''
		self.fields['password2'].help_text = '<span class="form-text text-muted-white"><small>Enter the same password as before, for verification.</small></span>'

	def clean_email(self):
		email = self.cleaned_data.get('email')
		if User.objects.filter(email=email).exists():
			raise forms.ValidationError('El email ya esta registrado, por favor introduzca otro.')
		return email