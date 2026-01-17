from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password, make_password
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from .models import Usuario, UserActivity
from .serializers import UsuarioSerializer, LoginSerializer, UserActivitySerializer, ProfesorSerializer
from .permissions import IsAdminCOrAdminP
from .signals import registrar_actividad_manual

# -----------------------------
# LOGIN
# -----------------------------
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """
    Endpoint de login. Devuelve access + refresh token y datos del usuario.
    """
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        correo = serializer.validated_data['correo']
        password = serializer.validated_data['password']

        try:
            usuario = Usuario.objects.get(correo=correo)

            if not usuario.estado:
                return Response({'error': 'Usuario desactivado'}, status=status.HTTP_403_FORBIDDEN)

            if check_password(password, usuario.password):
                refresh = RefreshToken.for_user(usuario)
                refresh['rol'] = usuario.rol  # Info extra

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


# -----------------------------
# CRUD + Gestión de Usuarios
# -----------------------------
class UsuarioViewSet(viewsets.ModelViewSet):
    """
    CRUD de usuarios con:
    - Activar / desactivar
    - Cambiar rol
    - Registro de actividad
    """
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    # Permisos dinámicos según acción
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        # Crear, actualizar, borrar solo AdminC/AdminP
        return [IsAdminCOrAdminP()]

    # -----------------------------
    # ACTIVAR USUARIO
    # -----------------------------
    @action(detail=True, methods=['post'])
    def activar(self, request, pk=None):
        usuario = self.get_object()
        usuario.estado = True
        usuario._skip_update_log = True  # Evita duplicar log en post_save
        usuario.save()

        registrar_actividad_manual(usuario, "Activó al usuario", request.user)
        return Response({'status': 'Usuario activado'}, status=status.HTTP_200_OK)

    # -----------------------------
    # DESACTIVAR USUARIO
    # -----------------------------
    @action(detail=True, methods=['post'])
    def desactivar(self, request, pk=None):
        usuario = self.get_object()
        usuario.estado = False
        usuario._skip_update_log = True
        usuario.save()

        registrar_actividad_manual(usuario, "Desactivó al usuario", request.user)
        return Response({'status': 'Usuario desactivado'}, status=status.HTTP_200_OK)

    # -----------------------------
    # CAMBIAR ROL
    # -----------------------------
    @action(detail=True, methods=['post'])
    def cambiar_rol(self, request, pk=None):
        usuario = self.get_object()
        nuevo_rol = request.data.get('rol')
        if nuevo_rol not in [r[0] for r in Usuario.ROLES]:
            return Response({'error': 'Rol inválido'}, status=status.HTTP_400_BAD_REQUEST)

        usuario.rol = nuevo_rol
        usuario._skip_update_log = True
        usuario.save()

        registrar_actividad_manual(usuario, f"Cambió rol a {nuevo_rol}", request.user)
        return Response({'status': f'Rol cambiado a {nuevo_rol}'}, status=status.HTTP_200_OK)

    # -----------------------------
    # SOBRESCRIBIR CREATE Y UPDATE PARA HASHEAR PASSWORD
    # -----------------------------
    def perform_create(self, serializer):
        password = serializer.validated_data.get('password')
        serializer.save(password=make_password(password))

    def perform_update(self, serializer):
        password = serializer.validated_data.get('password', None)
        instance = serializer.save()
        if password:
            instance.password = make_password(password)
            instance.save()

class UserActivityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UserActivity.objects.all().order_by('-timestamp')
    serializer_class = UserActivitySerializer
    permission_classes = [IsAdminCOrAdminP]

class ProfesorListView(ListAPIView):
    serializer_class = ProfesorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Usuario.objects.filter(rol='profesor', estado=True)