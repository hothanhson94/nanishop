from django.contrib import admin
import os
from django.conf import settings
from import_export.admin import ImportExportModelAdmin
from decimal import Decimal, InvalidOperation
from django.core.files.base import ContentFile
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import Category, Brand, Product
import logging

logger = logging.getLogger(__name__)

class CategoryForeignKeyWidget(ForeignKeyWidget):
    def clean(self, value, row=None, *args, **kwargs):
        return self.model.objects.get_or_create(slug=value)[0]

class BrandForeignKeyWidget(ForeignKeyWidget):
    def clean(self, value, row=None, *args, **kwargs):
        return self.model.objects.get_or_create(slug=value)[0]

class ProductResource(resources.ModelResource):
    category = fields.Field(
        column_name='category',
        attribute='category',
        widget=CategoryForeignKeyWidget(Category, 'slug')
    )
    brand = fields.Field(
        column_name='brand',
        attribute='brand',
        widget=BrandForeignKeyWidget(Brand, 'slug')
    )

    class Meta:
        model = Product
        fields = ('id', 'name', 'slug', 'description', 'price', 'category', 'brand', 'stock', 'available', 'top_selling', 'new', 'promotion', 'promotion_discount', 'image')

    def before_import_row(self, row, **kwargs):
        image_path = row.get('image')
        
        if image_path:
            # Chuyển đổi đường dẫn tương đối thành đường dẫn tuyệt đối từ BASE_DIR
            absolute_image_path = os.path.join(settings.BASE_DIR, image_path)
            print("Absolute Image Path:", absolute_image_path)  # In ra đường dẫn tuyệt đối
            # Kiểm tra xem tệp hình ảnh có tồn tại không
            if os.path.exists(absolute_image_path):
                with open(absolute_image_path, 'rb') as image_file:
                    row['image'] = ContentFile(image_file.read(), name=os.path.basename(absolute_image_path))
            else:
                logger.error(f"Image not found at {absolute_image_path}")
                row['image'] = None
        else:
            row['image'] = None

        # Chuyển đổi price sang Decimal với logging
        try:
            row['price'] = Decimal(row['price'])
        except (InvalidOperation, ValueError) as e:
            logger.error(f"Error converting price on row {row}: {e}")
            row['price'] = Decimal('0.00')  # Hoặc giá trị mặc định khác phù hợp

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = ProductResource
    list_display = ['name', 'slug', 'price', 'stock', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated', 'brand', 'category']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}
