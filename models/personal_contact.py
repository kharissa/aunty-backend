from models.base_model import BaseModel
from models.user import User
import peewee as pw

class PersonalContact(BaseModel):
    user_id = pw.ForeignKeyField(User, backref="contacts")
    name = pw.CharField()
    relationship = pw.CharField()
    location = pw.BooleanField() # 0 = Local, 1 = Foreign
    priority = pw.IntegerField() # allow users to save up to 5 contacts & rank them by priority
    email = pw.CharField()
    phone_number = pw.CharField()
