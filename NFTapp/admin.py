from django.contrib import admin
from .models import User, NFTProduct, Topic, OwnerNFTProduct, Type
# Register your models here.

admin.site.register(User)
admin.site.register(Topic)
admin.site.register(NFTProduct)
admin.site.register(OwnerNFTProduct)
admin.site.register(Type)