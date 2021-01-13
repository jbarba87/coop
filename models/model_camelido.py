from odoo import models, fields, api
from odoo.exceptions import ValidationError

from datetime import datetime, timedelta

class camelido_andino(models.Model):
  _name = "coop.camelido"
  _description = "Camelido Andino"
  _inherit = ['mail.thread', 'mail.activity.mixin'] # for Chatter
  _rec_name = "identificacion"
  
  ## Constrains

  @api.constrains('peso')
  def check_peso(self):
    for rec in self:
      if self.peso > 85:
        raise ValidationError('El peso de la alpaca no debe exceder los 85 Kg.')
  
  # Compute age from birth date
  @api.one
  @api.depends('fecha_nac')
  def calcula_edad(self):
    if self.fecha_nac is not False:
      today = datetime.today()
      nac = fields.Date.from_string(self.fecha_nac)
      self.edad = today.year - nac.year - ( (today.month, today.day) < (nac.month, nac.day) )



  #### Fields according to the technical data
  
  @api.one
  @api.depends('categoria_vellon_value')
  def select_categoria_vellon(self):
    if self.categoria_vellon_value is not False:
      if self.categoria_vellon_value > 50:
        self.categoria_vellon = 'extrafina'
      if self.categoria_vellon_value < 51 and self.categoria_vellon_value > 10:
        self.categoria_vellon = 'fina'
      if self.categoria_vellon_value < 11:
        self.categoria_vellon = 'media'

 
  @api.one
  @api.depends('longitud_mecha_value')
  def select_longitud_mecha(self):
    if self.longitud_mecha_value is not False:
      if self.categoria_vellon_value > 3:
        self.longitud_mecha = 'crec_mayor'
      if self.longitud_mecha_value < 4:
        self.longitud_mecha = 'crec_menor'


  @api.one
  @api.depends('densidad_value')
  def select_densidad(self):
    if self.densidad_value is not False:
      if self.densidad_value > 2:
        self.densidad = 'alta'
      if self.densidad_value < 3:
        self.densidad = 'baja'


  @api.one
  @api.depends('rizo_value')
  def select_rizo(self):
    if self.rizo_value is not False:
      if self.rizo_value > 3:
        self.rizo_ondulacion = 'con riso'
      if self.rizo_value < 4:
        self.rizo_ondulacion = 'sin riso'

  @api.one
  @api.depends('uniformidad_value')
  def select_uniformidad(self):
    if self.uniformidad_value is not False:
      if self.uniformidad_value > 3:
        self.uniformidad = 'homogeneo'
      if self.uniformidad_value < 4:
        self.uniformidad = 'no homogeneo'


  # Functions onchange who add domain constrains using self, which limit the search to the own associated
  @api.onchange('socio_id')
  def onchange_socio(self):
    for rec in self:
      if rec.socio_id.dni is not False:
        rec.identificacion = str(rec.socio_id.dni) + '-'
      # rec and self both work properly
        return {'domain': {'potrero_id': [('socio_id', '=', rec.socio_id.id)],
        'cod_padre': [('socio_id.id', '=', self.socio_id.id), ('sexo', '=', 'macho'),('identificacion', '!=', rec.identificacion)],
        'cod_madre': [('socio_id.id', '=', rec.socio_id.id), ('sexo', '=', 'hembra'),('identificacion', '!=', rec.identificacion)],
        'cod_abuelo': [('socio_id.id', '=', rec.socio_id.id), ('sexo', '=', 'macho'),('identificacion', '!=', rec.identificacion)],
        'cod_abuela': [('socio_id.id', '=', rec.socio_id.id), ('sexo', '=', 'hembra'),('identificacion', '!=', rec.identificacion)],
        'cod_bisabuelo': [('socio_id.id', '=', rec.socio_id.id), ('sexo', '=', 'macho'),('identificacion', '!=', rec.identificacion)],
        'cod_bisabuela': [('socio_id.id', '=', rec.socio_id.id), ('sexo', '=', 'hembra'),('identificacion', '!=', rec.identificacion)],
      }}
      
  @api.onchange('sexo')
  def onchange_identificacion(self):
    for rec in self:
      #rec.identificacion = rec.socio_id.dni + '-' + rec.identificacion
      # rec and self both work properly
      return {'domain': {'potrero_id': [('socio_id', '=', self.socio_id.id)],
        'cod_padre': [('socio_id.id', '=', self.socio_id.id), ('sexo', '=', 'macho'),('identificacion', '!=', self.identificacion)],
        'cod_madre': [('socio_id.id', '=', self.socio_id.id), ('sexo', '=', 'hembra'),('identificacion', '!=', self.identificacion)],
        'cod_abuelo': [('socio_id.id', '=', self.socio_id.id), ('sexo', '=', 'macho'),('identificacion', '!=', self.identificacion)],
        'cod_abuela': [('socio_id.id', '=', self.socio_id.id), ('sexo', '=', 'hembra'),('identificacion', '!=', self.identificacion)],
        'cod_bisabuelo': [('socio_id.id', '=', self.socio_id.id), ('sexo', '=', 'macho'),('identificacion', '!=', self.identificacion)],
        'cod_bisabuela': [('socio_id.id', '=', self.socio_id.id), ('sexo', '=', 'hembra'),('identificacion', '!=', self.identificacion)],
      }}


  # Function to calculate the total score for the camel
  @api.one
  @api.depends('categoria_vellon_value', 'longitud_mecha_value', 'densidad_value', 'rizo_value' ,'uniformidad_value', 'cabeza_value', 'talla_value', 'calze_value', 'ap_general_value')
  def calc_total(self):
    self.general_value = self.categoria_vellon_value + self.longitud_mecha_value + self.densidad_value + self.rizo_value + self.uniformidad_value + self.cabeza_value + self.talla_value + self.calze_value + self.ap_general_value

  # Function to count the 
  @api.one
  @api.depends('lista_esquilas.camelido_id')
  def contar_esquilas(self):
    self.num_esquila = self.env["coop.esquila"].search_count([('camelido_id', '=', self.id)])


  #### Fields
  
  identificacion = fields.Char(string="Número", required=True, track_visibility="always")

  fecha_empadre = fields.Date(string="Fecha de empadre")
  fecha_nac = fields.Date(string="Fecha de naciomiento")
  edad = fields.Integer(string="Edad", compute="calcula_edad", store=True)
  
  # Tipo de identificacion
  tipo_identificacion = fields.Selection([
    ('Tatuaje', 'Tatuaje'),
    ('Arete', 'Arete'),
    ('Senal', 'Senal'),
    ('Otro', 'Otro'),
  ], default="Tatuaje", string="Tipo de identificación", track_visibility="always")

 
  peso = fields.Float(string="Peso (kg)", track_visibility="always")
  
  
  sexo = fields.Selection([
    ('Macho', 'Macho'),
    ('Hembra', 'Hembra'),
  ], default="Hembra", string="Género")
  
  raza = fields.Selection([
    ('Huacaya', 'Huacaya'),
    ('Suri', 'Suri'),
  ], default="Huacaya", string="Raza")
  
  color = fields.Selection([
    ('Blanco', 'Blanco'),
    ('Color', 'Color'),
  ], default="Blanco", string="Color")

  categoria = fields.Selection([
    ('categoria 1', 'Categoria 1'),
    ('categoria 2', 'Categoria 2'),
    ('categoria 3', 'Categoria 3'),
    ('categoria 4', 'Categoria 4'),
  ], string="Categoria")

  cond_adquisicion = fields.Selection([
    ('Nacimiento', 'Nacimiento'),
    ('Alquilado', 'Alquilado'),
    ('Comprado', 'Comprado'),
    ('Trueque', 'Trueque'),
    ('Prestado', 'Prestado'),
  ], string="Condición de adquisición")

  num_esquila = fields.Integer(string="Número de esquila", compute="contar_esquilas")


  #observaciones
  observaciones = fields.Text(string="Observaciones")

  # Baja del animal
  active = fields.Boolean(default=True, string='Active')
  
  baja_motivo = fields.Selection([
    ('Muerte', 'Muerte'),
    ('Transferencia', 'Transferencia'),
  ], string="Motivo")


  ## Technical data
  
  categoria_vellon = fields.Selection([
    ('extrafina', 'Extrafina < 18 u'),
    ('fina', 'Fina >= 18 <= 0 22  u'),
    ('media', 'Media >= 22 < 28 u'),
  ], string="Categoria", compute="select_categoria_vellon")
  categoria_vellon_value = fields.Selection([(x, str(x)) for x in range(0, 61)], string="Finura")
 
  longitud_mecha = fields.Selection([
    ('crec_mayor', 'Crecimiento anual > 7.5cm'),
    ('crec_menor', 'Crecimiento anual < 7.5cm'),
  ], string="Longitud de fibra", compute="select_longitud_mecha")
  longitud_mecha_value = fields.Selection([(x, str(x)) for x in range(0, 9)], string="Longitud")
  
  densidad = fields.Selection([
    ('alta', 'Alta: Vellón compacto'),
    ('baja', 'Baja: Vellón flojo'),
  ], string="Densidad", compute="select_densidad")
  densidad_value = fields.Selection([(x, str(x)) for x in range(0, 6)], string="Densidad")

  rizo_ondulacion = fields.Selection([
    ('con riso', 'Con riso'),
    ('sin riso', 'Sin riso'),
  ], string="Rizo u ondulación", compute="select_rizo")
  rizo_value = fields.Selection([(x, str(x)) for x in range(0, 9)], string="Rizo")

  uniformidad = fields.Selection([
    ('Homogeneo', 'Homogeneo'),
    ('No homogeneidad', 'No homogeneidad'),
  ], string="Uniformidad", compute="select_uniformidad")
  uniformidad_value = fields.Selection([(x, str(x)) for x in range(0, 5)], string="Uniformidad")


  # Conformacion
  cabeza_descripcion = fields.Char(string="Cabeza")
  cabeza_value = fields.Selection([(0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], default="0")
  
  talla_descripcion  = fields.Char(string="Talla")
  talla_value = fields.Selection([(0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4')], default="0")
  
  calze_descripcion  = fields.Char(string="Calce")
  calze_value = fields.Selection([(0, '0'), (1, '1'), (2, '2'), (3, '3')], default="0")
  
  ap_general_descripcion  = fields.Char(string="Apariencia General")
  ap_general_value = fields.Selection([(0, '0'), (1, '1'), (2, '2'), (3, '3')], default="0")

  defectos = fields.Char(string="Defectos")

  general_value = fields.Integer(string="Puntuación", compute="calc_total")

  #### Campos que no se donde poner
  diametro = fields.Float(string="Diámetro")
  resistencia_tenacidad = fields.Float(string="Resistencia o tenacidad")
  lustre_brillo = fields.Float(string="Lustre o brillo")
  grasa = fields.Float(string="Grasa")
  
  clasificacion_vellon = fields.Selection([
    ('baby', 'Alpaca Baby (<23um)'),
    ('fleece', 'Alpaca Fleece (23.1 a 26.5um)'),
    ('medium_fleece', 'Alpaca Medium Fleece (26.6 a 29.0um)'),
    ('huarizo', 'Alpaca Huarizo (29.1 a 31.6um)'),
    ('gruesa', 'Alpaca Gruesa (>31um)'),
    ('corta', 'Alpaca Corta'),
  ], default="baby", string="Clasificación del Vellón")
  


  # Family fields

  cod_padre = fields.Many2one('coop.camelido', string="Código del padre", domain="[('sexo', '=', 'macho'), ('identificacion', '!=', identificacion)]")
  cod_madre = fields.Many2one('coop.camelido', string="Código de la madre", domain="[('sexo', '=', 'hembra'), ('identificacion', '!=', identificacion )]")
  cod_abuelo = fields.Many2one('coop.camelido', string="Código del abuelo", domain="[('sexo', '=', 'macho'), ('identificacion', '!=', identificacion)]")
  cod_abuela = fields.Many2one('coop.camelido', string="Código de la abuela", domain="[('sexo', '=', 'hembra'), ('identificacion', '!=', identificacion )]")
  cod_bisabuelo = fields.Many2one('coop.camelido', string="Código del bisabuelo", domain="[('sexo', '=', 'macho'), ('identificacion', '!=', identificacion)]")
  cod_bisabuela = fields.Many2one('coop.camelido', string="Código de la bisabuela", domain="[('sexo', '=', 'hembra'), ('identificacion', '!=', identificacion )]")
  
  
  # obtencion del socio
  #nombre_socio = fields.Char(string="Socio", compute="get_socio")
  #socio_id = fields.Integer(string="id", compute="get_socio_id", store=True)

  socio_id = fields.Many2one('res.partner', string="Socio", track_visibility="always", required=True)
  potrero_id = fields.Many2one('coop.potrero', string="Potrero", track_visibility="always")
  
  # Esquilas
  lista_esquilas = fields.One2many('coop.esquila', 'camelido_id', string="Esquilas")

  
  # Apareamiento

#  apareamiento = fields.One2many('coop.apareamiento', 'camelido_id', string="Apareamiento")


#  @api.multi
#  def write(self, vals):
#    print("            Overriding camelido")
#    res = super(camelido_andino, self).write(vals)
#    return res
    
#  @api.model
#  def create(self, vals):
#    print("            Creando camelido")
#    res = super(camelido_andino, self).create(vals)
#    return res


