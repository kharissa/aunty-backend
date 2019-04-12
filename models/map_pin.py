from models.base_model import BaseModel
from models.user import User
import peewee as pw
from playhouse.hybrid import hybrid_property

class MapPin(BaseModel):
    user = pw.ForeignKeyField(User, backref="pins")
    name = pw.CharField(max_length=255)
    description = pw.CharField(max_length=1000, null=True)
    longitude = pw.DecimalField(max_digits=9, decimal_places=6)
    latitude = pw.DecimalField(max_digits=9, decimal_places=6)
    is_safe = pw.BooleanField() # safe = True, dangerous = False
    category = pw.CharField()
    source = pw.CharField(default="User")
    radius = pw.IntegerField()
    address = pw.CharField(null=True)
    is_public = pw.BooleanField(default=True)


# mp = MapPin(name="House", longitude=-37.813629, latitude=114.963058, is_safe=True, category="home", source="user", radius=32, is_public=True, user=1)