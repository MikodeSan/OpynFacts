from django.http import HttpResponse
from django.template import loader

from .models import ZContact, ZProduct, ZCategory

def index(request):
    # print(ZContact.objects.all())
    # print()
    # ZContact.objects.filter(name="Mike")[-1])
    message = "This is the home page, the user is {}".format(ZContact.objects.filter(name="mike")[0]) 
    template = loader.get_template('product/index.html')
    return HttpResponse(template.render(request=request))

def result(request):
    contact_lst = ZContact.objects.all().order_by('-name')[:12]
    contacts_fromatted = ["<li>{}</li>".format(contact) for contact in contact_lst]
    product_lst = ZProduct.objects.all().order_by('name')[:12]
    product_formatted = ["<li>{}</li>".format(product) for product in product_lst]
    message = "This is the result page:<br>The contacts:<ul>{}</ul><br>The products:<ul>{}</ul>".format("\n".join(contacts_fromatted), "\n".join(product_formatted))
    return HttpResponse(message)

def favorite(request):
    message = "This is the favorite page"
    return HttpResponse(message)

def account(request):
    message = "This is the account page"
    return HttpResponse(message)

def product(request, _product_id):
    product_id = int(_product_id) # make sure we have an integer.
    try:
        product = ZProduct.objects.get(pk=product_id)
        s = ", ".join([contact.name for contact in product.contact.all()])
        message = "This is the product #{} description page owned by: {}".format(product_id, s)
    except:
        message = "Unkown product id"
    return HttpResponse(message)

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