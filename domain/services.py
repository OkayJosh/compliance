from django.forms import model_to_dict

from application.ports import ApplicantRepositoryPort, SumsubAPIPort
from domain.models import Applicant, Document


class SumsubApplicant:
    """
    Service class for managing applicant operations, including creation, document handling,
    and verification status retrieval.

    The SumsubApplicant class acts as an intermediary between the application's business logic
    and the external systems (such as the SUMSUB API and the applicant repository). It provides
    methods to create applicants, upload documents, and check verification statuses, encapsulating
    the logic necessary for these operations.

    Attributes:
        applicant_repo (ApplicantRepositoryPort): An interface for interacting with the applicant repository,
            allowing for persistence and retrieval of applicant data.
        sumsub_api (SumsubAPIPort): An interface for interacting with the SUMSUB API, facilitating
            operations related to applicant verification and document management.
    """

    def __init__(self, applicant_repo: ApplicantRepositoryPort, sumsub_api: SumsubAPIPort):
        """
        Initializes the SumsubApplicant with the specified repository and API interfaces.

        Args:
            applicant_repo (ApplicantRepositoryPort): The repository interface for managing applicants.
            sumsub_api (SumsubAPIPort): The API interface for interacting with the SUMSUB system.
        """
        self.applicant_repo = applicant_repo
        self.sumsub_api = sumsub_api
        self.applicant_db = None
        self.applicant = None

    def create_applicant(self, applicant_dto):
        """
        Creates a new applicant using the provided applicant data transfer object (DTO).

        This method constructs an Applicant instance from the given DTO, interacts with the SUMSUB API
        to create the applicant, and saves the applicant's information in the repository.

        Args:
            applicant_dto: An object containing the applicant's details required for creation.

        Returns:
            Applicant: The created Applicant instance, now including the assigned applicant ID.
        """
        self.applicant = Applicant(
            first_name=applicant_dto.first_name,
            last_name=applicant_dto.last_name,
            dob=applicant_dto.dob,
            nationality=applicant_dto.nationality,
            email=applicant_dto.email,
            phone=applicant_dto.phone,
        )
        self.applicant_db, created = self.applicant_repo.save_applicant(self.applicant)
        applicant_id = self.sumsub_api.create_applicant(Applicant(**model_to_dict(self.applicant_db)))
        self.applicant.applicant_id = applicant_id
        self.applicant_db.applicant_id = applicant_id
        self.applicant_db.save()
        return self

    def add_document(self, document_dto):
        """
        NOTE:: Instead of having another class called: SumsubDocument, I refactor to have a single class here with the
        add_document method.
        Adds a document for an existing applicant using the provided document data transfer object (DTO).

        This method constructs a Document instance from the given DTO and uploads it to the SUMSUB API.

        Args:
            document_dto: An object containing the document's details required for upload.
        """
        document = Document(
            doc_type=document_dto.doc_type,
            doc_subtype=document_dto.doc_subtype,
            document_file=document_dto.document_file,
            applicant_id=document_dto.applicant_id,
        )
        self.sumsub_api.add_document(document)

    def get_verification_status(self, applicant_id):
        """
        Retrieves the verification status of an applicant based on their unique applicant ID.

        This method queries the SUMSUB API to obtain the current verification status for the specified
        applicant.

        Args:
            applicant_id (str): The unique identifier of the applicant for whom the status is being retrieved.

        Returns:
            str: The verification status of the applicant (e.g., "INIT", "VERIFIED", "REJECTED").
        """
        status = self.sumsub_api.get_verification_status(applicant_id)
        self.applicant_db = self.applicant_repo.update_applicant(
            applicant_id=applicant_id, verification_status=status
        )
        # Get and print verification status
        print("status", status)
        return status
