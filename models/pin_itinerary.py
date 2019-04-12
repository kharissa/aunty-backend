from models.base_model import BaseModel
from models.user import User
import peewee as pw

class Pin(BaseModel):
    user_id = pw.ForeignKeyField(User, backref="itinerary")
    longitude = pw.FloatField(10,6)
    latitude = pw.FloatField(10,6)
    name = pw.CharField(max_length=255)
    description = pw.CharField(max_length=1000, null=True)
    address = pw.CharField(null=True)
    start_time = pw.DateTimeField()
    resolved = pw.BooleanField() # False if user has not confirmed safety status

