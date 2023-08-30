from rest_framework.response import Response

from knox.auth import TokenAuthentication
from knox.models import AuthToken
from knox.settings import CONSTANTS, knox_settings
from knox.crypto import hash_token
import binascii
from rest_framework import exceptions
from hmac import compare_digest


# Custom Classes
class CustomTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, token):
            msg = {
                'success': 0,
                'error': 'Invalid Token',
            }
            token = token.decode("utf-8")
            for auth_token in AuthToken.objects.filter(
                    token_key=token[:CONSTANTS.TOKEN_KEY_LENGTH]):
                if self._cleanup_token(auth_token):
                    continue

                try:
                    digest = hash_token(token)
                except (TypeError, binascii.Error):
                    raise exceptions.AuthenticationFailed(msg)
                if compare_digest(digest, auth_token.digest):
                    if knox_settings.AUTO_REFRESH and auth_token.expiry:
                        self.renew_token(auth_token)
                    return self.validate_user(auth_token)
            raise exceptions.AuthenticationFailed(msg)



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


