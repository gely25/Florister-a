from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.db.models import F
from .models import Flower, Service, Promotion, PreDesignedBouquet

class SellerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_seller

class HomeView(TemplateView):
    template_name = 'catalog/home.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dahsboard:index')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_flowers'] = Flower.objects.filter(is_active=True, is_featured=True)[:8]
        context['services'] = Service.objects.all()
        context['promotions'] = Promotion.objects.filter(is_active=True)
        return context

class CatalogIndexView(LoginRequiredMixin, SellerRequiredMixin, TemplateView):
    template_name = 'catalog/catalog_index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_flowers'] = Flower.objects.count()
        context['active_flowers'] = Flower.objects.filter(is_active=True).count()
        context['total_bouquets'] = PreDesignedBouquet.objects.count()
        context['active_bouquets'] = PreDesignedBouquet.objects.filter(is_active=True).count()
        context['total_services'] = Service.objects.count()
        
        # Featured items list
        context['featured_flowers'] = Flower.objects.filter(is_featured=True)
        return context

# Flower CRUD
class FlowerListView(LoginRequiredMixin, SellerRequiredMixin, ListView):
    model = Flower
    template_name = 'catalog/flower_list.html'
    context_object_name = 'flowers'
    ordering = ['name']

class FlowerCreateView(LoginRequiredMixin, SellerRequiredMixin, CreateView):
    model = Flower
    fields = ['name', 'tier', 'price', 'image', 'is_active', 'is_featured']
    template_name = 'catalog/flower_form.html'
    success_url = reverse_lazy('catalog:flower_list')

    def form_valid(self, form):
        messages.success(self.request, "Flor creada exitosamente.")
        return super().form_valid(form)

class FlowerUpdateView(LoginRequiredMixin, SellerRequiredMixin, UpdateView):
    model = Flower
    fields = ['name', 'tier', 'price', 'image', 'is_active', 'is_featured']
    template_name = 'catalog/flower_form.html'
    success_url = reverse_lazy('catalog:flower_list')

    def form_valid(self, form):
        messages.success(self.request, "Flor actualizada correctamente.")
        return super().form_valid(form)

class FlowerDeleteView(LoginRequiredMixin, SellerRequiredMixin, DeleteView):
    model = Flower
    template_name = 'catalog/flower_confirm_delete.html'
    success_url = reverse_lazy('catalog:flower_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Flor eliminada.")
        return super().delete(request, *args, **kwargs)

# Service CRUD
class ServiceListView(LoginRequiredMixin, SellerRequiredMixin, ListView):
    model = Service
    template_name = 'catalog/service_list.html'
    context_object_name = 'services'

class ServiceCreateView(LoginRequiredMixin, SellerRequiredMixin, CreateView):
    model = Service
    fields = ['title', 'description', 'price', 'stock', 'image', 'is_active']
    template_name = 'catalog/service_form.html'
    success_url = reverse_lazy('catalog:service_list')

class ServiceUpdateView(LoginRequiredMixin, SellerRequiredMixin, UpdateView):
    model = Service
    fields = ['title', 'description', 'price', 'stock', 'image', 'is_active']
    template_name = 'catalog/service_form.html'
    success_url = reverse_lazy('catalog:service_list')

class ServiceDeleteView(LoginRequiredMixin, SellerRequiredMixin, DeleteView):
    model = Service
    template_name = 'catalog/service_confirm_delete.html'
    success_url = reverse_lazy('catalog:service_list')

# PreDesignedBouquet CRUD
class PreDesignedBouquetListView(LoginRequiredMixin, SellerRequiredMixin, ListView):
    model = PreDesignedBouquet
    template_name = 'catalog/predesigned_list.html'
    context_object_name = 'bouquets'

class PreDesignedBouquetCreateView(LoginRequiredMixin, SellerRequiredMixin, CreateView):
    model = PreDesignedBouquet
    fields = ['name', 'description', 'price', 'image', 'stock', 'is_active']
    template_name = 'catalog/predesigned_form.html'
    success_url = reverse_lazy('catalog:predesigned_list')

class PreDesignedBouquetUpdateView(LoginRequiredMixin, SellerRequiredMixin, UpdateView):
    model = PreDesignedBouquet
    fields = ['name', 'description', 'price', 'image', 'stock', 'is_active']
    template_name = 'catalog/predesigned_form.html'
    success_url = reverse_lazy('catalog:predesigned_list')

class PreDesignedBouquetDeleteView(LoginRequiredMixin, SellerRequiredMixin, DeleteView):
    model = PreDesignedBouquet
    template_name = 'catalog/predesigned_confirm_delete.html'
    success_url = reverse_lazy('catalog:predesigned_list')

# Bulk Pricing
class BulkPriceUpdateView(LoginRequiredMixin, SellerRequiredMixin, TemplateView):
    template_name = 'catalog/price_update.html'

    def post(self, request, *args, **kwargs):
        tier = request.POST.get('tier')
        change_type = request.POST.get('change_type') # 'percent' or 'amount'
        operation = request.POST.get('operation')    # 'add' or 'sub'
        from decimal import Decimal
        value_dec = Decimal(str(request.POST.get('value', 0)))

        flowers = Flower.objects.all()
        if tier != 'all':
            flowers = flowers.filter(tier=tier)

        if change_type == 'percent':
            factor = Decimal('1.0') + (value_dec / Decimal('100.0')) if operation == 'add' else Decimal('1.0') - (value_dec / Decimal('100.0'))
            flowers.update(price=F('price') * factor)
        else:
            delta = value_dec if operation == 'add' else -value_dec
            flowers.update(price=F('price') + delta)

        messages.success(request, "Precios actualizados dinámicamente.")
        return redirect('catalog:flower_list')
