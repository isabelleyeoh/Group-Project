from models.base_model import BaseModel
import peewee as pw
from models.seller import Seller


class Product (BaseModel):
	name = pw.CharField(unique=True)
	description = pw.CharField()
	category = pw.CharField()
	price = pw.CharField()
	product_url = pw.CharField()
	custom_concept = pw.CharField()
	seller_id = pw.ForeignKeyField(Seller, backref='sellers')

	
	
