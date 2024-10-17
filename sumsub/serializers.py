"""
Serializer Module
"""
from rest_framework import serializers


class ApplicantSerializer(serializers.Serializer):
    """
    Serializer for applicant data.

    The ApplicantSerializer class is responsible for validating and serializing
    applicant-related data. It ensures that the incoming data adheres to the expected
    format and constraints before being processed by the application.

    Attributes:
        first_name (CharField): The applicant's first name. Must not exceed 255 characters.
        last_name (CharField): The applicant's last name. Must not exceed 255 characters.
        dob (DateField): The applicant's date of birth, formatted as YYYY-MM-DD.
        nationality (CharField): The applicant's nationality code. Must be 3 characters long.
        email (EmailField): The applicant's email address, validated for proper email format.
        phone (CharField): The applicant's phone number. Must not exceed 20 characters.
    """
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    dob = serializers.DateField()
    nationality = serializers.CharField(max_length=3)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=20)


class DocumentSerializer(serializers.Serializer):
    """
    Serializer for document data.

    The DocumentSerializer class is responsible for validating and serializing
    document-related data. It ensures that the document information provided is
    structured correctly and adheres to the defined constraints.

    Attributes:
        doc_type (CharField): The type of the document (e.g., ID Card, Passport).
                              Must not exceed 255 characters.
        doc_subtype (CharField): The subtype of the document (e.g., FRONT_SIDE, BACK_SIDE).
                                 Must not exceed 255 characters.
        document_file (FileField): The actual file content of the document being uploaded.
        applicant_id (CharField): The unique identifier of the applicant to whom this document belongs.
                                  Must not exceed 255 characters.
    """
    doc_type = serializers.CharField(max_length=255)
    doc_subtype = serializers.CharField(max_length=255)
    document_file = serializers.FileField()
    applicant_id = serializers.CharField(max_length=255)
