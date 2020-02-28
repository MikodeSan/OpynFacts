from django.http import HttpResponse

# from .models import ALBUMS

def index(request):
    message = "This is the home page"
    return HttpResponse(message)

def result(request):
    message = "This is the result page"
    return HttpResponse(message)

def favorite(request):
    message = "This is the favorite page"
    return HttpResponse(message)

def account(request):
    message = "This is the account page"
    return HttpResponse(message)

def product(request, _product_id):
    product_id = int(_product_id) # make sure we have an integer.
    message = "This is the product #{} description page".format(product_id)
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