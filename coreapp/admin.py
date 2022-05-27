from django import forms
from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.models import User
from coreapp.models import Brand, Category, Contact, Product, ProductImage

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'status', 'created_at']
    exclude = ['slug']

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if len(form.base_fields) > 0:
            print(form.base_fields['parent'])
            form.base_fields['parent'].required = False
            return form
        return form
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'created_at']

# @admin.register(ProductImage)
# class ProductImageAdmin(admin.ModelAdmin):
#     # For set Initial Values in admin
#     def get_changeform_initial_data(self, request):
#         return {'user': request.user.id}

#     def product_name(self, obj):
#         return format_html('<a target="_blank" href="%s">%s</a>' % ('/admin/coreapp/product/' + str(obj.product.id) + '/change', obj.product.title))
#     product_name.admin_order_field = 'product'

#     list_display = ['product_name', 'path', 'status']

class ProdutImageTabulurInline(admin.TabularInline):
    model = ProductImage
    exclude = ['user', 'name', 'status']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # This is for change tempalte if you want to
    change_form_template = 'admin/product-edit.html'
    inlines = [
        ProdutImageTabulurInline
    ]

    # For set Initial Values in create/update forms
    # def get_changeform_initial_data(self, request):
    #     return {'user': request.user.id}
    
    # For Fields Shown in listing
    def created_on(self, obj):
        return obj.created_at.strftime("%d %b %Y")
    created_on.admin_order_field = 'created_at'

    def product_name(self, obj):
        return format_html('<a href="%s">%s</a>' % ('/admin/coreapp/product/' + str(obj.id) + '/change', obj.title))
    product_name.admin_order_field = 'blog'

    # For Fields Shown in Create/Update Forms
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if len(form.base_fields) > 0:
            form.base_fields['category'].queryset = Category.objects.filter(parent=None)
            form.base_fields["title"].label = "Product Title:"
            form.base_fields['is_published'].label = "Is Product Published:"
            return form
        return form
    
    # For Do operation before save operation
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        return super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        for inline_form in formset.forms:
            inline_form.instance.user = request.user
            inline_form.instance.name = "sample name"
        super().save_formset(request, form, formset, change)

    # def save_related(self, request, form, formsets, change):
    #     obj = form.save(commit=False)
    #     obj.user = request.user
    #     obj.name = "sample name"
    #     obj.save()
    #     super(ProductAdmin, self).save_related(request, form, formsets, change)

    list_display = ['created_on', 'category', 'brand', 'product_name', 'stock_count', 'actual_price', 'is_published']
    list_filter = ['created_at','category','brand']
    search_fields = ("title",)
    exclude = ['slug', 'user']

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    def added_on(self, obj):
        return obj.created_at.strftime("%d %b %Y")
    added_on.admin_order_field = 'created_at'
    
    # def blog_title(self, obj):
    #     return format_html('<a target="_blank" href="%s">%s</a>' % ('/admin/blog/blog/' + str(obj.blog.id) + '/change', obj.blog.title))
    # blog_title.admin_order_field = 'blog'

    # def comment(self, obj):
    #     return obj.title
    # comment.admin_order_field = 'title'

    list_display = ['added_on', 'name', 'email', 'phone', 'message']
    list_filter = ['email', 'phone']