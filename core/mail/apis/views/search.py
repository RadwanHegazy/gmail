from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from elasticsearch_dsl import Q
from mail.documents import MailDocument
from mail.apis.serializers.search import MailSearchSerializer
from django.core.paginator import Paginator

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
                    'subject^3',  # boost subject matches
                    'content',
                    'sender.email',
                    'sender.username',
                    'reciver.email',
                    'reciver.username'
                ]
            )
            search = search.query(q)
        
        # Filter for user's emails only
        user_filter = Q('bool', should=[
            Q('term', **{'sender.id': user.id}),
            Q('term', **{'reciver.id': user.id})
        ])
        search = search.query(user_filter)
        
        # Execute search
        response = search.execute()
        
        # Get Django queryset from Elasticsearch results
        ids = [hit.id for hit in response]
        queryset = Mail.objects.filter(id__in=ids)
        
        return queryset