from django.conf.urls import url
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static
from . import views

urlpatterns = [
    url(r'^$', views.index, name = 'index'),

    url(r'^upload_manual$', views.upload_manual, name='upload_manual'),
    url(r'^add_cat$', views.add_cat, name='add_cat'),
    url(r'^add_li$', views.add_li, name='add_li'),
    url(r'^upload_csv$', views.upload_csv, name='upload_csv'),
    url(r'^post_cat_url$', views.post_cat, name='post_cat'),
    url(r'^post_li_url$', views.post_li, name='post_li'),
    url(r'^assign_cat_to_li$', views.assign_cat_to_li, name ='assign_cat_to_li'),
    url(r'^post_li_url$', views.post_li, name='post_li'),
    url(r'^button_input', views.button_input, name='button_input'),
    url(r'^analyze=(.*)$', views.analyze, name='analyze')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
