import json
import os

from .serializers import ImagesSerializer, VideosSerializer
from rest_framework import viewsets, mixins
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import images, videos, comment, feedback, AIRVC

# Create your views here.

from django.http import JsonResponse
from .models import images


@csrf_exempt
def getimages(request):
    try:
        image_objects = images.objects.all()
        image_list = []
        for image_obj in image_objects:
            image_info = {
                'id': image_obj.id,
                'img_url': image_obj.img.url if image_obj.img else None
            }
            image_list.append(image_info)
        return JsonResponse({'images': image_list})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def getvideos(request):
    try:
        video_objects = videos.objects.all()
        video_list = []
        for video_obj in video_objects:
            video_info = {
                'id': video_obj.id,
                'video_url': video_obj.video.url if video_obj.video else None
            }
            video_list.append(video_info)
        return JsonResponse({'videos': video_list})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def deleteimg(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data)
            id = data.get('id')
            if id:
                images.objects.filter(id=id).delete()
                return JsonResponse({'status': 'success', 'message': '删除成功'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Name 字段缺失'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': '无效的 JSON 数据'}, status=400)
    # 处理非 POST 请求
    return JsonResponse({'status': 'error', 'message': '只允许 POST 请求'}, status=405)


# @csrf_exempt
# def deletevideo(request):
#     if request.method == 'POST':
#         try:
#             video_id = request.POST.get('id')
#             videos.objects.filter(id=video_id).delete()
#             return JsonResponse({'status': 'success', 'message': '删除成功'})
#         except Exception as e:
#             return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
#     return JsonResponse({'status': 'error', 'message': '只允许 POST 请求'}, status=405)
@csrf_exempt
def deletevideo(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data)
            id = data.get('id')
            if id:
                videos.objects.filter(id=id).delete()
                return JsonResponse({'status': 'success', 'message': '删除成功'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Name 字段缺失'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': '无效的 JSON 数据'}, status=400)
    # 处理非 POST 请求
    return JsonResponse({'status': 'error', 'message': '只允许 POST 请求'}, status=405)


