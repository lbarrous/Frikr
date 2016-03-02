from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from photos.forms import PhotoForm
from photos.models import Photo, PUBLIC
from django.contrib.auth.decorators import login_required


def home(request):
    """
    Esta funcion devuelve el home de mi pagina
    """
    photos = Photo.objects.filter(visibility=PUBLIC).order_by('-created_at')
    context = {
        'photos_list': photos[:5]
    }
    return render(request,'photos/home.html', context)

def detail(request, pk):
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

    possible_photos = Photo.objects.filter(pk=pk) # Busca por clave primaria automaticamente con el atributo pk
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

@login_required()
def create(request):
    """
    Muestra un formulario para crear una foto y la crea si la peticion es POST
    :param request: HttpRequest
    :return: HttpResponse
    """
    success_message = ''
    if request.method == 'GET':
        form = PhotoForm()
    else:
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