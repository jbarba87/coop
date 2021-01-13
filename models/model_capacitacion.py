from odoo import models, fields, api
from odoo.exceptions import ValidationError

from datetime import datetime, timedelta

class capacitacion(models.Model):
  _name = "coop.capacitacion"
  _description = "Capacitacion del tecnico"

  socio_id = fields.Many2one('res.partner', string="Socio Propietario", required = True)
  tecnico_id = fields.Many2one('hr.employee', string="Técnico", required = True)

  fecha = fields.Date(string="Fecha")

  tema = fields.Selection([
    ('tema1', 'Tema 1'),
    ('tema2', 'Tema 2'),
    ('tema3', 'Tema 3'),
  ], default="tema1", string="Tema")

  financiacion = fields.Selection([
    ('fuente1', 'Fuente 1'),
    ('fuente2', 'Fuente 2'),
    ('fuente3', 'Fuente 3'),
  ], default="fuente1", string="Financiación")
