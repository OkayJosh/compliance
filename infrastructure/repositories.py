"""
Repositories for infrastructure.
"""
from application.ports import ApplicantRepositoryPort
from domain.models import Applicant
from sumsub.models import ApplicantModel


class ApplicantRepository(ApplicantRepositoryPort):
    """
    Concrete implementation of the ApplicantRepositoryPort interface.

    The ApplicantRepository class provides methods for saving and retrieving applicant data
    from the database. It interacts with the ApplicantModel, which represents the applicant's
    data structure in the database.

    Methods:
        save_applicant(applicant: Applicant) -> None:
            Saves the provided Applicant instance to the database.

        get_applicant(applicant_id: str) -> Applicant:
            Retrieves an Applicant instance based on the provided applicant ID from the database.
    """

    def save_applicant(self, applicant: Applicant) -> None:
        """
        Saves the provided Applicant instance to the database.

        This method maps the attributes of the Applicant instance to the fields in the
        ApplicantModel and creates a new entry in the database.

        Args:
            applicant (Applicant): The Applicant instance to be saved, containing all relevant
                                   details such as name, date of birth, and contact information.

        Example:
            >>> applicant = Applicant(first_name="John", last_name="Doe", dob="1990-01-01",
                                      nationality="US", email="john@example.com", phone="123456789")
            >>> repository.save_applicant(applicant)
        """
        return ApplicantModel.objects.get_or_create(
            first_name=applicant.first_name,
            last_name=applicant.last_name,
            dob=applicant.dob,
            nationality=applicant.nationality,
            email=applicant.email,
            phone=applicant.phone
        )

    def get_applicant(self, applicant_id: str) -> Applicant:
        """
        Retrieves an Applicant instance based on the provided applicant ID from the database.

        This method queries the ApplicantModel to find an applicant using their unique
        applicant ID and returns an Applicant instance populated with the retrieved data.

        Args:
            applicant_id (str): The unique identifier of the applicant to retrieve.

        Returns:
            Applicant: An instance of the Applicant class containing the retrieved details.

        Raises:
            DoesNotExist: If no applicant with the specified ID exists in the database.

        Example:
            >>> applicant = repository.get_applicant(applicant_id="12345")
            >>> print(applicant.first_name)
            John
        """
        applicant = ApplicantModel.objects.get(applicant_id=applicant_id)
        return Applicant(
            uuid=applicant.uuid,
            first_name=applicant.first_name,
            last_name=applicant.last_name,
            dob=applicant.dob,
            nationality=applicant.nationality,
            email=applicant.email,
            phone=applicant.phone,
            applicant_id=applicant.applicant_id,
            verification_status=applicant.verification_status
        )

    def update_applicant(self, applicant_id: str, **kwargs) -> Applicant:
        """
        Updates an existing Applicant instance based on the provided applicant ID.

        This method retrieves the Applicant instance from the database using the specified applicant ID
        and updates it with the provided keyword arguments. The keyword arguments should match the fields
        of the ApplicantModel, allowing for selective updates to the applicant's details.

        Args:
            applicant_id (str): The unique identifier of the applicant to update.
            **kwargs: Arbitrary keyword arguments representing the fields to be updated. This can include
                      any of the following attributes of the Applicant:
                      - first_name: Updated first name of the applicant.
                      - last_name: Updated last name of the applicant.
                      - dob: Updated date of birth of the applicant.
                      - nationality: Updated nationality of the applicant.
                      - email: Updated email address of the applicant.
                      - phone: Updated phone number of the applicant.
                      - verification_status: Updated verification status of the applicant.

        Returns:
            Applicant: The updated Applicant instance populated with the modified data from the database.

        Raises:
            DoesNotExist: If no applicant with the specified ID exists in the database.

        Example:
            >>> updated_applicant = repository.update_applicant(applicant_id="12345", email="newemail@example.com")
            >>> print(updated_applicant.email)
            newemail@example.com
        """
        return ApplicantModel.objects.filter(applicant_id=applicant_id).update(**kwargs)

