from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.forms.models import inlineformset_factory
from django.http.response import HttpResponseRedirect

from projects.views import CCCSDetailView

import cvs.models as cm


class CVListView(ListView):
    model = cm.CV


class CVDetailMixin(object):
    model = cm.CV

    def can_update(self, request):
        return (request.user == self.get_object().user) or request.user.is_staff


class CVDetailView(CVDetailMixin, CCCSDetailView):

    def get_context_data(self, **kwargs):
        context = super(CVDetailView, self).get_context_data(**kwargs)
        context['can_update'] = self.can_update(self.request)
        context['use_right_col'] = "No"
        context['cvproject_list'] = self.get_object().cvproject_set.all()
        return context


CVProjectFormSet = inlineformset_factory(cm.CV, cm.CVProject)


class CVUpdateView(CVDetailMixin, UpdateView):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect('/accounts/login?next={0}'.format(request.path))
        elif self.can_update(request):
            return super(CVUpdateView, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_context_data(self, **kwargs):
        context = super(CVUpdateView, self).get_context_data(**kwargs)
        context['use_right_col'] = "No"
        context['cvproject_formset'] = self.get_cvproject_formset()
        return context

    def get_cvproject_formset(self):
        cvproject_formset_kwargs = {
            'instance': self.object,
            'queryset': cm.CVProject.objects.filter(cv=self.object)}
        if self.request.method == 'POST':
            cvproject_formset = CVProjectFormSet(self.request.POST, **cvproject_formset_kwargs)
        else:
            cvproject_formset = CVProjectFormSet(**cvproject_formset_kwargs)
        return cvproject_formset

    def form_valid(self, form):
        context = self.get_context_data()
        cvproject_formset = context['cvproject_formset']
        if cvproject_formset.is_valid():
            form.save()
            cvproject_formset.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(CVUpdateView, self).form_valid(form)








