from django.urls import path
from .views import (
    BankAddView, BranchAddView, BranchDetailsView, BankBranchesAllView,
    BankListView, BankDetailView, BranchEditView
)

urlpatterns = [
    path('add/', BankAddView.as_view(), name='bank_add'),
    path('<int:bank_id>/branches/add/', BranchAddView.as_view(), name='branch_add'),
    path('branch/<int:branch_id>/details/', BranchDetailsView, name='branch_details'),
    path('<int:bank_id>/branches/all/', BankBranchesAllView, name='bank_branches_all'),
    path('all/', BankListView.as_view(), name='bank_list'),
    path('<int:bank_id>/details/', BankDetailView.as_view(), name='bank_details'),
    path('branch/<int:branch_id>/edit/', BranchEditView.as_view(), name='branch_edit'),
]

