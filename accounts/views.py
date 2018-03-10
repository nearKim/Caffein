import datetime
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.template.loader import render_to_string

from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.tokens import account_activation_token
from core.models import OperationScheme
from .models import User
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


class UserUpdateView(LoginRequiredMixin,UserActionMixin, UpdateView):
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


def signup(request):
    now = datetime.date.today()
    os_object = OperationScheme.objects.latest('id')
    if now < os_object.get_start_date() or now > os_object.end_date:
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
