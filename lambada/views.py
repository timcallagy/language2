import os
import json
import pytz
import datetime
import time
from random import randint
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView, DetailView, ListView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, StreamingHttpResponse, Http404, HttpResponseForbidden
from django.utils.timezone import utc
from django.utils.translation import ugettext as _
from django.utils import translation
from django.core.mail import send_mail
from django.core import serializers
from django.core.files import File
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import ensure_csrf_cookie
from django.conf import settings
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Max
from lambada.forms import UserForm, UserProfileForm, TopicForm, PracticeForm, PracticeWritingForm, SpeakingErrorForm
from lambada.models import Topic, UserProfile, Practice, LearnerRecording, SpeakingError, WritingError, ChannelPrivate, ChannelDefault


##################################
###
### Landing Page 
###
##################################


class Index(TemplateView):
	template_name = 'lambada/index.html'

	# This code gets User and Profile forms to display in the Registration popup box.
	def get_context_data(self, **kwargs):
		context = super(Practice, self).get_context_data(**kwargs)
		context['user_form'] = UserForm()
		context['userprofile_form'] = UserProfileForm()
		return context


##################################
###
### Registration and Authorization
###
##################################


def register(request):
	context = RequestContext(request)
	
	if request.method == 'POST':
		# Get the User and UserProfile info from the form's POST
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)

		# If the form information is valid, do this.
		if user_form.is_valid() and profile_form.is_valid():
			#Save the User information to the DB, and get a User object instance.
			user = user_form.save()
			if user:
				user.set_password(user.password)
				user.save()
				profile = profile_form.save(commit=False)
				profile.user = user
				profile.timezone = request.POST['timezone']
				request.session['django_timezone'] = request.POST['timezone']
				profile.language = request.POST['language']
				profile.save()
				user = authenticate(username=user.username, password=request.POST['password'])
				request.session['django_language'] = request.POST['language']
				login(request, user)
				return HttpResponseRedirect('/dashboard/')
			else:
				return HttpResponse('Error saving to the database.')
		else:
			return render_to_response('lambada/register.html', {'timezones': pytz.common_timezones, 'user_form': user_form, 'userprofile_form': profile_form}, context)
	else:
		user_form = UserForm()
		userprofile_form = UserProfileForm()
		return render_to_response('lambada/register.html', {'timezones': pytz.common_timezones, 'user_form': user_form, 'userprofile_form': userprofile_form}, context)


def user_login(request):
	context = RequestContext(request)
	next_page = request.GET.get('next', '')
	user_form = UserForm()
	userprofile_form = UserProfileForm()
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		next_page = request.POST['next_page']
		user = authenticate(username=username, password=password)

		if user:
			login(request, user)
			language = UserProfile.objects.get(user=request.user.id).language
			request.session['django_timezone'] = UserProfile.objects.get(user=request.user.id).timezone
			request.session['django_language'] = language
			if next_page:
				return HttpResponseRedirect(next_page)
			else:
				return HttpResponseRedirect('/dashboard/')
		else:
			return render_to_response('lambada/invalid_login.html', context)
	else:
		return render_to_response('lambada/login.html', {'user_form': user_form, 'userprofile_form': userprofile_form, 'next_page': next_page}, context)


@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/')


def forgot_login(request):
	context = RequestContext(request)
	if request.method == 'POST':
		try:
			email=request.POST['email']
			user = User.objects.get(email=email)
			if user:
				username = user.username
				password = user.password
				send_mail("Language Lambada - login details reminder", "Username: " + username + ", Password: " + password, "Bizi Team  <info@lambada-english.com>", [email])
				confirmation = _("An email with your login details has been sent.")
				return render_to_response('lambada/forgot_login.html', {'confirmation': confirmation}, context)

		except User.DoesNotExist:
			error = _("Sorry - that email address is not registered.")
			return render_to_response('lambada/forgot_login.html', {'error': error}, context)
	else:
		return render_to_response('lambada/forgot_login.html', context)


################################
###
### Dashboard
###
################################


