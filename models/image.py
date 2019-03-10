from models.base_model import BaseModel
import peewee as pw
from models.seller import Seller
from models.product import Product


class Image (BaseModel):
	product_id = pw.ForeignKeyField(Product, backref='product')
	seller_id = pw.ForeignKeyField(Seller, backref='sellers')
	image_url = pw.CharField(unique=True)



	
