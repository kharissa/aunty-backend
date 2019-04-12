from models.base_model import BaseModel
from models.user import User
import peewee as pw

class UserContact(BaseModel):
    user_id = pw.ForeignKeyField(User, backref="contacts")
    contact_name = pw.CharField()
    contact_type = pw.CharField()
    location = pw.BooleanField() # 0 = Local, 1 = Foreign
    priority = pw.IntegerField()
    # allow users to save up to 5 contacts & rank them by priority
    contact_email = pw.CharField()
    contact_num = pw.CharField()
