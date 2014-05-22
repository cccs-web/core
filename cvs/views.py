from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.core.urlresolvers import reverse

from projects.views import CCCSDetailView

import cvs.models as cm


class CVListView(ListView):
    model = cm.CV

    def get_context_data(self, **kwargs):
        context = super(CVListView, self).get_context_data(**kwargs)
        context['object_list'] = context['object_list'].order_by('user__last_name')
        return context


class CVDetailView(CCCSDetailView):
    model = cm.CV


class CVUpdateView(UpdateView):
    model = cm.CV



