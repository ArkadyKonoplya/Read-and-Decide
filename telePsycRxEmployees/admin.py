from django.contrib import admin
from .models import Role, TelePsycRxEmployee, Department, Division

admin.site.register(Division)
admin.site.register(Department)
admin.site.register(Role)
admin.site.register(TelePsycRxEmployee)



# Register your models here.
