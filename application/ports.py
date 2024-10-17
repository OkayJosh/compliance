"""
Application ports
"""
from abc import ABC, abstractmethod

from domain.models import Applicant, Document


class ApplicantRepositoryPort(ABC):
    """
    Abstract base class defining the interface for an applicant repository.

    The ApplicantRepositoryPort specifies the methods that any concrete implementation of an
    applicant repository must provide. This allows the application to interact with different
    storage mechanisms (e.g., databases, in-memory stores) without being tightly coupled to any
    specific implementation.

    Methods:
        save_applicant(applicant: Applicant) -> None:
            Saves the provided Applicant instance to the repository.

        get_applicant(applicant_id: str) -> Applicant:
            Retrieves an Applicant instance based on the provided applicant ID.
    """

    @abstractmethod
    def save_applicant(self, applicant: Applicant) -> None:
        """
        Saves the provided Applicant instance to the repository.

        Args:
            applicant (Applicant): The Applicant instance to be saved.
        """
        pass

    @abstractmethod
    def get_applicant(self, applicant_id: str) -> Applicant:
        """
        Retrieves an Applicant instance based on the provided applicant ID.

        Args:
            applicant_id (str): The unique identifier of the applicant to retrieve.

        Returns:
            Applicant: The Applicant instance associated with the given ID.

        Raises:
            NotFoundError: If an applicant with the specified ID does not exist in the repository.
        """
        pass

    @abstractmethod
    def update_applicant(self, applicant_id: str, **kwargs) -> Applicant:
        """
        Retrieves an Applicant instance based on the provided applicant ID.

        Args:
            applicant_id: str, the applicant id we would update
            kwargs (dict): key, value pair that you need to update.

        Returns:
            Applicant: The Applicant instance associated with the given ID.

        Raises:
            NotFoundError: If an applicant with the specified ID does not exist in the repository.
        """
        pass


class SumsubAPIPort(ABC):
    """
    Abstract base class defining the interface for interacting with the SUMSUB API.

    The SumsubAPIPort specifies the methods that any concrete implementation of the SUMSUB API
    adapter must provide. This allows the application to use different API implementations or
    mock implementations during testing without being tightly coupled to any specific API.

    Methods:
        create_applicant(dto: Applicant) -> str:
            Creates a new applicant in the SUMSUB system and returns the assigned applicant ID.

        add_document(document: Document) -> None:
            Uploads a document for an existing applicant to the SUMSUB system.

        get_verification_status(applicant_id: str) -> str:
            Retrieves the verification status of an applicant based on their unique applicant ID.
    """

    @abstractmethod
    def create_applicant(self, applicant: Applicant) -> str:
        """
        Creates a new applicant in the SUMSUB system and returns the assigned applicant ID.

        Args:
            applicant (Applicant): The Applicant instance containing the applicant's details.

        Returns:
            str: The unique identifier assigned to the created applicant by the SUMSUB system.
        """
        pass

    @abstractmethod
    def add_document(self, document: Document) -> None:
        """
        Uploads a document for an existing applicant to the SUMSUB system.

        Args:
            document (Document): The Document instance to be uploaded, associated with an applicant.
        """
        pass

    @abstractmethod
    def get_verification_status(self, applicant_id: str) -> str:
        """
        Retrieves the verification status of an applicant based on their unique applicant ID.

        Args:
            applicant_id (str): The unique identifier of the applicant for whom to retrieve the status.

        Returns:
            str: The current verification status of the applicant (e.g., "PENDING", "VERIFIED", "REJECTED").
        """
        pass
