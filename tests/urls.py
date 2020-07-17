from django.apps import apps
from django.urls import include, path

from paypalv2.views import PaypalCancelView, PaypalSuccessView

app_name = 'paypalcheckout'

urlpatterns = [
    path('success/<int:orderno>', PaypalSuccessView.as_view(), name='paypalsuccess'),
    path('cancel/<int:orderno>', PaypalCancelView.as_view(), name='paypalcancel'),
    path('', include(apps.get_app_config('oscar').urls[0])),
]
