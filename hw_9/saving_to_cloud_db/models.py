from datetime import datetime

from mongoengine import EmbeddedDocument, Document
from mongoengine.fields import DateTimeField, EmbeddedDocumentField, ListField, StringField, ReferenceField


class Authors(Document):
    fullname = StringField()
    born_date = DateTimeField(default=datetime.now())
    born_location = StringField()
    description = StringField()


class Tag(EmbeddedDocument):
    name = StringField()


class Quotes(Document):
    tags = ListField(EmbeddedDocumentField(Tag))
    author = ReferenceField(Authors)
    quote = StringField()