@login_required
def dashboard(request):
	context = RequestContext(request)
	current_time = datetime.datetime.utcnow().replace(tzinfo=utc)
	end_of_week = current_time + datetime.timedelta(days=7)
	upcoming_coaching_sessions = Practice.objects.filter(coach=request.user.username, dateTime__lte=end_of_week, dateTime__gte=current_time)
	upcoming_practice_sessions = Practice.objects.filter(user_id=request.user.id, dateTime__lte=end_of_week, dateTime__gte=current_time)
	pending_speech_reports = Practice.objects.filter(coach=request.user.username, dateTime__lte=current_time, speaking_report_published=False).order_by('dateTime')
	pending_writing_reports = Practice.objects.filter(coach=request.user.username, writing_complete=True, writing_report_published=False)
	return render_to_response('lambada/dashboard.html', {'upcoming_coaching_sessions': upcoming_coaching_sessions, 'upcoming_practice_sessions': upcoming_practice_sessions, 'pending_speech_reports': pending_speech_reports, 'pending_writing_reports': pending_writing_reports}, context)


################################
###
### Topics
###
################################


class TopicCreate(CreateView):
	model = Topic
	form_class = TopicForm
	
	def form_valid(self, form):
		form.instance.created_by = self.request.user
		form.instance.creation_date = datetime.datetime.now()
		return super(TopicCreate, self).form_valid(form)


class TopicDetail(DetailView):
	model = Topic

	def get_object(self, queryset=None):
		if queryset is None:
			queryset = self.get_queryset()
		pk = self.kwargs.get(self.pk_url_kwarg, None)
		queryset = queryset.filter(pk=pk, created_by=self.request.user)
		try:
			obj = queryset.get()
		except ObjectDoesNotExist:
			raise Http404()
		return obj
	###$ Class Designer


class TopicList(ListView):
	paginate_by = 10
		
	def get_queryset (self):
		return Topic.objects.filter(created_by=self.request.user)


@login_required
def topic_publish(request, pk):
	context = RequestContext(request)
	try:
		topic=Topic.objects.get(pk=pk)
		if topic.created_by == request.user:
			topic.published=True
			topic.save()
			return HttpResponseRedirect('/topic/list/')
		else:
			return render_to_response('lambada/404.html', {}, context)
	except Topic.DoesNotExist:
		return HttpResponse('Error: Topic does not exist.')


class TopicUpdate(UpdateView):
	model = Topic
	form_class = TopicForm
	template_name = 'lambada/topic_update.html'

	def get_object(self, queryset=None):
		if queryset is None:
			queryset = self.get_queryset()
		pk = self.kwargs.get(self.pk_url_kwarg, None)
		queryset = queryset.filter(pk=pk, created_by=self.request.user)
		try:
			obj = queryset.get()
		except ObjectDoesNotExist:
			raise Http404()
		return obj


class TopicDelete(DeleteView):
	model = Topic
	success_url = '/topic/list/'

	def get_object(self, queryset=None):
		if queryset is None:
			queryset = self.get_queryset()
		pk = self.kwargs.get(self.pk_url_kwarg, None)
		queryset = queryset.filter(pk=pk, created_by=self.request.user)
		try:
			obj = queryset.get()
		except ObjectDoesNotExist:
			raise Http404()
		return obj


################################
###
### Learner's Practice sessions
###
################################


# Learner views Topics available for booking on this page.
class PracticeBook(ListView):
	paginate_by = 3
	template_name = 'lambada/practice_book.html'

	def get_queryset (self):
		return Topic.objects.filter(published=True).exclude(created_by=self.request.user)
		
	def get_context_data(self, **kwargs):
		context = super(PracticeBook, self).get_context_data(**kwargs)
		context['practice_form'] = PracticeForm()
		return context


# Learner books a Practice session here. 
@login_required
def practice_add(request, pk):
	context = RequestContext(request)
