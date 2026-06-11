from inspect import _ParameterKind
from django.shortcuts import redirect, render
from django.views.generic import ListView
from django.views.generic.edit import DeleteView
from django.forms import formset_factory
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from .models import Post, Content
from .forms import PostForm, ContentForm

# Create your views here.

class PostListView(ListView):
    model = Post
    paginate_by = 10
    context_object_name = "post_list"

def post_detail(request, id):
    post = Post.objects.get(pk=id)
    contents = post.contents.all()
    return render(request, 'blog_app/post_detail.html', {'post': post, 'contents': contents})

@login_required(login_url='/common/login')
def create_post(request):
    
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            post = post_form.save()
            post.author = request.user
            post.save()
            
            contents = request.POST.getlist('content_type')
            texts = request.POST.getlist('text')
            images = request.FILES.getlist('image')
            orders = request.POST.getlist('order')
            
            text_cursor = 0
            image_cursor = 0
            
            content_map = {
                'text': lambda: (texts[text_cursor], None),
                'youtube': lambda: (texts[text_cursor], None),
                'image': lambda: ('', images[image_cursor])
            }
            
            for i, content_type in enumerate(contents):
                get_content = content_map.get(content_type, lambda: ('', None))
                text, image = get_content()

                if content_type == 'text' or content_type == 'youtube':#TODO:임시방편 정상화
                    text_cursor += 1
                elif content_type == 'image':
                    image_cursor += 1

                order = orders[i]

                Content.objects.create(post=post, 
                                       content_type=content_type, 
                                       text=text, 
                                       image=image, 
                                       order=order)

            return redirect('blog_app:read_post', id=post.id)
    else:
        post_form = PostForm()
        content_form = ContentForm()

        return render(request, 'blog_app/post_create.html', {'post_form': post_form, 'content_form': content_form})


@login_required(login_url='/common/login')
def delete_post(request, id):
    post = Post.objects.get(pk=id)
    if post.author != request.user:
        return HttpResponseForbidden("You are not allowed to delete this post.")
    
    post.delete()
    return redirect('blog_app:index')

@login_required(login_url='/common/login')
def edit_post(request, slug):#이미지 업로드에 뭔가 문제잏음
    post = Post.objects.get(slug=slug)
    if post.author != request.user:
        return HttpResponseForbidden("You are not allowed to edit this post.")

    if request.method == 'POST':
        post_form = PostForm(request.POST, instance=post)
        if post_form.is_valid():
            post = post_form.save()
            Content.objects.filter(post=post).delete()
            contents = request.POST.getlist('content_type')
            texts = request.POST.getlist('text')
            images = request.FILES.getlist('image')
            orders = request.POST.getlist('order')
            
            #텍스트와 이미지를 순회하는 데 하나의 인덱스를 쓸 수 없음(전체 길이=텍스트 요소 길이+이미지 요소 길이) -> 각 요소를 별개 인덱스로 순회
            text_cursor = 0
            image_cursor = 0

            content_map = {
                'text': lambda: (texts[text_cursor], None),
                'youtube': lambda: (texts[text_cursor], None),
                'image': lambda: ('', images[image_cursor])
            }

            for i, content_type in enumerate(contents):
                get_content = content_map.get(content_type, lambda: ('', None))
                text, image = get_content()

                if content_type == 'text' or content_type == 'youtube':
                    text_cursor += 1
                elif content_type == 'image':
                    image_cursor += 1

                order = orders[i]

                Content.objects.create(post=post, 
                                       content_type=content_type, 
                                       text=text, 
                                       image=image, 
                                       order=order)
                
            return redirect('blog_app:read_post', id=post.id)
    else:
        post_form = PostForm(instance=post)
        content_form = ContentForm()
        contents = post.contents.all()
        initial_contents_data = {content.id: {
            'content_type': content.content_type,
            'text': content.text if content.text else '', 
            'image': content.image.url if content.image else '',
            'order': content.order,} for content in contents
        }
        
        return render(request, 'blog_app/post_edit.html', 
                      {'post_form': post_form, 
                        'content_form': content_form, 
                        'contents': contents, 
                        'initial_contents_data':initial_contents_data
                      }
                     )