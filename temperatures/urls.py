from django.urls import path

from .views import UploadTextView, DeviceReportsView, DeviceListView

urlpatterns = [
    path('devicesList/', DeviceListView.as_view(), name='devicesList'),
    path('uploadTemp/', UploadTextView.as_view(), name='uploadTemp'),
    path('device_reports/<int:device_id>/', DeviceReportsView.as_view(), name='device-reports'),
]
