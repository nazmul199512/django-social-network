import random
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils.http import is_safe_url
from django.conf import settings
from .models import Post
from .forms import PostForm

from .serializers import PostSerializer, PostActionSerializer, PostCreateSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
ALLOWED_HOST = settings.ALLOWED_HOSTS


def home(request):
    print(request.user or None)
    return render(request, 'home.html', {})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_create_view(request):

    serializer = PostCreateSerializer(data=request.POST)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)

    return Response({}, status=400)


@api_view(['GET'])
def post_list_view(request, *args, **kwargs):
    qs = Post.objects.all()
    serializer = PostSerializer(qs, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def post_detail_view(request, post_id, *args, **kwargs):
    qs = Post.objects.filter(id=post_id)
    if not qs.exists():
        return Response({}, status=404)
    obj = qs.first()
    serializer = PostSerializer(obj)
    return Response(serializer.data, status=200)


@api_view(['DELETE', 'POST'])
@permission_classes([IsAuthenticated])
def post_delete_view(request, post_id, *args, **kwargs):
    qs = Post.objects.filter(id=post_id)
    if not qs.exists():
        return Response({}, status=404)
    qs = qs.filter(user=request.user)
    if not qs.exists():
        return Response({"message": "You cann't delete this Post!"}, status=401)
    obj = qs.first()
    obj.delete()
    return Response({"message": "Post Removed"}, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_action_view(request, *args, **kwargs):  # Action options are like, unlike , re-post
    serializers = PostActionSerializer(data=request.data)
    if serializers.is_valid(raise_exception=True):
        data = serializers.validated_data
        post_id = data.get('id')
        action = data.get('action')
        content = data.get('content')
        qs = Post.objects.filter(id=post_id)
        if not qs.exists():
           return Response({}, status=404)
        obj = qs.first()
        if action == "like":
            obj.likes.add(request.user)
            serializer = PostSerializer(obj)
            return Response(serializer.data, status=200)
        elif action == "unlike":
            obj.likes.remove(request.user)
        elif action == "re-post":

            new_post = Post.objects.create(
                user=request.user,
                parent=obj,
                content=content
            )
            serializer = PostSerializer(new_post)
            return Response(serializer.data, status=200)
    return Response({}, status=200)


def post_create_view_django(request):
    user = request.user
    if not request.user.is_authenticated:
        user = None
        if request.is_ajax():
            return JsonResponse({}, status=401)
        return redirect(settings.LOGIN_URL)
    form = PostForm(request.POST or None)
    next = request.POST.get('next') or None
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = user
        instance.save()
        if request.is_ajax():
            return JsonResponse(instance.serialize(), status=201)
        if next != None and is_safe_url(next, ALLOWED_HOST):
            return redirect(next)
        form = PostForm()
    if PostForm.errors:
        if request.is_ajax():
            return JsonResponse(form.errors, status=400)
    return render(request, "posts/form.html", context={'form': form})


def post_list_view_django(request, *args, **kwargs):
    qs = Post.objects.all()
    posts = [x.serialize() for x in qs]
    data = {
        'response': posts
    }
    return JsonResponse(data)


def post_detail_view_django(request, post_id, *args, **kwargs):
    data = {
        'isUser': False,
        'id': post_id,
    }
    status = 200
    try:
        obj = Post.objects.get(id=post_id)
        data['content'] = obj.content
    except:
        data['message'] = "Not Found"
        status = 404

    return JsonResponse(data, status=status)

