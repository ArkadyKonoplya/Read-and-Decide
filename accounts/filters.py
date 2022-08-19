from rest_framework import filters


class StateFilterBackend(filters.BaseFilterBackend):
    """
    Filter that returns doctors based on state license
    """
    def filter_queryset(self, request, queryset, view):
        if request.GET.get('state'):
            return queryset.filter(states__icontains=request.GET.get('state'))
        else:
            return queryset


class AcceptingFilterBackend(filters.BaseFilterBackend):
    """
    Filter that returns doctors based on accepting new patients
    """
    def filter_queryset(self, request, queryset, view):
        if request.GET.get('accepting_new_patients'):
            return queryset.filter(office_is_active=True, accepting_new_patients=True, is_approved=True)
        else:
            return queryset