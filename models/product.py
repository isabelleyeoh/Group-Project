from models.base_model import BaseModel
import peewee as pw
from models.user import User

# Hybrid property import
from playhouse.hybrid import hybrid_property
from app import app

class Product (BaseModel):
	name = pw.CharField(unique=True)
	description = pw.CharField()
	category = pw.CharField()
	price = pw.CharField()
	product_url = pw.CharField()
	custom_concept = pw.CharField()
	seller_id = pw.ForeignKeyField(User, backref='sellers')

	
	

 # Hybrid property
    @hybrid_property
    def image_photo_url(self):
        return f'{app.config["S3_LOCATION"]}{self.image_url}'