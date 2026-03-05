from django.views.generic import TemplateView, ListView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.catalog.models import Flower, BouquetSize
from apps.catalog.views import SellerRequiredMixin
from .models import Bouquet

class BouquetDesignView(TemplateView):
    template_name = 'bouquet/designer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['flowers'] = Flower.objects.filter(is_active=True)
        context['sizes'] = BouquetSize.objects.all()
        return context

class BouquetListView(LoginRequiredMixin, SellerRequiredMixin, ListView):
    model = Bouquet
    template_name = 'bouquet/bouquet_list.html'
    context_object_name = 'bouquets'
    ordering = ['-created_at']

class BouquetDetailView(LoginRequiredMixin, SellerRequiredMixin, DetailView):
    model = Bouquet
    template_name = 'bouquet/bouquet_detail.html'
    context_object_name = 'bouquet'

class BouquetDeleteView(LoginRequiredMixin, SellerRequiredMixin, DeleteView):
    model = Bouquet
    template_name = 'bouquet/bouquet_confirm_delete.html'
    success_url = reverse_lazy('bouquet:bouquet_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['flowers'] = Flower.objects.filter(is_active=True)
        context['sizes'] = BouquetSize.objects.all()
