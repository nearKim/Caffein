from django.contrib import admin
from django.utils.timezone import now
from .models import (
    User,
    ActiveUser,
    Partners
)

current_year = now().year
current_semester = 1 if now().month in range(3, 9) else 2


class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'phone', 'student_no', 'college', 'department',
                    'student_category', 'enroll_year', 'enroll_semester']
    actions = ['make_active_user', ]
    search_fields = ['name', 'email', 'phone']
    list_filter = ('college', 'department', 'student_category', 'enroll_year', 'enroll_semester')

    def make_active_user(self, request, queryset):
        """
        Select Users from User table and make them acvie users.
        Do not confuse with User table's 'is_active' flag.
        """

        for user in queryset:
            if user.enroll_year == current_year and user.enroll_semester == current_semester:
                new_active_user = ActiveUser.objects.create(user=user,
                                                            is_new=True,
                                                            active_year=current_year,
                                                            active_semester=current_semester)
                new_active_user.save()
            else:
                old_active_user = ActiveUser.objects.create(user=user,
                                                            is_new=False,
                                                            active_year=current_year,
                                                            active_semester=current_semester)
                old_active_user.save()
        self.message_user(request, "성공적으로 추가되었습니다.")

    make_active_user.short_description = '활동회원으로 추가'


class ActiveUserAdmin(admin.ModelAdmin):
    list_display = ['get_username', 'active_semester', 'active_year', 'is_new', 'is_paid']
    list_filter = ['active_semester', 'active_year', 'is_new', 'is_paid']
    search_fields = ['user__name']
    actions = ['paid_check', 'unpaid_check', 'make_partners']

    def get_username(self, queryset):
        return queryset.user.name

    get_username.short_description = '회원 이름'

    def paid_check(self, request, queryset):
        for active_user in queryset:
            active_user.is_paid = True
            active_user.save()
        self.message_user(request, "총 {}명의 활동회원이 입금확인 되었습니다.".format(queryset.count()))

    def unpaid_check(self, request, queryset):
        for active_user in queryset:
            active_user.is_paid = False
            active_user.save()
        self.message_user(request, "총 {}명의 활동회원의 입금확인이 취소되었습니다.".format(queryset.count()))

    def make_partners(self, request, queryset):
        if queryset.count() < 2 or queryset.count() > 4:
            self.message_user(request, "짝지로 묶을 회원들의 숫자를 다시 확인해보세요. 위,아래짝지 포함 2~4명 이어야 합니다.")
            return NotImplemented
        if not queryset.filter(is_new=False).count() == 1:
            self.message_user(request, "위짝지는 반드시 1명이어야 합니다.")
            return NotImplemented

        old_member = queryset.get(is_new=False)
        new_members = queryset.filter(is_new=True).values_list('id', flat=True)
        partner = Partners.objects.create(partner_year=current_year,
                                          partner_semester=current_semester,
                                          old_partner=old_member,
                                          new_partner=list(new_members))
        partner.save()
        self.message_user(request, "짝지가 생성 되었습니다.")

    paid_check.short_description = '입금확인'
    unpaid_check.short_description = '입금확인 취소'
    make_partners.short_description = '짝지로 만들기'


class PartnerAdmin(admin.ModelAdmin):
    list_display = ['partner_year', 'partner_semester', 'old_partner', 'new_partner', 'score']
    list_filter = ['partner_year', 'partner_semester', 'old_partner']
    ordering = ['-partner_year', '-partner_semester', '-score']


admin.site.register(User, UserAdmin)
admin.site.register(ActiveUser, ActiveUserAdmin)
admin.site.register(Partners, PartnerAdmin)
