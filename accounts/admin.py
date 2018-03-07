from django.contrib import admin
from django.utils.timezone import now
from .models import (
    User,
    ActiveUser,
    Partners
)


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
        current_year = now().year
        current_semester = 1 if now().month in range(3, 9) else 2

        for user in queryset:
            active_user = ActiveUser.objects.create(user=user, active_year=current_year,
                                                    active_semester=current_semester)
            active_user.save()
        self.message_user(request, "성공적으로 추가되었습니다.")

    make_active_user.short_description = '활동회원으로 추가'


class ActiveUserAdmin(admin.ModelAdmin):
    # TODO: make 'user' field to user table related field.
    list_display = ['user', 'active_semester', 'active_year', 'is_paid']
    actions = ['paid_check', 'unpaid_check', ]
    list_filter = ['active_semester', 'active_year', 'is_paid']

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
        # for active_user in queryset:

        pass
    paid_check.short_description = '입금확인'
    unpaid_check.short_description = '입금확인 취소'


admin.site.register(User, UserAdmin)
admin.site.register(ActiveUser, ActiveUserAdmin)
admin.site.register(Partners)
