import os

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.db import models
from .models import user, userData
from .serializers import UserSerializer, UserDataSerializer, UserShowDataSerializer
from rest_framework import viewsets, mixins
from django.http import JsonResponse
from rest_framework.pagination import PageNumberPagination
import json


# Create your views here.
def get_users(request):
    name = request.GET.get('name')
    if name:
        users = user.objects.filter(name=name)
    else:
        users = user.objects.all()
    userlist = []
    for user1 in users:
        user_dict = {
            'name': user1.name,
            'img': user1.img.url if user1.img else None,
            'account': user1.account,
            'password': user1.password
        }
        userlist.append(user_dict)
    return JsonResponse(userlist, safe=False)


@csrf_exempt
def delete(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data)
            id = data.get('id')
            if id:
                user.objects.filter(id=id).delete()
                return JsonResponse({'status': 'success', 'message': '删除成功'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Name 字段缺失'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': '无效的 JSON 数据'}, status=400)
    # 处理非 POST 请求
    return JsonResponse({'status': 'error', 'message': '只允许 POST 请求'}, status=405)


@csrf_exempt
def register(request):
    print("1")
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data)
            name = data.get('name')
            account = data.get('account')
            password = data.get('password')

            # 创建新用户
            if name != '' and account != '' and password != '':
                user1 = user(name=name, account=account, password=password)
                user1.save()
                return JsonResponse({'message': '注册成功'}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'message': '无效的 JSON 数据'}, status=400)
    return JsonResponse({'message': '只支持 POST 请求'}, status=405)


@csrf_exempt
def check_username(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        if user.objects.filter(name=username).exists():
            return JsonResponse({'isDuplicate': True})
        return JsonResponse({'isDuplicate': False})


@csrf_exempt
def updateUserInfo(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        account = data.get('account')
        name = data.get('name')
        try:
            user1 = user.objects.get(account=account)
            if name:
                user1.name = name
                user1.save()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'更新用户信息失败: {str(e)}'}, status=500)
    return JsonResponse({'status': 'error', 'message': '只支持 POST 请求'}, status=405)


@csrf_exempt
def update_password(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        old_password = data.get('oldPassword')
        new_password = data.get('newPassword')
        try:
            user1 = user.objects.get(name=username)
            if user1.check_password(old_password):
                user1.set_password(new_password)
                user1.save()
                return JsonResponse({'status': 'success'})
            return JsonResponse({'status': 'error', 'message': '原始密码错误'})
        except user.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': '用户不存在'})


@csrf_exempt
def uploadAvatar(request):
    """
    处理头像上传的视图函数
    """
    if request.method == 'POST':
        # 获取上传的文件
        file = request.FILES.get('avatar')
        # 获取用户账号
        account = request.POST.get('account')

        if not file:
            return JsonResponse({'status': 'error', 'message': '未找到上传的文件'}, status=400)

        if not account:
            return JsonResponse({'status': 'error', 'message': '未提供用户账号'}, status=400)

        try:
            # 根据账号查找用户
            user1 = user.objects.get(account=account)
            # 保存文件
            user1.img = file
            user1.save()

            # 构建头像的访问 URL
            img_url = user1.img.url
            return JsonResponse({'status': 'success', 'imgUrl': 'http://127.0.0.1:8000/'+img_url})

        except user.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': '未找到该用户'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'文件保存失败: {str(e)}'}, status=500)

    return JsonResponse({'status': 'error', 'message': '只支持 POST 请求'}, status=405)


@csrf_exempt
def update_myself(request):
        try:
            data = json.loads(request.body)
            account = data.get('account')
            myself = data.get('myself')

            user1 = user.objects.get(account=account)
            user1.myself = myself
            user1.save()

            return JsonResponse({'status': 'success'}, status=200)
        except user.DoesNotExist:
            return JsonResponse({'status': 'failed', 'message': '用户不存在'}, status=405)
        except Exception as e:
            return JsonResponse({'status': 'failed', 'message': str(e)}, status=500)
class UserViews(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        return user.objects.all()


class UserDataViews(viewsets.ModelViewSet):
    serializer_class = UserDataSerializer

    def get_queryset(self):
        return userData.objects.all()


"""
主键调用外键
"""


class UserShowDataViews(viewsets.ModelViewSet):
    serializer_class = UserShowDataSerializer

    def get_queryset(self):
        return user.objects.all()
