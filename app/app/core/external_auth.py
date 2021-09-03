from abc import ABC, abstractmethod
from datetime import datetime
from httpx import Client
from pydantic import BaseModel
from typing import Generic, Optional, Type, TypeVar

from app.core.exceptions import ApiAuthenticationError
from app.core.logging import get_logger


class BaseOAuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class BaseOAuthRequest(BaseModel):
    client_id: str
    client_secret: str
    grant_type: str = "client_credentials"


RequestSchemaType = TypeVar("RequestSchemaType", bound=BaseOAuthRequest)
ResponseSchemaType = TypeVar("ResponseSchemaType", bound=BaseOAuthResponse)


class Singleton(type):
    """
    Stores a dictionary of classes to class instances, and provides the override necessary to first use that dictionary.
    """

    _instances = {}  # type: ignore

    def __call__(cls, *args, **kwargs):
        """
        The metaclass's call method is executed before the class using the metaclass would execute any
        __new__ or __init__ methods.  In this way, by storing a reference to the instances of the class, existing
        instances of a class can be stored and returned, rather than a new one being created.

        TODO:  If the eligibility service is horizontally scaled, the singleton model should be shifted to
               a 'borg' model where state is shared across instances, rather than enforcing a single instance
               in this way we can store the state remotely, likely on redis, so to be shared across instances
               of the application.
        """
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class AbstractSingletonMetaClass(ABC, Singleton):
    pass


class BaseCredentials(
    Generic[RequestSchemaType, ResponseSchemaType], metaclass=AbstractSingletonMetaClass
):
    """
    Class to contain the logic around OAuth flow.
    """

    def __init__(
        self,
        request_type: Type[RequestSchemaType],
        response_type: Type[ResponseSchemaType],
        *,
        oauth_response: Optional[ResponseSchemaType] = None,
        client: Optional[Client] = None,
        accessed_at: Optional[datetime] = None,
    ):
        """
        oauth: Response from api request for OAuth token
        accessed_at: Timestamp of the authentication request (default now)
        """
        self.response_type = response_type
        self.request_type = request_type
        self._client = client or Client()
        self._oauth = oauth_response
        self._accessed_at = accessed_at or datetime.now()

    @classmethod
    def _reset(cls):
        """
        Remove the saved instance (for testing purposes)
        """
        try:
            if cls._instances:
                instance = cls._instances[cls]
                cls._instances = {}
                del instance
        except KeyError:  # pragma: no cover
            pass

    @property
    @abstractmethod
    def authentication_endpoint(self) -> str:
        raise NotImplementedError("Child class must implement")

    @property
    @abstractmethod
    def authentication_request(self) -> RequestSchemaType:
        raise NotImplementedError("Child class must implement")

    @property
    def accessed_at(self) -> datetime:
        return self._accessed_at

    @property
    def access_token(self) -> str:
        if self.expired:
            self._oauth = self.retrieve_token()
            self._accessed_at = datetime.now()
        return self.oauth_response.access_token

    @property
    def authorization_header(self) -> dict:
        return {"Authorization": f"Bearer {self.access_token}"}

    @property
    def expired(self) -> bool:
        seconds_elapsed = (datetime.now() - self.accessed_at).seconds
        # May be advantageous to return false a little bit before schedule
        if seconds_elapsed >= self.oauth_response.expires_in:
            return True
        return False

    @property
    def oauth_response(self) -> ResponseSchemaType:
        if not self._oauth:
            self._oauth = self.retrieve_token()
        return self._oauth

    @property
    def request_headers(self) -> Optional[dict]:
        return None

    def retrieve_token(self) -> ResponseSchemaType:
        logger = get_logger(name=__name__)
        response = self._client.post(
            self.authentication_endpoint,
            data=self.authentication_request.dict(),
            headers=self.request_headers or {},
        )
        if response.is_error:
            logger.warning(
                f"Error authenticating with credentials ({self.authentication_request.client_id})"
            )
            json_ = response.json()
            message = f"Received a {response.status_code} response with an error"
            if "error" not in json_:
                raise ApiAuthenticationError(
                    f"{message} (content: {json_}",
                    api_endpoint=self.authentication_endpoint,
                )
            raise ApiAuthenticationError(
                f"{message} of {json_['error']}",
                api_endpoint=self.authentication_endpoint,
            )
        return self.response_type(**response.json())  # type: ignore
