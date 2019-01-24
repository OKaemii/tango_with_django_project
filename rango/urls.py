from django.conf.urls import url
from rango import views

#imports d relevant Django machinery f URL mappings n d 'views' module from 'rango'
#allows t call function 'url' n point t d 'index' view f d mapping in 'urlpatterns'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.show_category, name='show_category'),
]
