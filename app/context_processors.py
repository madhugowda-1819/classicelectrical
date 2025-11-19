from app.models import ProductCategory

def categories_footer(request):
    return {
        'footer_categories': ProductCategory.objects.all()
    }