from django.db import models

# Create your models here.
class Quotes(models.Model):
    quote = models.CharField(max_length=500)
    author = models.CharField(max_length=20, default='Unknown')
    date_added = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    # String representation of the model
    def __str__(self):
        return f'{self.quote} - {self.author}'