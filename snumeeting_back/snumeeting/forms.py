from .models import Meeting 
from simple_search import search_form_factory

SearchForm = search_form_factory(Meeting.objects.all(),
                                 ['^title', '=subject_id'])