#	user_id=request.user.id
#	user = User.objects.get(pk=user_id)
	topic = Topic.objects.get(pk=pk)
	dateTime = request.POST.get('dateTime_0')
	practice, created = Practice.objects.get_or_create(
			user = request.user,
			topic = topic,
			dateTime = dateTime,
			### TO DO ###
			### Smart coach picking ##
			coach = "timc"
	)
	return HttpResponseRedirect('/practice/list/')


# Learner pays for their Practice session here.
@login_required
def practice_payment(request, pk):
	context = RequestContext(request)
	topic = Topic.objects.get(pk=pk)
	naive = datetime.datetime.strptime(request.POST.get('dateTime_0', datetime.datetime.now), '%Y-%m-%d %H:%M:%S')
	tz = pytz.timezone(request.session['django_timezone'])
	aware = tz.localize(naive)
	return render_to_response('lambada/practice_payment.html', {'object': topic, 'dateTime': aware}, context)
	###$ Method Learner
	
	
# Details (time, language, instructions) of a learner's particular Practice session are shown on this page. Redundant?
class PracticeTopicDetail(DetailView):
	model = Topic
	template_name = 'lambada/practice_topic_detail.html'

	def get_context_data(self, **kwargs):
		context = super(PracticeTopicDetail, self).get_context_data(**kwargs)
		context['practice_form'] = PracticeForm()
		return context


# Learner views a list of their booked Practice sessions on this page. 
#class PracticeList(ListView):
#	paginate_by = 6
#	template_name = 'lambada/practice_list.html'

#	def get_queryset (self):
#		return Practice.objects.filter(user=self.request.user).filter(dateTime__lte=datetime.datetime.utcnow().replace(tzinfo=utc)).order_by('-dateTime')

#	def get_context_data(self, **kwargs):
#		context = super(PracticeList, self).get_context_data(**kwargs)
#		now = datetime.datetime.utcnow().replace(tzinfo=utc)
#		practice_upcoming = Practice.objects.filter(user=self.request.user).filter(dateTime__gte=datetime.datetime.utcnow().replace(tzinfo=utc)).order_by('dateTime')
#		for practice in practice_upcoming:
#			date = practice.dateTime;
#			practice.timeUntil = ((date - now).total_seconds()) 
#			practice.save()
#		context['practice_upcoming'] = practice_upcoming

@login_required
def practice_list(request):
	context = RequestContext(request)
	practices_list = Practice.objects.filter(user=request.user).order_by('-dateTime')
	now = datetime.datetime.utcnow().replace(tzinfo=utc)
	paginator = Paginator(practices_list, 6)

	page = request.GET.get('page')
	try:
		practices = paginator.page(page)
	except PageNotAnInteger:
        # If page is not an integer, deliver first page.
		practices = paginator.page(1)
	except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
		practices = paginator.page(paginator.num_pages)

	for practice in practices:
		date = practice.dateTime;
		timeUntil = (date - now).total_seconds()
		practice.timeUntil = timeUntil
		if timeUntil > 21600:
			practice.state = 'WAITING'
		elif timeUntil <= 21600 and timeUntil > 0:
			practice.state = 'NOMODIFY'
		elif timeUntil <= 0 and timeUntil > -1500:
			practice.state = 'SPEAKING'
		elif timeUntil <= -1500 and timeUntil > -3600:
			practice.state = 'WRITING'
		else:
			practice.state = 'COMPLETE'

	errors_max = SpeakingError.objects.filter(learner=practice.user).aggregate(Max('id'))['id__max']
	try:
		speakingError = SpeakingError.objects.get(pk=randint(1, errors_max))
	except SpeakingError.DoesNotExist:
		pass
	print('errors_max: ' + str(errors_max))
	return render_to_response('lambada/practice_list.html', {'practices': practices, 'paginator': paginator, 'speakingError': speakingError, 'S3_URL': settings.S3_URL}, context)


