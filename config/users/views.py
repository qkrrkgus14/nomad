import os
import requests
from django.views import View
from django.views.generic import FormView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.core.files.base import ContentFile
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import PasswordChangeView

from . import forms, models, mixins

# 로그인 FormView 형식 -> 니콜라스 선생님은 아래의 주석처리된 LoginView보다 FormView를 더 선호한다.
class LoginView(mixins.LoggedOutOnlyView, FormView):
    template_name = 'users/login.html'
    form_class = forms.LoginForm
    # success_url = reverse_lazy("core:home")
    initial = {
        'email':'qkrrkgus15@gmail.com',
    }

    def get_success_url(self):
        next_arg = self.request.GET.get("next")
        if next_arg is not None:
            return next_arg
        else:
            return reverse("core:home")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)

'''
class LoginView(View):
    def get(self,request):     # initial -> 초기값을 만들어줌
        form = forms.LoginForm(initial={"email":"qkrrkgus14@naver.com"})
        return render(request, "users/login.html", {'form':form })

    def post(self,request):
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                redirect(reverse("core:home"))

        return render(request, "users/login.html", {"form":form})
'''


# 로컬 회원가입
class SignUpView(FormView):

    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        user.verify_email()
        return super().form_valid(form)


def log_out(request):
    messages.info(request, 'See you later')
    logout(request)
    return redirect(reverse('core:home'))


def complete_verification(request,key):
    try:
        user = models.User.objects.get(email_secret=key)
        user.email_verified = True
        user.email_secret = ""
        user.save()
        # to do: add success message(django message framework 검색)
    except models.User.DoesNotExist:
        # to do: add error message(django message framework 검색)
        pass
    return redirect(reverse("core:home"))


# 깃허브 로그인
def github_login(request):
    client_id = os.environ.get("GH_ID")
    redirect_url = "http://127.0.0.1:8000/users/login/github/callback"
    return redirect(
        f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_url}&scope=read:user"
    )

class GithubException(Exception):
    pass

# 깃허브 로그인시 콜백 함수
def github_callback(request):
    try:
        client_id = os.environ.get("GH_ID")
        client_secret = os.environ.get("GH_SECRET")
        code = request.GET.get("code", None)
        if code is not None:
            token_request = requests.post(
                f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
                headers={"Accept":"application/json"},
            )

            result_json = token_request.json()
            error = result_json.get("error", None)
            if error is not None:
                raise GithubException("Can't get access token")
            else:
                access_token = result_json.get("access_token")
                profile_request = requests.get(f"https://api.github.com/user",
                                           headers = {
                                           "Authorization" : f"token {access_token}",
                                           "Accept": "application/json",
                                           },
                                           )
                profile_json = profile_request.json()
                username = profile_json.get('login', None)
                if username is not None:
                    name = profile_json.get('name')
                    email = profile_json.get('email')
                    # 각자 깃허브 메인 주소에서 이메일주소가 공개이메일로 설정이 안되어 있을 수도 있다. (None)
                    ''' 에러 페이지 주소로 넘겨 주어야 할 것 이다.
                    if email == None:
                        return render
                    '''
                    bio = profile_json.get('bio')
                    try:
                        user = models.User.objects.get(email=email)
                        if user.login_method != models.User.LOGIN_GITHUB:
                            raise GithubException(
                                f'Please log in with : {user.login_method}'
                            )
                    except models.User.DoesNotExist:
                        user = models.User.objects.create(
                            email=email,
                            first_name=name,
                            username=email,
                            bio=bio,
                            login_method=models.User.LOGIN_GITHUB,
                            email_verified=True,
                        )
                        user.set_unusable_password()
                        user.save()
                    login(request, user)
                    messages.success(request, f"Welcome back {user.username}")
                    return redirect(reverse('core:home'))
                else:
                    raise GithubException("Can't get you profile")
        else:
            raise GithubException("Can't get code")
    except GithubException as e:
        messages.error(request, e)
        return redirect(reverse('users:login'))


def kakao_login(request):
    client_id = os.environ.get("KAKAO_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
    return redirect(f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code")

class KakaoException(Exception):
    pass

def kakao_callback(request):
    try:
        code = request.GET.get("code")
        client_id = os.environ.get("KAKAO_ID")
        redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
        token_request = requests.get(f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}")
        token_json = token_request.json()
        error = token_json.get("error", None)
        if error is not None:
            raise KakaoException("Can't get authorization code.")
        access_token = token_json.get("access_token")
        profile_request = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization":f"Bearer {access_token}"},
        )

        profile_json = profile_request.json()
        profile_json = profile_json.get("kakao_account", None)
        email = profile_json.get("email", None)
        if email is None:
            raise KakaoException("Please also give me you email")

        profile = profile_json.get("profile")
        nickname = profile.get("nickname")
        profile_image = profile.get("profile_image_url")
        try:
            user = models.User.objects.get(email=email)
            if user.login_method != models.User.LOGIN_KAKAO:
                raise  KakaoException(f"Please log in with : {user.login_method}")
        except models.User.DoesNotExist:
            user = models.User.objects.create(
                email=email,
                username=email,
                first_name=nickname,
                login_method=models.User.LOGIN_KAKAO,
                email_verified=True,
            )
            user.set_unusable_password()
            user.save()
            if profile_image is not None:
                photo_request = requests.get(profile_image)
                print(photo_request.content)
                user.avatar.save(f"{nickname}-avatar", ContentFile(photo_request.content))
        messages.success(request, f"Welcome back {user.username}")
        login(request, user)
        return redirect(reverse("core:home"))
    except KakaoException as e:
        messages.error(request,e)
        return redirect(reverse("users:login"))

class UserProfileView(DetailView):
    model = models.User
    context_object_name = "user_obj"

class UpdateProfileView(mixins.LoggedInOnlyView,SuccessMessageMixin,UpdateView):
    model = models.User
    template_name = "users/update-profile.html"
    fields = (
        "email",
        'first_name',
        'last_name',
        'gender',
        'bio',
        'birthdate',
        'language',
        'currency',
    )
    success_message = "Profile Updated!"

    def get_object(self, queryset=None):
        return self.request.user

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["birthdate"].widget.attrs = {"placeholder":"Birthdate"}
        return form
    '''
    def form_valid(self, form):
        email = form.cleaned_date.get("email")
        self.object.username = email
        self.object.save()
        return super().form_valid(form)
    '''


class UpdatePassword(
    mixins.LoggedInOnlyView,
    mixins.EmailLoginOnlyView,
    SuccessMessageMixin,
    PasswordChangeView,
):
    template_name = "users/update-password.html"
    success_message = "Password Updated!"

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["old_password"].widget.attrs = {"placeholder":"Current Password"}
        form.fields["new_password1"].widget.attrs = {"placeholder": "New Password"}
        form.fields["new_password2"].widget.attrs = {"placeholder": "Confirm New Password"}
        return form

    # success_url = "user" 설정해야함

    def get_success_url(self):
        return self.request.user.get_absolute_url()
