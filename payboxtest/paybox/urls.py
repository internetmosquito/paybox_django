from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.post_list),
    url(r'^manage_response$', views.manage_response),
    url(r'^error_response$', views.error_response),
    url(r'^payment/(?P<order_reference>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/$',
        views.make_payment),
]
