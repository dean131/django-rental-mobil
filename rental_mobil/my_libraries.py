from rest_framework.response import Response


# Custom Functons
def custom_response(data=None, success=None, message=None, error=None, status_code=None):
    response = {}
    response['success'] = success
    if message: 
        response['message'] = message
    if error: 
        response['error'] = error
    if data: 
        response['data'] = data
    return Response(response, status=status_code)


