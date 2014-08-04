from django.contrib.auth.models import User
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView, DetailView, ListView
from lambada.forms import UserForm, UserProfileForm, TopicForm, PracticeForm, PracticeWritingForm, SpeakingErrorForm
from django.contrib.auth.decorators import login_required
import pytz
from django.http import HttpResponseRedirect, HttpResponse, StreamingHttpResponse
from lambada.models import Topic, TopicLikes, UserProfile, Practice, Report, Recording, Channel, SpeakingError, WritingError
import datetime
from django.utils.timezone import utc
from django.utils.translation import ugettext as _
from django.utils import translation
from django.core.mail import send_mail
from django.views.decorators.csrf import ensure_csrf_cookie
import os
from django.conf import settings
import json
from django.core import serializers

class Index(TemplateView):
	template_name = 'lambada/index.html'

	# This code gets User and Profile forms to display in the Registration popup box.
	def get_context_data(self, **kwargs):
		context = super(Practice, self).get_context_data(**kwargs)
		context['user_form'] = UserForm()
		context['userprofile_form'] = UserProfileForm()
		return context

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
	user_form = UserForm()
	userprofile_form = UserProfileForm()
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)

		if user:
			login(request, user)
			language = UserProfile.objects.get(user=request.user.id).language
			request.session['django_timezone'] = UserProfile.objects.get(user=request.user.id).timezone
			request.session['django_language'] = language
			return HttpResponseRedirect('/dashboard/')
		else:
			return render_to_response('lambada/invalid_login.html', context)
	else:
		return render_to_response('lambada/login.html', {'user_form': user_form, 'userprofile_form': userprofile_form}, context)

@login_required
def topic_publish(request, pk):
	context = RequestContext(request)
	try:
		print("start try")
		topic=Topic.objects.get(pk=pk)
		topic.published=True
		topic.save()
		print("end try")
		return HttpResponseRedirect('/topic/list/')
	except Topic.DoesNotExist:
		return HttpResponse('Error: Topic does not exist.')

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


class TopicCreate(CreateView):
	model = Topic
	form_class = TopicForm
	
	def form_valid(self, form):
		form.instance.created_by = self.request.user
		form.instance.creation_date = datetime.datetime.now()
		return super(TopicCreate, self).form_valid(form)

	# This code gets User and Profile forms to display in the Registration popup box.
	def get_context_data(self, **kwargs):
		context = super(TopicCreate, self).get_context_data(**kwargs)
		context['user_form'] = UserForm()
		context['userprofile_form'] = UserProfileForm()
		return context


class TopicDelete(DeleteView):
	model = Topic
	success_url = '/topic/list/'

	# This code gets User and Profile forms to display in the Registration popup box.
	def get_context_data(self, **kwargs):
		context = super(TopicDelete, self).get_context_data(**kwargs)
		context['user_form'] = UserForm()
		context['userprofile_form'] = UserProfileForm()
		return context


class TopicUpdate(UpdateView):
	model = Topic
	form_class = TopicForm
	template_name = 'lambada/topic_update.html'


class TopicDetail(DetailView):
	model = Topic


class TopicList(ListView):
	paginate_by = 10
		
	def get_queryset (self):
		return Topic.objects.filter(created_by=self.request.user)
 
	
	# This code gets User and Profile forms to display in the Registration popup box.
	def get_context_data(self, **kwargs):
		context = super(TopicList, self).get_context_data(**kwargs)
		context['user_form'] = UserForm()
		context['userprofile_form'] = UserProfileForm()
		return context


@login_required
def like_topic(request):
	print("####### 1")
	user = request.user 
	userProfile = UserProfile.objects.get(user=user)
	topic_id = request.GET['topic_id']
	topic = Topic.objects.get(id=topic_id)
	print("####### 2")
	like, created = TopicLikes.objects.get_or_create(
			userProfile = userProfile,
			topic = topic
	)
	if not created:
		print("This is the second time this user has like this topic.")
		return HttpResponse('4')
	else:
		print("This is the first time this user has liked this topic.")
		likes = TopicLikes.objects.filter(topic=topic).count()
		return HttpResponse(likes)


