
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .serializers import CreateUserSerializer, LoginUserSerializer
from .service import authorize_token, revoke_token


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    '''
    Registers user to the server. Input should be in the format:
    {"phone_number": "987654321", "password": "1234abcd", "name":"name", "email"}
    '''
    serializer = CreateUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        response = authorize_token(
            request.data['phone_number'], request.data['password'])
        return Response(response.json())
    return Response(serializer.errors, status=400)


@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):
    '''
    Gets tokens with username and password. Input should be in the format:
    {"username": "username", "password": "1234abcd"}
    '''
    serializer = LoginUserSerializer(data=request.data)
    if not serializer.is_valid():
        return Response('Invalid Username or Password', status=400)
    response = authorize_token(
        request.data['username'], request.data['password'])
    return Response(response.json())


@api_view(['POST'])
@permission_classes([AllowAny])
def logout(request):
    '''
    Method to revoke tokens.
    {"token": "<token>"}
    '''
    response = revoke_token(request.data['token'])
    if response.status_code == 200:
        return Response({'message': 'token revoked'}, response.status_code)
