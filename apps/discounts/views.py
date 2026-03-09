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
    paginate_by = 10

    def get_queryset(self):
        queryset = Discount.objects.all().order_by('-valid_from')
        search_query = self.request.GET.get('q', '').strip()
        if search_query:
            queryset = queryset.filter(code__icontains=search_query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context

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
