# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

from datetime import datetime, timedelta


class asociacion(models.Model):
  _name = "coop.asociacion"
  _description = "Asociacion"
  _rec_name = "nombre_asociacion"
  
  nombre_asociacion = fields.Char(string="Nombre")
  departamento = fields.Selection([
    ('Ayacucho', 'Ayacucho'),
    ('Apurimac', 'Apurimac'),
    ('Arequipa', 'Arequipa'),
    ('Cusco', 'Cusco'),
  ], default="Ayacucho", string="Departamento")

