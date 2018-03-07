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

    def make_active_user(self, request, queryset):
        """
        Select Users from User table and make them acvie users.
        Do not confuse with User table's 'is_active' flag.
        """
        current_year = now().year
        current_semester = True if now().month in range(3, 9) else False

        for user in queryset:
            active_user = ActiveUser.objects.create(user=user, active_year=current_year,
                                                    active_semester=current_semester)
            active_user.save()
        self.message_user(request, "성공적으로 추가되었습니다.")

    make_active_user.short_description = '활동회원으로 추가'


admin.site.register(User, UserAdmin)

admin.site.register(ActiveUser)
admin.site.register(Partners)
