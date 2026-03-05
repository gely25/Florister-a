from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.catalog.views import SellerRequiredMixin
from .models import Discount
from .forms import DiscountForm

class DiscountListView(LoginRequiredMixin, SellerRequiredMixin, ListView):
    model = Discount
    template_name = 'discounts/discount_list.html'
    context_object_name = 'discounts'

class DiscountCreateView(LoginRequiredMixin, SellerRequiredMixin, CreateView):
    model = Discount
    form_class = DiscountForm
    template_name = 'discounts/discount_form.html'
    success_url = reverse_lazy('discounts:discount_list')

class DiscountUpdateView(LoginRequiredMixin, SellerRequiredMixin, UpdateView):
    model = Discount
    form_class = DiscountForm
    template_name = 'discounts/discount_form.html'
    success_url = reverse_lazy('discounts:discount_list')

class DiscountDeleteView(LoginRequiredMixin, SellerRequiredMixin, DeleteView):
    model = Discount
    template_name = 'discounts/discount_confirm_delete.html'
    success_url = reverse_lazy('discounts:discount_list')
