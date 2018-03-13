from django.contrib import admin

from accounts.models import User
from partners.models import Partners, PartnerMeeting


class PartnerAdmin(admin.ModelAdmin):
    list_display = ['partner_year', 'partner_semester', 'get_old', 'get_new', 'score']
    list_filter = ['partner_year', 'partner_semester', 'old_partner']
    ordering = ['-partner_year', '-partner_semester', '-score']

    def get_old(self, queryset):
        return queryset.old_partner.user.name
    get_old.short_description = '위짝지'

    def get_new(self, queryset):
        return queryset.new_partner.user.name
    get_new.short_description = '아래짝지'


admin.site.register(Partners, PartnerAdmin)
admin.site.register(PartnerMeeting)