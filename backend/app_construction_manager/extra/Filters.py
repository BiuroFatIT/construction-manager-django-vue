import django_filters
from django.db.models import Q
from datetime import datetime, timedelta


class CustomDateRangeFilter(django_filters.Filter):
    def __init__(self, *args, param_name=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.param_name = param_name or self.field_name

    def filter(self, qs, value):
        values = self.parent.request.GET.getlist(self.param_name)

        if len(values) == 2:
            start, end = values
            try:
                start_date = datetime.strptime(start, "%Y-%m-%d").date()
                end_date = datetime.strptime(end, "%Y-%m-%d").date() + timedelta(days=1)
            except ValueError:
                return qs.none()  # Błędny format daty

            return qs.filter(**{
                f"{self.field_name}__gte": start_date,
                f"{self.field_name}__lt": end_date
            })
        return qs
    
class BooleanInFilter(django_filters.BaseInFilter, django_filters.BooleanFilter):
    def filter(self, qs, value):
        param_name = self.field_name + '[]'
        values = self.parent.request.GET.getlist(param_name)
        if not values:
            values = self.parent.request.GET.getlist(self.field_name)
        if values:
            # Konwersja stringów na boolean
            bool_values = [val.lower() == 'true' for val in values if val.lower() in ('true', 'false')]
            return qs.filter(**{f"{self.field_name}__in": bool_values})
        return qs
    
class RelatedNameFilter(django_filters.Filter):
    def __init__(self, *args, param_name=None, related_field='name', **kwargs):
        self.related_field = related_field
        super().__init__(*args, **kwargs)
        self.param_name = param_name or self.field_name

    def filter(self, qs, value):
        values = self.parent.request.GET.getlist(self.param_name)
        if not values:
            values = self.parent.request.GET.getlist(self.field_name)

        if values:
            query = Q()
            for val in values:
                query |= Q(**{f"{self.field_name}__{self.related_field}__icontains": val})
            return qs.filter(query).distinct()
        return qs