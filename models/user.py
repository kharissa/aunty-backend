from models.base_model import BaseModel
import peewee as pw

class User(BaseModel):
    email = pw.CharField(unique=True)
    password = pw.CharField()
    first_name = pw.CharField()
    last_name = pw.CharField()
    dob = pw.DateField()
    passport_num = pw.CharField(null=True)
    passport_img = pw.CharField(null=True)
    nationality = pw.CharField(max_length=2, null=True)
    language_primary = pw.CharField(null=True)
    language_secondary = pw.CharField(null=True)
    verified = pw.BooleanField(default=0)

    def validate(self):
        duplicate_email = User.get_or_none(User.email == self.email)
        if duplicate_email:
            self.errors.append('Email has been registered.')

    def save(self, *args, **kwargs):
        # self.validate()
        # validate the user fields
        pass