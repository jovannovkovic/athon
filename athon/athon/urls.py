from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers

from athon.views import views, account


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
router.register(r'user/by_id', views.AthonUserView)

other_api_urls = patterns('',
    url(r'^api/user/register/$', account.RegistrationView.as_view()),
    url(r'^api/user/activate/(?P<activation_key>\w+)/$', views.IndexView.as_view(),
        name='registration_activate'),
    url(r'^api/user/activate$', account.ActivationView.as_view()),
    url(r'^api/user/login/$', account.AuthenticateView.as_view()),
    url(r'^api/user/logout/$', account.LogoutView.as_view()),
    url(r'^api/user/fallow/$', views.FallowUserView.as_view()),
    url(r'^api/user/unfallow/$', views.UnFallowUserView.as_view()),
    url(r'^api/user/request_to_fallow/$', views.RequestToFallowUserView.as_view()),
    url(r'^api/user/remove_request_to_fallow/$',
            views.RemoveRequestToFallowUserView.as_view()),
    url(r'^api/user/accept_request/$', views.AcceptRequestToFallowUserView.as_view()),
)

urlpatterns = patterns('',
    url(r'^api/', include(router.urls)),
    if_debug(r'^api/docs/', include('rest_framework_swagger.urls')),

    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += other_api_urls
