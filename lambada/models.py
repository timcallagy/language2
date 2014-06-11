from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, tzinfo
import pytz
from django.utils.timezone import utc
from django.core.urlresolvers import reverse
from tinymce.models import HTMLField
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
	learners_text = HTMLField(_("Enter the Learner's information below. Click here to see an example.")) 
	guides_text = HTMLField(_("Enter the Guide's information below. Click here to see an example.")) 
#	text = BleachField()
	def get_absolute_url(self):
		return reverse('topic_detail', kwargs={'pk': self.pk})

class Practice(models.Model):
	userProfile = models.ForeignKey(UserProfile)

class Report(models.Model):
	userProfile = models.ForeignKey(UserProfile)

# Create your models here.