# TO DO: Don't allow Modifications if the pratice sessions is less than 6 hours away.
class PracticeUpdate(UpdateView):
	model = Practice 
	form_class = PracticeForm
	template_name = 'lambada/practice_update.html'

	def get_object(self, queryset=None):
                if queryset is None:
                        queryset = self.get_queryset()
                pk = self.kwargs.get(self.pk_url_kwarg, None)
                queryset = queryset.filter(pk=pk, user=self.request.user)
                try:
                        obj = queryset.get()
                except ObjectDoesNotExist:
                        raise Http404()
                return obj 


class PracticeDelete(DeleteView):
	model = Practice
	success_url = '/practice/list/'

	def get_object(self, queryset=None):
                if queryset is None:
                        queryset = self.get_queryset()
                pk = self.kwargs.get(self.pk_url_kwarg, None)
                queryset = queryset.filter(pk=pk, user=self.request.user)
                try:
                        obj = queryset.get()
                except ObjectDoesNotExist:
                        raise Http404()
                return obj 


################################
###
### Coach's Practice sessions
###
################################


class CoachList(ListView):
	paginate_by = 3
	template_name = 'lambada/coach_list.html'

	def get_queryset (self):
		return Practice.objects.filter(coach=self.request.user).order_by('dateTime')


@login_required
def coach_practice_cancel(request, pk):
	### TO DO ###
	### REmove this coach and assign a new one ###
	context = RequestContext(request)
        try:
                practice=Practice.objects.get(pk=pk)
                if practice.coach == request.user.username:
                        # Assign a new coach
                        #return HttpResponseRedirect('/coach/list/')
			return HttpResponse('Error: Coach cancellation not implemented yet.')
                else:
                        return render_to_response('lambada/404.html', {}, context)
        except Practice.DoesNotExist:
                return HttpResponse('Error: Practice session does not exist.')


################################
###
### Practice session execution 
###
################################


# Learner makes their phone call and does their writing exercise on this page.
#class PracticeDetail(DetailView):
#	model = Practice
#
#	def get_context_data(self, **kwargs):
#		context = super(PracticeDetail, self).get_context_data(**kwargs)
#		context['practice_writing_form'] = PracticeWritingForm()
#		return context

#	def get_object(self, queryset=None):
#               if queryset is None:
#                        queryset = self.get_queryset()
#                pk = self.kwargs.get(self.pk_url_kwarg, None)
#                queryset = queryset.filter(pk=pk, user=self.request.user)
#                try:
#                        obj = queryset.get()
#                except ObjectDoesNotExist:
#                        raise Http404()
#                return obj 


# Learner makes their phone call and does their writing exercise on this page.
def practice_detail(request, pk):
	context = RequestContext(request)
	practice = Practice.objects.get(pk=pk)
	practice_writing_form = PracticeWritingForm(initial={'learners_writing': practice.learners_writing})
	if practice.user == request.user:
		now = datetime.datetime.utcnow().replace(tzinfo=utc)
		date = practice.dateTime;
		timeUntil = (date - now).total_seconds()
		practice.timeUntil = timeUntil
		if timeUntil > 0:
			practice.state = 'WAITING'
		elif timeUntil <= 0 and timeUntil > -1500:
			practice.state = 'SPEAKING'
		elif timeUntil < -1500 and timeUntil > -3600:
			practice.state = 'WRITING'
		else:
			practice.state = 'COMPLETE'
		return render_to_response('lambada/practice_detail.html', {'practice': practice, 'practice_writing_form': practice_writing_form}, context)
	else:
		return render_to_response('lambada/404.html', {}, context)
	

# Coach makes their phone call on this page.
@login_required
def coach_practice_detail(request, pk):
	context = RequestContext(request)
	practice = Practice.objects.get(pk=pk)
	if practice.coach == request.user.username:
		topic = practice.topic
		now = datetime.datetime.utcnow().replace(tzinfo=utc)
		date = practice.dateTime;
		timeUntil = (date - now).total_seconds()
		practice.timeUntil = timeUntil
		if timeUntil > 0:
			practice.state = 'WAITING'
		elif timeUntil <= 0 and timeUntil > -1500:
			practice.state = 'SPEAKING'
		elif timeUntil < -1500 and timeUntil > -3600:
			practice.state = 'WRITING'
		else:
			practice.state = 'COMPLETE'
		return render_to_response('lambada/coach_practice_detail.html', {'topic': topic, 'practice': practice}, context)
	else:
		return render_to_response('lambada/404.html', {}, context)


