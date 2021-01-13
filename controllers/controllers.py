# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
# class Coop1(http.Controller):
#     @http.route('/coop1/coop1/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/coop1/coop1/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('coop1.listing', {
#             'root': '/coop1/coop1',
#             'objects': http.request.env['coop1.coop1'].search([]),
#         })

#     @http.route('/coop1/coop1/objects/<model("coop1.coop1"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('coop1.object', {
#             'object': obj
#         })

class Coop(http.Controller):
  @http.route('/socios', auth='user')
  def index(self, **kw):
    #return "Hello, world"
    socios = request.env['res.partner'].sudo().search([('es_socio', '=', True)])

    maximo = max([ socio.alpacas_total for socio in socios])
    print("       maximo", maximo)

    return http.request.render('coop.prueba', {
      'socios': socios,
      'maximo': maximo,
    })
