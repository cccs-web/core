from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.forms.models import inlineformset_factory, modelform_factory
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
        return context


CVProjectFormSet = inlineformset_factory(cm.CV, cm.CVProject)
CVUpdateForm = modelform_factory(cm.CV, exclude=('slug',))
CVMODEL_CLASSES = (cm.CVEducation,
                   cm.CVTraining,
                   cm.CVMembership,
                   cm.CVLanguage,
                   cm.CVProject)
CV_FORMSET_MAP = {cls: inlineformset_factory(cm.CV, cls)
                        for cls in CVMODEL_CLASSES}


class CVUpdateView(CVDetailMixin, UpdateView):
    form_class = CVUpdateForm

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
        for model_class in CVMODEL_CLASSES:
            context['formset_' + model_class._meta.model_name] = self.get_cv_formset(model_class)
        return context

    def get_cv_formset(self, model_class):
        formset_kwargs = {
            'instance': self.object,
            'queryset': model_class.objects.filter(cv=self.object)}
        cv_formset_class = CV_FORMSET_MAP[model_class]
        if self.request.method == 'POST':
            cv_formset = cv_formset_class(self.request.POST, **formset_kwargs)
        else:
            cv_formset = cv_formset_class(**formset_kwargs)
        return cv_formset

    def form_valid(self, form):
        context = self.get_context_data()
        cvproject_formset = context['cvproject_formset']
        if cvproject_formset.is_valid():
            form.save()
            cvproject_formset.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(CVUpdateView, self).form_valid(form)