# Coach marks time of speaking errors here.
@login_required
def speaking_error_notification(request, pk):
	error_time = datetime.datetime.utcnow().replace(tzinfo=utc)
	practice = Practice.objects.get(pk=pk)
	if practice.coach == request.user.username:
		count = practice.learner_recording_count
		learner_recording = LearnerRecording.objects.get(practice=practice, count=count)
		time_of_error = error_time - learner_recording.call_start_time
		hours, remainder = divmod(time_of_error.seconds, 3600)
		minutes, seconds = divmod(remainder, 60)
		speaking_error = SpeakingError(practice=practice, learnerRecording=learner_recording, error_time_min=minutes, error_time_sec=seconds, coach=request.user.username, learner=practice.user)
		speaking_error.save()
		return HttpResponse(time_of_error)
	else:
		return render_to_response('lambada/404.html', {}, context)


# Creation of sessions recordings is done here.
@login_required
def recording_upload(request, pk, partNum):
	practice = Practice.objects.get(pk=pk)
	coachLeg = request.META['HTTP_COACH_LEG']
	if practice.user == request.user or practice.coach == request.user.username:
		if partNum == '0':
			if coachLeg == 'true':
				practice.coach_recording_count +=1
				count = practice.coach_recording_count
				target = open(settings.STATIC_PATH + '/coach_session_' + pk + '_recording_' + str(count) + '.ogg', 'a+b')
			else:
				practice.learner_recording_count +=1
				practice.callTimeElapsed +=5
				count = practice.learner_recording_count
				call_start_time = datetime.datetime.utcnow().replace(tzinfo=utc) - datetime.timedelta(seconds=5)
				learnerRecording = LearnerRecording(practice=practice, count=count, call_start_time=call_start_time)
				learnerRecording.save()
				target = open(settings.STATIC_PATH + '/learner_session_' + pk + '_recording_' + str(count) + '.ogg', 'a+b')
		else: 
			if coachLeg == 'true':
				count = practice.coach_recording_count
				target = open(settings.STATIC_PATH + '/coach_session_' + pk + '_recording_' + str(count) + '.ogg', 'a+b')
			else:
				practice.callTimeElapsed +=5
				count = practice.coach_recording_count
				target = open(settings.STATIC_PATH + '/learner_session_' + pk + '_recording_' + str(count) + '.ogg', 'a+b')
		target.write(request.body)
		target.close()
		callTimeElapsed = practice.callTimeElapsed
		practice.save()
		return HttpResponse(callTimeElapsed)
	else:
		return render_to_response('lambada/404.html', {}, context)
		

# Learner submits their writing exercise here.
@login_required
def practice_add_writing(request, pk):
	context = RequestContext(request)
	learners_writing = request.POST.get('learners_writing')
	practice = Practice.objects.get(pk=pk)
	if practice.user == request.user:
		practice.learners_writing = learners_writing
		practice.writing_complete = True
		practice.save()
		return HttpResponseRedirect('/practice/list/')
	else:
		return render_to_response('lambada/404.html', {}, context)
	

# Logs of the signalling messages sent on the default channel can be accessed here.
@login_required
def defaultChannel_log_download(request, pk):
	return HttpResponse(open(settings.STATIC_PATH + '/session_' + pk + '_default_channel.txt'), content_type="text/plain")


# Logs of the signalling messages sent on the private channel can be accessed here.
@login_required
def privateChannel_log_download(request, pk):
	print('In PrivateChannel log download')
	return HttpResponse(open(settings.STATIC_PATH + '/session_' + pk + '_private_channel.txt'), content_type="text/plain")


################################
###
### Speaking Report
###
################################