@login_required
def practice_payment(request, pk):
	context = RequestContext(request)
	topic = Topic.objects.get(pk=pk)
	naive = datetime.datetime.strptime(request.POST.get('dateTime_0', datetime.datetime.now), '%Y-%m-%d %H:%M:%S')
	print('practice_payment dateTime NAIVE: ' + str(naive))
	tz = pytz.timezone(request.session['django_timezone'])
	aware = tz.localize(naive)
	print('practice_payment dateTime AWARE: ' + str(aware))
	return render_to_response('lambada/practice_payment.html', {'object': topic, 'dateTime': aware}, context)
	
@login_required
def practice_add(request, pk):
	context = RequestContext(request)
	user_id=request.user.id
	user = User.objects.get(pk=user_id)
	topic = Topic.objects.get(pk=pk)
	dateTime = request.POST.get('dateTime_0')
	print('practice_payment dateTime AWARE: ' + str(dateTime))
	practice, created = Practice.objects.get_or_create(
			user = request.user,
			topic = topic,
			dateTime = dateTime,
			### TO DO ###
			### Smart coach picking ##
			coach = "farty"
	)
	print(practice.id)
	report, created = Report.objects.get_or_create(
			practice = practice
	)

#	return HttpResponseRedirect('/practice/' + str(practice.id))
	return HttpResponseRedirect('/practice/list/')

@login_required
def practice_add_writing(request, pk):
	context = RequestContext(request)
	learners_writing = request.POST.get('learners_writing')
	practice = Practice.objects.get(pk=pk)
	practice.learners_writing = learners_writing
	practice.writing_complete = True
	practice.save()
	return HttpResponseRedirect('/practice/list/')
	

@login_required
def report_add_speech_correction(request, pk):
	speakingError = SpeakingError.objects.get(pk=pk)
	speakingError.correction_text = request.POST['error_correction']
	speakingError.save()
	return HttpResponse()


@login_required
def report_add_writing_correction(request, pk):
	practice = Practice.objects.get(pk=pk)
	report = practice.report
	print('original_text: ' +request.POST['original_text'])
	writingError = WritingError(report=report, original_text=request.POST['original_text'], correction_text=request.POST['correction_text']) 
	writingError.save()
	return HttpResponse(writingError.pk)


@login_required
def recording_upload(request, pk, partNum):
	print('In recording upload'+settings.STATIC_PATH + '/recordings/session_' + pk + '_recording.ogg')
	coachLeg = request.META['HTTP_COACH_LEG']
	if coachLeg == 'false':
		# Check whether the recording file exists to determine if this is the start of the call.
		if os.path.isfile(settings.STATIC_PATH + '/recordings/learner_session_' + pk + '_recording.ogg'):
			target = open(settings.STATIC_PATH + '/recordings/learner_session_' + pk + '_recording.ogg', 'a+b')
		else:
			print('### Learners file does not exist. New Recording!')
			practice = Practice.objects.get(pk=pk)
			report = practice.report
			# DANGER!!! The timedelta here must correspond to the time delay set in the RTCMultiConnection.js file (in the _captureUserMedia function).
			report.call_start_time = datetime.datetime.utcnow().replace(tzinfo=utc) - datetime.timedelta(seconds=5)
			report.save()
			target = open(settings.STATIC_PATH + '/recordings/learner_session_' + pk + '_recording.ogg', 'a+b')
	else:
		target = open(settings.STATIC_PATH + '/recordings/coach_session_' + pk + '_recording.ogg', 'a+b')
	target.write(request.body)
	target.close()
	return HttpResponse()


@login_required
def recording_correction_upload(request, pk):
	if os.path.isfile(settings.STATIC_PATH + '/recordings/correction_' + pk + '_recording.ogg'):
		os.remove(settings.STATIC_PATH + '/recordings/correction_' + pk + '_recording.ogg')
		target = open(settings.STATIC_PATH + '/recordings/correction_' + pk + '_recording.ogg', 'a+b')
	else:
		target = open(settings.STATIC_PATH + '/recordings/correction_' + pk + '_recording.ogg', 'a+b')
	target.write(request.body)
	target.close()
	speakingError = SpeakingError.objects.get(pk=pk)
	speakingError.correction_recording = True
	speakingError.save()
	return HttpResponse()


