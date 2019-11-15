from rest_framework.generics import ListAPIView, CreateAPIView, \
    RetrieveUpdateAPIView
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import UserProfileSerializer

from .models import UserProfile


class UserProfileList(ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('id', 'user_type')


class UserProfileRetrieveUpdate(RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    lookup_field = "id"
    serializer_class = UserProfileSerializer