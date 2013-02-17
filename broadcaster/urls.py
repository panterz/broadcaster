from django.conf.urls import patterns, include, url
from voting import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'broadcaster.views.home', name='home'),
    # url(r'^broadcaster/', include('broadcaster.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index),
    url(r'^poll/', views.get_poll_details),
    url(r'^submit-vote/', views.submit_vote),
)