@csrf_exempt
def uploadimg(request):
    if request.method == 'POST':
        try:
            # 从 request.FILES 中获取上传的文件
            if 'file' in request.FILES:
                img_file = request.FILES['file']
                new_img = images(img=img_file)
                new_img.save()
                return JsonResponse({'status': 'success', 'message': '上传成功'})
            else:
                return JsonResponse({'status': 'error', 'message': '未找到上传的文件'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    # 处理非 POST 请求
    return JsonResponse({'status': 'error', 'message': '只允许 POST 请求'}, status=405)


@csrf_exempt
def uploadvideo(request):
    if request.method == 'POST':
        try:
            # 从 request.FILES 中获取上传的文件
            if 'file' in request.FILES:
                video_file = request.FILES['file']
                new_video = videos(video=video_file)
                new_video.save()
                return JsonResponse({'status': 'success', 'message': '上传成功'})
            else:
                return JsonResponse({'status': 'error', 'message': '未找到上传的文件'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    # 处理非 POST 请求
    return JsonResponse({'status': 'error', 'message': '只允许 POST 请求'}, status=405)


@csrf_exempt
def getcomments(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            blog_id = data.get('id')
            if blog_id is None:
                comment_list = comment.objects.all()
            else:
                comment_list = comment.objects.filter(blog_id=blog_id)
            comments_data = []
            for comment_obj in comment_list:
                comment_dict = {
                    'id': comment_obj.id,
                    'blog_id': comment_obj.blog_id,
                    'content': comment_obj.content,
                    'last_edit_time': str(comment_obj.last_edit_time),
                    'user_id': comment_obj.user_id,
                    'father_id': comment_obj.father_id
                }
                comments_data.append(comment_dict)
            return JsonResponse({'comments': comments_data})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': '请求数据不是有效的 JSON 格式'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'获取评论失败: {str(e)}'}, status=500)
    return JsonResponse({'status': 'error', 'message': '只支持 POST 请求'}, status=405)


@csrf_exempt
def addcomment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            blog_id = data.get('blog_id')
            content = data.get('content')
            user_id = data.get('user_id')
            father_id = data.get('father_id')  # 修正拼写错误

            # 创建新评论
            if father_id:
                comment1 = comment(blog_id=blog_id, content=content, user_id=user_id, father_id=father_id)
            else:
                comment1 = comment(blog_id=blog_id, content=content, user_id=user_id)

            comment1.save()
            # 将评论对象转换为字典
            comment_data = {
                'id': comment1.id,
                'blog_id': comment1.blog_id,
                'content': comment1.content,
                'last_edit_time': str(comment1.last_edit_time),
                'user_id': comment1.user_id,
                'father_id': comment1.father_id
            }
            return JsonResponse({'message': comment_data}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'message': '无效的 JSON 数据'}, status=400)
    return JsonResponse({'message': '只支持 POST 请求'}, status=405)


@csrf_exempt
def deletecomment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            id = data.get('id')
            comment.objects.filter(id=id).delete()
            return JsonResponse({'message': '删除成功'}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'message': '无效的 JSON 数据'}, status=400)
    return JsonResponse({'message': '只支持 POST 请求'}, status=405)


@csrf_exempt
def addfeedback(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            content = data.get('content')
            name = data.get('name')
            feed1 = feedback(content=content, name=name)
            feed1.save()
            return JsonResponse({'message': 'success'}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'message': '无效的 JSON 数据'}, status=400)
    return JsonResponse({'message': '只支持 POST 请求'}, status=405)


@csrf_exempt
def getfeedbacks(request):
    try:
        feedbacks = feedback.objects.all()
        feedback1 = []
        for item in feedbacks:
            feed = {
                'name': item.name,
                'content': item.content,
                'last_edit_time': item.last_edit_time
            }
            feedback1.append(feed)
        return JsonResponse({'feeds': feedback1})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def get_airvcs(request):
    try:
        airvc_objects = AIRVC.objects.all()
        airvc_list = []
        for airvc_obj in airvc_objects:
            airvc_info = {
                'id': airvc_obj.id,
                'content': airvc_obj.content,
                'audio_url': 'http://127.0.0.1:8000/'+airvc_obj.audio.url if airvc_obj.audio else None
            }
            airvc_list.append(airvc_info)
        return JsonResponse({'airvcs': airvc_list})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# 创建 AIRVC 实例
@csrf_exempt
def create_airvc(request):
    if request.method == 'POST':
        try:
            # 不需要解析 JSON，因为是 FormData 数据
            content = request.POST.get('content')
            if 'audio' in request.FILES:
                audio_file = request.FILES['audio']
                new_airvc = AIRVC(content=content, audio=audio_file)
                new_airvc.save()
                return JsonResponse({'status':'success'})
            else:
                return JsonResponse({'status': 'error','message': '未找到上传的音频文件'}, status=400)
        except Exception as e:
            import traceback
            traceback.print_exc()  # 打印详细的错误堆栈信息
            return JsonResponse({'status': 'error','message': str(e)}, status=500)
    return JsonResponse({'status': 'error','message': 'Invalid request method'}, status=405)


# 删除 AIRVC 实例
@csrf_exempt
def delete_airvc(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            id = data.get('id')
            if id:
                count, _ = AIRVC.objects.filter(id=id).delete()
                if count > 0:
                    return JsonResponse({'status':'success','message': '删除成功'})
                else:
                    return JsonResponse({'status': 'error','message': '未找到对应的 AIRVC 实例'}, status=404)
            else:
                return JsonResponse({'status': 'error','message': 'id 字段缺失'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error','message': '无效的 JSON 数据'}, status=400)
    return JsonResponse({'status': 'error','message': '只允许 POST 请求'}, status=405)