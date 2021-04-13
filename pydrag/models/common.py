import os
import time
from collections import UserList
from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field
from dataclasses import fields
from typing import Dict, ClassVar, Tuple
from typing import List
from typing import Optional
from typing import Sequence
from typing import Type
from typing import TypeVar
from typing import Union

from pydrag.utils import md5
from pydrag.utils import to_camel_case

T = TypeVar("T", bound="BaseModel")

def filter_none_and_dicts(x: Tuple) -> Dict:
    return {k: v for k, v in x if v is not None}

@dataclass
class BaseModel:
    """
    Pydrag Base Model.

    :param params: The params used to fetch the api response data
    """

    params: Union[List, Dict, None] = field(init=False, default=None)

    def to_dict(self) -> Dict:
        """
        Convert our object to a traditional dictionary. Filter out None values
        and dictionary values. The last one is like a validation for the unit
        tests in case we forgot to properly deserialize an dict to an object.

        :rtype: Dict
        """
        return asdict(self, dict_factory=filter_none_and_dicts)

    @classmethod
    def from_dict(cls: Type, data: Dict) -> "BaseModel":
        """
        Construct a BaseModel from a dictionary based on the class fields type
        annotations. Only primitive types are supported.

        :param data:
        :type data: Type[BaseModel]
        :rtype: :class:`~pydrag.models.common.BaseModel`
        """
        for f in fields(cls):
            if f.name not in data or data[f.name] is None:
                continue

            if f.type == str or f.type == Optional[str]:
                data[f.name] = str(data[f.name])
            elif f.type == int or f.type == Optional[int]:
                try:
                    data[f.name] = int(data[f.name])
                except ValueError:
                    data[f.name] = 0
            elif f.type == float or f.type == Optional[float]:
                data[f.name] = float(data[f.name])
            elif f.type == bool or f.type == Optional[bool]:
                data[f.name] = bool(int(data[f.name]))

        return cls(**data)


@dataclass(eq=False)
class ListModel(UserList, Sequence[T], BaseModel):
    """
    Wrap a list of :class:`~pydrag.models.common.BaseModel` objects with
    metadata.

    :param data: Our list of objects
    :param page: Current page number
    :param limit: Per page limit
    :param total: Total number of items
    :param tag: Tag name
    :param user: User name
    :param artist: Artist name
    :param track: Track name
    :param album: Album name
    :param country: Country name
    :param from_date: From date timestamp
    :param to_date: To date timestamp
    :param search_terms: Search query string
    """

    data: List[T] = field(default_factory=list)
    page: Optional[int] = field(default=None)
    limit: Optional[int] = field(default=None)
    total: Optional[int] = field(default=None)
    tag: Optional[str] = field(default=None)
    user: Optional[str] = field(default=None)
    artist: Optional[str] = field(default=None)
    track: Optional[str] = field(default=None)
    album: Optional[str] = field(default=None)
    country: Optional[str] = field(default=None)
    from_date: Optional[int] = field(default=None)
    to_date: Optional[int] = field(default=None)
    search_terms: Optional[str] = field(default=None)

    @classmethod
    def from_dict(cls: Type, data: Dict):
        if "attr" in data:
            data.update(data.pop("attr"))

        if "query" in data:
            data["query"].pop("text", None)
            data["query"].pop("role", None)
            data.update(data.pop("query"))

        if "offset" in data and "page" not in data and "limit" in data:
            data["page"] = int(data["offset"]) / int(data["limit"])

        data.pop("offset", None)
        return super().from_dict(data)


@dataclass
class RawResponse(BaseModel):
    """
    Most of the write operations don't return any response body but still for
    consistency we need to return a BaseModel with all the metadata params.

    :param data: The raw response dictionary
    """

    data: Optional[Dict] = field(default=None)

    def to_dict(self) -> Dict:
        return self.data

    @classmethod
    def from_dict(cls, data):
        return cls(data)


@dataclass
class Config:
    """
    Pydrag config object for your last.fm api.

    :param api_key: Your application api key
    :param api_secret: Your application api secret
    :param username: The user' name you want to authenticate
    :param password: The user's password you want to authenticate
    :param session: The already authenticated user's session key
    """

    api_key: str = field()
    api_secret: Optional[str] = field(default=None)
    username: Optional[str] = field(default=None)
    password: Optional[str] = field(default=None)
    session: Optional["AuthSession"] = field(default=None)

    api_url: ClassVar[str] = "https://ws.audioscrobbler.com/2.0/"
    auth_url: ClassVar[str] = "https://www.last.fm/api/auth?token={}&api_key={}"
    _instance: ClassVar[Optional["Config"]] = field(default=None)

    def __post_init__(self):
        Config._instance = self
        self.password = md5(self.password)

    @property
    def auth_token(self):
        return md5(str(self.username) + str(self.password))

    @staticmethod
    def instance(
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        session: Optional[str] = None,
    ):
        """Get/Create a config instance, if no api key is specified it attempt
        to read the settings from environmental variables."""

        keys = [f.name for f in fields(Config)]
        if Config._instance is None or api_key:
            if api_key:
                values = locals()
                params = {k: values[k] for k in keys}
            else:
                params = {
                    k: os.getenv(
                        f"LASTFM_{k.upper()}",
                        "" if k == "api_key" else None,
                    )
                    for k in keys
                }

            if len(params["api_key"]) == 0:
                raise ValueError("Provide a valid last.fm api key.")

            Config(**params)
        return Config._instance

    def to_dict(self):
        return asdict(self)


@dataclass
class Image(BaseModel):
    size: str
    text: str


@dataclass
class Chart(BaseModel):
    text: str
    from_date: str
    to_date: str


@dataclass
class Link(BaseModel):
    href: str
    rel: str
    text: str


@dataclass
class Wiki(BaseModel):
    content: Optional[str] = field(default=None)
    summary: Optional[str] = field(default=None)
    published: Optional[str] = field(default=None)
    links: Optional[List[Link]] = field(default=None)

    @classmethod
    def from_dict(cls, data: Dict):
        if "links" in data:
            if isinstance(data["links"]["link"], dict):
                data["links"]["link"] = [data["links"]["link"]]

            data["links"] = list(map(Link.from_dict, data["links"]["link"]))
        return super().from_dict(data)


@dataclass
class ScrobbleTrack(BaseModel):
    artist: str
    track: str
    timestamp: int = field(default_factory=lambda: int(time.time()))
    track_number: Optional[str] = field(default=None)
    album: Optional[str] = field(default=None)
    album_artist: Optional[str] = field(default=None)
    duration: Optional[int] = field(default=None)
    mbid: Optional[str] = field(default=None)
    context: Optional[str] = field(default=None)
    stream_id: Optional[str] = field(default=None)
    chosen_by_user: Optional[bool] = field(default=None)

    def to_api_dict(self):
        return {to_camel_case(k): v for k, v in self.to_dict().items()}

    @classmethod
    def from_dict(cls, data: Dict):
        data.update(
            {
                k: data[k]["text"] if data.get(k, {}).get("text", "") != "" else None
                for k in ["album", "artist", "track", "album_artist"]
            }
        )
        return super().from_dict(data)
