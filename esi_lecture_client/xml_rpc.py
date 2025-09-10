import xmlrpc.client
import itertools

PORT = 8069
URL = f"http://localhost:{PORT}"
DB = "dev01"
COMMON = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common')
MODELS = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')


def connect(login, password):
    return COMMON.authenticate(DB, login, password, {})


def db_interact(uid, password, table, mode, fields=None):
    return MODELS.execute_kw(
        DB, uid, password, table, mode, [],
        {'fields': fields})



def get_books(uid, password):
    books = db_interact(uid, password, 'esi_lecture.book', 'search_read', ['id','name','authors','num_pages',
                'like_count','publication_date','cover_image','description','is_liked_by_current_user'])
    
    for book in books:
        authors_ids = book.get('authors', [])
        authors_names = MODELS.execute_kw(DB, uid, password, 'res.partner', 'name_get', [authors_ids])
        book['authors'] = ', '.join([name for _, name in authors_names])

    return books


def add_like(uid, password, book_id):
   return MODELS.execute_kw(DB, uid, password, 'esi_lecture.book','toggle_like', [book_id])
    #return db_interact(uid, password, 'esi_lecture.book', 'toggle_like', [[book_id]])
    
    

