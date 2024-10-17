"""
Endpoint for SumSub Module
"""
from django.conf import settings
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response

from domain.models import Applicant, Document
from domain.services import SumsubApplicant
from infrastructure.repositories import ApplicantRepository
from infrastructure.sumsub_api import SumsubAPIAdapter
from sumsub.serializers import ApplicantSerializer, DocumentSerializer


class BaseApplicantView(APIView):
    """
    Base view class to initialize the SumsubApplicant.
    Other views will inherit this to avoid duplicating service instantiation.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.applicant_service = SumsubApplicant(
            applicant_repo=ApplicantRepository(),
            sumsub_api=SumsubAPIAdapter(
                api_token=settings.SUMSUB_API_TOKEN,
                secret_key=settings.SUMSUB_API_SECRET,
                base_url=settings.SUMSUB_BASE_URL
            )
        )


class ApplicantCreateView(BaseApplicantView):
    """
    Handles the creation of new applicants by interacting with the SUMSUB API
    and storing applicant data in the local database.
    """

    def post(self, request):
        """
        Handle POST requests to create a new applicant.

        - Validates incoming data using `ApplicantSerializer`.
        - Calls the `SumsubApplicant` to create an applicant using SUMSUB API.
        - Stores the applicant data in the local database.

        Returns:
            - 201 status code on successful applicant creation along with applicant_id.
            - 400 status code with validation errors if the input data is invalid.
        """
        serializer = ApplicantSerializer(data=request.data)
        if serializer.is_valid():
            applicant_obj = self.applicant_service.create_applicant(Applicant(**serializer.validated_data))
            return Response({"applicant_id": applicant_obj.applicant.applicant_id}, status=201)
        return Response(serializer.errors, status=400)


class DocumentUploadView(BaseApplicantView):
    """
    Handles the uploading of identity documents for applicants by interacting with the SUMSUB API.
    """

    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        """
        Handle POST requests to upload an identity document for an applicant.

        - Validates incoming data using `DocumentSerializer`.
        - Calls the `SumsubApplicant` to upload the document using the SUMSUB API.

        Returns:
            - 200 status code on successful document upload.
            - 400 status code with validation errors if the input data is invalid.
        """
        serializer = DocumentSerializer(data=request.data)
        if serializer.is_valid():
            self.applicant_service.add_document(Document(**serializer.validated_data))
            return Response({"status": "Document uploaded"}, status=200)
        return Response(serializer.errors, status=400)


class VerificationStatusView(BaseApplicantView):
    """
    Retrieves the verification status of a given applicant by interacting with the SUMSUB API.
    """

    def get(self, request, applicant_id):
        """
        Handle GET requests to fetch the verification status of an applicant.

        - Calls the `SumsubApplicant` to fetch the verification status from the SUMSUB API.

        Returns:
            - 200 status code with the applicant's current verification status.
        """
        status = self.applicant_service.get_verification_status(applicant_id)
        return Response({"verification_status": status}, status=200)
