from models.base_model import BaseModel
import peewee as pw

class SafeLocation(BaseModel):
    category = pw.CharField()
    name = pw.CharField()
    description = pw.CharField(max_length=3000)
    longitude = pw.DecimalField(max_digits=9, decimal_places=6)
    latitude = pw.DecimalField(max_digits=9, decimal_places=6)
    address = pw.CharField(null=True)
    phone_num = pw.CharField(null=True)
    opening_time = pw.DateTimeField(null=True)
    closing_time = pw.DateTimeField(null = True)
