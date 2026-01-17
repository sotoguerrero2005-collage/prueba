from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UsuarioViewSet, login, UserActivityViewSet, ProfesorListView

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'actividades', UserActivityViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', login, name='login'),
    path('profesores/', ProfesorListView.as_view(), name='profesores'),

]
