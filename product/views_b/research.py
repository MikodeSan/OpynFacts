from . import *


def result(request, user_query):

    context = {"page": "result", "product_lst": []}

    # Get most popular product according to query

    ## Get from local db
    product_targeted_mdl = search_product(user_query)

    ## Get from remote source db
    if not product_targeted_mdl:

        logger.info(
            "User query: {} not in local db".format(user_query),
            exc_info=True,
            extra={
                # Optionally pass a request and we'll grab any information we can
                "request": request,
            },
        )

        product_targeted_mdl = import_product_from_source(user_query)

    if product_targeted_mdl:

        if request.user.is_authenticated:
            # Save searched product according to authenticated user
            request.user.searches.add(product_targeted_mdl)

            # Get user's favorite product
            favorite_product_mdl_lst = request.user.favorites.all()
            context["favorite_lst"] = favorite_product_mdl_lst

        # alternative_product_lst = products.nutrition(product_data_dct, 7)
        # for alternative_data_dct in alternative_product_lst:
        #     product_targeted_mdl.alternatives.add( set_product_model(alternative_data_dct) )
        alternative_product_lst = get_alternative_product(
            product_targeted_mdl.code, 12, 3
        )
        for alternative_mdl in alternative_product_lst:
            product_targeted_mdl.alternatives.add(alternative_mdl)

        context["product_lst"] = product_targeted_mdl.alternatives.all().order_by(
            "nutrition_grades", "nova_group", "-unique_scans_n"
        )

    else:
        logger.info(
            "User query: {} not found".format(user_query),
            exc_info=True,
            extra={
                # Optionally pass a request and we'll grab any information we can
                "request": request,
            },
        )

    #     product_data_dct = {}
    #     alternative_product_lst = []

    context["query"] = user_query
    context["product_target"] = product_targeted_mdl
    return render(request, "product/list.html", context)


def import_product_from_source(user_query):

    product_targeted_mdl = ZProduct.objects.none()

    r_json = products.search(user_query, locale="fr")
    if r_json["products"]:
        product_dct = r_json["products"][0]

        # Get product data
        product_data_dct = products.extract_data(product_dct)

        # Update or insert product into db
        product_targeted_mdl = set_product_model(product_data_dct)

    return product_targeted_mdl


def search_product(query):

    # Parse user query

    ## delete stop word
    print("> User Query:", query)

    word_lst = query.split()
    # print(word_lst)

    # Search targeted product

    ## Get all products
    product_lst_db = ZProduct.objects.all()
    # print_product_list(product_lst_db)

    targeted_product_lst_db = ZProduct.objects.none()

    for idx, word in enumerate(word_lst):
        print(idx, "-", word)

        ## Filter product by brand and name
        filtered_product_lst_db = ZProduct.objects.none()

        filtered_product_lst_db = filtered_product_lst_db.union(
            product_lst_db.filter(brands__icontains=word)
        )
        # print_product_list(filtered_product_lst_db)

        filtered_product_lst_db = filtered_product_lst_db.union(
            product_lst_db.filter(name__icontains=word)
        )
        # print_product_list(filtered_product_lst_db)

        ## Get targeted product
        if not targeted_product_lst_db:
            targeted_product_lst_db = filtered_product_lst_db
        else:
            targeted_product_lst_db = targeted_product_lst_db.intersection(
                filtered_product_lst_db
            )

        print("targeted product list")
        print_product_list(targeted_product_lst_db)

    # Targeted product is the most popular
    # print_product_list(targeted_product_lst_db.order_by('-unique_scans_n'))
    targeted_product_db = targeted_product_lst_db.order_by("-unique_scans_n").first()
    if targeted_product_db:
        print(
            "TARGET:",
            targeted_product_db,
            "-",
            targeted_product_db.nutrition_grades,
            "-",
            targeted_product_db.nova_group,
            "-",
            targeted_product_db.unique_scans_n,
        )
    else:
        print("NO TARGET FOUND")

    return targeted_product_db


