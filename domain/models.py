from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from django.core.files.uploadedfile import InMemoryUploadedFile


@dataclass
class Applicant:
    """
    Represents an applicant's information and associated verification details.

    The Applicant class serves as a comprehensive representation of an individual
    who is undergoing verification through the SUMSUB API. It encapsulates both the
    personal details of the applicant and the state of their verification process,
    allowing for efficient management of applicant data within the system.

    Attributes:
        first_name (str): The first name of the applicant.
        last_name (str): The last name of the applicant.
        dob (str): The date of birth of the applicant in YYYY-MM-DD format.
        nationality (str): The nationality of the applicant, represented by a country code (e.g., "DEU" for Germany).
        email (str): The email address of the applicant for communication and notifications.
        phone (str): The phone number of the applicant, used for contact and verification purposes.
        applicant_id (Optional[str]): The unique identifier assigned by the SUMSUB API to this applicant.
        uuid (Optional[uuid.UUID]): A universally unique identifier for tracking the applicant within the internal data store.
        verification_status (Optional[str]): The current status of the applicant's verification (e.g., "PENDING", "VERIFIED", "REJECTED").
    """

    first_name: str
    last_name: str
    dob: str
    nationality: str
    email: str
    phone: str
    applicant_id: Optional[str] = None
    uuid: Optional[UUID] = None
    verification_status: Optional[str] = None


@dataclass
class Document:
    """
    Represents the details of an identity document associated with an applicant.

    The Document class encapsulates the necessary information for uploading
    and managing identity documents that belong to an applicant. It includes
    details about the document type, its content, and the associated applicant ID,
    enabling efficient document handling and processing within the system.

    Attributes:
        doc_type (str): The type of document being uploaded (e.g., "ID_CARD", "PASSPORT").
        doc_subtype (str): The subtype of the document, providing further classification (e.g., "FRONT_SIDE", "BACK_SIDE").
        document_file (InMemoryUploadedFile): The InMemoryUploadedFile content of the document file.
        applicant_id (str): The unique identifier of the applicant to whom this document belongs, linking the document
                            to their application in the database or external verification system.
    """

    doc_type: str
    doc_subtype: str
    document_file: InMemoryUploadedFile
    applicant_id: str
