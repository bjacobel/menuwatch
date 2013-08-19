from django.contrib import admin
from django.conf.urls import patterns, include, url
from apps.menus import views as menu_views


# See: https://docs.djangoproject.com/en/dev/ref/contrib/admin/#hooking-adminsite-instances-into-your-urlconf
admin.autodiscover()


# See: https://docs.djangoproject.com/en/dev/topics/http/urls/
urlpatterns = patterns(
    '',

    # Admin panel and documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # Menu views
    url(r'^$', menu_views.IndexView, name='index'),
    url(r'^login/', menu_views.LoginView, name='login'),
    url(r'^logout/', menu_views.LogoutView, name='logout'),
    url(r'^signup/', menu_views.SignupView, name='signup'),
    url(r'^account/', menu_views.AccountView, name='account'),
    url(r'^browse/', menu_views.BrowseView, name='browse'),
    url(r'^upgrade/', menu_views.UpgradeView, name='upgrade'),
    url(r'^exclude/', menu_views.ExcludeView, name='exclude'),

)