import logging
# from django.db.models.functions import Concat
from django.db.models.query import QuerySet
# from django.db.models import Manager, Value
from viewflow.models import Task

logger = logging.getLogger(__name__)


class AccessRequestQuerySet(QuerySet):
    def importer_requests(self):
        "Defer import to circumvent circular dependency"
        from .models import AccessRequest
        return self.filter(request_type__in=[
            AccessRequest.IMPORTER, AccessRequest.IMPORTER_AGENT
        ])

    def exporter_requests(self):
        "Defer import to circumvent circular dependency"
        from .models import AccessRequest
        return self.filter(request_type__in=[
            AccessRequest.EXPORTER, AccessRequest.EXPORTER_AGENT
        ])


class ProcessQuerySet(QuerySet):
    """
    Base manager for the flow Process extended to query processeses
    a user has started
    """
    def owned_process(self, user):
        """
        Queryset filter to get all processes user has started
        """

        tasks = Task.objects.filter(owner=user)
        process_ids = []
        for task in tasks:
            process_ids.append(task.process_id)

        return self.filter(
            process_ptr_id__in=process_ids).prefetch_related('access_request')


#  class ImporterManager(Manager):
#      def get_queryset(self):
#          return super().get_queryset().annotate(full_name=Concat(
#              'title', Value(' '), 'name', Value(' '), 'last_name'))
