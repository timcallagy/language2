from django import forms
from lambada.models import UserProfile, Topic
from django.contrib.auth.models import User
import pytz
from django.utils.translation import ugettext_lazy as _
from language2 import settings
#from crispy_forms.helper import FormHelper
#from crispy_forms.layout import MultiField, Layout, Alert

class UserForm(forms.ModelForm):
	error_css_class = 'error'
	password = forms.CharField(widget=forms.PasswordInput())
	password2 = forms.CharField(label=_("Repeat Password"), widget=forms.PasswordInput())

	def clean(self):
		username = self.cleaned_data.get('username')
		email = self.cleaned_data.get('email')
		password = self.cleaned_data.get('password')
		password2 = self.cleaned_data.get('password2')
		if User.objects.filter(username=username):
			raise forms.ValidationError(_("That username is already taken"))
		if User.objects.filter(email=email):
			raise forms.ValidationError(_("Someone has already registered with that email address"))
		if password and password != password2:
			raise forms.ValidationError(_("Passwords don't match"))
		return self.cleaned_data

	class Meta:
		model = User
		fields = ('username', 'email', 'password')
	

class UserProfileForm(forms.ModelForm):
	timezone = forms.ChoiceField(choices=[(x, x) for x in pytz.common_timezones])
	#language = forms.ChoiceField(choices=[(x, x) for x in ('en','ru')])
	language = forms.ChoiceField(label=_(u'Default Language'), choices=settings.LANGUAGES)

	class Meta:
		model = UserProfile
		fields = ('timezone', 'language')

class TopicForm(forms.ModelForm):
	language = forms.ChoiceField(label=_(u'Language'), choices=[(x, x) for x in ('en','ru')])

	class Meta:
		model = Topic
		fields = ('headline', 'language', 'learners_text', 'guides_text')

