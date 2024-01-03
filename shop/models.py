from django.db import models
from django.db.models.query import QuerySet
from django.utils.text import slugify
import random
import string
from django.urls import reverse
# Create your models here.

def rand_slug():
    return ''.join(random.choice.string.ascii_lowercase + string.digits)

class Category(models.Model):
    name = models.CharField(max_length=250,db_index=True)
    parent = models.ForeignKey('self',on_delete=models.CASCADE, related_name='children',blank=True,null=True )
    slug = models.SlugField('URL',max_length=250,unique=True,null=False,editable=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        unique_together = (['slug','parent'])
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        
        
        
    def __str__(self) -> str:
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k=k.parent
        return ' > '.join(full_path[::-1])
    
    
    def save(self, *args, **kwargs):
        if not self.save_base:
            self.slug = slugify(rand_slug() + '-pickBetter'+ self.name)
        super(Category, self).save(*args,**kwargs)
        
    
    # def get_absolute_url(self):
    #     return reverse("model_detail", kwargs={"pk": self.pk})
    
    
class Product(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='products')
    title = models.CharField(max_length=250)
    brand = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    slug = models.SlugField('URL',max_length=250,unique=True,null=False,editable=True)
    price = models.DecimalField(max_digits=7,decimal_places=2,default=99.99)
    image = models.ImageField(upload_to='products/products/%Y/%m/%d')
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        
    def __str__(self) -> str:
        return self.title
    
    
    # def get_absolute_url(self):
    #     return reverse("model_detail", kwargs={"pk": self.pk})
    
class ProductManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super(ProductManager,self).get_queryset().filter(available=True)
    
    
class ProductProxy(Product):
    
    objects = ProductManager()
    
    class Meta:
        proxy = True