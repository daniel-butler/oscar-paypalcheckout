from django.apps import apps
from django.urls import include, path
from django.contrib import admin

from paypalv2.views import PaypalCancelView, PaypalSuccessView

app_name = 'paypalcheckout'

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('', include(apps.get_app_config('oscar').urls[0])),

    # Paypalv2 URLS
    path('success/<int:orderno>', PaypalSuccessView.as_view(), name='paypalsuccess'),
    path('cancel/<int:orderno>', PaypalCancelView.as_view(), name='paypalcancel'),

]
