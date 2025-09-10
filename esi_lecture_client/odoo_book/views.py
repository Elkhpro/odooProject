import xmlrpc.client

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.conf import settings
import xml_rpc


class BookView:
    uid = False
    context = {}
    password = ''

    @staticmethod
    def index(request):
        try:
            with open(settings.BASE_DIR / '.env') as f:
                login, password = f.readline().split(',')
                BookView.password = password
            BookView.uid = xml_rpc.connect(login, password)
            if not BookView.uid:
                BookView.context = {}
                messages.error(request, "Veuillez vous connecter pour voir vos livres.")

            books = xml_rpc.get_books(BookView.uid, BookView.password)
            search_query = request.GET.get('search', '').lower()

            if search_query:  # Vérifiez si une chaîne de recherche est présente
                filtered_books = [book for book in books if search_query in  book['name'].lower()]
                sorted_books = sorted(filtered_books, key=lambda x: (-x.get('like_count', 0), x.get('name', '').lower()))   
                BookView.context = {'books': sorted_books}
            else:
                filtered_books = books  # Si aucune recherche n'est effectuée, retournez tous les livres 
                BookView.context = {'books': filtered_books} 

        except FileNotFoundError:
            BookView.context = {}
            messages.error(request, "Veuillez d'abord vous connecter.")
        except ConnectionError:
            BookView.context = {}
            messages.error(request, "Assurez-vous que le serveur Odoo est fonctionne")

        return render(request, 'odoo_book/index.html', BookView.context)


    @staticmethod
    def addLike(request, book_id):  
        try:
            xml_rpc.add_like(BookView.uid, BookView.password, book_id)
        except xmlrpc.client.Fault as e:
            BookView.context = {}   
        except FileNotFoundError:
            BookView.context = {}
            messages.error(request, "Veuillez d'abord vous connecter.")
        except ConnectionError:
            BookView.context = {}
            messages.error(request, "Assurez-vous que le serveur Odoo est fonctionne")

        #return render(request, 'odoo_book/index.html', BookView.context)   
        return HttpResponseRedirect(reverse('odoo_book:index'))        
