from django.shortcuts import render , redirect
from django.views.generic import TemplateView ,RedirectView
from user_backend.models import *
from .forms import *

# Create your views here.
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from user_backend.apibase import *

#access only for superuser

class Login_view (TemplateView):
    template_name = 'login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('login')
        else:
            context = super(Login_view, self).dispatch(request, *args, **kwargs)
        return context
    
    def post(self,request):

        username = request.POST.get('username','')
        password = request.POST.get('password','')
        next_url = request.POST['next']
        if username and password:
            user = authenticate(request, username=username, password=password)

            if user is not None and user.is_superuser:
                login(request, user)
                # Redirect to a success page.
                if next_url != "":
                    return redirect(next_url)
                return redirect('home')
            else:
                messages.error(request,"Invalid Credentials")
                return redirect('login')
        else:
            messages.error(request,"Username and Password Required")
            return redirect('login')

class LogoutView(RedirectView):
    
    url = 'login'

    def get(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            logout(request)
        
        return super(LogoutView, self).get(request, *args, **kwargs)

class Home_view(LoginRequiredMixin,TemplateView):

    template_name = 'home.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):

        context = super(Home_view, self).get_context_data(**kwargs)
        post = Post.objects.all()
        form = PostForm
        context['post'] = post
        context['form'] = form
        return context

    def post(self,request):
        postform = PostForm (request.POST or None)
        print(postform)
        if postform.is_valid():
            postform.save()
        return redirect('home')

class PostsView(LoginRequiredMixin,TemplateView):
    
    template_name = 'post_profile.html'
    login_url = 'login'

    def get_context_data(self,id,**kwargs):

        context = super(PostsView, self).get_context_data(**kwargs)
        post = Post.objects.get(pk=id)
        post_tag = post.tags.all()
        likes = post.total_likes()
        dislikes = post.total_dislikes()
        context['post'] = post
        context['tags'] = post_tag
        context['likes'] = likes
        context['dislikes'] = dislikes
        return context

class AddtagView(RedirectView):
    
    url = '/dashboard/home'
    
    def post(self,request,id,*args, **kwargs):
        
        tags = request.POST.get('tags',"")
        tag = tags.lower()
        post = Post.objects.get(pk=id)
        if tags != "" and Tags.objects.filter(tags=tag):
            getd_tag=Tags.objects.filter(tags=tag)
            current_post=post.tags.all().values()
            current_post_tags=ValuesQuerySetToDict(current_post)
            tag_list=[]
            for item in current_post_tags:
                tag_list.append(item['tags'])
            for gtag in getd_tag:
                if gtag in tag_list :
                    break
                else:
                    post.tags.add(gtag.id)
                    messages.success(request,"Tag added successfully")
                    break
        elif tags != "" :
            new_tag = Tags(tags=tag)
            new_tag.save()
            getd_tag=Tags.objects.filter(tags=tag)
            for gtag in getd_tag:
                post.tags.add(gtag.id)
                messages.success(request,"Tag added successfully")
                break
        else:
            pass
        
        return super(AddtagView, self).get(request, *args, **kwargs)

def delete(request,id):
    post = Post.objects.get(pk=id)
    post.delete()
    return redirect('/dashboard/home')
            