@login_required
def recording_download(request, pk):
	print('In recording download')
	return StreamingHttpResponse(open(settings.STATIC_PATH + '/recordings/learner_session_' + pk + '_recording.ogg'), content_type="audio/ogg")


@login_required
def recording_correction_download(request, pk):
	print('In recording correction download')
	return StreamingHttpResponse(open(settings.STATIC_PATH + '/recordings/correction_' + pk + '_recording.ogg'), content_type="audio/ogg")


@login_required
def speaking_error_notification(request, pk):
	error_time = datetime.datetime.utcnow().replace(tzinfo=utc)
	report = Report.objects.get(pk=pk)
	time_of_error = error_time - report.call_start_time
	print('### DateTime of Error: ' + str(time_of_error))
	hours, remainder = divmod(time_of_error.seconds, 3600)
	minutes, seconds = divmod(remainder, 60)
	speaking_error = SpeakingError(report=report, error_time_min=minutes, error_time_sec=seconds)
	speaking_error.save()
	return HttpResponse(time_of_error)


@login_required
def report_create(request, pk):
	print('In report_Create')
	context = RequestContext(request)
	return render_to_response('lambada/report_form.html', {'practice_id': pk}, context)

@login_required
def report_add_speech_error(request, pk):
	context = RequestContext(request)
	minutes = request.POST['error_time_min']
	seconds = request.POST['error_time_sec']
	practice = Practice.objects.get(pk=pk)
	report = practice.report
	speaking_error = SpeakingError(report=report, error_time_min=minutes, error_time_sec=seconds)
	speaking_error.save()
	speaking_error_list = SpeakingError.objects.filter(report=report).order_by('id')
	return render_to_response('lambada/coach_report_add_speech.html', {'practice': practice, 'report': report,'speaking_error_list': speaking_error_list, 'speaking_error_form': SpeakingErrorForm()}, context)


@login_required
def report_delete_speech_error(request, pk):
	context = RequestContext(request)
	error_pk = request.POST['error_pk']
	speaking_error = SpeakingError.objects.filter(pk=error_pk).delete()
	if os.path.isfile(settings.STATIC_PATH + '/recordings/correction_' + error_pk + '_recording.ogg'):
		os.remove(settings.STATIC_PATH + '/recordings/correction_' + error_pk + '_recording.ogg')
	practice = Practice.objects.get(pk=pk)
	report = practice.report 
	speaking_error_list = SpeakingError.objects.filter(report=report).order_by('id')
	return render_to_response('lambada/coach_report_add_speech.html', {'practice': practice, 'report': report,'speaking_error_list': speaking_error_list, 'speaking_error_form': SpeakingErrorForm()}, context)

	
@login_required
def report_delete_writing_correction(request):
	error_pk = request.POST['error_pk']
	writing_error = WritingError.objects.filter(pk=error_pk).delete()
	return HttpResponse() 

	
@login_required
def report_add_speech(request, pk):
	context = RequestContext(request)
	practice = Practice.objects.get(pk=pk)
	report = practice.report 
	speaking_error_list = SpeakingError.objects.filter(report=report).order_by('id')
	return render_to_response('lambada/coach_report_add_speech.html', {'practice': practice, 'report': report,'speaking_error_list': speaking_error_list, 'speaking_error_form': SpeakingErrorForm()}, context)


@login_required
def report_add_writing(request, pk):
	context = RequestContext(request)
	practice = Practice.objects.get(pk=pk)
	report = practice.report 
	writing_error_list = WritingError.objects.filter(report=report).order_by('id')
	return render_to_response('lambada/coach_report_add_writing.html', {'practice': practice, 'report': report, 'writing_error_list': writing_error_list}, context)


@login_required
def practice_report_speaking_review(request, pk):
	context = RequestContext(request)
	practice = Practice.objects.get(pk=pk)
	report = practice.report 
	speaking_error_list = SpeakingError.objects.filter(report=report).order_by('id').exclude(correction_text='', correction_recording=False)
	return render_to_response('lambada/coach_report_speaking_review.html', {'practice': practice, 'report': report,'speaking_error_list': speaking_error_list, 'speaking_error_form': SpeakingErrorForm()}, context)


