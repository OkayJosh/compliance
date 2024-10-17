from dataclasses import dataclass

@dataclass
class ApplicantDTO:
    """
    Data Transfer Object (DTO) for encapsulating applicant information.

    The ApplicantDTO class serves as a structured representation of an individual's
    data required for creating and managing applicants in the system. It includes
    essential personal details necessary for identity verification and compliance
    checks through the SUMSUB API.

    Attributes:
        first_name (str): The first name of the applicant.
        last_name (str): The last name of the applicant.
        dob (str): The date of birth of the applicant in YYYY-MM-DD format.
        nationality (str): The nationality of the applicant, represented by a country code (e.g., "DEU" for Germany).
        email (str): The email address of the applicant for communication and notifications.
        phone (str): The phone number of the applicant, used for contact and verification purposes.
    """

    first_name: str
    last_name: str
    dob: str
    nationality: str
    email: str
    phone: str


@dataclass
class DocumentDTO:
    """
    Data Transfer Object (DTO) for encapsulating document information related to an applicant.

    The DocumentDTO class represents the essential details required to upload
    identity documents for applicants. It includes information about the type and
    content of the document, as well as the associated applicant ID for linking
    documents to specific applicants in the system.

    Attributes:
        doc_type (str): The type of document being uploaded (e.g., "ID_CARD", "PASSPORT").
        doc_subtype (str): The subtype of the document, providing further classification (e.g., "FRONT_SIDE", "BACK_SIDE").
        content (bytes): The binary content of the document file, typically encoded in base64 for API transmission.
        applicant_id (str): The unique identifier of the applicant to whom this document belongs, linking the document
                            to their application in the database or external verification system.
    """

    doc_type: str
    doc_subtype: str
    content: bytes
    applicant_id: str
