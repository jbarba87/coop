from odoo import models, fields, api
from odoo.exceptions import ValidationError

from datetime import datetime, timedelta

class potrero_hist(models.Model):
  _name = "coop.potrerohist"
  _description = "Historial del potrero"
  _inherit = ['mail.thread', 'mail.activity.mixin'] # for Chatter

  potrero_id = fields.Many2one('coop.potrero', string="Potrero")
  
  fecha = fields.Date(string="Fecha")
  area_pasto_cultivado = fields.Float(string="Area del pasto cultivado (Ha)")

  area_pasto_natural = fields.Float(string="Area del pasto natural (Ha)")
