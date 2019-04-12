from models.base_model import BaseModel
from models.user import User
from models.pin_detail import Pin
import peewee as pw

class PinRating(BaseModel):
    pin_id = pw.ForeignKeyField(Pin, backref="ratings")
    user_id = pw.ForeignKeyField(User, backref="raters")
    pin_rating = pw.BooleanField()