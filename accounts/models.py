from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail

class Profile(models.Model):
    DEPARTMENT_CATEGORY = (
        ('hum', '인문대학'),
        ('soc', '사회과학대학'),
        ('nat', '자연과학대학'),
        ('nur', '간호대학'),
        ('mba', '경영대학'),
        ('eng', '공과대학'),
        ('agr', '농업생명과학대학'),
        ('art', '미술대학'),
        ('law', '법과대학'),
        ('edu', '사범대학'),
        ('che', '생활과학대학'),
        ('vet', '수의과대학'),
        ('pha', '약학대학'),
        ('mus', '음악대학'),
        ('med', '의과대학'),
        ('cls', '자유전공학부'),
        ('uni', '연합전공'),
        ('cor', '연계전공'),
    )

    STUDENT_CATEGORY = (
        ('u', '학부'),
        ('g', '대학원'),
        ('i', '교환학생'),
    )
    SEMESTER_CATEGORY = (
        ('s', '1학기'),
        ('f', '2학기')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, null=False, blank=False)
    birth_date = models.DateField(null=False, blank=False)
    phone = models.CharField(max_length=20, blank=False, null=False)
    student_no = models.CharField(max_length=12, blank=False, null=False)
    college = models.CharField(max_length=3, choices=DEPARTMENT_CATEGORY, null=False, blank=False)
    # department =
    student_category = models.CharField(max_length=1, choices=STUDENT_CATEGORY, null=False, blank=False)
    enroll_year = models.DateField(auto_now_add=True)
    enroll_semester = models.CharField(max_length=1, choices=SEMESTER_CATEGORY, null=False, blank=False)
    profile_pic = ProcessedImageField(blank=True, upload_to='profile_pic',
                                      processors=[Thumbnail(300,300)],
                                      format='JPEG',
                                      options={'quality': 60})

    def __str__(self):
        return self.name
