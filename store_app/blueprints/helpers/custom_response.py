from flask import Response


class Resp(Response):

    def __init__(self, response=None, status=200, headers=None,
                 mimetype="application/json", content_type="application/json; UTF-8"):
        super(Response, self).__init__(response=response,
                                       status=status,
                                       headers=headers,
                                       mimetype=mimetype,
                                       content_type=content_type)
