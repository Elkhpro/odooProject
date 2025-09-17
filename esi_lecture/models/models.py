from odoo import models, fields, api
from datetime import date

class Book(models.Model):
    _name = 'esi_lecture.book'
    _description = 'Book Model'

    name = fields.Char(string="Title", required=True, unique=True)
    description = fields.Text(string="Description")
    cover_image = fields.Image(string="Cover Image")
    publication_date = fields.Date(string="Publication Date", default=date.today())
    num_pages = fields.Integer(string="Number of Pages", required=True, default=1)
    authors = fields.Many2many('res.partner', string='Authors')    

    _sql_constraints = [
        ('name_unique',
         'UNIQUE(name)',
         "A book with this title already exists. The title must be unique!"),
    ]

    
    liked_by_users = fields.Many2many('res.users', string="Liked By")
    like_count = fields.Integer(string="Like Count", compute='_compute_like_count')
    is_liked_by_current_user = fields.Boolean( compute='_compute_is_liked_by_current_user')

    products = fields.Many2many('product.template', string='Products')

    @api.constrains('publication_date')
    def _check_publication_date(self):
        for book in self:
            if book.publication_date and book.publication_date > date.today():
                raise models.ValidationError("Publication date must be less than today")

    # Nouvelle méthode pour vérifier si l'utilisateur actuel a aimé le livre
    @api.depends('liked_by_users')
    def _compute_like_count(self):
        for book in self:
            book.like_count = len(book.liked_by_users)

    @api.depends('liked_by_users')
    def _compute_is_liked_by_current_user(self):
        for book in self:
            book.is_liked_by_current_user = self.env.user in book.liked_by_users

    @api.model
    def toggle_like(self, book_id):
        book = self.browse(book_id)
        if self.env.user in book.liked_by_users:
            book.liked_by_users -= self.env.user
        else:
            book.liked_by_users |= self.env.user

    @api.constrains('num_pages')
    def _check_num_pages(self):
        for book in self:
            if book.num_pages <= 0:
                raise models.ValidationError("Number of pages must be strictly greater than 0.")

class Author(models.Model):
    _inherit = 'res.partner'
    
    books = fields.Many2many('esi_lecture.book', string='Books')


class BookProduct(models.Model):
    _inherit= 'product.template'    

    books = fields.Many2many('esi_lecture.book', string='Composés des livres')
