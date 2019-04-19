from models.base_model import BaseModel
from models.user import User
import peewee as pw

class PersonalContact(BaseModel):
    user = pw.ForeignKeyField(User, backref="contacts")
    name = pw.CharField()
    relationship = pw.CharField(null=True)
    location = pw.BooleanField(null=True) # 0 = Local, 1 = Foreign
    priority = pw.IntegerField(null=True) # allow users to save up to 5 contacts & rank them by priority
    email = pw.CharField(null=True)
    phone_number = pw.CharField()