# Coach creates the Speaking report here. This view also transfers the recordings from the local server to AWS.
@login_required
def report_add_speech(request, pk):
	context = RequestContext(request)
	practice = Practice.objects.get(pk=pk)
	if practice.coach == request.user.username:
		count = practice.learner_recording_count
		for x in range(1, count+1):
			learnerRecording = LearnerRecording.objects.get(practice=practice, count=x)
			if learnerRecording.recording == "":
				print('In if')
				target = open(settings.STATIC_PATH + '/learner_session_' + pk + '_recording_' + str(x) + '.ogg', 'a+b')
				djangofile = File(target)
				learnerRecording.recording.save('learner_session_' + pk + '_recording_' + str(x) + '.ogg', djangofile)
				learnerRecording.save()
				target.close()
				os.remove(settings.STATIC_PATH + '/learner_session_' + pk + '_recording_' + str(x) + '.ogg')
		learnerRecordings = LearnerRecording.objects.filter(practice=practice)
	        speaking_error_list = SpeakingError.objects.filter(practice=practice).order_by('id')
		return render_to_response('lambada/coach_report_add_speech.html', {'practice': practice, 'learnerRecordings': learnerRecordings, 'speaking_error_list': speaking_error_list, 'speaking_error_form': SpeakingErrorForm(), 'S3_URL': settings.S3_URL}, context)
	else: 
		return render_to_response('lambada/404.html', {}, context)


# Coach adds a written correction to a single Speaking Error here.
@login_required
def report_add_speech_correction(request, pk):
	speakingError = SpeakingError.objects.get(pk=pk)
	if speakingError.coach == request.user:
		speakingError.correction_text = request.POST['error_correction']
		speakingError.save()
		return HttpResponse()
	else:
		return render_to_response('lambada/404.html', {}, context)


# Coach adds a recorded correction to a single Speaking Error here.
@login_required
def recording_correction_upload(request, pk):
	speakingError = SpeakingError.objects.get(pk=pk)
	if speakingError.coach == request.user:
		target = open(settings.STATIC_PATH + '/correction_' + pk + '_recording.ogg', 'a+b')
		target.write(request.body)
		djangofile = File(target)
		speakingError.correction_recording.save('correction_' + pk + '_recording.ogg', djangofile)
		speakingError.correction_recording_flag = True
		speakingError.save()
		target.close()
		os.remove(settings.STATIC_PATH + '/correction_' + pk + '_recording.ogg')
		return HttpResponse()
	else: 
		return render_to_response('lambada/404.html', {}, context)


# Recording of Learner's leg of the session is downloaded here.
#@login_required
#def recording_download(request, pk):
#	return StreamingHttpResponse(open(settings.STATIC_PATH + '/learner_session_' + pk + '_recording.ogg'), content_type="audio/ogg")


# Recording of Coach's error correction is downloaded here.
#@login_required
#def recording_correction_download(request, pk):
#	return StreamingHttpResponse(open(settings.STATIC_PATH + '/correction_' + pk + '_recording.ogg'), content_type="audio/ogg")


# Coach adds the time of a Speaking Error to the report here.
@login_required
def report_add_speech_error(request, pk):
	context = RequestContext(request)
	practice = Practice.objects.get(pk=pk)
	if practice.coach == request.user.username:
		minutes = request.POST['error_time_min']
		seconds = request.POST['error_time_sec']
		count = request.POST['recording_number']
		print('LearnerRecording:' + count)
		learnerRecordings = LearnerRecording.objects.filter(practice=practice)
		learner_recording = learnerRecordings.get(practice=practice, count=count)
		speaking_error = SpeakingError(practice=practice, learnerRecording=learner_recording, error_time_min=minutes, error_time_sec=seconds, coach=request.user.username, learner=practice.user)
		speaking_error.save()
		speaking_error_list = SpeakingError.objects.filter(practice=practice).order_by('id')
		return render_to_response('lambada/coach_report_add_speech.html', {'practice': practice, 'learnerRecordings': learnerRecordings, 'speaking_error_list': speaking_error_list, 'speaking_error_form': SpeakingErrorForm(), 'S3_URL': settings.S3_URL}, context)
	else:
		return render_to_response('lambada/404.html', {}, context)


