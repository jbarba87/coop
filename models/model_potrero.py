# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

from datetime import datetime, timedelta

class potrero(models.Model):
  _name = "coop.potrero"
  _description = "Potrero"
  _inherit = ['mail.thread', 'mail.activity.mixin'] # for Chatter
  _rec_name = "nombre_potrero"

  ### Constrains
  @api.constrains('area', 'area_pasto_natural', 'area_pasto_cultivado', 'area_bofedales', 'area_ereazeos', 'otros')
  def check_area(self):
    if self.area < 0.0 or self.area_pasto_natural < 0.0 or self.area_pasto_cultivado < 0.0 or self.area_bofedales < 0.0 or self.area_ereazeos < 0.0 or self.otros < 0.0:
      raise ValidationError('El área no puede ser negativa.')


  # Funcion que cuenta la cantidad de camelidos del potrero
  @api.one
  @api.depends('camelidos')
  def count_camelidos(self):
    if self.camelidos is not False:
      self.num_camelidos = self.env["coop.camelido"].search_count([('potrero_id', '=', self.id)])


  # Functions to get the associated data
  @api.one
  @api.depends('parcela_id')
  def get_socio(self):
    print("    hola desde get socios potreros")
    if self.parcela_id is not False:
      socio = self.parcela_id.cabana_id.socio_id
      self.nombre_socio = socio.name

  @api.one
  @api.depends('parcela_id')
  def get_socio_id(self):
    if self.parcela_id is not False:
      socio = self.parcela_id.cabana_id.socio_id
      self.socio_id = socio.id



  # Functions to get the type of camels
  
  @api.one
  @api.depends('camelidos.potrero_id')
  def calc_huacaya(self):
    self.huacaya = self.env['coop.camelido'].search_count([('potrero_id', '=', self.id), ('raza', '=', 'huacaya')])

  @api.one
  @api.depends('camelidos.potrero_id')
  def calc_suri(self):
    self.suri = self.env['coop.camelido'].search_count([('potrero_id', '=', self.id), ('raza', '=', 'suri')])

  # Funcion que cuenta las alpacas por genero
  @api.one
  @api.depends('huacaya', 'suri')
  def calc_total_alpacas_raza(self):
    self.total_alpacas_raza = self.huacaya + self.suri




  
  ###### DATOS DE LOS CAMELIDOS #############

  # Function to calculate female camel
  @api.one
  @api.depends('tui_hembra', 'alp_hembra_adulto')
  def calc_hembra(self):
    self.alp_hembra = self.tui_hembra + self.alp_hembra_adulto

  # Function to calculate total camels by race
  @api.one
  @api.depends('huacaya', 'suri')
  def calc_alp_raza(self):
    self.total_alpacas_raza = self.huacaya + self.suri


  # Functions wich calculate camels by gender and age  
  @api.one
  @api.depends('camelidos.potrero_id')
  def calc_alp_macho_adulto(self):
    self.alp_macho_adulto = self.env['coop.camelido'].search_count([('potrero_id', '=', self.id), ('edad', '>=', 2), ('sexo', '=', 'macho')])

  @api.one
  @api.depends('camelidos.potrero_id')
  def calc_alp_hembra_adulto(self):
    self.alp_hembra_adulto = self.env['coop.camelido'].search_count([('potrero_id', '=', self.id), ('edad', '>=', 2), ('sexo', '=', 'hembra')])

  @api.one
  @api.depends('camelidos.potrero_id')
  def calc_tui_macho(self):
    self.tui_macho = self.env['coop.camelido'].search_count([('potrero_id', '=', self.id), ('edad', '=', 1), ('sexo', '=', 'macho')])

  @api.one
  @api.depends('camelidos.potrero_id')
  def calc_tui_hembra(self):
    self.tui_hembra = self.env['coop.camelido'].search_count([('potrero_id', '=', self.id), ('edad', '=', 1), ('sexo', '=', 'hembra')])

  @api.one
  @api.depends('camelidos.potrero_id')
  def calc_menores(self):
    self.menores = self.env['coop.camelido'].search_count([('potrero_id', '=', self.id), ('edad', '=', 0)])

  # Total of camels
  @api.one
  @api.depends('alp_hembra_adulto', 'alp_macho_adulto', 'tui_macho', 'tui_hembra', 'menores')
  def calc_alp_genero(self):
    self.total_alpacas_gen = self.alp_hembra_adulto + self.alp_macho_adulto + self.tui_macho + self.tui_hembra + self.menores


  ### Saca per year
  @api.one
  @api.depends('saca')
  def calc_saca(self):
    if self.total_alpacas_gen != 0:
      self.porc_saca = (self.saca/self.total_alpacas_gen)*100.0
    else:
      self.porc_saca = 0.0

  huacaya = fields.Integer(string="Alpacas Huacaya", compute="calc_huacaya", track_visibility="always")
  suri = fields.Integer(string="Alpacas Suri", compute="calc_suri", track_visibility="always")
 
 
 
