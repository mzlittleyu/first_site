from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate,login
from .forms import LoginForm,User_RegistrationForm,UserProfileForm
from django.contrib.auth.decorators import login_required
from .models import UserProfile,UserInfo
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from .forms import UserInfoForm,UserProfileForm,UserForm
from django.core.urlresolvers import reverse
def user_login(request):
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            cd = login_form.cleaned_data
            user = authenticate(username = cd['username'],password = cd['password'])
            if user:
                login(request,user)
                return HttpResponse("Welcome to my secret base")
            else:
                return HttpResponse("Wow,Something is wrong")
    if request.method == "GET":
        login_form = LoginForm()
        return render(request,"account/login.html",{"form":login_form})
def register(request):
    if request.method == "POST":
        user_form = User_RegistrationForm(request.POST)#用户，邮箱，密码
        userprofile_form = UserProfileForm(request.POST)#出生日期，电话
        if user_form.is_valid()*userprofile_form.is_valid():
            new_user = user_form.save(commit=False)#密码需要手动存储
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            new_profile = userprofile_form.save(commit=False)#用户也必须手动存储
            new_profile.user = new_user
            new_profile.save()
            UserInfo.objects.create(user=new_user)
            '''userprofile_form2 = UserProfileForm(request.POST, instance=UserProfile(user=new_user))
            userprofile_form2.save()'''#另一种保存到数据库的方法
            return HttpResponseRedirect(reverse("account:user_login"))
        if user_form.is_valid():
            return HttpResponse("出生日期或者电话不对呢~")
        if userprofile_form.is_valid():
            return HttpResponse("输入的两次密码或许不对呢~或者换一个用户名吧~")
        else:
            return HttpResponse("哈哈哈，错误太多了，我也不知道你的注册哪里出问题了")
    else:
        user_form = User_RegistrationForm
        userprofile_form = UserProfileForm()
        return render(request,"account/register.html",{"form":user_form,"profile":userprofile_form})
def register2(request):
    if request.method =="POST":
        user_form = User_RegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return HttpResponse("6")
        else:
            return HttpResponse("cao")

    else:
        user_form = User_RegistrationForm()
        return render(request, "account/register2.html", {"form":user_form})
@login_required(login_url='/account/login/')
def myself(request):
    #user = User.objects.get(username=request.user.username)#request.user返回User对象且objects返回的是一个大User类！！！！1
    user = request.user
    userprofile = UserProfile.objects.get(user = user)#通过外键得到了一个用户档案大类！！！
    userinfo = UserInfo.objects.get(user = user)#同上，注意model里面的User
    return render(request,"account/myself.html",{"user":user,"userinfo":userinfo,"userprofile":userprofile})
@login_required(login_url='/account/login')
def edit_myself(request):
    #user = User.objects.get(username=request.user.username)
    user = request.user
    userprofile = UserProfile.objects.get(user = user)
    userinfo = UserInfo.objects.get(user = user)
    if request.method =="POST":
        user_form = UserForm(request.POST)
        userprofile_form = UserProfileForm(request.POST)
        userinfo_form = UserInfoForm(request.POST)
        if user_form.is_valid() * userprofile_form.is_valid() * userinfo_form.is_valid():
            user_cd = user_form.cleaned_data
            userprofile_cd = userprofile_form.cleaned_data
            userinfo_cd = userinfo_form.cleaned_data
            print(user_cd['email'])
            user.email = user_cd['email']
            userprofile.birth = userprofile_cd['birth']
            userprofile.phone = userprofile_cd['phone']
            userinfo.aboutme = userinfo_cd['aboutme']
            userinfo.address = userinfo_cd['address']
            userinfo.company = userinfo_cd['company']
            userinfo.profession = userinfo_cd['profession']
            userinfo.school = userinfo_cd['school']
            user.save()
            userprofile.save()
            userinfo.save()
        return HttpResponseRedirect('/account/my-information/')
    else:
        #user_form = UserForm(instance=request.user)另一种显示邮箱信息的方法
        user_form = UserForm(initial={"email":user.email})
        userprofile_form = UserProfileForm(initial={"birth":userprofile.birth,"phone":userprofile.phone})
        userinfo_form = UserInfoForm(initial={"address":userinfo.address,"school":userinfo.school,"company":userinfo.company,
                                              "profession":userinfo.profession,"aboutme":userinfo.aboutme})
        return render(request,"account/edit_myself.html",{"user_form":user_form,"userprofile_form":userprofile_form,
                                                          "userinfo_form":userinfo_form})
@login_required(login_url='/account/login')
def my_image(request):
    if request.method == "POST":
        img = request.POST['img']
        userinfo = UserInfo.objects.get(user = request.user.id)
        userinfo.photo = img
        userinfo.save()
        return HttpResponse("1")
    else:
        return render(request,'account/imagecrop.html',)
def register_test(request):
        return render(request,'account/register_test.html')
def arriving_at_homepage2(request):
    return render(request,'account/home.html')