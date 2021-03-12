# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json
import hashlib

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
  @http.route('/socios', auth='public')
  def index(self, **kw):
    #return "Hello, world"
    socios = request.env['res.partner'].sudo().search([('es_socio', '=', True)])

    maximo = max([ socio.alpacas_total for socio in socios])
    print("       maximo", maximo)

    return http.request.render('coop.prueba', {
      'socios': socios,
      'maximo': maximo,
    })

class get_productor(http.Controller):
  @http.route('/productor/<string:dni>', auth="public")
  def index(self, **kw):
    values = dict(kw)
    dni = values['dni']

    datos = request.params
    var = list(datos.items())[0]

    dict_params = json.loads(var[0])
    usuario = dict_params['usuario']
    password = dict_params['pass']

    #print("hola desde controller")
    print(hashlib.sha256(password.encode()).hexdigest())
    if hashlib.sha256(password.encode()).hexdigest() == '03621896c4979e51e59fe3a27d58066c3923c98a355961907d7c6614a249c86d':
      socio = request.env['res.partner'].sudo().search([('es_socio', '=', True), ('dni', '=', dni)])
      if len(socio) is 0:
        return "No encontrado"
      else:
        dat = {'nombre': socio.name, 'dni':socio.dni, 'sexo':socio.sexo}
        return json.dumps(dat)
    else:
      return "No permitido"