# Coach deletes the time of a Speaking Error from the report here.
@login_required
def report_delete_speech_error(request, pk):
	context = RequestContext(request)
	error_pk = request.POST['error_pk']
	practice = Practice.objects.get(pk=pk)
	if practice.coach == request.user.username:
		speaking_error = SpeakingError.objects.filter(pk=error_pk).delete()
		if os.path.isfile(settings.STATIC_PATH + '/correction_' + error_pk + '_recording.ogg'):
			os.remove(settings.STATIC_PATH + '/correction_' + error_pk + '_recording.ogg')
		learnerRecordings = LearnerRecording.objects.filter(practice=practice)
		speaking_error_list = SpeakingError.objects.filter(practice=practice).order_by('id')
		return render_to_response('lambada/coach_report_add_speech.html', {'practice': practice, 'learnerRecordings': learnerRecordings, 'speaking_error_list': speaking_error_list, 'speaking_error_form': SpeakingErrorForm(), 'S3_URL': settings.S3_URL}, context)
	else:
		return render_to_response('lambada/404.html', {}, context)


# Coach reviews the Speaking Report here.
@login_required
def practice_report_speaking_review(request, pk):
	context = RequestContext(request)
	practice = Practice.objects.get(pk=pk)
	if practice.coach == request.user.username:
		learnerRecordings = LearnerRecording.objects.filter(practice=practice)
		speaking_error_list = SpeakingError.objects.filter(practice=practice).order_by('id').exclude(correction_text='', correction_recording_flag=False)
		return render_to_response('lambada/coach_report_speaking_review.html', {'practice': practice, 'learnerRecordings': learnerRecordings, 'speaking_error_list': speaking_error_list, 'S3_URL': settings.S3_URL}, context)
	else:
		return render_to_response('lambada/404.html', {}, context)


# Coach publishes the Speaking report here.
@login_required
def practice_report_speaking_publish(request, pk):
	practice = Practice.objects.get(pk=pk)
	if practice.coach == request.user.username:
		practice.speaking_report_published = True
		practice.save()
		SpeakingError.objects.filter(practice=practice, correction_text='', correction_recording_flag=False).delete()
		return HttpResponseRedirect('/dashboard/')
	else:
		return render_to_response('lambada/404.html', {}, context)


# Learner views the Speaking report.
@login_required
def report_speaking(request, pk):
	context = RequestContext(request)
	practice = Practice.objects.get(pk=pk)
	if practice.user == request.user:
		learnerRecordings = LearnerRecording.objects.filter(practice=practice)
		speaking_error_list = SpeakingError.objects.filter(practice=practice).order_by('id').exclude(correction_text='', correction_recording=False)
		return render_to_response('lambada/practice_report_speaking.html', {'practice': practice, 'learnerRecordings': learnerRecordings, 'speaking_error_list': speaking_error_list, 'speaking_error_form': SpeakingErrorForm(), 'S3_URL': settings.S3_URL}, context)
	else: 
		return render_to_response('lambada/404.html', {}, context)


################################
###
### Writing Report
###
################################


# Coach creates the report for the Writing exercise here. 	
@login_required
def report_add_writing(request, pk):
	context = RequestContext(request)
	practice = Practice.objects.get(pk=pk)
	if practice.coach == request.user.username:
		writing_error_list = WritingError.objects.filter(practice=practice).order_by('id')
		return render_to_response('lambada/coach_report_add_writing.html', {'practice': practice, 'writing_error_list': writing_error_list}, context)
	else: 
		return render_to_response('lambada/404.html', {}, context)


# Coach adds a written correction to a single Written Error of the report here.
@login_required
def report_add_writing_correction(request, pk):
	practice = Practice.objects.get(pk=pk)
	if practice.coach == request.user.username:
		writingError = WritingError(practice=practice, original_text=request.POST['original_text'], correction_text=request.POST['correction_text'], learner=practice.user) 
		writingError.save()
		return HttpResponse(writingError.pk)
	else: 
		return render_to_response('lambada/404.html', {}, context)


