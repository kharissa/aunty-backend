from models.base_model import BaseModel
from models.subcategory import Subcategory
import peewee as pw

class Pin(BaseModel):
    name = pw.CharField(max_length=255)
    description = pw.CharField(max_length=1000, null=True)
    longitude = pw.FloatField(10,6)
    latitude = pw.FloatField(10,6)
    category = pw.BooleanField() # safe = True, dangerous = False
    subcategory_id = pw.ForeignKeyField(Subcategory, backref="subcategories")
    source = pw.CharField()
    radius = pw.IntegerField()
    address = pw.CharField(null=True)

