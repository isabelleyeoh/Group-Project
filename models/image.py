from models.base_model import BaseModel
import peewee as pw
from models.seller import Seller


class Image (BaseModel):
	name = pw.CharField(unique=True)
	image_url = pw.CharField(unique=True)
	product_url = pw.CharField(unique=True)
	price = pw.CharField()
	description = pw.CharField()
	size = pw.CharField()
	seller_id = pw.ForeignKeyField(Seller, backref='sellers')

	
	
