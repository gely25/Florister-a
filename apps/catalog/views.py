from django.views.generic import TemplateView
from .models import Flower, Service, Promotion

class HomeView(TemplateView):
    template_name = 'catalog/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_flowers'] = Flower.objects.filter(is_active=True, is_featured=True)[:8]
        context['services'] = Service.objects.all()
        context['promotions'] = Promotion.objects.filter(is_active=True)
        return context
