from import_export import resources
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE

class CleanModelResource(resources.ModelResource):
  def export_field(self, field, obj):
    v = super(CleanModelResource, self).export_field(field, obj)
    if type(v) == str:
      v = ILLEGAL_CHARACTERS_RE.sub('', v)
    return v
