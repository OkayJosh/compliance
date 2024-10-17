"""
API call for the infrastructures
"""
import base64
import hashlib
import hmac
import json
import time

import requests

from application.ports import SumsubAPIPort


class SumsubAPIAdapter(SumsubAPIPort):
    """
    Adapter class for interacting with the SUMSUB API.

    The SumsubAPIAdapter class implements the SumsubAPIPort interface, providing
    methods to create applicants, add documents, and retrieve verification statuses
    via the SUMSUB API. This adapter abstracts the details of API interaction
    and formats requests according to the SUMSUB specifications.

    Attributes:
        api_token (str): The API token used for authorization with the SUMSUB API.
        base_url (str): The base URL for the SUMSUB API.

    Methods:
        create_applicant(applicant: Applicant) -> str:
            Creates a new applicant in the SUMSUB system and returns the applicant ID.

        add_document(document: Document) -> None:
            Adds a document for the specified applicant in the SUMSUB system.

        get_verification_status(applicant_id: str) -> str:
            Retrieves the verification status of an applicant by their unique ID.
    """
    TIMEOUT = 40000

    def __init__(self, api_token: str, secret_key: str, base_url: str):
        """
        Initializes the SumsubAPIAdapter with the provided API token and base URL.

        Args:
            api_token (str): The token for authenticating requests to the SUMSUB API.
            base_url (str): The base URL of the SUMSUB API.

        Example:
            >>> adapter = SumsubAPIAdapter(api_token="your_token", secret_key="secret-key", base_url="https://api.sumsub.com")
        """
        self.api_token = api_token
        self.base_url = base_url
        self.secret_key = secret_key

    def _get_headers(self, request: requests.Request) -> requests.PreparedRequest:
        """
        Constructs headers, including token, timestamp, and HMAC signature.
        """
        prepared_request = request.prepare()
        now = int(time.time())
        method = request.method.upper()
        path_url = prepared_request.path_url
        body = b'' if prepared_request.body is None else prepared_request.body

        if isinstance(body, str):
            body = body.encode('utf-8')

        data_to_sign = str(now).encode('utf-8') + method.encode('utf-8') + path_url.encode('utf-8') + body
        signature = hmac.new(
            self.secret_key.encode('utf-8'),
            data_to_sign,
            digestmod=hashlib.sha256
        ).hexdigest()

        prepared_request.headers['X-App-Token'] = self.api_token
        prepared_request.headers['X-App-Access-Ts'] = str(now)
        prepared_request.headers['X-App-Access-Sig'] = signature
        return prepared_request

    def create_applicant(self, applicant) -> str:
        """
        Creates a new applicant in the SUMSUB system.

        This method sends a POST request to the SUMSUB API to create a new applicant
        with the provided details and returns the unique applicant ID.

        Args:
            applicant (Applicant): An instance of the Applicant class containing
                                   the applicant's details such as name, date of birth,
                                   nationality, email, and phone number.

        Returns:
            str: The unique identifier of the newly created applicant.

        Raises:
            HTTPError: If the request to the SUMSUB API fails.

        Example:
            >>> applicant_id = adapter.create_applicant(applicant)
        """
        endpoint = "/resources/applicants"
        url = f"{self.base_url}{endpoint}?levelName=basic-kyc-level"
        payload = {
            "fixedInfo": {
                "firstName": applicant.first_name,
                "lastName": applicant.last_name,
                "countryOfBirth": "NGN",
                "stateOfBirth": "Lagos",
                "country": applicant.nationality,
                "nationality": applicant.nationality,
                "gender": "M",
                "dob": applicant.dob.strftime('%Y-%m-%d')
            },
            "externalUserId": str(applicant.uuid),
            "email": applicant.email,
            "phone": applicant.phone,
            "lang": "en",
            "type": "individual"
        }

        request = requests.Request(
            'POST', url, data=json.dumps(payload),
            headers={'Content-Type': 'application/json'}
        )

        # Sign the request and send
        signed_request = self._get_headers(request)
        session = requests.Session()
        response = session.send(signed_request, timeout=self.TIMEOUT)

        response.raise_for_status()
        return response.json()['id']

    def add_document(self, document) -> None:
        """
        Adds a document for the specified applicant in the SUMSUB system.

        This method encodes the document content to base64 and sends a POST request
        to the SUMSUB API to associate the document with the given applicant.

        Args:
            document (Document): An instance of the Document class containing
                                 the document's details such as type, subtype,
                                 content (in bytes), and associated applicant ID.

        Raises:
            HTTPError: If the request to the SUMSUB API fails.

        Example:
            >>> adapter.add_document(document)
        """
        url = f"{self.base_url}/resources/applicants/{document.applicant_id}/info/idDoc"

        # Read the file content directly from the InMemoryUploadedFile
        binary_content = document.document_file.read()  # Read in binary mode

        # Prepare the files for the POST request
        files = {
            'content': ('document_file', binary_content, document.document_file.content_type)
            # Use the content type from the file
        }

        # Prepare the metadata payload
        payload = {
            "metadata": json.dumps({
                "idDocSubType": document.doc_subtype,
                "idDocType": document.doc_type,
                "country": "NGA"
            })
        }

        # Create the request
        request = requests.Request(
            'POST', url, data=payload, files=files,
            headers={'X-Return-Doc-Warnings': 'true'}
        )

        # Sign the request and send
        signed_request = self._get_headers(request)
        session = requests.Session()
        response = session.send(signed_request, timeout=self.TIMEOUT)

        response.raise_for_status()
        return response.headers.get('X-Image-Id')

    def get_verification_status(self, applicant_id: str) -> str:
        """
        Retrieves the verification status of an applicant by their unique ID.

        This method sends a GET request to the SUMSUB API to fetch the verification
        status of the specified applicant and returns the result.

        Args:
            applicant_id (str): The unique identifier of the applicant whose
                                verification status is to be retrieved.

        Returns:
            str: The verification status of the applicant (e.g., 'GREEN', 'RED').

        Raises:
            HTTPError: If the request to the SUMSUB API fails.

        Example:
            >>> status = adapter.get_verification_status(applicant_id)
        """
        url = f"{self.base_url}/resources/applicants/{applicant_id}/status"
        request = requests.Request('GET', url)

        # Sign the request and send
        signed_request = self._get_headers(request)
        session = requests.Session()
        response = session.send(signed_request, timeout=self.TIMEOUT)

        response.raise_for_status()
        return response.json()['reviewStatus']
