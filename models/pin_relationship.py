from models.base_model import BaseModel
from models.user import User
from models.pin_detail import Pin
import peewee as pw
from playhouse.hybrid import hybrid_property

class Pin(BaseModel):
    user_id = pw.ForeignKeyField(User, backref="pins")
    pin_id = pw.ForeignKeyField(Pin)
    is_public = pw.BooleanField(default=True)

    # @hybrid_property
    # def pin_rating(self):
    #     # return
    #     pass