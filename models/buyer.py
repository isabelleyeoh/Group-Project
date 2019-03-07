from models.base_model import BaseModel
import peewee as pw
import re


class Buyer(BaseModel):
    username = pw.CharField(unique=True)
    email = pw.CharField(unique=True)
    password = pw.CharField()

    def validate(self):
        duplicate_users = Buyer.get_or_none(Buyer.email == self.email)

        validate_email = re.compile('[^@]+@[^@]+\.[^@]+')

        validate_password = re.compile(
            '^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$')

        if duplicate_users:
            self.errors.append('email not unique')

        if not validate_email.match(self.email):
            self.errors.append('check your email address given')