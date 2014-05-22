from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect

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

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect('/accounts/login?next={0}'.format(request.path))
        elif (request.user == self.get_object().user) or request.user.is_staff:
            return super(CVUpdateView, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied




