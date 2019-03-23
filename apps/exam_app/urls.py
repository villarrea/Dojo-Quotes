from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^process$', views.process),
    url(r'^logout$', views.logout),
    url(r'^login$', views.login),


    url(r'^wall$', views.wall),
    url(r'^users/(?P<user_id>\d+)$', views.user_info),
    url(r'^favorite/(?P<user_id>\d+)$', views.add_favorite),
    # url(r'^re_add/(?P<user_id>\d+)$', views.re_add),
    url(r'^remove/(?P<user_id>\d+)$', views.remove),
    url(r'^post_quote$', views.post_quote),
]