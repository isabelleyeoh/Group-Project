from models.base_model import BaseModel
import peewee as pw
from models.seller import Seller


class Product (BaseModel):
    seller_id = pw.ForeignKeyField(Seller, backref='sellers')
    name = pw.CharField(unique=True)
    image_url = pw.CharField(unique=True)
    category=pw.CharField()
    price = pw.CharField()
    description = pw.CharField()
    concept=pw.CharField()

