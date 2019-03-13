from models.base_model import BaseModel
from models.buyer import Buyer
import peewee as pw
import re
from flask_login import UserMixin

class Seller(BaseModel, UserMixin):
    name = pw.CharField(null=True)
    username = pw.CharField(unique=True)
    email = pw.CharField(unique=True)
    password = pw.CharField()

    def is_active(self):
        return True

    def validate(self):
        duplicate_users = Seller.get_or_none(Seller.email == self.email)

        validate_email = re.compile('[^@]+@[^@]+\.[^@]+')

        validate_password = re.compile(
            '^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$')

        if duplicate_users:
            self.errors.append('email not unique')

        if not validate_email.match(self.email):
            self.errors.append('check your email address given')