import hashlib
from typing import Optional


def md5(text: Optional[str]) -> Optional[str]:
    """
    Util method to produce a 32char md5 digest, if string is empty or None
    return empty string.

    :param str text: The string to hash
    :type text: Optional[str]
    :rtype: str
    """
    if text == "" or text is None:
        return text
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def to_camel_case(text):
    """
    Convert string with underscores to camel case.

    .. note:: Source StackOverflow <https://stackoverflow.com/a/19053800>`_
    :param str text: The string to convert
    :rtype: str
    """

    components = text.split("_")
    return components[0].lower() + "".join(x.title() for x in components[1:])


def get_nested(obj, keys, ensure_list=False):
    for key in keys:
        obj = obj[key]

    if ensure_list and isinstance(obj, dict):
        obj = [obj]
    return obj
