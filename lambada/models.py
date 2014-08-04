from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, tzinfo
import pytz
from django.utils.timezone import utc
from django.core.urlresolvers import reverse
from tinymce.models import HTMLField
from django.utils.translation import ugettext_lazy as _
import secretballot

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
#	@property
#	def likes(self):
#		return TopicLikes.objects.filter(topic=self).count()
#	@property
#	def already_liked(self):
#		user = User.objects.filter(username=self.created_by)
#		print(user)
#		userProfile = UserProfile.objects.filter(user=user)
#		print(userProfile)
#		print("#### 1 ")
#		print("User: " + self)
#		return TopicLikes.objects.filter(topic=self).exists()
#		return TopicLikes.objects.filter(userProfile=userProfile).exists()

#secretballot.enable_voting_on(Topic)

class TopicLikes(models.Model):
	class Meta:
		unique_together = (('userProfile','topic'),)
	userProfile = models.ForeignKey(UserProfile, default=1)
	topic = models.ForeignKey(Topic, default=1)

#class PracticeDateTime(models.Model):
#	dateTime = models.DateTimeField(_(u"Practice Session Time"))
 

class Practice(models.Model):
	user = models.ForeignKey(User)
	topic = models.ForeignKey(Topic)
	dateTime= models.DateTimeField(_(u"Practice Session Time"))
	coach = models.CharField(_("Coach"), max_length=255, blank=True, null=True, default='')
	learners_writing= HTMLField(_("Write your text here (2000 words maximum)."), max_length=255)
	writing_complete = models.BooleanField(blank=True, default=False)
	speaking_report_published = models.BooleanField(blank=True, default=False)
	writing_report_published = models.BooleanField(blank=True, default=False)

	def get_absolute_url(self):
		return reverse('practice_list')


class Report(models.Model):
	practice = models.OneToOneField(Practice, primary_key=True)
	call_start_time = models.DateTimeField(blank=True, null=True)
	call_end_time = models.DateTimeField(blank=True, null=True)


class SpeakingError(models.Model):
	report = models.ForeignKey(Report)
	error_time_min = models.CharField(_("Minute"), max_length=2, blank=True, null=True, default='')
	error_time_sec = models.CharField(_("Second"), max_length=2, blank=True, null=True, default='')
	correction_text = models.CharField(_("Correction Text"), max_length=255, blank=True, null=True, default='')
	correction_recording = models.BooleanField(blank=True, default=False) #You could replace this with the File upload.


class WritingError(models.Model):
	report = models.ForeignKey(Report)
	original_text = models.CharField(_("Original Text"), max_length=255, blank=True, null=True, default='')
	correction_text = models.CharField(_("Correction Text"), max_length=255, blank=True, null=True, default='')


class Recording(models.Model):
	report = models.ForeignKey(Report)
	#blob = models.BinaryField(blank=True)
	partNum = models.IntegerField()


class Channel(models.Model):
	practice_pk = models.CharField(max_length=255, blank=True, null=True)
	message = models.CharField(max_length=3000, blank=True, null=True)
# Create your models here.
