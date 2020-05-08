import os, sys
import json

from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
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
    
    context = {'page': 'home'}
    user_query = ""
    response = None

    if request.method == 'POST':
        # POST method
        
        form = QueryForm(request.POST)
        context['page'] = 'result'
        context['query'] = user_query
        if form.is_valid():
            # Form is correct.
            # We can proceed to booking.
            user_query = request.POST.get('query')

            # return HttpResponseRedirect(reverse('product:result', args=[user_query]))
            response = redirect('product:result', user_query=user_query)

        else:   # [TODO]: is not necessary
            # Form data doesn't match the expected format.
            # Add errors to the template.
            context['errors'] = form.errors.items()
            print('Form error')
            response = render(request, 'product/list.html', context)
    else:
        # GET method.
        
        response = render(request, 'product/index.html', context)
    
    return response


def result(request, user_query):
    # contact_lst = ZContact.objects.all().order_by('-name')[:12]

    # Get most popular product according to query
    context = {'page':'result'}
        
    r_json = products.search(user_query, locale='fr')
    if r_json['products']:
        product_dct = r_json['products'][0]

        # Get product data
        product_data_dct = products.extract_data(product_dct)

        # Update or insert product into db
        product_targeted_mdl = set_product_model(product_data_dct)

        if request.user.is_authenticated:
            # Save searched product according to authenticated user

            request.user.searches.add(product_targeted_mdl)

            # Get user's favorite product
            favorite_product_mdl_lst = request.user.favorites.all()
            context['favorite_lst'] = favorite_product_mdl_lst

        alternative_product_lst = products.nutrition(product_data_dct, 7)
        
        for alternative_data_dct in alternative_product_lst:
            product_targeted_mdl.alternatives.add( set_product_model(alternative_data_dct) )

    else:
        product_data_dct = {}
        alternative_product_lst = []

    context['query'] = user_query
    context['product_target'] = product_targeted_mdl
    context['product_lst'] = product_targeted_mdl.alternatives.all()
    return render(request, 'product/list.html', context)


@login_required()      # By default, use LOGIN_URL in settings
def favorite(request):

    product_lst = request.user.favorites.order_by('name')[:]

    context = {'page':'favorite'}
    context['product_lst'] = product_lst
    context['favorite_lst'] = product_lst

    return render(request, 'product/list.html', context)


def product(request, product_id, page_origin=None, product_id_origin=None, user_query=None):

    if request.user.is_authenticated:
        # Get user's favorite product
        favorite_lst = request.user.favorites.all()

    try:
        product = ZProduct.objects.get(code=int(product_id))
    except ZProduct.DoesNotExist:
        message = "Unkown product id"
    else:
        message = "This is the product #{}-{} description page".format(product_id, product.name)

    return render(request, 'product/product.html', locals())


def parse_favorite(request):
    
    context = {}

    if request.method == 'POST':

        code = int(request.POST.get('code'))
        favorite = request.POST.get('favorite')
        print(type(code), code)
        print(type(favorite), favorite)

        if favorite == 'true':
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
        context = {'code' : code, 'favorite' : favorite}

    return HttpResponse( json.dumps( context ) )


def notice(request):

    return render(request, 'product/notice.html', locals())


def set_product_model(product_data_dct):
    """
    Update or insert product into database
    """

    product_targeted, created = ZProduct.objects.get_or_create(code=product_data_dct['code'])
    print("Product created:", created, "; ", product_targeted)

    if created or product_targeted.last_modified_t < product_data_dct['last_modified_t']:

        product_targeted.categories.clear()

        code = product_data_dct['code']
        categories_hierarchy_lst = product_data_dct['categories_hierarchy']
        nutrient_levels = product_data_dct['nutrient_levels']
        image = product_data_dct['image']
        del product_data_dct['code']
        del product_data_dct['categories_hierarchy']
        del product_data_dct['nutrient_levels']
        del product_data_dct['image']

        product_targeted, created = ZProduct.objects.update_or_create(defaults=product_data_dct, code=code)
        if created:
            # TODO: critical error
            print("/!\\ CRITICAL ERROR: PRODUCT TARGETED CREATED AGAIN /!\\")

        for idx, category_id in enumerate(categories_hierarchy_lst):

            category_mdl, created = ZCategory.objects.get_or_create(identifier=category_id)
            print(category_mdl, created)
            product_targeted.categories.add(category_mdl, through_defaults={'hierarchy_index': idx} )
            # category_mdl.products.add(product_targeted, through_defaults={'hierarchy_index': idx} )
            # relation = ZCategory_Product.objects.create(product=product_targeted, category=category_mdl, hierarchy_index=idx)
            # relation.save()

        product_data_dct['code'] = code
        product_data_dct['categories_hierarchy'] = categories_hierarchy_lst
        product_data_dct['nutrient_levels'] = nutrient_levels
        product_data_dct['image'] = image

        # brands = product_data_dct['brands']
        # product_targeted.name = product_data_dct['name']
        # product_targeted.save()

    # categories_hierarchy
    # nutrient_levels
    # created_t
    # last_modified_t

    return product_targeted




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