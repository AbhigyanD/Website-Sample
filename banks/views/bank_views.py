from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.http import Http404, HttpResponseForbidden, HttpResponse, JsonResponse
from django.urls import reverse
from ..models import Bank, Branch
from ..forms import BankForm, BranchForm


class BankAddView(LoginRequiredMixin, FormView):
    template_name = 'banks/bank_add.html'
    form_class = BankForm

    def handle_no_permission(self):
        return HttpResponse('Unauthorized', status=401)

    def form_valid(self, form):
        bank = Bank.objects.create(
            name=form.cleaned_data['name'],
            description=form.cleaned_data['description'],
            institution_number=form.cleaned_data['inst_num'],
            swift_code=form.cleaned_data['swift_code'],
            owner=self.request.user
        )
        return redirect(f'/banks/{bank.id}/details/')


class BranchAddView(LoginRequiredMixin, FormView):
    template_name = 'banks/branch_add.html'
    form_class = BranchForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponse('Unauthorized', status=401)
        
        bank_id = kwargs.get('bank_id')
        try:
            self.bank = Bank.objects.get(pk=bank_id)
        except Bank.DoesNotExist:
            return HttpResponse('Not Found', status=404)

        if self.bank.owner != request.user:
            return HttpResponse('Forbidden', status=403)

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        capacity = form.cleaned_data.get('capacity')
        branch = Branch.objects.create(
            name=form.cleaned_data['name'],
            transit_number=form.cleaned_data['transit_num'],
            address=form.cleaned_data['address'],
            email=form.cleaned_data['email'],
            capacity=capacity if capacity is not None else None,
            bank=self.bank
        )
        return redirect(f'/banks/branch/{branch.id}/details/')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bank'] = self.bank
        return context


def BranchDetailsView(request, branch_id):
    try:
        branch = Branch.objects.get(pk=branch_id)
    except Branch.DoesNotExist:
        return JsonResponse({'error': 'Not Found'}, status=404)

    return JsonResponse({
        'id': branch.id,
        'name': branch.name,
        'transit_num': branch.transit_number,
        'address': branch.address,
        'email': branch.email,
        'capacity': branch.capacity,
        'last_modified': branch.last_modified.isoformat()
    })


def BankBranchesAllView(request, bank_id):
    try:
        bank = Bank.objects.get(pk=bank_id)
    except Bank.DoesNotExist:
        return JsonResponse({'error': 'Not Found'}, status=404)

    branches = bank.branches.all()
    branches_data = [{
        'id': branch.id,
        'name': branch.name,
        'transit_num': branch.transit_number,
        'address': branch.address,
        'email': branch.email,
        'capacity': branch.capacity,
        'last_modified': branch.last_modified.isoformat()
    } for branch in branches]

    return JsonResponse(branches_data, safe=False)

