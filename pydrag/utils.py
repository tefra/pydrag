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
