from django.contrib.auth.models import User
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView, DetailView, ListView
from lambada.forms import UserForm, UserProfileForm, TopicForm, PracticeForm
from django.contrib.auth.decorators import login_required
import pytz
from django.http import HttpResponseRedirect, HttpResponse, StreamingHttpResponse
from lambada.models import Topic, TopicLikes, UserProfile, Practice, Report, Recording 
import datetime
from django.utils.translation import ugettext as _
from django.utils import translation
from django.core.mail import send_mail
from django.views.decorators.csrf import ensure_csrf_cookie
import os
from django.conf import settings

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

	# This code gets User and Profile forms to display in the Registration popup box.
	def get_context_data(self, **kwargs):
		context = super(TopicUpdate, self).get_context_data(**kwargs)
		context['user_form'] = UserForm()
		context['userprofile_form'] = UserProfileForm()
		return context


class TopicDetail(DetailView):
	model = Topic

	# This code gets User and Profile forms to display in the Registration popup box.
	def get_context_data(self, **kwargs):
		context = super(TopicDetail, self).get_context_data(**kwargs)
		context['user_form'] = UserForm()
		context['userprofile_form'] = UserProfileForm()
		context['likes'] = 3
		return context


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
def practice_add(request, pk):
	context = RequestContext(request)
	user_id=request.user.id
	user = User.objects.get(pk=user_id)
	topic = Topic.objects.get(pk=pk)
	dateTime = datetime.datetime.strptime(request.POST.get('dateTime_0', datetime.datetime.now), '%d/%m/%Y %H:%M')
	practice, created = Practice.objects.get_or_create(
			user = request.user,
			topic = topic,
			dateTime = dateTime
	)
	print(practice.id)
	report, created = Report.objects.get_or_create(
			practice = practice
	)

	return HttpResponseRedirect('/practice/' + str(practice.id))
		
@login_required
def recording_upload(request, pk, partNum):
#	report=Report.objects.get(pk=pk)
#	recording = Recording(report=report, blob=request.body, partNum=partNum) 
#	recording.save()
#	return HttpResponse()
	print('In recording upload'+settings.STATIC_PATH + '/recordings/session_' + pk + '_recording.ogg')
#	path = os.path.join(settings.STATIC_PATH, pk, 'recording.ogg')
#	path = os.path.join(, 'recording_file.ogg')
	target = open(settings.STATIC_PATH + '/recordings/session_' + pk + '_recording.ogg', 'a+b')
	target.write(request.body)
	target.close()
	return HttpResponse()


@login_required
def recording_download(request, pk):
	print('In recording download')
	#response = HttpResponse(mimetype='audio/ogg')
	#response['X-Sendfile'] = smart_str()
	return HttpResponse(open(settings.STATIC_PATH + '/recordings/session_' + pk + '_recording.ogg'), content_type="audio/ogg")

#	return StreamingHttpResponse(target, content_type="audio/ogg")


#	while(counter<partCount):
#		recording.join(Recording.objects.get(report=pk, partNum=counter).blob)
#		counter = counter + 1
#		print('counter is: ' + str(counter))
#	return HttpResponse(recording, content_type="audio/ogg")
	#recording=Recording.objects.get(partNum=0)
	#return HttpResponse(recording.blob, content_type="audio/ogg")

@login_required
def report_create(request, pk):
	print('In report_Create')
	context = RequestContext(request)
	return render_to_response('lambada/report_form.html', {'practice_id': pk}, context)

class PracticeList(ListView):
	paginate_by = 3
	template_name = 'lambada/practice_list.html'

	def get_queryset (self):
		return Topic.objects.filter(published=True).exclude(created_by=self.request.user)

	# This code gets User and Profile forms to display in the Registration popup box.
	def get_context_data(self, **kwargs):
		context = super(PracticeList, self).get_context_data(**kwargs)
		context['user_form'] = UserForm()
		context['userprofile_form'] = UserProfileForm()
		context['practice_form'] = PracticeForm()
		return context


class PracticeDetail(DetailView):
	model = Practice


class Dashboard(TemplateView):
	template_name = 'lambada/dashboard.html'

	# This code gets User and Profile forms to display in the Registration popup box.
	def get_context_data(self, **kwargs):
		context = super(Dashboard, self).get_context_data(**kwargs)
		context['user_form'] = UserForm()
		context['userprofile_form'] = UserProfileForm()
		return context
