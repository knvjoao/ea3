from rest_framework.views import APIView
import jwt
from django.conf import settings
from jwt import ExpiredSignatureError, InvalidTokenError
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from rest_framework import status

#O código foi testado com o curl, criando um usuário e gerando o token, que só funciona com credenciais válidas. O retorno é valid: True somente para tokens válidos.

class GerarToken(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            user = User.objects.get(username=username)
            if not user.check_password(password):
                return Response({'error': 'Credenciais inválidas'}, status=status.HTTP_401_UNAUTHORIZED)

            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        except User.DoesNotExist:
            return Response({'error': 'Usuário não encontrado'}, status=status.HTTP_404_NOT_FOUND)
        

class ValidarToken(APIView):
    def get(self, request):
        token = request.headers.get('Authorization')  

        if not token:
            return Response({'error': 'Token não fornecido'}, status=status.HTTP_400_BAD_REQUEST)
        token = token.replace('Bearer ', '')

        try:
            decoded_token = jwt.decode(token, settings.JWT_SIGNING_KEY, algorithms=['HS256'])
            return Response({'valid': True, 'payload': decoded_token})         #Em caso de token válido, retorna verdadeiro para valid.
        except ExpiredSignatureError:                                          #Respostas para token inválido e expirado
            return Response({'error': 'Token expirado'}, status=status.HTTP_401_UNAUTHORIZED)
        except InvalidTokenError:
            return Response({'error': 'Token inválido'}, status=status.HTTP_401_UNAUTHORIZED)