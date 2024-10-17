"""
Database Entity definitions for sumsub
"""
import uuid
from django.db import models


class ApplicantModel(models.Model):
    """
    A Django model representing an applicant in the system.

    The ApplicantModel class defines the structure of the applicant entity, including
    their personal information and verification status. This model is mapped to the
    underlying database.

    Attributes:
        uuid (UUIDField): A unique identifier for the applicant, set as the primary key.
        first_name (CharField): The applicant's first name.
        last_name (CharField): The applicant's last name.
        email (EmailField): The applicant's email address.
        dob (DateField): The applicant's date of birth.
        nationality (CharField): The applicant's nationality.
        phone (CharField): The applicant's phone number.
        applicant_id (CharField): A unique identifier assigned by the SUMSUB API for the applicant.
        verification_status (CharField): The current verification status of the applicant.
    """

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4())
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    dob = models.DateField()
    nationality = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    applicant_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    verification_status = models.CharField(max_length=100, null=True, blank=True)
