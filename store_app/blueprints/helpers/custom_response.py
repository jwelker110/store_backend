from flask import Response
from custom_encoder import multi_enc


class Resp(Response):
    """
    Custom Response object that implements default values
    """
    def __init__(self, response=None, status=200, headers=None,
                 mimetype="application/json", content_type="application/json; UTF-8"):
        super(Response, self).__init__(response=response,
                                       status=status,
                                       headers=headers,
                                       mimetype=mimetype,
                                       content_type=content_type)


def create_response(data, **kwargs):
    """
    Function for creating a response using custom Resp class
    :param data: the response data to be JSONified
    :param kwargs: additional keyword args utilized by base Response class constructor
    :return: Response object
    """
    if isinstance(data, dict):
        r = multi_enc(data)
        return Resp(response=r, **kwargs)
    else:
        raise TypeError("First argument must be a dictionary containing key-value pairs to encode")
