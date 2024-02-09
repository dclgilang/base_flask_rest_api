class BaseResponse(object):

    data = None
    success = False
    message = None

    def __init__(self, data, exception, page, limit, total, success):
        self.total = total
        self.page = page
        self.limit = limit
        self.data = data
        self.message = str(exception) if exception is not None else None
        self.success = success

    def serialize(self):
        return {
            'meta' : {
                "total": self.total,
                "page": self.page,
                "limit": self.limit
            },
            'success': self.success,
            'message': self.message,
            'data': self.data,
        }