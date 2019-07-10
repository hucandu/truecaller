
class StandardResponse(object):
    """
    Contains all the standard response structure for search
    service of this api containing major 3 keys [code, status, errors]
    """

    def __init__(self):
        self.core_response = {"code": "","status": "","errors": []}

    def failed_response(self, code=200, reason=""):
        self.core_response["code"] = code
        self.core_response["status"] = "failed"
        self.core_response["errors"].append(reason)
        return self.core_response


    def success_response(self, result=None):
        self.core_response["code"] = 200
        self.core_response["status"] = "success"
        self.core_response["result"] = result
        return self.core_response
