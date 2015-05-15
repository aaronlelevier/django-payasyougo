from django.conf.urls import include, url
from django.contrib import admin

from rest_framework import routers

from payg import views
from user import views as user_views

router = routers.DefaultRouter()
router.register(r'users-profile', user_views.UserProfileViewSet)
router.register(r'users', user_views.UserViewSet)
router.register(r'groups', user_views.GroupViewSet)


urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^404/$', views.handler404, name='404'),
    url(r'^500/$', views.handler500, name='500'),
    # Admin
    url(r'^admin/', include(admin.site.urls)),
    # REST Views
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # My Apps
    url(r'^account/', include('account.urls')),
    url(r'',include('contact.urls')),
    url(r'', include('user.urls')),
]
