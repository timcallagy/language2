from django.contrib.auth.decorators import login_required, permission_required
from django.conf.urls import url, patterns
from lambada import views
from lambada.views import TopicCreate, TopicDetail, TopicUpdate, TopicDelete, TopicList, Practice

urlpatterns = patterns('',
		url(r'^$', Practice.as_view(), name='index'),
		url(r'^register/$', views.register, name='register'),
		url(r'^user_login/$', views.user_login, name='user_login'),
		url(r'^user_logout/$', views.user_logout, name='user_logout'),
		url(r'^forgot_login/$', views.forgot_login, name='forgot_login'),
		url(r'^topic/add/$', login_required(TopicCreate.as_view()), name='topic_add'),
		url(r'^topic/list/$', login_required(TopicList.as_view()), name='topic_list'),
		url(r'^topic/(?P<pk>[0-9]+)/$', login_required(TopicDetail.as_view()), name='topic_detail'),
		url(r'^topic/(?P<pk>[0-9]+)/update/$', login_required(TopicUpdate.as_view()), name='topic_update'),
		url(r'^topic/(?P<pk>[0-9]+)/delete/$', login_required(TopicDelete.as_view()), name='topic_update'),
		url(r'^practice/$', login_required(Practice.as_view()), name='practice'),
)
