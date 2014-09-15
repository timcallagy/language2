import datetime
import pytz
from datetimewidget.widgets import DateTimeWidget
from schedule.models.calendars import Calendar
from schedule.periods import Day
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.forms.widgets import SplitDateTimeWidget
from django.db import models
from django.utils.timezone import utc
from lambada.models import UserProfile, Topic, Practice, SpeakingError
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
		fields = ('headline', 'language', 'learners_speaking_instructions', 'learners_writing_instructions', 'guides_speaking_instructions')


class PracticeForm(forms.ModelForm):
	dateTime = forms.DateTimeField(label=_('When'), widget=forms.SplitDateTimeWidget(date_format='%Y-%m-%d'))
	
	class Meta:
		model = Practice
		fields = ('dateTime',)	
		dateTime = forms.SplitDateTimeField(input_date_formats=['%Y-%m-%d'], input_time_formats=['%H:%M'])

	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		self.pk = kwargs.pop('pk', None)
		super(PracticeForm, self).__init__(*args, **kwargs)

	def clean(self):
		now = datetime.datetime.utcnow().replace(tzinfo=utc)
		bookingTime = self.cleaned_data.get('dateTime')
		print(bookingTime)

		# Check that the booking is in the future.
		if now > bookingTime:
			raise forms.ValidationError(_("That time has already passed!"))
		latestBookingTime = bookingTime - datetime.timedelta(hours=3)
		print(latestBookingTime)

		# Check that they are booking in advance.
		if now > latestBookingTime:
			raise forms.ValidationError(_("You can't book a lesson less than 3 hours before the lesson start time"))

		# Check if a coach is available and create a practice session (not yet paid).
		coach_list = UserProfile.objects.all().order_by('-total_coach_rating')
                coach_available = False
                for coach in coach_list:
                        try:
                                practice_list = Practice.objects.get(coach=coach, dateTime=bookingTime)
                        except Practice.DoesNotExist:
                                calendar = Calendar.objects.get(name=coach)
                                event_list = calendar.event_set.all()
                                occurrences = Day(event_list, bookingTime)._get_sorted_occurrences()
                                for o in occurrences:
                                        if o.start <= bookingTime and o.end > bookingTime:
                                                coach_available = True
                                                break
                                print('Coach available:')
                                print(coach_available)
                                if coach_available == True:
                                        break
		if coach_available == False:
			raise forms.ValidationError(_("Sorry, but there is no coach available at that time"))
		else:
			print('Chosen coach:')
			print(coach)
			topic = Topic.objects.get(pk=self.pk)
			practice = Practice(
				user = self.request.user,
				topic = topic,
				dateTime = bookingTime,
				coach = coach 
			)
			practice.save()

		return self.cleaned_data


class PracticeWritingForm(forms.ModelForm):
	def clean(self):
		return self.cleaned_data

	class Meta:
		model = Practice
		fields = ('learners_writing',)


class SpeakingErrorForm(forms.ModelForm):
	#language = forms.ChoiceField(label=_(u'Language'), choices=[(x, x) for x in ('en','ru')])
	#error_time_min = forms.ChoiceField(choices=[(x, x) for x in (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20)])
	error_time_min = forms.ChoiceField(choices=[(x, x) for x in range(21)])
	error_time_sec = forms.ChoiceField(choices=[(x, x) for x in range(61)])

	def clean(self):
		return self.cleaned_data

	class Meta:
		model = SpeakingError
		fields = ('error_time_min','error_time_sec')
