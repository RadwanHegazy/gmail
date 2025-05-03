from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from elasticsearch_dsl import Q
from django.db.models import Q as django_q
from mail.documents import MailDocument
from mail.apis.serializers.search import MailSearchSerializer
from mail.models import Mail
from uuid import UUID

class SearchMailAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MailSearchSerializer

    def get_queryset(self):
        user = self.request.user
        query = self.request.query_params.get('q', '')
        
        # Build search query
        search = MailDocument.search()
        if query:
            q = Q(
                'multi_match',
                query=query,
                fields=[
                    'header^2'
                ]
            )
            search = search.query(q)
        
     
        # Execute search
        response = search.execute()

        # Get Django queryset from Elasticsearch results
        ids = [UUID(hit.id) for hit in response]

        queryset = Mail.objects.filter(id__in=ids)
        queryset = queryset.filter(
            django_q(sender=user) |
            django_q(reciver=user)
        )
        return queryset