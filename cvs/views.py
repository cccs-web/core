from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.core import serializers

import cvs.models as cm


class ProjectDetailView(DetailView):
    model = cm.Project

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        context['serialized'] = serializers.serialize('python', [self.get_object()])[0]
        return context

class ProjectListView(ListView):
    model = cm.Project


