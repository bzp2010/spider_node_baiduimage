from __future__ import absolute_import, division, print_function, \
    with_statement
from peewee import *


class BaseModel(Model):
    class Meta:
        database = SqliteDatabase(":memory:")


class DataModel(BaseModel):
    image_name = CharField(null=False, unique=True)
    image_url  = CharField(null=False, unique=True)