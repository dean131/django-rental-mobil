from rest_framework.response import Response
from rest_framework import status


class CustomResponse():

# Custom Functons
    def custom(data=None, success=None, message=None, error=None, status_code=None):
        response = {}
        response['success'] = success
        if message: 
            response['message'] = message
        if error: 
            response['error'] = error
        if data: 
            response['data'] = data
        return Response(response, status=status_code)

    def success(message=None, data=None, status_code=status.HTTP_200_OK):
        response = {
            'success': 1,
            'message': message,
            'data': data,
        }
        return Response(response, status=status_code)

    def error(message=None, error=None, status_code=status.HTTP_400_BAD_REQUEST):
        response = {
            'success': 0,
            'message': message,
            'error': error,
        }
        return Response(response, status=status_code)