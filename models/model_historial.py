from odoo import models, fields, api
from odoo.exceptions import ValidationError

from datetime import datetime, timedelta

class historial(models.Model):
  _name = "coop.historial"
  _description = "Historial del socio"
  
  fecha_muestreo = fields.Date()
  socio_id = fields.Many2one('res.partner', string="Socio Propietario", required = True)
  
  cant_suri = fields.Integer(string="Suri")
  cant_huacaya = fields.Integer(string="Huacaya")

  cant_macho_adulto = fields.Integer(string="Machos adultos")
  cant_hembra_adulto = fields.Integer(string="Hembras adultas")

  cant_hembra = fields.Integer(string="Hembras total")

  cant_tui_macho = fields.Integer(string="Tuis machos")
  cant_tui_hembra = fields.Integer(string="Tuis hembras")
  
  cant_menores = fields.Integer(string="Menores")
  
  total_camelidos = fields.Integer(string="Total camélidos")

