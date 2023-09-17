from django.urls import path

from .views import DeviceListView, UploadTextView, DeviceReportsDetailView, BaseDeviceReportView, chart_view

urlpatterns = [
    path('search_temp/', chart_view, name='search_temp'),
    path('draw_temp/<int:device_id>/', BaseDeviceReportView.as_view(), name='draw_temp'),
    path('devicesList/', DeviceListView.as_view(), name='devicesList'),
    path('uploadTemp/', UploadTextView.as_view(), name='uploadTemp'),
    path('device_reports/<int:device_id>/', DeviceReportsDetailView.as_view(), name='device-reports'),
]
