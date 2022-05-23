from django.shortcuts import render
from .models import Product, ProductImage
from django.http import HttpRequest, HttpResponse
from django.views.generic.detail import DetailView

# Create your views here.
def index(request):
    product = Product.objects.filter(is_published=1).order_by('-id')
    for singleblog in product:
        blogsImg = ProductImage.objects.filter(product=singleblog.id).first()
        singleblog.image = ""
        if blogsImg:
            singleblog.image = blogsImg
    params = {
        'productData': product,
    }

    return render(request, 'coreapp/index.html', params)

class productDetail(DetailView):
    model = Product
    template_name = "coreapp/product-details.html"
    context_object_name = "productData"

    def get_context_data(self, *args, **kwargs):
        product  = Product.objects.get(slug=self.kwargs.get("slug"))
        context = super().get_context_data(*args, **kwargs)
        context['productImg'] = ProductImage.objects.filter(product=product)
        return context