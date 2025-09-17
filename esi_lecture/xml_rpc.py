import xmlrpc.client
import getpass

# Configuration de la connexion
url = "http://localhost:8069"  # Remplacez par l'URL de votre instance Odoo
db = "dev01"            # Remplacez par le nom de votre base de données Odoo
username = input("Entre votre username: ")  # Saisie du nom d'utilisateur
password = getpass.getpass("Enter votre password: ")  # Saisie sécurisée du mot de passe

# Connexion au service commun
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})

# Vérification de la connexion
if uid:
    print("Successfully authenticated!")
else:
    print("Authentication failed.")
    exit(1)

# Connexion au service des modèles

models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
# Boucle de recherche de livres
while True:
    book_name = input("Enter a book title to search (ou 'exit' pour quitter): ")
    if book_name.lower() == 'exit':
        break
    
    books = models.execute_kw(db, uid, password,'esi_lecture.book', 'search_read',[[['name', '=', book_name]]],{'fields': ['name', 'authors']})

    if books:
        print("Livres Trouvés:")
        for book in books:
            authors = models.execute_kw(db, uid, password,'res.partner', 'read',[book['authors']], {'fields': ['name']})
            author_names = ', '.join(author['name'] for author in authors)
            print(f"Titre: {book['name']}, Auteur: {author_names}")
    else:
        print("Aucun livre trouvé avec ce titre")
