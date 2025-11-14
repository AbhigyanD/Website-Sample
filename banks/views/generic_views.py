from django.views.generic import ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from ..models import Bank, Branch
from ..forms import BranchForm


class BankListView(ListView):
    model = Bank
    template_name = 'banks/bank_list.html'
    context_object_name = 'banks'


class BankDetailView(DetailView):
    model = Bank
    template_name = 'banks/bank_details.html'
    context_object_name = 'bank'
    pk_url_kwarg = 'bank_id'


class BranchEditView(LoginRequiredMixin, UpdateView):
    model = Branch
    template_name = 'banks/branch_edit.html'
    form_class = BranchForm
    pk_url_kwarg = 'branch_id'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponse('Unauthorized', status=401)
        
        branch = get_object_or_404(Branch, pk=kwargs['branch_id'])
        
        if branch.bank.owner != request.user:
            return HttpResponse('Forbidden', status=403)

        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        branch = self.get_object()
        initial['name'] = branch.name
        initial['transit_num'] = branch.transit_number
        initial['address'] = branch.address
        initial['email'] = branch.email
        initial['capacity'] = branch.capacity
        return initial

    def get_success_url(self):
        return f'/banks/branch/{self.object.id}/details/'

    def form_valid(self, form):
        branch = self.get_object()
        branch.name = form.cleaned_data['name']
        branch.transit_number = form.cleaned_data['transit_num']
        branch.address = form.cleaned_data['address']
        branch.email = form.cleaned_data['email']
        capacity = form.cleaned_data.get('capacity')
        branch.capacity = capacity if capacity is not None else None
        branch.save()
        return redirect(self.get_success_url())

