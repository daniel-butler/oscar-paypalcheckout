from django.urls import path

from .views import PaypalCancelView, PaypalSuccessView

app_name = 'paypalcheckout'

urlpatterns = [
    path('success/<int:orderno>',PaypalSuccessView.as_view(), name='paypalsuccess'),
    path('cancel/<int:orderno>',PaypalCancelView.as_view(), name='paypalcancel'),
]