# -*- coding: utf-8 -*-
# from odoo import http


# class GameStore(http.Controller):
#     @http.route('/game_store/game_store/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/game_store/game_store/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('game_store.listing', {
#             'root': '/game_store/game_store',
#             'objects': http.request.env['game_store.game_store'].search([]),
#         })

#     @http.route('/game_store/game_store/objects/<model("game_store.game_store"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('game_store.object', {
#             'object': obj
#         })
