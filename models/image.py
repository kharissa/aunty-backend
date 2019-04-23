from app import app
import os
from models.base_model import BaseModel
from models.user import User
import peewee as pw
from playhouse.hybrid import hybrid_property

class Image(BaseModel):
    user = pw.ForeignKeyField(User, backref="images")
    filename = pw.CharField()
    weapon = pw.FloatField(null=True)
    alcohol = pw.FloatField(null=True)
    drugs = pw.FloatField(null=True)
    male = pw.FloatField(null=True)
    female = pw.FloatField(null=True)
    minor = pw.FloatField(null=True)
    sunglasses = pw.FloatField(null=True)
    scam = pw.FloatField(null=True)
    nudity = pw.FloatField(null=True)

    @hybrid_property
    def url(self):
        # Add S3 location to config
        return f'{app.config["S3_LOCATION"]}{self.filename}'
