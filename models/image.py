from models.base_model import BaseModel
import peewee as pw
from models.product import Product


class Image (BaseModel):
	image_url = pw.CharField(unique=True)
	product_id = pw.ForeignKeyField(Product, backref='products')

	
	
