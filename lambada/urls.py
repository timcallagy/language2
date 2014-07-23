from django.contrib.auth.decorators import login_required, permission_required
from django.conf.urls import url, patterns
from lambada import views
from lambada.views import TopicCreate, TopicDetail, TopicUpdate, TopicDelete, TopicList, PracticeList, PracticeBook, PracticeTopicDetail, PracticeDetail, PracticeDelete, PracticeUpdate, CoachList, Dashboard

urlpatterns = patterns('',
		url(r'^$', Dashboard.as_view(), name='index'),
		url(r'^register/$', views.register, name='register'),
		url(r'^user_login/$', views.user_login, name='user_login'),
		url(r'^user_logout/$', views.user_logout, name='user_logout'),
		url(r'^forgot_login/$', views.forgot_login, name='forgot_login'),
		url(r'^topic/add/$', login_required(TopicCreate.as_view()), name='topic_add'),
		url(r'^topic/list/$', login_required(TopicList.as_view()), name='topic_list'),
		url(r'^topic/(?P<pk>[0-9]+)/$', login_required(TopicDetail.as_view()), name='topic_detail'),
		url(r'^topic/(?P<pk>[0-9]+)/update/$', login_required(TopicUpdate.as_view()), name='topic_update'),
		url(r'^topic/(?P<pk>[0-9]+)/publish/$', views.topic_publish, name='topic_publish'),
		url(r'^topic/(?P<pk>[0-9]+)/delete/$', login_required(TopicDelete.as_view()), name='topic_update'),
		url(r'^like_topic/$', views.like_topic, name='like_topic'),
		url(r'^practice/list/$', login_required(PracticeList.as_view()), name='practice_list'),
		url(r'^practice/book/$', login_required(PracticeBook.as_view()), name='practice_book'),
		url(r'^practice/book/payment/(?P<pk>[0-9]+)/$', views.practice_payment, name='practice_payment'),
		url(r'^practice/topic/(?P<pk>[0-9]+)/$', login_required(PracticeTopicDetail.as_view()), name='practice_topic_detail'),
		url(r'^practice/(?P<pk>[0-9]+)/$', login_required(PracticeDetail.as_view()), name='practice_detail'),
		url(r'^practice/(?P<pk>[0-9]+)/add/$', views.practice_add, name='practice_add'),
		url(r'^practice/(?P<pk>[0-9]+)/delete/$', login_required(PracticeDelete.as_view()), name='practice_delete'),
		url(r'^practice/(?P<pk>[0-9]+)/update/$', login_required(PracticeUpdate.as_view()), name='practice_update'),
		url(r'^recording/upload/(?P<pk>[0-9]+)/(?P<partNum>[0-9]+)/$', views.recording_upload, name='recording_upload'),
		url(r'^recording/download/(?P<pk>[0-9]+)/$', views.recording_download, name='recording_download'),
		url(r'^coach/list/$', login_required(CoachList.as_view()), name='coach_list'),
		url(r'^coach/practice/(?P<pk>[0-9]+)/$', views.coach_practice_detail, name='coach_practice_detail'),
		url(r'^coach/practice/(?P<pk>[0-9]+)/cancel/$', views.coach_practice_cancel, name='coach_practice_cancel'),
		url(r'^report/add/(?P<pk>[0-9]+)/$', views.report_create, name='report_add'),
		url(r'^dashboard/$', login_required(Dashboard.as_view()), name='dashboard'),
)
