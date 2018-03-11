import datetime
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.template.loader import render_to_string

from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.tokens import account_activation_token
from core.models import OperationScheme
from .models import (
    User,
    ActiveUser
)
from django.views.generic import (
    UpdateView,
    DetailView
)
from .forms import SignUpForm


class UserActionMixin(object):
    fields = ('name', 'email', 'phone', 'student_no', 'college', 'department',
              'student_category', 'enroll_year', 'enroll_semester', 'profile_pic')

    @property
    def success_msg(self):
        return NotImplemented

    def form_valid(self, form):
        messages.info(self.request, self.success_msg)
        return super(UserActionMixin, self).form_valid(form)


class UserUpdateView(LoginRequiredMixin, UserActionMixin, UpdateView):
    model = User
    success_msg = "회원정보가 수정되었습니다."


class UserDetail(LoginRequiredMixin, DetailView):
    model = User


@login_required()
def user_delete_view(request):
    template = loader.get_template('accounts/user_delete_fake.html')
    return HttpResponse(template.render(context=None, request=request))


@login_required()
def account_index(request, user):
    return render(request, 'accounts/index.html', context={'user': user})


def new_signup(request):
    now = datetime.date.today()
    os_object = OperationScheme.objects.latest('id')
    if now < os_object.new_register_start() or now > os_object.new_register_end:
        return render(request, 'accounts/user_register_not_now.html')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = '[Caffe人] 서울대학교 인증 메일입니다.'
            mail_content = render_to_string('accounts/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': user.id,
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, mail_content, to=[to_email])
            email.send()
            return HttpResponse('이메일을 확인해주세요.')
    else:
        form = SignUpForm()
    return render(request, 'accounts/user_register.html', {'form': form})


def activate(request, uid, token):
    try:
        user = User.objects.get(id=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # TODO: add go to hompage url after deploy
        os_object = OperationScheme.objects.latest('id')

        return render(request, 'accounts/user_verified_now_pay.html', {'operation': os_object})
    else:
        return HttpResponse('Verification Link is invalid!')


@login_required()
def old_signup(request, pk):
    user = User.objects.get(id=pk)
    now = datetime.date.today()
    os_object = OperationScheme.objects.latest('id')
    if now < os_object.old_register_start or now > os_object.old_register_end:
        return render(request, 'accounts/user_register_not_now.html')
    if request.method == 'POST':
        HttpResponse('Bad Request.')
    else:
        return render(request, 'accounts/old_register.html', {'operation': os_object, 'user': user})


@login_required()
def old_now_pay(request, pk):
    old_user = User.objects.get(id=pk)
    current_os = OperationScheme.get_os_now()
    latest_os = OperationScheme.get_latest_os()
    # os_object = OperationScheme.objects.latest('id')
    if current_os.old_register_start is None or current_os.old_register_end is None:
        # Boss didn't input old register start date
        return HttpResponse('운영진이 기존 회원 재가입 기간을 아직 입력하지 않았습니다.')
    elif datetime.date.today() < current_os.old_register_start or datetime.date.today() > current_os.old_register_end:
        return HttpResponse('재가입 신청기간이 아닙니다.')
    elif latest_os.id == current_os.id:
        return HttpResponse("운영진이 아직 다음 학기 운영 스키마를 작성하지 않았습니다.")
    else:
        try:
            active_user = ActiveUser.objects.create(user=old_user,
                                                    active_year=latest_os.current_year,
                                                    active_semester=latest_os.current_semester,
                                                    is_new=False,
                                                    is_paid=False)
        except IntegrityError:
            return HttpResponse('이미 재가입신청 됨. 이런 페이지까지 만들기 귀찮다... 킹갓엠퍼러 콤퓨-타 공학과.. 웹개발 어케하냐 졸라힘드네 진짜.<br> 뒤로가기 누르셈ㅇㅇ')
        active_user.save()

    return render(request, 'accounts/old_user_now_pay.html', {'operation': current_os, 'user': old_user})



