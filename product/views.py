import os, sys
import json

import logging


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

    context = {'page':'result', 'product_lst':[]}

    # Get most popular product according to query

    ## Get from local db
    product_targeted_mdl = search_product(user_query)

    ## Get from remote source db
    if not product_targeted_mdl:

        logger.info('User query: {} not in local db'.format(user_query), exc_info=True, extra={
            # Optionally pass a request and we'll grab any information we can
            'request': request,
            })

        r_json = products.search(user_query, locale='fr')
        if r_json['products']:
            product_dct = r_json['products'][0]

            # Get product data
            product_data_dct = products.extract_data(product_dct)

            # Update or insert product into db
            product_targeted_mdl = set_product_model(product_data_dct)

    if product_targeted_mdl:

        if request.user.is_authenticated:
            # Save searched product according to authenticated user
            request.user.searches.add(product_targeted_mdl)

            # Get user's favorite product
            favorite_product_mdl_lst = request.user.favorites.all()
            context['favorite_lst'] = favorite_product_mdl_lst

        # alternative_product_lst = products.nutrition(product_data_dct, 7)
        # for alternative_data_dct in alternative_product_lst:
        #     product_targeted_mdl.alternatives.add( set_product_model(alternative_data_dct) )
        alternative_product_lst = get_alternative_product(product_targeted_mdl.code, 12, 3)
        for alternative_mdl in alternative_product_lst:
            product_targeted_mdl.alternatives.add(alternative_mdl)

        context['product_lst'] = product_targeted_mdl.alternatives.all().order_by('nutrition_grades', 'nova_group', '-unique_scans_n')

    else:
        logger.info('User query: {} not found'.format(user_query), exc_info=True, extra={
            # Optionally pass a request and we'll grab any information we can
            'request': request,
            })

    #     product_data_dct = {}
    #     alternative_product_lst = []

    context['query'] = user_query
    context['product_target'] = product_targeted_mdl
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


def search_product(query):

        # Parse user query

        ## delete stop word
        print('> User Query:', query)

        word_lst = query.split()
        # print(word_lst)


        # Search targeted product

        ## Get all products
        product_lst_db = ZProduct.objects.all()
        # print_product_list(product_lst_db)

        targeted_product_lst_db = ZProduct.objects.none()

        for idx, word in enumerate(word_lst):
            print(idx, '-', word)
    
            ## Filter product by brand and name
            filtered_product_lst_db = ZProduct.objects.none()
            
            filtered_product_lst_db = filtered_product_lst_db.union(product_lst_db.filter(brands__icontains=word))
            # print_product_list(filtered_product_lst_db)

            filtered_product_lst_db = filtered_product_lst_db.union(product_lst_db.filter(name__icontains=word))
            # print_product_list(filtered_product_lst_db)
            
            ## Get targeted product
            if not targeted_product_lst_db:
                targeted_product_lst_db = (filtered_product_lst_db)
            else:
                targeted_product_lst_db = targeted_product_lst_db.intersection(filtered_product_lst_db)

            print('targeted product list')
            print_product_list(targeted_product_lst_db)


        # Targeted product is the most popular
        # print_product_list(targeted_product_lst_db.order_by('-unique_scans_n'))
        targeted_product_db = targeted_product_lst_db.order_by('-unique_scans_n').first()
        if targeted_product_db:
            print('TARGET:', targeted_product_db, '-', targeted_product_db.nutrition_grades, '-', targeted_product_db.nova_group, '-', targeted_product_db.unique_scans_n)
        else:
            print('NO TARGET FOUND')


        return targeted_product_db


def get_alternative_product(product_code, n_product_max=12, n_best_product_max=7):

    final_alternative_mdl_lst = ZProduct.objects.none()


    # Get all products sharing the categories of the targeted product

    relation_mdl_lst = ZCategory_Product.objects.filter(product__code=product_code)

    if relation_mdl_lst:

        ## Get each category
    
        # for idx, relation_mdl in enumerate(relation_mdl_lst.order_by('hierarchy_index')):
        flag = True
        is_complete = False
        category_idx = 0
        n_best_product_max = 7
        alternative_mdl_lst = ZProduct.objects.none()
        relation_mdl_it = iter(relation_mdl_lst.order_by('hierarchy_index'))

        while not is_complete and flag == True: 
            
            try:
                relation_mdl = next(relation_mdl_it)

                print('CATEGORY', category_idx, relation_mdl.category.identifier, relation_mdl.hierarchy_index)
                category_idx += 1

                ### Get products from current category
                product_mdl_lst = relation_mdl.category.products.all()
                # for index, prd_mdl in enumerate(product_mdl_lst):
                #     print('PRODUCT', index, prd_mdl)

                ### Concatenate products
                if product_mdl_lst:
    
                    # print('PRE ALTERNATIVE:', alternative_mdl_lst)
                    # print('UNION:', alternative_mdl_lst.union(product_mdl_lst))
                    alternative_mdl_lst = alternative_mdl_lst.union(product_mdl_lst)
                    # print('ALTERNATIVE LIST:', alternative_mdl_lst)
                    for index, alternative_mdl in enumerate(alternative_mdl_lst.order_by('nutrition_grades', 'nova_group', '-unique_scans_n')):
                        print('ALTERNATIVE', index, alternative_mdl.brands, '-', alternative_mdl.name,
                                                    '-', alternative_mdl.nutrition_grades, '-', alternative_mdl.nova_group, '-', alternative_mdl.unique_scans_n)
                    ## Get the final product list
                    final_alternative_mdl_lst = alternative_mdl_lst.order_by('nutrition_grades', 'nova_group', '-unique_scans_n')[:n_product_max]
                    # print('FINAL ALTERNATIVE LIST:', final_alternative_mdl_lst)
                    for index, alternative_mdl in enumerate(final_alternative_mdl_lst):
                        print('FINAL ALTERNATIVE:', index, alternative_mdl.brands, '-', alternative_mdl.name,
                                                '-', alternative_mdl.nutrition_grades, '-', alternative_mdl.nova_group, '-', alternative_mdl.unique_scans_n)
                    
                    ## Stop loop if maximal best product amount is reached
                    if len(final_alternative_mdl_lst) >= n_best_product_max:
                        if final_alternative_mdl_lst[n_best_product_max-1].nutrition_grades == 'a':
                            flag = False

                else:
                    print('NO PRODUCT IN CATEGORY:', relation_mdl.category.identifier)

            except StopIteration:
                is_complete = True

    return final_alternative_mdl_lst




def print_product_list(zlist):
    for idx, product_db in enumerate(zlist):
        print(idx, '-', product_db.brands, '-', product_db.name, '-', product_db.unique_scans_n)


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