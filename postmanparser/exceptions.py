class MissingRequiredFieldException(Exception):
    """
    Object missing required fields
    """

    pass


class InvalidPropertyValueException(Exception):
    """
    Value of property present in object is invalid
    """

    pass


class InvalidObjectException(Exception):
    pass


class FolderNotFoundError(Exception):
    """
    Item Group does not exists
    """

    pass
