# Generated by Django 2.0.2 on 2018-03-02 10:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import imagekit.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ActiveUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_active_year', models.DateField(auto_now=True, verbose_name='최종활동년도')),
                ('last_active_semester', models.CharField(choices=[('s', '1학기'), ('f', '2학기')], max_length=1, verbose_name='최종활동학기')),
                ('is_new', models.BooleanField(default=False, verbose_name='신입회원여부')),
                ('is_paid', models.BooleanField(default=False, verbose_name='입금확인')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Partners',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('partner_year', models.DateField(verbose_name='짝지 년도')),
                ('partner_semester', models.CharField(choices=[('s', '1학기'), ('f', '2학기')], max_length=1, verbose_name='짝지 학기')),
                ('score', models.IntegerField(default=0, verbose_name='점수')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('new_partner1', models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='new_partner1', to=settings.AUTH_USER_MODEL, verbose_name='아래짝지1')),
                ('new_partner2', models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='new_partner2', to=settings.AUTH_USER_MODEL, verbose_name='아래짝지2')),
                ('new_partner3', models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='new_partner3', to=settings.AUTH_USER_MODEL, verbose_name='아래짝지3')),
                ('old_partner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='old_partner', to=settings.AUTH_USER_MODEL, verbose_name='위짝지')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='이름')),
                ('birth_date', models.DateField(verbose_name='생년월일')),
                ('phone', models.CharField(max_length=20, verbose_name='전화번호')),
                ('student_no', models.CharField(max_length=12, verbose_name='학번')),
                ('college', models.CharField(choices=[('hum', '인문대학'), ('soc', '사회과학대학'), ('nat', '자연과학대학'), ('nur', '간호대학'), ('mba', '경영대학'), ('eng', '공과대학'), ('agr', '농업생명과학대학'), ('art', '미술대학'), ('law', '법과대학'), ('edu', '사범대학'), ('che', '생활과학대학'), ('vet', '수의과대학'), ('pha', '약학대학'), ('mus', '음악대학'), ('med', '의과대학'), ('cls', '자유전공학부'), ('uni', '연합전공'), ('cor', '연계전공')], max_length=3, verbose_name='단과대학')),
                ('department', models.CharField(choices=[('aa', '국어국문학과'), ('bb', '중어중문학과'), ('cc', '영어영문학과'), ('dd', '독어독문학과'), ('ee', '노어노문학과'), ('ff', '서어서문학과'), ('gg', '아시아언어문명학부'), ('hh', '불어불문학과'), ('ii', '언어학과'), ('jj', '국사학과'), ('kk', '동양사학과'), ('ll', '서양사학과'), ('mm', '철학과'), ('nn', '종교학과'), ('oo', '미학과'), ('pp', '고고미술사학과'), ('qq', '정치외교학부'), ('rr', '경제학부'), ('ss', '사회학과'), ('tt', '인류학과'), ('uu', '심리학과'), ('vv', '지리학과'), ('ww', '사회복지학과'), ('xx', '언론정보학과'), ('yy', '수리과학부'), ('zz', '통계학과'), ('ab', '물리천문학부'), ('ac', '화학부'), ('ad', '생명과학부'), ('ae', '지구환경과학부'), ('af', '간호학과'), ('ag', '경영학과'), ('ah', '건설환경공학부'), ('ai', '기계항공공학부'), ('aj', '재료공학부'), ('ak', '전기정보공학부'), ('al', '컴퓨터공학부'), ('am', '산업공학과'), ('an', '화학생물공학부'), ('ao', '건축학과'), ('ap', '건축공학과'), ('aq', '조선해양공학과'), ('ar', '에너지자원공학과'), ('as', '원자력공학과'), ('at', '식물생산과학부'), ('au', '산림과학부'), ('av', '응용생물화학부'), ('aw', '식품동물생명공학부'), ('ax', '바비오시스템소재학부'), ('ay', '조경지역시스템공학부'), ('az', '농경제사회학부'), ('bc', '동양화과'), ('bd', '서양화과'), ('be', '조소과'), ('bf', '공예과'), ('bg', '디자인과'), ('lw', '법학부'), ('11', '교육학과'), ('22', '국어교육과'), ('33', '영어교육과'), ('44', '불어교육과'), ('55', '독어교육과'), ('66', '사회교육과'), ('77', '역사교육과'), ('88', '지리교육과'), ('99', '윤리교육과'), ('00', '수학교육과'), ('1a', '물리교육과'), ('1b', '화학교육과'), ('1c', '생물교육과'), ('1d', '지구과학교육과'), ('1e', '체육교육과'), ('1f', '소비자아동학부'), ('1g', '식품영양학과'), ('1h', '의류학과'), ('1i', '수의예과'), ('1j', '수의학과'), ('1k', '약학과'), ('1l', '제약학과'), ('1m', '성악과'), ('1n', '작곡과(이론)'), ('1o', '작곡과(작곡)'), ('1p', '기악과'), ('1q', '국악과'), ('1r', '의예과'), ('1s', '의학과'), ('1t', '자유전공학부'), ('2a', '계산과학'), ('2b', '글로벌환경경영학'), ('2c', '기술경영'), ('2d', '영상매체예술'), ('2e', '정보문화학'), ('2f', '벤처경영학'), ('2g', '동아시아비교인문학'), ('3a', '중국학'), ('3b', '미국학'), ('3c', '러시아학'), ('3d', '라틴아메리카학'), ('3e', '유럽지역학'), ('3f', '뇌마음행동'), ('3g', '금융경제'), ('3h', '금융수학'), ('3i', '과학기술학'), ('3j', '공학바이오'), ('3k', '통합창의디자인'), ('3l', '고전문헌학'), ('3m', '인문데이터과학'), ('3n', '정치경제철학')], max_length=2, verbose_name='학과')),
                ('student_category', models.CharField(choices=[('u', '학부'), ('g', '대학원'), ('i', '교환학생')], max_length=1, verbose_name='학생 유형')),
                ('enroll_year', models.DateField(auto_now_add=True, verbose_name='가입년도')),
                ('enroll_semester', models.CharField(choices=[('s', '1학기'), ('f', '2학기')], max_length=1, verbose_name='가입학기')),
                ('profile_pic', imagekit.models.fields.ProcessedImageField(blank=True, upload_to='profile_pic')),
                ('is_first_paid', models.BooleanField(default=False, verbose_name='최초입금확인')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]