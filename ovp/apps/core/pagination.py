from rest_framework import pagination

class NoPagination(pagination.PageNumberPagination):
  page_size = 0
  page_size_query_param = 'page_size'
  max_page_size = 0
