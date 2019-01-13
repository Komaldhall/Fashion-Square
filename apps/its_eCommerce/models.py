from django.db import models

class Category(models.Model):
    name=models.CharField(max_length=100)
    # slug = models.SlugField(max_length=150, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    catType=models.CharField(max_length=100)
    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.name) # set the slug explicitly
    #     super(Article, self).save(*args, **kwargs) # call Django's save()
    
class Product(models.Model):
    name=models.CharField(max_length=100)
    # slug = models.SlugField(max_length=150, unique=True)
    link=models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    price=models.IntegerField(default=0)
    category=models.ForeignKey(Category, related_name="products", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.name) # set the slug explicitly
    #     super(Article, self).save(*args, **kwargs) # call Django's save()

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    # birth=models.CharField(max_length=10)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Order(models.Model):
    user = models.ForeignKey(User, related_name="orders", on_delete=models.CASCADE)
    product = models.ManyToManyField(Product, related_name="orderedProducts")
    quantity=models.IntegerField(default=0)
    paid=models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)




 
