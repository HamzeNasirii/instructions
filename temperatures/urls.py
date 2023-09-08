from django.urls import path

from .views import UploadTextView

urlpatterns = [
    path('uploadTemp/', UploadTextView.as_view(), name='uploadTemp'),
    # path('uploadTemp/', BaseTXTView.as_view(), name='uploadTemp'),
]
