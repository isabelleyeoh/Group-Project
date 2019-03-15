from models.base_model import BaseModel
import peewee as pw
from models.product import Product
from models.user import User


class Image (BaseModel):
	product_id = pw.ForeignKeyField(Product, backref='product')
	seller_id = pw.ForeignKeyField(User, backref='sellers')
	image_url = pw.CharField(unique=True)


	
