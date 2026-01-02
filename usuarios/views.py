from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from .models import Usuario
from .serializers import UsuarioSerializer, LoginSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        correo = serializer.validated_data['correo']
        password = serializer.validated_data['password']
        
        try:
            usuario = Usuario.objects.get(correo=correo)
            if check_password(password, usuario.password):
                refresh = RefreshToken()
                refresh['id_usuario'] = usuario.id_usuario
                refresh['rol'] = usuario.rol
                
                return Response({
                    'token': str(refresh.access_token),
                    'refresh': str(refresh),
                    'usuario': UsuarioSerializer(usuario).data
                })
            else:
                return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)
        except Usuario.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
