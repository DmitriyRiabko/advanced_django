from django.db import models
from django.utils.text import slugify
# Create your models here.



class Category(models.Model):
    name = models.CharField(max_length=250,db_index=True)
    parent = models.ForeignKey('self',on_delete=models.CASCADE, related_name='children',blank=True,bull=True )
    slug = models.SlugField(max_length=250,unique=True,null=False,editable=True)
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