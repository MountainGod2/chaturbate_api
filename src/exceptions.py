class CBApiException(Exception):
    pass


class FetchDataError(CBApiException):
    print("FetchDataError")


# You can define more specific exceptions if needed
