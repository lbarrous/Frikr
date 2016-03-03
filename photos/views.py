from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from photos.forms import PhotoForm
from photos.models import Photo, PUBLIC
from django.contrib.auth.decorators import login_required
from django.views.generic import View, ListView
from django.utils.decorators import method_decorator
from django.db.models import Q

"""
Implementacion de autenticacion con clase, esta clase comprueba si el usuario esta autenticado
y luego llama a la clase super para recoger el parametro request, si no, redirige a un sitio.
Las demas clases heredarian de esta y llamarian a dicho metodo antes de ejecutar los suyos para
comprobar si los usuarios estan autenticados sin necesidad de decoradores.

class OnlyAuthenticatedView(View):
    def get(self, request):
        if request.user.is_authenticated():
            return super(OnlyAuthenticatedView, self).get(request)
"""

class PhotosQueryset(object):
    def get_photos_queryset(self, request):
        if not request.user.is_authenticated(): # Si no esta autenticado
            photos = Photo.objects.filter(visibility=PUBLIC)
        elif request.user.is_superuser: #Si es admin
            photos = Photo.objects.all()
        else:
            photos = Photo.objects.filter(Q(owner=request.user) | Q(visibility=PUBLIC))
        return photos

class HomeView (View):

    def get(self, request):
        """
        Esta funcion devuelve el home de mi pagina
        """
        photos = Photo.objects.filter(visibility=PUBLIC).order_by('-created_at')
        context = {
            'photos_list': photos[:5]
        }
        return render(request,'photos/home.html', context)


class DetailView(View, PhotosQueryset):
    def get(self, request, pk):
        """
        Carga la pagina de detalle de una foto
        :param request: HttpRequest
        :param pk: id de la foto
        :return: HttpResponse
        """
        """
        Posible sintaxis de recuperacion de objeto en peticion al servidor
        try:
            photo = Photo.objects.get(pk=pk)
        except Photo.DoesNotExist:
            photo = None
        except Photo.MultipleObjects:
            photo = None
        """

        possible_photos = self.get_photos_queryset(request).filter(pk=pk).select_related('owner') # Busca por clave primaria automaticamente con el atributo pk y ademas busca con un inner join la informacion del atributo clave ajena
        # photo = (possible_photos.length == 1) ? possible_photos[0] : null; --> Pseudocodigo
        photo = possible_photos[0] if len(possible_photos) >= 1 else None

        if photo is not None:
            #Cargar plantilla de detalle
            context = {
                'photo': photo
            }
            return render(request, 'photos/detail.html', context)
        else:
            return HttpResponseNotFound('No existe la foto.') #404 not found

class CreateView(View):
    @method_decorator(login_required())
    def get(self, request):
        """
        Muestra un formulario para crear una foto
        :param request: HttpRequest
        :return: HttpResponse
        """
        form = PhotoForm()
        context = {
            'form': form,
            'success_message': ''
        }
        return render(request, 'photos/new_photo.html', context)

    @method_decorator(login_required())
    def post(self, request):
        """
        Crea la foto en base a la informacion del post
        :param request: HttpRequest
        :return: HttpResponse
        """
        success_message = ''
        photo_with_owner = Photo()
        photo_with_owner.owner = request.user # Asigno como propietario de la foto al usuario autenticado actual
        form = PhotoForm(request.POST, instance=photo_with_owner)
        if form.is_valid():
            new_photo = form.save() # Guarda el objeto y me lo devuelves
            form = PhotoForm()
            success_message = 'Foto guardada con exito!'
            success_message += '<a href="{0}">'.format(reverse('photos_detail', args=[new_photo.pk]))
            success_message += 'Ver foto'
            success_message += '</a>'
        context = {
            'form': form,
            'success_message': success_message
        }
        return render(request, 'photos/new_photo.html', context)

class PhotoListView(View, PhotosQueryset):
    def get(self, request):
        """
        Devuelve las fotos publicas si el usuario no esta autenticado
        Devuelve las fotos del usuario autenticado o las publicas de otros
        Devuelve todas las fotos si es admin
        :param request: HttpRequest
        :return: HttpResponse
        """
        context = {
            'photos': self.get_photos_queryset(request)
        }
        return render(request,'photos/photos_list.html', context)

class UserPhotosView(ListView):
    model = Photo
    template_name = 'photos/user_photos.html'

    def get_queryset(self):
        queryset = super(UserPhotosView, self).get_queryset()
        return queryset.filter(owner=self.request.user)
