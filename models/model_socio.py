# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import json
from datetime import datetime, timedelta
import os

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

import numpy as np
import base64
from io import BytesIO


class socio(models.Model):

  _inherit = "res.partner"

  ## SQL constrain for DNI
  #_sql_constraints = [
  #  ('DNI_unico', 'unique (dni)', 'Ya existe un socio con ese número de DNI.')
  #]


  # Constrains for DNI
  @api.constrains('dni')
  def check_dni(self):
    for rec in self:
      if len(rec.dni) < 8:
        raise ValidationError('El campo DNI debe tener 8 digitos.')
      if not rec.dni.isnumeric():
        raise ValidationError('El campo DNI solo debe contener números.')



  ## Computed fields: records for cabana, parcela, potrero and camelido
  @api.one
  @api.depends('cabanas.parcelas.potreros.camelidos.socio_id')
  def contar_camelidos(self):
    self.num_fichas_camelidos = self.env["coop.camelido"].search_count([('socio_id', '=', self.id)])

  @api.one
  @api.depends('cabanas.socio_id')
  def contar_cabanas(self):
    if self.cabanas is not False:
      self.num_cabanas = self.env["coop.cabana"].search_count([('socio_id', '=', self.id)])

  @api.one
  @api.depends('cabanas.parcelas.socio_id')
  def contar_parcelas(self):
    self.num_parcelas = self.env["coop.parcela"].search_count([('socio_id', '=', self.id)])


  @api.one
  @api.depends('cabanas.parcelas.potreros.socio_id')
  def contar_potreros(self):
    self.num_potreros = self.env["coop.potrero"].search_count([('socio_id', '=', self.id)])


  # Computed fields: record for camels types.
  @api.one
  @api.depends('cabanas.parcelas.potreros.camelidos.socio_id')
  def contar_huacayos(self):
    self.num_alpacas_huacayo = self.env["coop.camelido"].search_count([('socio_id', '=', self.id), ('raza', '=', 'huacayo')])

  @api.one
  @api.depends('cabanas.parcelas.potreros.camelidos.socio_id')
  def contar_suris(self):
    self.num_alpacas_suri = self.env["coop.camelido"].search_count([('socio_id', '=', self.id), ('raza', '=', 'suri')])

  @api.one
  @api.depends('cabanas.parcelas.potreros.camelidos.socio_id')
  def contar_machos(self):
    self.num_alpacas_macho = self.env["coop.camelido"].search_count([('socio_id', '=', self.id), ('sexo', '=', 'macho')])

  @api.one
  @api.depends('cabanas.parcelas.potreros.camelidos.socio_id')
  def contar_hembras(self):
    self.num_alpacas_hembra = self.env["coop.camelido"].search_count([('socio_id', '=', self.id), ('sexo', '=', 'hembra')])



  ## Computed field: Total number of sons
  @api.one
  @api.depends('num_hijos_1', 'num_hijos_2', 'num_hijos_3', 'num_hijos_4', 'num_hijos_5')
  def calc_hijos(self):
    self.num_hijos_total = self.num_hijos_1 + self.num_hijos_2 + self.num_hijos_3 + self.num_hijos_4 + self.num_hijos_5


  ## Computed field: Total number of camels
  @api.one
  @api.depends('macho_adulto_total', 'hembra_adulto_total', 'tui_macho_total', 'tui_hembra_total', 'menores_total')
  def calc_alpacas(self):
    self.alpacas_total = self.macho_adulto_total + self.hembra_adulto_total + self.tui_macho_total + self.tui_hembra_total + self.menores_total


  # Computed graph according to the fields about camels
  @api.one
  @api.depends('macho_adulto_total', 'hembra_adulto_total', 'tui_macho_total', 'tui_hembra_total', 'menores_total')
  def grafica_camelidos(self):
    #print("       Generating graphs")
    fig = plt.figure()
    buf = BytesIO()
    tags = ['Macho adulto', 'hembra adulta', 'tui macho', 'tui hembra', 'menores']
    values = [self.macho_adulto_total, self.hembra_adulto_total, self.tui_macho_total, self.tui_hembra_total, self.menores_total]
    if sum(values) == 0:
      return
    ax = fig.add_axes([0,0,1,1])
    ax.axis('equal')
    ax.pie(values, labels=tags, autopct='%1.2f%%')
    
    fig.savefig(buf, format="png")
    self.camel_graph_percentage = base64.encodestring(buf.getbuffer())



  # Function which takes a snapshot, activated by a button in the view
  def socio_registrar_muestra_camelido(self):
    t = datetime.today()
    #print("    EScribiendo datos")
    values = {
      'fecha_muestreo': t.strftime("%Y-%m-%d"),
      'socio_id': self.id,
      'cant_suri': self.suri_total,
      'cant_huacaya': self.huacaya_total,
      'cant_macho_adulto': self.macho_adulto_total,
      'cant_hembra_adulto': self.hembra_adulto_total,
      'cant_tui_macho': self.tui_macho_total,
      'cant_tui_hembra': self.tui_hembra_total,
      'cant_menores': self.menores_total,
      'total_camelidos': self.alpacas_total,
    }
    self.env['coop.historial'].create(values)
    


  ######  Fields


  es_socio = fields.Boolean(default = False, string="¿Es socio?")
  cabanas = fields.One2many('coop.cabana', 'socio_id', string="Cabañas")
  camelidos = fields.One2many('coop.camelido', 'socio_id', string="Camélidos")

  # Campos personales
  dni = fields.Char(string="DNI", size=8, required=True)
  fecha_nac = fields.Date(string="Fecha de nacimiento")
  direccion = fields.Char(string="Dirección", size=30)
  
  # Lugar de nacimiento
  distrito_nac = fields.Char(string = "Distrito")
  provincia_nac = fields.Char(string = "Provincia")
  departamento_nac = fields.Selection([
    ('Ayacucho', 'Ayacucho'),
    ('Apurimac', 'Apurimac'),
    ('Arequipa', 'Arequipa'),
    ('Cusco', 'Cusco'),
  ], default="Ayacucho", string="Departamento")

  #archive = os.getcwd() + '/addons/coop/models/dep.txt'
  
  # Importar departamentos
  #with open(archive, 'r') as dptos:
  #  data = json.load(dptos)
    
  #departamentos = [ (d['departamento'], d['departamento']) for d in data ]
  #departamento_nac = fields.Selection(departamentos, string = "Departamento")

  # Otros datos
  sexo = fields.Selection([('Masculino', 'Masculino'), ('Femenino', 'Femenino')], default="masculino", string="Sexo")
  
  estado_civil = fields.Selection([
  ('Soltero', 'Soltero'),
  ('Casado', 'Casado'),
  ('Viudo', 'Viudo'),
  ('Divorciado', 'Divorciado'),
  ], default="Soltero", string="Estado Civil")
  
  # Campo relacional al historial del socio
  historial = fields.One2many('coop.historial', 'socio_id', string="Historial")
  
  # Domicilio
  dom_permanente = fields.Char(size=30)
  dom_transitorio = fields.Char(size=30)
  
  num = [(x, str(x)) for x in range(1, 20)]
  personas_nucleo = fields.Selection(num, string="Personas nucleo familiar")
  

	## CAMPOS AGREGADOS DEBIDO AL DOCUMENTO #### 

  num = [(x, str(x)) for x in range(0, 10)]
  num_hijos_1 = fields.Selection(num, string="Hijos de 0 a 5 años")
  num_hijos_2 = fields.Selection(num, string="Hijos de 6 a 10 años")
  num_hijos_3 = fields.Selection(num, string="Hijos de 11 a 15 años")
  num_hijos_4 = fields.Selection(num, string="Hijos de 16 a 20 años")
  num_hijos_5 = fields.Selection(num, string="Hijos de 21 años a más")
  
  num_hijos_total = fields.Integer(string="Total hijos", compute="calc_hijos")
  
  
  ###################################################
  ##### CAMPOS PARA LAS ESTADISTICAS
  ###################################################  
  
  num_fichas_camelidos = fields.Integer(string="Fichas de camelidos", compute="contar_camelidos")
  num_cabanas = fields.Integer(string="Numero de cabañas", compute="contar_cabanas", store=True)
  num_parcelas = fields.Integer(string="Numero de parcelas", compute="contar_parcelas", store=True)
  num_potreros = fields.Integer(string="Numero de potreros", compute="contar_potreros", store=True)
  

