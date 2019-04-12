from models.base_model import BaseModel
from models.user import User
import peewee as pw
from playhouse.hybrid import hybrid_property

class MapPin(BaseModel):
    user = pw.ForeignKeyField(User, backref="pins")
    name = pw.CharField(max_length=255)
    description = pw.CharField(max_length=1000, null=True)
    # longitude = pw.FloatField(10,6)
    # latitude = pw.FloatField(10,6)
    is_safe = pw.BooleanField() # safe = True, dangerous = False
    category = pw.CharField()
    source = pw.CharField()
    radius = pw.IntegerField()
    address = pw.CharField(null=True)
    is_public = pw.BooleanField(default=True)


