from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers

from views import views, account


def if_debug(*args, **kwargs):
    ret = url(*args, **kwargs)
    if not settings.DEBUG:
        ret.resolve = lambda *args: None
    return ret

# Note the order in the router's setup - all nested URL parts mast be
# registered before the parent one (i.e. `user/photos` must be
# before `user`), or else you'll get that method is not allowed on request.
router = routers.DefaultRouter()
# router.register(r'user/register', views.UserRegister)
router.register(r'user', views.AthonUserView)

urlpatterns = patterns('',
    url(r'^api/user/register/$', account.RegistrationView.as_view()),
    url(r'^user/activate/(?P<activation_key>\w+)/$', views.IndexView.as_view(),
        name='registration_activate'),
    url(r'^api/user/activate$', account.ActivationView.as_view()),
    url(r'^api/user/login/$', account.AuthenticateView.as_view()),
    url(r'^api/user/logout/$', account.LogoutView.as_view()),
    url(r'^api/user/available/username/$', account.CheckUsernameView.as_view()),
    url(r'^api/user/available/email/$', account.CheckEmailView.as_view()),
    url(r'^api/user/(?P<id>[0-9]+)/follow/$', views.FollowUserView.as_view()),
    url(r'^api/user/(?P<id>[0-9]+)/unfollow/$', views.UnFollowUserView.as_view()),
    url(r'^api/user/(?P<id>[0-9]+)/request_to_follow/$', views.RequestToFollowUserView.as_view()),
    url(r'^api/user/(?P<id>[0-9]+)/remove_request_to_follow/$',
            views.RemoveRequestToFollowUserView.as_view()),
    url(r'^api/user/(?P<id>[0-9]+)/accept_request/$', views.AcceptRequestToFollowUserView.as_view()),
    url(r'^api/user/(?P<id>[0-9]+)/following/$', views.FollowingUserView.as_view()),
    url(r'^api/user/(?P<id>[0-9]+)/followers/$', views.FollowersUserView.as_view()),
    url(r'^api/user/password/reset/$', 'account_password_reset', name='api_account_password_reset'),
    url(r'^api/user/password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$',
            'account_password_reset_key', name='api_account_password_reset_key'),

)

urlpatterns += patterns('',
    url(r'^api/', include(router.urls)),
    if_debug(r'^api/docs/', include('rest_framework_swagger.urls')),

    url(r'^admin/', include(admin.site.urls)),
)