# Coach deletes a single Written Error correction here.
@login_required
def report_delete_writing_correction(request):
	error_pk = request.POST['error_pk']
	writing_error = WritingError.objects.filter(pk=error_pk)
	if writing_error.coach == request.user.username:
		writing_error.delete()	
		return HttpResponse() 
	else:
		return render_to_response('lambada/404.html', {}, context)


# Coach reviews the Writing report here.
@login_required
def practice_report_writing_review(request, pk):
	context = RequestContext(request)
	practice = Practice.objects.get(pk=pk)
	if practice.coach == request.user.username:
		writing_error_list = WritingError.objects.filter(practice=practice).order_by('id')
		return render_to_response('lambada/coach_report_writing_review.html', {'practice': practice, 'writing_error_list': writing_error_list}, context)
	else:
		return render_to_response('lambada/404.html', {}, context)


# Coach publishes the Writing report here.
@login_required
def practice_report_writing_publish(request, pk):
	practice = Practice.objects.get(pk=pk)
	if practice.coach == request.user.username:
		practice.writing_report_published = True
		practice.save()
		return HttpResponseRedirect('/dashboard/')
	else:
		return render_to_response('lambada/404.html', {}, context)


# Learner views the Writing report.
@login_required
def report_writing(request, pk):
	context = RequestContext(request)
	practice = Practice.objects.get(pk=pk)
	if practice.user == request.user.username:
		writing_error_list = WritingError.objects.filter(practice=practice).order_by('id')
		return render_to_response('lambada/practice_report_writing.html', {'practice': practice, 'writing_error_list': writing_error_list}, context)
	else:
		return render_to_response('lambada/404.html', {}, context)


################################
###
### Error Handling
###
################################


def handler404(request):
	return render_to_response('lambada/404.html', {})


#@login_required
#def private_channel_write(request, pk):
#	response_data = {}
#	message = request.POST.get('message')
#	target = open(settings.STATIC_PATH + '/session_' + pk + '_private_channel.txt', 'a+b')
#	target.write(str(datetime.datetime.now()) + " -- " + message + "\n \n")
#	target.close()
#	# Consider checking messages before deleting them. You might delete a message before the other party has had a chance to read it.
#	ChannelPrivate.objects.filter(practice_pk=pk).delete()
#	channel = ChannelPrivate(practice_pk=pk, message=message)
#	channel.save()
#	response_data['message'] = 'success'
#	return HttpResponse(json.dumps(response_data), content_type="application/json")


#@login_required
#def default_channel_write(request, pk):
#	response_data = {}
#	message = request.POST.get('message')
#	target = open(settings.STATIC_PATH + '/session_' + pk + '_default_channel.txt', 'a+b')
#	target.write(str(datetime.datetime.now()) + " -- " + message + "\n \n")
#	target.close()
#	# Consider checking messages before deleting them. You might delete a message before the other party has had a chance to read it.
#	ChannelDefault.objects.filter(practice_pk=pk).delete()
#	channel = ChannelDefault(practice_pk=pk, message=message)
#	channel.save()
#	response_data['message'] = 'success'
#	return HttpResponse(json.dumps(response_data), content_type="application/json")



#@login_required
#def private_channel_check(request, pk):
#	try:
#		channel = ChannelPrivate.objects.filter(practice_pk=pk)
#		data = serializers.serialize("json", channel)
#	except ChannelPrivate.DoesNotExist:
#		return HttpResponse()
#	return HttpResponse(data, mimetype = "application/json")


#@login_required
#def default_channel_check(request, pk):
#	try:
#		channel = ChannelDefault.objects.filter(practice_pk=pk)
#		data = serializers.serialize("json", channel)
#	except ChannelDefault.DoesNotExist:
#		return HttpResponse()
#	return HttpResponse(data, mimetype = "application/json")


