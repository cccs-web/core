import os

from django.http.response import Http404, HttpResponse
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404

import documents.models as dm


class DocumentListView(ListView):
    model = dm.Document
    paginate_by = 25

    def get_queryset(self):
        queryset = super(DocumentListView, self).get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(status=dm.CONTENT_STATUS_PUBLISHED)
        return queryset


class DocumentDetailView(DetailView):
    model = dm.Document

    def get_object(self, queryset=None):
        obj = super(DocumentDetailView, self).get_object(queryset)
        if not self.request.user.is_staff and obj.status != dm.CONTENT_STATUS_PUBLISHED:
            raise Http404
        return obj


def download(request, slug):
    """
    Download the file
    :param request:
    :param slug:
    :return: response
    """

    document = get_object_or_404(dm.Document, slug=slug)
    filename = os.path.basename(document.source_file.name)

    response = HttpResponse(document.source_file, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)

    return response
