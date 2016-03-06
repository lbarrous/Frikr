from photos.models import Photo
from photos.serializers import PhotoSerializer, PhotoListerializer
from photos.views import PhotosQueryset
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet


class PhotoViewSet(PhotosQueryset, ModelViewSet):

    queryset = Photo.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)

    search_fields = ('name', 'description', 'owner__first_name')
    ordering_fields = ('name', 'owner')
    filter_backends = (SearchFilter, OrderingFilter)

    def get_queryset(self):
        return self.get_photos_queryset(self.request)

    def get_serializer_class(self):
        if self.action == 'list':
            return PhotoListerializer
        else:
            return PhotoSerializer

    def perform_create(self, serializer):
        """
        Asigna automaticamente la autoria de la nueva foto al usuario autenticado
        :param serializer:
        :return:
        """
        serializer.save(owner=self.request.user)

"""class PhotoListAPI(PhotosQueryset, ListCreateAPIView):

    queryset = Photo.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        return PhotoSerializer if self.request.method == "POST" else PhotoListerializer

    def get_queryset(self):
        return self.get_photos_queryset(self.request)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)



class PhotoDetailAPI(PhotosQueryset, RetrieveUpdateDestroyAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        return self.get_photos_queryset(self.request)
"""