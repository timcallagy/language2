from django.contrib.auth.models import User
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView, DetailView, ListView
from lambada.forms import UserForm, UserProfileForm, TopicForm
from django.contrib.auth.decorators import login_required
import pytz
from django.http import HttpResponseRedirect, HttpResponse
from lambada.models import Topic, UserProfile
import datetime
from django.utils.translation import ugettext as _
from django.utils import translation
from django.core.mail import send_mail

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
				return HttpResponseRedirect('/practice/')
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
			return HttpResponseRedirect('/practice/')
		else:
			return render_to_response('lambada/invalid_login.html', context)
	else:
		return render_to_response('/login.html', {'user_form': user_form, 'userprofile_form': userprofile_form}, context)

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
		return context


class TopicList(ListView):
	paginate_by = 3
	
	def get_queryset (self):
		return Topic.objects.filter(created_by=self.request.user)
	
	# This code gets User and Profile forms to display in the Registration popup box.
	def get_context_data(self, **kwargs):
		context = super(TopicList, self).get_context_data(**kwargs)
		context['user_form'] = UserForm()
		context['userprofile_form'] = UserProfileForm()
		return context


class Practice(TemplateView):
	template_name = 'lambada/practice.html'

	# This code gets User and Profile forms to display in the Registration popup box.
	def get_context_data(self, **kwargs):
		context = super(Practice, self).get_context_data(**kwargs)
		context['user_form'] = UserForm()
		context['userprofile_form'] = UserProfileForm()
		return context
