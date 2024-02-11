from django.contrib import admin

# Register your models here.
# Register your models here.
from .models import *

admin.site.register(CustomUser)
admin.site.register(Capture)
admin.site.register(Alerte)