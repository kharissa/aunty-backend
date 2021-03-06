from models.base_model import BaseModel
from models.user import User
import peewee as pw

class ItineraryPin(BaseModel):
    user = pw.ForeignKeyField(User, backref="itinerary")
    longitude = pw.DecimalField(max_digits=9, decimal_places=6)
    latitude = pw.DecimalField(max_digits=9, decimal_places=6)
    name = pw.CharField(max_length=255)
    description = pw.CharField(max_length=1000, null=True)
    address = pw.CharField(null=True)
    start_time = pw.DateTimeField()
    resolved = pw.BooleanField(default=False) # False if user has not confirmed safety status

