from django.views.generic import TemplateView
from apps.catalog.models import Flower, BouquetSize

class BouquetDesignView(TemplateView):
    template_name = 'bouquet/designer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['flowers'] = Flower.objects.filter(is_active=True)
        context['sizes'] = BouquetSize.objects.all()
        return context
