from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from mail.models import Mail

@registry.register_document
class MailDocument(Document):
    sender = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'email': fields.TextField(),
        'username': fields.TextField(),
    })
    reciver = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'email': fields.TextField(),
        'username': fields.TextField(),
    })
    header = fields.TextField()
    datetime = fields.DateField()
    is_read = fields.BooleanField()
    status = fields.TextField()

    class Index:
        name = 'mails'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

    class Django:
        model = Mail
        fields = [
            'id',
        ]