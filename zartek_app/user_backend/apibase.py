from django.views.generic import View
from django.http import JsonResponse

class StatusCode(View):
    # Success Codes
    HTTP_200_OK = 200
    HTTP_201_CREATED = 201
    HTTP_202_ACCEPTED = 202
    HTTP_203_NON_AUTHORITATIVE = 203
    HTTP_204_NO_CONTENT = 204
    HTTP_205_RESET_CONTENT = 205
    HTTP_206_PARTIAL_CONTENT = 206

    # Client Error Codes
    HTTP_400_BAD_REQUEST = 400
    HTTP_401_UNAUTHORIZED = 401
    HTTP_402_PAYMENT_REQUIRED = 402
    HTTP_403_FORBIDDEN = 403
    HTTP_404_NOT_FOUND = 404
    HTTP_405_METHOD_NOT_ALLOWED = 405
    HTTP_406_NOT_ACCEPTABLE = 406
    HTTP_408_REQUEST_TIMEOUT = 408
    HTTP_409_CONFLICT = 409
    HTTP_410_GONE = 410
    HTTP_415_UNSUPPORTED_MEDIA_TYPE = 415
    HTTP_426_FORCE_UPDATE = 426

    # Server Error Codes
    HTTP_500_INTERNAL_SERVER_ERROR = 500
    HTTP_501_NOT_IMPLEMENTED = 501
    HTTP_502_BAD_GATEWAY = 502
    HTTP_503_SERVICE_UNAVAILABLE = 503
    HTTP_504_GATEWAY_TIMEOUT = 504

# This class is for wrapping the json response.
class JsonWrapper(JsonResponse):
    def __init__(self, data, flag):
        wrapper_dic = {
            'status': flag,
            'data': data
        }
        super(JsonWrapper, self).__init__(wrapper_dic, status=flag, json_dumps_params={"indent": 4})

# This function is for Changing Queryset to Dictnory
def ValuesQuerySetToDict(vqs):
    return [item for item in vqs]
