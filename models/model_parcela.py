# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

from datetime import datetime, timedelta

class parcela(models.Model):
  _name = "coop.parcela"
  _description = "Parcela de la cabaña"
  _rec_name = "nombre_parcela"
  
  
  # Funcion que cuenta la cantidad de potreros de la parcela
  @api.one
  @api.depends('potreros')
  def count_potreros(self):
    if self.potreros is not False:
      self.num_potreros = self.env["coop.potrero"].search_count([('parcela_id', '=', self.id)])

  # Funcion que autocompleta el campo Socio, para saber el socio dueño de la parcela
  @api.one
  @api.depends('cabana_id')
  def get_socio(self):
    if self.cabana_id is not False:
      socio = self.cabana_id.socio_id
      self.nombre_socio = socio.name

  @api.one
  @api.depends('cabana_id')
  def get_socio_id(self):
    if self.cabana_id is not False:
      socio = self.cabana_id.socio_id
      self.socio_id = socio.id


  nombre_parcela = fields.Char(string="Nombre de la parcela", required = True)
  area = fields.Float(string="Area")
    
  # condicion de tenencia de tierras (de la parcela)
  cond_tenencia_tierras = fields.Selection([
    ('Posesionario', 'Posesionario'),
    ('Propietario', 'Propietario'),
    ('Comunero', 'Comunero'),
    ('Alquilado', 'Alquilado'),
    ('otro', 'Otro'),
  ], default="posesionario", string="Condicion de tenencia de tierras")

  # Campos computados
  num_potreros = fields.Integer(string="Cantidad potreros", compute="count_potreros", store=True)
  #socio_id = fields.Char(string="Socio", compute="get_socio", store=True)
  
  # Campos relacionales

  cabana_id = fields.Many2one('coop.cabana', string="Rebaño/Cabaña", required = True)
  potreros = fields.One2many('coop.potrero', 'parcela_id', string="Potreros")


  # Datos del socio
  nombre_socio = fields.Char(string="Socio", compute="get_socio")
  socio_id = fields.Integer(compute="get_socio_id", store=True)
