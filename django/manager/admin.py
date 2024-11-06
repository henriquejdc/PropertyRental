# Django imports
from django.contrib import admin

# Project imports
from manager.models import (
    Owner,
    Host,
    Property,
    Reservation,
    SeazoneCommission,
    HostCommission,
    OwnerCommission,
)
from property_rental.admin import property_rental_admin as admin_site


class BaseAdmin(admin.ModelAdmin):  # pragma: no cover
    def get_list_display(self, request):
        fields = [field.name for field in self.model._meta.fields]
        return fields

admin_site.register(Owner, BaseAdmin)
admin_site.register(Host, BaseAdmin)
admin_site.register(Property, BaseAdmin)
admin_site.register(Reservation, BaseAdmin)
admin_site.register(SeazoneCommission, BaseAdmin)
admin_site.register(HostCommission, BaseAdmin)
admin_site.register(OwnerCommission, BaseAdmin)