def set_product_model(product_data_dct):
    """
    Update or insert product into database
    """

    product_targeted, created = ZProduct.objects.get_or_create(
        code=product_data_dct["code"]
    )
    print("Product created:", created, "; ", product_targeted)

    if (
        created
        or product_targeted.last_modified_t < product_data_dct["last_modified_t"]
    ):

        product_targeted.categories.clear()

        code = product_data_dct["code"]
        categories_hierarchy_lst = product_data_dct["categories_hierarchy"]
        nutrient_levels = product_data_dct["nutrient_levels"]
        image = product_data_dct["image"]
        del product_data_dct["code"]
        del product_data_dct["categories_hierarchy"]
        del product_data_dct["nutrient_levels"]
        del product_data_dct["image"]

        product_targeted, created = ZProduct.objects.update_or_create(
            defaults=product_data_dct, code=code
        )
        if created:
            # TODO: critical error
            print("/!\\ CRITICAL ERROR: PRODUCT TARGETED CREATED AGAIN /!\\")

        for idx, category_id in enumerate(categories_hierarchy_lst):

            category_mdl, created = ZCategory.objects.get_or_create(
                identifier=category_id
            )
            print(category_mdl, created)
            product_targeted.categories.add(
                category_mdl, through_defaults={"hierarchy_index": idx}
            )
            # category_mdl.products.add(product_targeted, through_defaults={'hierarchy_index': idx} )
            # relation = ZCategory_Product.objects.create(product=product_targeted, category=category_mdl, hierarchy_index=idx)
            # relation.save()

        product_data_dct["code"] = code
        product_data_dct["categories_hierarchy"] = categories_hierarchy_lst
        product_data_dct["nutrient_levels"] = nutrient_levels
        product_data_dct["image"] = image

        # brands = product_data_dct['brands']
        # product_targeted.name = product_data_dct['name']
        # product_targeted.save()

    # categories_hierarchy
    # nutrient_levels
    # created_t
    # last_modified_t

    return product_targeted


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
        relation_mdl_it = iter(relation_mdl_lst.order_by("hierarchy_index"))

        while not is_complete and flag == True:

            try:
                relation_mdl = next(relation_mdl_it)

                print(
                    "CATEGORY",
                    category_idx,
                    relation_mdl.category.identifier,
                    relation_mdl.hierarchy_index,
                )
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
                    for index, alternative_mdl in enumerate(
                        alternative_mdl_lst.order_by(
                            "nutrition_grades", "nova_group", "-unique_scans_n"
                        )
                    ):
                        print(
                            "ALTERNATIVE",
                            index,
                            alternative_mdl.brands,
                            "-",
                            alternative_mdl.name,
                            "-",
                            alternative_mdl.nutrition_grades,
                            "-",
                            alternative_mdl.nova_group,
                            "-",
                            alternative_mdl.unique_scans_n,
                        )
                    ## Get the final product list
                    final_alternative_mdl_lst = alternative_mdl_lst.order_by(
                        "nutrition_grades", "nova_group", "-unique_scans_n"
                    )[:n_product_max]
                    # print('FINAL ALTERNATIVE LIST:', final_alternative_mdl_lst)
                    for index, alternative_mdl in enumerate(final_alternative_mdl_lst):
                        print(
                            "FINAL ALTERNATIVE:",
                            index,
                            alternative_mdl.brands,
                            "-",
                            alternative_mdl.name,
                            "-",
                            alternative_mdl.nutrition_grades,
                            "-",
                            alternative_mdl.nova_group,
                            "-",
                            alternative_mdl.unique_scans_n,
                        )

                    ## Stop loop if maximal best product amount is reached
                    if len(final_alternative_mdl_lst) >= n_best_product_max:
                        if (
                            final_alternative_mdl_lst[
                                n_best_product_max - 1
                            ].nutrition_grades
                            == "a"
                        ):
                            flag = False

                else:
                    print("NO PRODUCT IN CATEGORY:", relation_mdl.category.identifier)

            except StopIteration:
                is_complete = True

    return final_alternative_mdl_lst
