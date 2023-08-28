from rest_framework.response import Response

def custom_response(data=None, success=None, message=None, error=None, status_code=None):
    response = {}
    response['success'] = success
    if data: 
        response['data'] = data
    if message: 
        response['message'] = message
    if error: 
        response['error'] = error
    return Response(response, status=status_code)
