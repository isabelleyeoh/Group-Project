from models.base_model import BaseModel
import peewee as pw
from models.seller import Seller

# Hybrid property import
from playhouse.hybrid import hybrid_property
from app import app

class Product (BaseModel):
    seller_id = pw.ForeignKeyField(Seller, backref='sellers')
    name = pw.CharField(unique=True)
    image_url = pw.CharField(unique=True)
    category=pw.CharField()
    price = pw.CharField()
    description = pw.CharField()
    concept=pw.CharField()  
    clarifai_id=pw.CharField(default="Yes")


 # Hybrid property
    @hybrid_property
    def image_photo_url(self):
        return f'{app.config["S3_LOCATION"]}{self.image_url}'