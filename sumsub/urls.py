"""
Expose the route
"""
from django.urls import path

from sumsub.views import ApplicantCreateView, DocumentUploadView, VerificationStatusView

urlpatterns = [
    path('create/', ApplicantCreateView.as_view(), name='create-applicant'),
    path('upload-document/', DocumentUploadView.as_view(), name='upload-document'),
    path('<str:applicant_id>/status/', VerificationStatusView.as_view(), name='verification-status'),
]
