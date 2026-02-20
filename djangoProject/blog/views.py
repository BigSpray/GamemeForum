import logging
import os

from django.core.files.storage import FileSystemStorage
from django.utils.html import escape
from django.forms import model_to_dict
from django.shortcuts import render
from .serializer import BlogSerializer
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.db import models
from .models import blog, blogtype
from rest_framework import viewsets, mixins
from django.http import JsonResponse, HttpResponse
from rest_framework.pagination import PageNumberPagination
import json
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from djangoProject import settings


# Create your views here.


def get_blogs(request):
    try:
        title = request.GET.get('title')
        if title:
            blogs = blog.objects.filter(title__icontains=title)
        else:
            # 查询所有的 blog 记录
            blogs = blog.objects.all()
        blog_list = []
        for single_blog in blogs:
            # 将每个 blog 模型实例转换为字典
            blog_dict = model_to_dict(single_blog)
            # 处理 ImageField 类型的字段，将其转换为可访问的 URL
            blog_dict['img'] = single_blog.img.url if single_blog.img else None
            blog_dict['video'] = single_blog.video.url if single_blog.video else None  # 处理 video 字段
            # 将 last_edit_time 转换为上海时间并格式化为字符串
            if single_blog.last_edit_time:
                local_time = timezone.localtime(single_blog.last_edit_time)
                blog_dict['last_edit_time'] = local_time.strftime('%Y年%m月%d日 %H:%M')
            blog_list.append(blog_dict)
        # 返回包含所有 blog 数据的 JSON 响应
        return JsonResponse({'blogs': blog_list}, safe=False)
    except Exception as e:
        # 若出现异常，返回错误信息和 500 状态码
        return JsonResponse({'error': str(e)}, status=500)


def get_blogtypes(request):
    try:
        # 查询所有的 blog 记录
        blogtypes = blogtype.objects.all()
        blogtypes_list = []
        for single_blog in blogtypes:
            # 将每个 blog 模型实例转换为字典
            blog_dict = model_to_dict(single_blog)
            blogtypes_list.append(blog_dict)
        # 返回包含所有 blog 数据的 JSON 响应
        return JsonResponse({'blogtypes': blogtypes_list}, safe=False)
    except Exception as e:
        # 若出现异常，返回错误信息和 500 状态码
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def deletetype(request):
    if request.method == 'POST':
        print(request.body)
        try:
            select_value = request.body.decode('utf-8')
            if select_value:
                blogtype.objects.filter(type=select_value).delete()
                return JsonResponse({'status': 'success', 'message': '删除成功'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Name 字段缺失'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': '无效的 JSON 数据'}, status=400)
    # 处理非 POST 请求
    return JsonResponse({'status': 'error', 'message': '只允许 POST 请求'}, status=405)


logger = logging.getLogger(__name__)


@csrf_exempt
def update_blog(request, pk):
    try:
        if request.method == 'PUT':
            logger.info(f"Received PUT request for blog ID: {pk}")
            try:
                data = json.loads(request.body)
                logger.info(f"Parsed data: {data}")
            except json.JSONDecodeError as e:
                logger.error(f"JSON 解析错误: {e}, 请求体: {request.body}")
                return JsonResponse({'error': '无效的 JSON 数据'}, status=400)
            try:
                single_blog = blog.objects.get(id=pk)
                logger.info(f"Found blog: {single_blog}")
                title = data.get('title')
                content = data.get('content')
                print(title)
                print(escape(title))
                print(content)
                print(escape(content))
                if title:
                    single_blog.title = title  # 转义标题
                    logger.info(f"Updated title to {single_blog.title}")
                if content:
                    single_blog.content = content  # 转义内容
                    logger.info(f"Updated content to {single_blog.content}")
                single_blog.last_edit_time = timezone.now()  # 手动更新时间
                single_blog.full_clean()
                single_blog.save()
                logger.info(f"Blog with ID {pk} updated successfully")
                return JsonResponse({'message': '更新成功'}, status=200)
            except blog.DoesNotExist:
                logger.error(f"博客不存在，ID: {pk}")
                return JsonResponse({'error': '博客不存在'}, status=404)
            except Exception as e:
                logger.error(f"数据验证或保存错误: {e}")
                return JsonResponse({'error': str(e)}, status=400)
    except Exception as e:
        logger.error(f"服务器内部错误: {e}")
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def deleteblog(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data)
            id = data.get('id')
            if id:
                blog.objects.filter(id=id).delete()
                return JsonResponse({'status': 'success', 'message': '删除成功'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Name 字段缺失'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': '无效的 JSON 数据'}, status=400)
    # 处理非 POST 请求
    return JsonResponse({'status': 'error', 'message': '只允许 POST 请求'}, status=405)


@csrf_exempt
def addtype(request):
    print("1")
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data)
            gettype = data.get('type')
            # 创建新用户
            if gettype != '':
                type1 = blogtype(type=gettype)
                type1.save()
                return JsonResponse({'message': '添加成功'}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'message': '无效的 JSON 数据'}, status=400)
    return JsonResponse({'message': '只支持 POST 请求'}, status=405)


