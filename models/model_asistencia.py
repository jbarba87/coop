from odoo import models, fields, api
from odoo.exceptions import ValidationError

from datetime import datetime, timedelta

class asistencia(models.Model):
  _name = "coop.asistencia"
  _description = "Asistencia del tecnico"


  socio_id = fields.Many2one('res.partner', string="Socio Propietario", required = True)
  tecnico_id = fields.Many2one('hr.employee', string="Técnico", required = True)

  fecha = fields.Date(string="Fecha")

  tema = fields.Selection([
    ('tema1', 'Tema 1'),
    ('tema2', 'Tema 2'),
    ('tema3', 'Tema 3'),
  ], default="tema1", string="Tema")

  recomendacion = fields.Char(string="Recomendación")
  cumplio = fields.Boolean(string = "¿Se cumplió la recomendación?")
