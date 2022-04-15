from peewee import *

from models.article import Article
from models.tags import Tags
db = MySQLDatabase(
    database='Cloudmarkdown',
    user='Cloudmarkdown',
    password="Cloudmarkdown",
    host="192.168.11.13",
    port=3306)
class Relate_Tags(Model):
    id = AutoField(primary_key=True)
    article_id = ForeignKeyField(Article) #外部キー
    tag_id=ForeignKeyField(Tags)


    class Meta:
        database = db

db.create_tables([Relate_Tags])
# データ挿入
# Relate_Tags.create(article_id=1, tag_id=1)