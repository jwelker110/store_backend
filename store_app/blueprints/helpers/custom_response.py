from flask import Response
from custom_encoder import multi_enc


class Resp(Response):

    def __init__(self, response=None, status=200, headers=None,
                 mimetype="application/json", content_type="application/json; UTF-8"):
        super(Response, self).__init__(response=response,
                                       status=status,
                                       headers=headers,
                                       mimetype=mimetype,
                                       content_type=content_type)


def create_response(data, **kwargs):
    if isinstance(data, dict):
        r = multi_enc(data)
        return Resp(response=r, **kwargs)
    else:
        raise TypeError("First argument must be a dictionary containing key-value pairs to encode")
