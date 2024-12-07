from mongoengine import (
    Document,
    EmbeddedDocument,
    StringField,
    DecimalField,
    IntField,
    ListField,
    EmbeddedDocumentField,
    DateTimeField,
)
from datetime import datetime


class OrderItem(EmbeddedDocument):
    """
    Embedded document for items within an order.
    This represents each individual item in the order with its quantity and price.
    """

    pass
