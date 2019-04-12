from models.base_model import BaseModel
import peewee as pw


class User(BaseModel):
    first_name = pw.CharField()
    last_name = pw.CharField()
    