@csrf_exempt
def change_horse_status(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            id = data.get('id')
            horse = int(data.get('horse'))
            blog1 = blog.objects.get(id=id)
            blog1.horse = horse
            blog1.save()
            return JsonResponse({'success': True})
        except (blog.DoesNotExist, ValueError):
            return JsonResponse({'success': False, 'message': '博客不存在或数据格式错误'})
    return JsonResponse({'success': False, 'message': '请求方法错误'})


@csrf_exempt
def addma(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            img1 = data.get('img')
            horse1 = 1
            blog1 = blog.objects.create(img=img1, horse=horse1, type='走马灯', forblog='走马灯')
            blog1.save()
            return JsonResponse({'success': True})
        except (blog.DoesNotExist, ValueError):
            return JsonResponse({'success': False, 'message': '博客不存在或数据格式错误'})
    return JsonResponse({'success': False, 'message': '请求方法错误'})


@csrf_exempt
def change_recommend_status(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            id = data.get('id')
            recommend = int(data.get('recommend'))
            blog1 = blog.objects.get(id=id)
            blog1.recommend = recommend
            blog1.save()
            return JsonResponse({'success': True})
        except (blog.DoesNotExist, ValueError):
            return JsonResponse({'success': False, 'message': '博客不存在或数据格式错误'})
    return JsonResponse({'success': False, 'message': '请求方法错误'})


class BlogFavoriteView(APIView):
    def post(self, request, blog_id):
        try:
            blog_obj = blog.objects.get(id=blog_id)
            blog_obj.collection += 1
            blog_obj.save()
            return Response({'message': '收藏成功', 'collection_count': blog_obj.collection}, status=status.HTTP_200_OK)
        except blog.DoesNotExist:
            return Response({'message': '博客不存在'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, blog_id):
        try:
            blog_obj = blog.objects.get(id=blog_id)
            if blog_obj.collection > 0:
                blog_obj.collection -= 1
                blog_obj.save()
            return Response({'message': '取消收藏成功', 'collection_count': blog_obj.collection},
                            status=status.HTTP_200_OK)
        except blog.DoesNotExist:
            return Response({'message': '博客不存在'}, status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
def viewadd(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            id = data.get('id')
            if id:
                blog_obj = blog.objects.get(id=id)
                blog_obj.increase_view()  # 增加浏览量
                return JsonResponse({'status': 'success', 'message': '更新成功'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Name 字段缺失'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': '无效的 JSON 数据'}, status=400)
    # 处理非 POST 请求
    return JsonResponse({'status': 'error', 'message': '只允许 POST 请求'}, status=405)


logger = logging.getLogger(__name__)



@csrf_exempt
def uploadEditorImage(request):
    if request.method == 'POST':
        try:
            imgUrls = []
            fs = FileSystemStorage()
            logger.info('接收到的请求内容:', request.POST)  # 打印请求内容
            logger.info('接收到的文件:', request.FILES)  # 打印接收到的文件
            if 'images' not in request.FILES:
                logger.error('未接收到图片文件')
                return JsonResponse({'status': 'error', 'message': '未接收到图片文件'})
            for image in request.FILES.getlist('images'):
                try:
                    logger.info(f'开始保存图片: {image.name}')
                    filename = fs.save(image.name, image)
                    imgUrl = fs.url(filename)
                    imgUrls.append(imgUrl)
                    logger.info(f'图片 {image.name} 保存成功，URL: {imgUrl}')
                except Exception as e:
                    logger.error(f'保存图片 {image.name} 时出错: {str(e)}')
            if not imgUrls:
                return JsonResponse({'status': 'error', 'message': '没有成功保存任何图片'})
            return JsonResponse({'status':'success', 'imgUrls': imgUrls})
        except Exception as e:
            logger.error(f'上传图片时出错: {str(e)}')
            return JsonResponse({'status': 'error','message': str(e)})
    return JsonResponse({'status': 'error','message': '无效的请求方法'})


@csrf_exempt
def saveBlog(request):
    if request.method == 'POST':
        try:
            # 获取封面文件
            cover_file = request.FILES.get('img')
            # 获取视频文件
            video_file = request.FILES.get('video')
            # 获取其他表单数据
            title = request.POST.get('title')
            name = request.POST.get('name')
            blog_type = request.POST.get('type')
            content = request.POST.get('content')
            forblog = request.POST.get('forblog')

            new_blog = blog(
                title=title,
                img=cover_file,
                name=name,
                type=blog_type,
                content=content,
                video=video_file,
                forblog=forblog,
            )
            new_blog.last_edit_time = timezone.now()  # 手动更新时间
            new_blog.save()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            logger.error(f"保存博客时出错: {str(e)}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)


@csrf_exempt
def update_blogs_username(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        old_name = data.get('oldName')
        new_name = data.get('newName')

        if old_name and new_name:
            try:
                # 更新所有使用旧名字的博客的 name 字段
                blogs = blog.objects.filter(name=old_name)
                blogs.update(name=new_name)
                return JsonResponse({'status': 'success'})
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
        else:
            return JsonResponse({'status': 'error', 'message': '缺少必要的参数'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': '只支持 POST 请求'}, status=405)
