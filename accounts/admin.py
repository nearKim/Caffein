from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import (
    Profile,
    ActiveUser,
    Partners
)


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = '프로필'


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ('id', 'username', 'get_name', 'email', 'is_staff', 'get_student_no', 'get_college', 'get_department',
    'get_student_category', 'get_enroll_year', 'get_enroll_semester')
    list_display_links = ('id', 'username', 'get_name',)
    list_select_related = ('profile',)

    def get_name(self, instance):
        return instance.profile.name

    def get_student_no(self, instance):
        return instance.profile.student_no

    def get_college(self, instance):
        return instance.profile.get_college_display()

    def get_department(self, instance):
        return instance.profile.get_department_display()

    def get_student_category(self, instance):
        return instance.profile.get_student_category_display()

    def get_enroll_year(self, instance):
        return instance.profile.enroll_year

    def get_enroll_semester(self, instance):
        return instance.profile.get_enroll_semester_display()

    get_name.short_description = '이름'
    get_student_no.short_description = '학번'
    get_college.short_description = '단과대'
    get_department.short_description = '학과'
    get_student_category.short_description = '분류'
    get_enroll_year.short_description = '가입년도'
    get_enroll_semester.short_description = '가입학기'

    def get_inline_instances(self, request, obj=None):
        """
        We need to override the get_inline_instances method, so to display the inlines only in the edit form
        https://simpleisbetterthancomplex.com/tutorial/2016/11/23/how-to-add-user-profile-to-django-admin.html
        """
        if not obj:
            return list()
        return super(UserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(ActiveUser)
admin.site.register(Partners)
