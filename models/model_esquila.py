from odoo import models, fields, api
from odoo.exceptions import ValidationError

from datetime import datetime, timedelta

class esquila(models.Model):
  _name = "coop.esquila"
  _description = "Esquilada de camelido"
  _inherit = ['mail.thread', 'mail.activity.mixin'] # for Chatter
#  _rec_name = "identificacion"


  @api.one
  @api.depends('camelido_id.peso')
  def estimar_produccion(self):
    if self.camelido_id.peso is not False:
      self.estimacion = 0.03*self.camelido_id.peso



  camelido_id = fields.Many2one('coop.camelido', string="Camelido")
  
  fecha = fields.Date(string="Fecha")
  produccion = fields.Float(string="Peso")


  estimacion = fields.Float(string="Estimacion", compute="estimar_produccion", store=True)

