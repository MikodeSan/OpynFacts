from . import *

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
