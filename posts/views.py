from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponse

from posts import forms
from posts.forms import PostForm, CommentForm
from posts.models import Post, Comment
from posts.constants import PAGINATION_LIMIT
from django.views import View
from django.views.generic import ListView, CreateView, DeleteView


def get_user_from_request(request):
    return request.user if not request.user.is_anonymous else None


class MainView(ListView):
    queryset = Post.objects.all()
    template_name = 'posts.html'
    context_object_name = 'posts'

    # def  get_context_data(self, **kwargs):
    #     return

    def get(self, request, **kwargs):
        page = int(request.GET.get('page', 1))

        start_post = PAGINATION_LIMIT * page if page != 1 else 0
        end_post = start_post + PAGINATION_LIMIT

        max_page = len(self.queryset) / PAGINATION_LIMIT
        if max_page > round(max_page): max_page = round(max_page) + 1
        else:
            max_page = round(max_page)

        data = {
            'posts': self.queryset[start_post:end_post],
            'user': get_user_from_request(self.request),
            'pages': range(1, max_page)
        }

        return render(request, self.template_name, context=data)
    # def get(self, request, **kwargs):
    #     page = int(request.GET.get('page', 1))
    #     pages = len(self.queryset) // PAGINATION_LIMIT
    #     start_post = (len(self.queryset) // pages) * page if page > 1 else 0
    #     # start_post = (len(posts) // PAGINATION_LIMIT) * page - 1 if page > 1 else 0
    #     end_post = start_post + PAGINATION_LIMIT
    #     print(start_post, end_post)
    #
    #     data = {
    #         'posts': self.queryset[start_post:end_post],
    #         'user': get_user_from_request(request),
    #         'pages': range(1, pages + 1)
    #     }
    #
    #     return render(request, self.template_name, context=data)


class PostDetailView(DeleteView):
    queryset = Post.objects.all()
    template_name = 'detail.html'
    context_object_name = 'post'

    # def post_detail(request, id):
    #     post = Post.objects.get(id=id)
    #     comments = Comment.objects.filter(post=post)
    #     if request.method == 'GET':
    #         data = {
    #             'post': post,
    #             'comments': comments,
    #             'comment_form': CommentForm,
    #             'user': get_user_from_request(request),
    #         }
    #
    #         return render(request, 'detail.html', context=data)
    #
    #     elif request.method == "POST":
    #         form = CommentForm(request.POST)
    #         if form.is_valid():
    #             Comment.objects.create(
    #                 author=form.cleaned_data.get('author'),
    #                 text=form.cleaned_data.get('text'),
    #                 post_id=id
    #             )
    #             return redirect(f'/posts/{id}/')
    #         else:
    #             return render(request, 'detail.html', context={
    #                 'post_form': form,
    #                 'post': post,
    #                 'comments': comments,
    #                 'comment_form': CommentForm,
    #                 'user': get_user_from_request(request),
    #
    #             })


class RegPostView(CreateView):
    model = Post
    template_name = 'reg_post.html'
    form_class = PostForm

    def get(self, request, **kwargs):
        return render(request, self.template_name, context={
            'post_form': self.form_class
        })

    # def reg_post(request):
    #     if request.method == 'GET':
    #         return render(request, 'reg_post.html', context={
    #             'post_form': PostForm,
    #             'user': get_user_from_request(request)
    #         })
    #
    #     elif request.method == 'POST':
    #         form = PostForm(request.POST)
    #         if form.is_valid():
    #             Post.objects.create(
    #                 title=form.cleaned_data.get('title'),
    #                 description=form.cleaned_data.get('description'),
    #                 stars=form.cleaned_data.get('stars'),
    #                 type=form.cleaned_data.get('type'),
    #             )
    #             return redirect('/')
    #         else:
    #             return render(request, 'reg_post.html', context={
    #                 'post_form': form,
    #                 'user': get_user_from_request(request)
    #             })


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
            post.date = form_edit.cleaned_data.get('date')

            post.save()

            return redirect('/')

        else:
            return render(request, 'update_post.html', context={
                'edit_form': form_edit,
                'id': id
            })
