from models.base_model import BaseModel
import peewee as pw
from models.buyer import Buyer
from models.product import Product

class Search (BaseModel):
	search_image_url = pw.CharField()
	general_concept = pw.CharField()
	buyer_id = pw.ForeignKeyField(Buyer, backref='buyers')
	product_id = pw.ForeignKeyField(Product, backref='products')

	
	