#  num_alpacas_huacayo = fields.Integer(string="Alpacas Huacayo", compute="contar_huacayos", store=True)
#  num_alpacas_suri = fields.Integer(string="Alpacas Suri", compute="contar_suris", store=True)
#  num_alpacas_macho = fields.Integer(string="Alpacas Macho", compute="contar_machos", store=True)
#  num_alpacas_hembra = fields.Integer(string="Alpacas Hembra", compute="contar_hembras", store=True)
 

  # Total of camels registered to the associated
  suri_total = fields.Integer(string="Alpacas Suri")
  huacaya_total = fields.Integer(string="Alpacas Huacaya")
  macho_adulto_total = fields.Integer(string="Alpacas Macho adulto")
  hembra_adulto_total = fields.Integer(string="Alpacas Hembra adulto")
  tui_macho_total = fields.Integer(string="Tui macho")
  tui_hembra_total = fields.Integer(string="Tui hembra")
  alp_hembra_total = fields.Integer(string="Alpacas Hembra")
  menores_total = fields.Integer(string="Menores")

  alpacas_total = fields.Integer(string="Total alpacas", compute="calc_alpacas", store=True)


  # Pye image of the camels
  camel_graph_percentage = fields.Binary(compute="grafica_camelidos")


  # Capacitaciones y asistencias
  asistencias = fields.One2many('coop.asistencia', 'socio_id', string="Asistencias")
  capacitaciones = fields.One2many('coop.capacitacion', 'socio_id', string="Capacitaciones")

  # Comunidad/Asociacion
  comunidad = fields.Many2one('coop.asociacion', string="Comunidad/Asociación")