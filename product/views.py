import os, sys
import json

import logging


from django.http import (
    HttpResponse,
    HttpResponseRedirect,
    HttpResponsePermanentRedirect,
)
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

from .models import ZProduct, ZCategory, ZSearch, ZCategory_Product
from .forms import QueryForm, FavoriteForm


DIR_BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print(DIR_BASE)
sys.path.append(DIR_BASE)
from zopynfacts import products

# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


# Get an instance of a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def index(request):
    # print(ZContact.objects.all())
    # ZContact.objects.filter(name="Mike")[-1])
    # message = "This is the home page, the user is {}".format(ZContact.objects.filter(name="mike")[0])

    # album = get_object_or_404(Album, pk=album_id)
    # artists = [artist.name for artist in album.artists.all()]
    # artists_name = " ".join(artists)

    # context = {
    #     'album_title': album.title,
    #     'artists_name': artists_name,
    #     'album_id': album.id,
    #     'thumbnail': album.picture
    # }

    context = {"page": "home"}
    user_query = ""
    response = None

    if request.method == "POST":
        # POST method

        form = QueryForm(request.POST)
        context["page"] = "result"
        context["query"] = user_query
        if form.is_valid():
            # Form is correct.
            # We can proceed to booking.
            user_query = request.POST.get("query")

            # return HttpResponseRedirect(reverse('product:result', args=[user_query]))
            response = redirect("product:result", user_query=user_query)

        else:  # [TODO]: is not necessary
            # Form data doesn't match the expected format.
            # Add errors to the template.
            context["errors"] = form.errors.items()
            print("Form error")
            response = render(request, "product/list.html", context)
    else:
        # GET method.

        response = render(request, "product/index.html", context)

    return response


@login_required()  # By default, use LOGIN_URL in settings
def favorite(request):

    product_lst = request.user.favorites.order_by("name")[:]

    context = {"page": "favorite"}
    context["product_lst"] = product_lst
    context["favorite_lst"] = product_lst

    return render(request, "product/list.html", context)


def product(
    request, product_id, page_origin=None, product_id_origin=None, user_query=None
):

    if request.user.is_authenticated:
        # Get user's favorite product
        favorite_lst = request.user.favorites.all()

    try:
        product = ZProduct.objects.get(code=int(product_id))
    except ZProduct.DoesNotExist:
        message = "Unkown product id"
    else:
        message = "This is the product #{}-{} description page".format(
            product_id, product.name
        )

    return render(request, "product/product.html", locals())


def parse_favorite(request):

    context = {}

    if request.method == "POST":

        code = int(request.POST.get("code"))
        favorite = request.POST.get("favorite")
        print(type(code), code)
        print(type(favorite), favorite)

        if favorite == "true":
            favorite = True
        else:
            favorite = False

        print(code)
        print(favorite)

        # Update or create favorite product into db
        user_mdl = get_user_model().objects.get(username=request.user.username)
        print(request.user)
        print(user_mdl)
        try:
            favorite_mdl = ZProduct.objects.get(code=int(code))
        except ZProduct.DoesNotExist:
            print("CRITICAL ERROR GETINNG FAVORITE PRODUCT")
        else:
            if favorite:
                user_mdl.favorites.add(favorite_mdl)
            else:
                user_mdl.favorites.remove(favorite_mdl)
            favorite = not favorite
            print(favorite)

        print(user_mdl.favorites.all())
        context = {"code": code, "favorite": favorite}

    return HttpResponse(json.dumps(context))


def notice(request):

    return render(request, "product/notice.html", locals())


#     id = int(album_id) # make sure we have an integer.
#     album = ALBUMS[id] # get the album with its id.
#     artists = " ".join([artist['name'] for artist in album['artists']]) # grab artists name and create a string out of it.
#     message = "Le nom de l'album est {}. Il a été écrit par {}".format(album['name'], artists)
#     return HttpResponse(message)


# def search(request):
#     query = request.GET.get('query')
#     if not query:
#         message = "Aucun artiste n'est demandé"
#     else:
#         albums = [
#             album for album in ALBUMS
#             if query in " ".join(artist['name'] for artist in album['artists'])
#         ]

#         if len(albums) == 0:
#             message = "Misère de misère, nous n'avons trouvé aucun résultat !"
#         else:
#             albums = ["<li>{}</li>".format(album['name']) for album in albums]
#             message = """
#                 Nous avons trouvé les albums correspondant à votre requête ! Les voici :
#                 <ul>
#                     {}
#                 </ul>
#             """.format("</li><li>".join(albums))

#     return HttpResponse(message)
