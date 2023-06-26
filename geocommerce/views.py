from django.views.generic import TemplateView
from contentmanager.models import Category


class AboutTemplateView(TemplateView):
    template_name = 'layouts/hero.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        context['user'] = self.request.user
        context['categories'] = Category.objects.order_by('name')        
        return context