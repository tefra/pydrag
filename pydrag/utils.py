import hashlib


def md5(text: str) -> str:
    """
    Util method to produce a 32char md5 digest, if string is empty return
    immediately.

    :param str text: The string to hash
    :rtype: str
    """
    if text == "":
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
