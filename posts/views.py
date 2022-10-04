from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponse

from posts import forms
from posts.forms import PostForm, CommentForm
from posts.models import Post, Comment


def get_user_from_request(request):
    return request.user if not request.user.is_anonymous else None


def main(request):
    posts = Post.objects.all()

    data = {
        'posts': posts,
        'user': get_user_from_request(request),
    }

    return render(request, 'posts.html', context=data)


def post_detail(request, id):
    post = Post.objects.get(id=id)
    comments = Comment.objects.filter(post=post)
    if request.method == 'GET':
        data = {
            'post': post,
            'comments': comments,
            'comment_form': CommentForm,
            'user': get_user_from_request(request),
        }

        return render(request, 'detail.html', context=data)

    elif request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            Comment.objects.create(
                author=form.cleaned_data.get('author'),
                text=form.cleaned_data.get('text'),
                post_id=id
            )
            return redirect(f'/posts/{id}/')
        else:
            return render(request, 'detail.html', context={
                'post_form': form,
                'post': post,
                'comments': comments,
                'comment_form': CommentForm,
                'user': get_user_from_request(request),

            })


def reg_post(request):
    if request.method == 'GET':
        return render(request, 'reg_post.html', context={
            'post_form': PostForm,
            'user': get_user_from_request(request)
        })

    elif request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            Post.objects.create(
                title=form.cleaned_data.get('title'),
                description=form.cleaned_data.get('description'),
                stars=form.cleaned_data.get('stars'),
                type=form.cleaned_data.get('type'),
            )
            return redirect('/')
        else:
            return render(request, 'reg_post.html', context={
                'post_form': form,
                'user': get_user_from_request(request)
            })


def edit_post(request, id):
    if request.method == 'GET':
        return render(request, 'update_post.html', context={
            'edit_form': PostForm,
            'id': id
        })

    elif request.method == 'POST':
        form_edit = PostForm(request.POST)
        if form_edit.is_valid():
            post = Post.objects.get(id=id)
            post.title = form_edit.cleaned_data.get('title')
            post.description = form_edit.cleaned_data.get('description')
            post.stars = form_edit.cleaned_data.get('stars')
            post.type = form_edit.cleaned_data.get('type')

            post.save()

            return redirect('/')

        else:
            return render(request, 'update_post.html', context={
                'edit_form': form_edit,
                'id': id
            })
