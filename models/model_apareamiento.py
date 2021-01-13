from odoo import models, fields, api
from odoo.exceptions import ValidationError

from datetime import datetime, timedelta

class apareamiento(models.Model):
  _name = "coop.apareamiento"
  _description = "Apareamiento del camelido"

  camelido_id = fields.Many2one('coop.camelido', string="Camelido 1")
  camelido_id2 = fields.Many2one('coop.camelido', string="Camelido 2")

  fecha = fields.Date(string="Fecha")
  duracion = fields.Integer(string="Duración (min)")