@login_required
def practice_report_speaking_publish(request, pk):
	practice = Practice.objects.get(pk=pk)
	practice.speaking_report_published = True
	practice.save()
	return HttpResponseRedirect('/dashboard/')


class PracticeList(ListView):
	paginate_by = 3
	template_name = 'lambada/practice_list.html'

	def get_queryset (self):
		return Practice.objects.filter(user=self.request.user)


class PracticeBook(ListView):
	paginate_by = 3
	template_name = 'lambada/practice_book.html'

	def get_queryset (self):
		return Topic.objects.filter(published=True).exclude(created_by=self.request.user)
		
	def get_context_data(self, **kwargs):
		context = super(PracticeBook, self).get_context_data(**kwargs)
		context['practice_form'] = PracticeForm()
		return context


class PracticeTopicDetail(DetailView):
	model = Topic
	template_name = 'lambada/practice_topic_detail.html'

	def get_context_data(self, **kwargs):
		context = super(PracticeTopicDetail, self).get_context_data(**kwargs)
		context['practice_form'] = PracticeForm()
		return context


class PracticeDetail(DetailView):
	model = Practice

	def get_context_data(self, **kwargs):
		context = super(PracticeDetail, self).get_context_data(**kwargs)
		context['practice_writing_form'] = PracticeWritingForm()
		return context


class PracticeDelete(DeleteView):
	model = Practice
	success_url = '/practice/list/'


class PracticeUpdate(UpdateView):
	model = Practice 
	form_class = PracticeForm
	template_name = 'lambada/practice_update.html'


class CoachList(ListView):
	paginate_by = 3
	template_name = 'lambada/coach_list.html'

	def get_queryset (self):
		return Practice.objects.filter(coach=self.request.user)


#class CoachPracticeDetail(DetailView):
#	model = Topic
#	template_name = 'lambada/coach_practice_detail.html'


@login_required
def coach_practice_detail(request, pk):
	context = RequestContext(request)
	practice = Practice.objects.get(pk=pk)
	topic = practice.topic
	return render_to_response('lambada/coach_practice_detail.html', {'topic': topic, 'practice': practice}, context)

@login_required
def coach_practice_cancel(request, pk):
	### TO DO ###
	### REmove this coach and assign a new one ###
	return HttpResponse('Error: Coach cancellation not implemented yet.')


@login_required
def call_setup(request, pk):
	response_data = {}
	message = request.POST.get('message')
	Channel.objects.filter(practice_pk=pk).delete()
	channel = Channel(practice_pk=pk, message=message)
	channel.save()
	response_data['message'] = 'success'
	return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required
def call_join(request, pk):
	try:
		channel = Channel.objects.filter(practice_pk=pk)
		data = serializers.serialize("json", channel)
	except Channel.DoesNotExist:
		return HttpResponse()
	return HttpResponse(data, mimetype = "application/json")


@login_required
def dashboard(request):
	context = RequestContext(request)
	current_time = datetime.datetime.utcnow().replace(tzinfo=utc)
	end_of_week = current_time + datetime.timedelta(days=7)
	upcoming_coaching_sessions = Practice.objects.filter(coach=request.user.username, dateTime__lte=end_of_week, dateTime__gte=current_time)
	upcoming_practice_sessions = Practice.objects.filter(user_id=request.user.id, dateTime__lte=end_of_week, dateTime__gte=current_time)
	pending_speech_reports = Practice.objects.filter(coach=request.user.username, dateTime__lte=current_time, speaking_report_published=False).order_by('dateTime')
	pending_writing_reports = Practice.objects.filter(coach=request.user.username, writing_complete=True, writing_report_published=False)
	#reports = practices_finished_writing
	#pending_writing_reports = practices_finished_writing.objects.exclude(reports.writing_report_published=True)
	return render_to_response('lambada/dashboard.html', {'upcoming_coaching_sessions': upcoming_coaching_sessions, 'upcoming_practice_sessions': upcoming_practice_sessions, 'pending_speech_reports': pending_speech_reports, 'pending_writing_reports': pending_writing_reports}, context)
