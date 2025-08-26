from rest_framework.pagination import PageNumberPagination
from DjangoVlog.config import config


class StandardResultsSetPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = config.max_page_size