#  total_alpacas_raza = fields.Integer(string="Total alpacas", compute="calc_total_alpacas_raza", store=True)
 

  ####Fields


  nombre_potrero = fields.Char(string="Nombre del potrero", required = True)
  area = fields.Float(string="Area del potrero (Ha)")
  material = fields.Selection([
    ('madera', 'Madera'),
    ('estera', 'Estera'),
    ('otros', 'otros'),
  ], default="madera", string="Material del potrero", track_visibility="always") 

  area_pasto_natural = fields.Float(string="Area de pastos naturales (Ha)", track_visibility="always")

  
  # Pasto cultivado
  area_pasto_cultivado = fields.Float(string="Area de pastos cultivados (Ha)")
  tipo_pasto_cultivado = fields.Selection([
    ('tipo 1', 'Tipo 1'),
    ('tipo 2', 'Tipo 2'),
    ('tipo 3', 'Tipo 3'),
  ], default="tipo 1", string="Tipo de pasto cultivado")
  
  # Año de instalacion
  anho_actual = datetime.today().year
  anhos = [(x, str(x)) for x in range(1990, anho_actual + 1)] 
  
  ahno_instalacion = fields.Selection( anhos, default="1990", string="Año de instalacion")
  
  riegos = [(x, str(x)) for x in range(0, 11)]
  riego_semana = fields.Selection(riegos, default='0', string="Nº riegos por semana")

  tipo_riego = fields.Selection([
    ('aspersion', 'Aspersion'),
    ('graverdad', 'Gravedad'),
    ('otros', 'otros'),
  ], default="aspersion", string="Tipo de riego")


  cortes = [(x, str(x)) for x in range(0, 100)]
  num_corte = fields.Selection(cortes, default='0', string="Nº corte o pastoreo/año")
  
  #Rendimiento
  peso_x_m2 = fields.Float(string="Peso por m2 (kg)")
  densidad = fields.Float(string="Densidad (g/cm3)")
  longitud = fields.Float(string="Longitud (m)")
  
  # Fuente de agua
  fuente_agua = fields.Selection([
    ('Manantial/Ojo de agua', 'Manantial/Ojo de agua'),
    ('Acequia', 'Acequia'),
    ('Rio', 'Rio'),
    ('Subterraneo', 'Subterraneo'),
    ('otros', 'otros'),
  ], string="Fuente de agua")

  
  # Aforo de agua
  aforo_agua = fields.Float("Aforo de agua")
  epoca_lluvia = fields.Float("Epoca de lluvia L/s")
  epoca_estiage = fields.Float("Epoca de estiage L/s")
  
  observaciones = fields.Text("Observaciones")
  
  area_bofedales = fields.Float("Area de bofedales totales (Ha)")
  area_ereazeos = fields.Float("Area de zonas ereazeos totales (Ha)")
  otros = fields.Float("Otros")

  # Campos relacionales
  parcela_id = fields.Many2one('coop.parcela', string="Parcela", required=True)
  
  camelidos = fields.One2many('coop.camelido', 'potrero_id', string="Camelidos")
  potrero_historial = fields.One2many('coop.potrerohist', 'potrero_id', string="Historial")
  

  # Datos del socio
  nombre_socio = fields.Char(string="Socio", compute="get_socio")
  socio_id = fields.Integer(compute="get_socio_id", store=True)
   
  # Computed fields
  num_camelidos = fields.Integer(string="Cantidad camelidos", compute="count_camelidos", store=True)
  
  
  alp_macho_adulto = fields.Integer(string="Alpacas macho adulto", compute="calc_alp_macho_adulto", track_visibility="always")
  alp_hembra_adulto = fields.Integer(string="Alpacas hembra adulto", compute="calc_alp_hembra_adulto", track_visibility="always")
  
  tui_macho = fields.Integer(string="Tui Macho", compute="calc_tui_macho", track_visibility="always")
  tui_hembra = fields.Integer(string="Tui Hembra", compute="calc_tui_hembra", track_visibility="always")

  alp_hembra = fields.Integer(string="Alpacas hembra", compute="calc_hembra", store=True)

  menores = fields.Integer(string="Menores", compute="calc_menores", track_visibility="always")

  total_alpacas_gen =fields.Integer(string="Total alpacas", compute="calc_alp_genero")


  saca = fields.Integer(string="Saca Anual")
  porc_saca = fields.Float(string="% Saca", compute="calc_saca", store=True)
