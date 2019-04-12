from models.base_model import BaseModel
import peewee as pw


class Subcategory(BaseModel):
    category = pw.BooleanField() # safe = True, dangerous = False
    subcategory_name = pw.CharField()