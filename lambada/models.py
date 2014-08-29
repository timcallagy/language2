import pytz
import secretballot
from tinymce.models import HTMLField
from datetime import datetime, tzinfo
from django.utils.timezone import utc
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

# blank=True means the field will NOT be required in forms.
# null=True means you are going to allow a field to be blank in your DB.
# Note: charField and textField are never stored as null but rather as an empty string ''.i
# So blank=False and null=True don't make logical sense.
# blank=True and null=True is ok.
# blank=True and null=False only makes sense for charField and textField.

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	payment_addr = models.CharField(max_length=255, blank=True, null=True)
	skype_addr = models.CharField(max_length=255, blank=True, null=True)
	picture = models.ImageField(upload_to='profile_images', blank=True)
	timezone = models.CharField(max_length=255, blank=False, null=False, default='GMT')
	language = models.CharField(max_length=255, blank=False, null=False, default='en')
	def __unicode__(self):
		return self.user.username
	#def get_absolute_url(self):
	#	return reverse('index')

# Each UserProfile has many Subscriptions, each Subscription has only one UserProfile
class Subscription(models.Model):
	userProfile = models.ForeignKey(UserProfile)

class Rating(models.Model):
	userProfile = models.ForeignKey(UserProfile)

class Comment(models.Model):
	userProfile = models.ForeignKey(UserProfile)

class Topic(models.Model):
	created_by = models.ForeignKey(User)
	headline = models.CharField(_("Topic Headline"), max_length=255, blank=False, null=False, default='')
	language = models.CharField(_("Topic Language"), max_length=255, blank=False, null=False, default='en')
	creation_date = models.DateTimeField(blank=False, null=False, default=datetime.now())
	learners_speaking_instructions = HTMLField(_("Enter the Learner's Speaking Instructions below. Click here to see an example.")) 
	learners_writing_instructions = HTMLField(_("Enter the Learner's Writing Instructions below. Click here to see an example.")) 
	guides_speaking_instructions = HTMLField(_("Enter the Guide's information below. Click here to see an example.")) 
	published = models.NullBooleanField(blank=True, null=True, default=False)
#	text = BleachField()
	def get_absolute_url(self):
		return reverse('topic_detail', kwargs={'pk': self.pk})


class Practice(models.Model):
	user = models.ForeignKey(User)
	topic = models.ForeignKey(Topic)
	dateTime = models.DateTimeField(_(u"Practice Session Time"))
	timeUntil = models.IntegerField(null=False, default=0)
	coach = models.CharField(_("Coach"), max_length=255, blank=True, null=True, default='')
	learners_writing = HTMLField(_("Write your text here (2000 words maximum)."), max_length=255)
	coach_recording_count = models.IntegerField(null=False, default=0)
	learner_recording_count = models.IntegerField(null=False, default=0)
	writing_complete = models.BooleanField(blank=True, default=False)
	speaking_report_published = models.BooleanField(blank=True, default=False)
	writing_report_published = models.BooleanField(blank=True, default=False)

	def get_absolute_url(self):
		return reverse('practice_list')


#class Report(models.Model):
#	practice = models.OneToOneField(Practice, primary_key=True)
#	call_start_time = models.DateTimeField(blank=True, null=True)
#	call_end_time = models.DateTimeField(blank=True, null=True)


class LearnerRecording(models.Model):
	practice = models.ForeignKey(Practice)
	count = models.IntegerField(null=False, default=0)
	recording = models.FileField(upload_to='learnerRecordings', blank=True, null=True)
	call_start_time = models.DateTimeField(blank=True, null=True)


class SpeakingError(models.Model):
	practice = models.ForeignKey(Practice)
	coach = models.ForeignKey(User)
	learnerRecording = models.ForeignKey(LearnerRecording)
	error_time_min = models.CharField(_("Minute"), max_length=2, blank=True, null=True, default='')
	error_time_sec = models.CharField(_("Second"), max_length=2, blank=True, null=True, default='')
	correction_text = models.CharField(_("Correction Text"), max_length=255, blank=True, null=True, default='')
	correction_recording_flag = models.BooleanField(blank=True, default=False)
	correction_recording = models.FileField(upload_to='corrections', blank=True, null=True)	
	STATES = (
			('WAITING', 'Waiting'),
			('SPEAKING', 'Speaking'),
			('WRITING', 'Writing'),
			('COMPLETE', 'Complete'),
			)
	state = models.CharField(max_length=8, choices=STATES)


class WritingError(models.Model):
	practice = models.ForeignKey(Practice)
	coach = models.ForeignKey(User)
	original_text = models.CharField(_("Original Text"), max_length=255, blank=True, null=True, default='')
	correction_text = models.CharField(_("Correction Text"), max_length=255, blank=True, null=True, default='')


#class CorrectionRecording(models.Model):
#	error = models.ForeignKey(SpeakingError)
#	correctionRec = models.FileField(upload_to='corrections')	


class ChannelPrivate(models.Model):
	practice_pk = models.CharField(max_length=255, blank=True, null=True)
	message = models.CharField(max_length=3000, blank=True, null=True)


class ChannelDefault(models.Model):
	practice_pk = models.CharField(max_length=255, blank=True, null=True)
	message = models.CharField(max_length=3000, blank=True, null=True)
# Create your models here.
