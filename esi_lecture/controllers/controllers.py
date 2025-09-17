# -*- coding: utf-8 -*-
# from odoo import http


# class /mnt/extra-addons/esiLecture(http.Controller):
#     @http.route('//mnt/extra-addons/esi_lecture//mnt/extra-addons/esi_lecture/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('//mnt/extra-addons/esi_lecture//mnt/extra-addons/esi_lecture/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('/mnt/extra-addons/esi_lecture.listing', {
#             'root': '//mnt/extra-addons/esi_lecture//mnt/extra-addons/esi_lecture',
#             'objects': http.request.env['/mnt/extra-addons/esi_lecture./mnt/extra-addons/esi_lecture'].search([]),
#         })

#     @http.route('//mnt/extra-addons/esi_lecture//mnt/extra-addons/esi_lecture/objects/<model("/mnt/extra-addons/esi_lecture./mnt/extra-addons/esi_lecture"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('/mnt/extra-addons/esi_lecture.object', {
#             'object': obj
#         })
