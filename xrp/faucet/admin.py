from django.contrib import admin

from xrp.faucet.models import Faucet, Instance


class FaucetAdmin(admin.ModelAdmin):
    pass


class InstanceAdmin(admin.ModelAdmin):
    pass


admin.site.register(Faucet, FaucetAdmin)
admin.site.register(Instance, InstanceAdmin)
