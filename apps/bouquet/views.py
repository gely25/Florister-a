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
    paginate_by = 10

    def get_queryset(self):
        queryset = Bouquet.objects.all().order_by('-created_at')
        
        search_query = self.request.GET.get('q', '').strip()
        if search_query:
            if search_query.isdigit():
                queryset = queryset.filter(id=search_query)
            else:
                queryset = queryset.filter(user__username__icontains=search_query)
                
        size_filter = self.request.GET.get('size', '').strip()
        if size_filter:
            queryset = queryset.filter(size_id=size_filter)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        context['current_size'] = self.request.GET.get('size', '')
        context['sizes'] = BouquetSize.objects.all()
        return context

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
