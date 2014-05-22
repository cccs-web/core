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
        context['cv_list'] = context['cv_list'].order_by('user__last_name')
        return context


class CVDetailMixin(object):
    model = cm.CV

    def can_update(self, request):
        return (request.user == self.get_object().user) or request.user.is_staff


class CVDetailView(CVDetailMixin, CCCSDetailView):

    def get_context_data(self, **kwargs):
        context = super(CVDetailView, self).get_context_data(**kwargs)
        context['can_update'] = self.can_update(self.request)
        return context


class CVUpdateView(CVDetailMixin, UpdateView):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect('/accounts/login?next={0}'.format(request.path))
        elif self.can_update(request):
            return super(CVUpdateView, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied




