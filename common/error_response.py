from common.base_response import BaseResponse
from flask import jsonify


class ErrorResponse(object):

    data = None
    success = False
    message = None
    total = 0
    page = 0
    limit = 0
    code = 400

    def __init__(self, exception, code):
        self.message = str(exception) if exception is not None else None
        self.code = code

    def serialize(self):
        return (
            jsonify(BaseResponse(None, self.message, 0, 0, 0, False).serialize()),
            self.code,
        )
