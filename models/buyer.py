from models.base_model import BaseModel
import peewee as pw


class Buyer(BaseModel):
    name = pw.CharField(unique=False)
