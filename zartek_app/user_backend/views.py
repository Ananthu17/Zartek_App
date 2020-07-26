from django.shortcuts import render
# Create your views here.
import json
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .apibase import *
from django.conf import settings
from django.contrib.auth import authenticate, login




# to get all post 
class main_class(APIView):
    
    def get(self,request):
        dic={}
        post = Post.objects.all().values()
        post_dict= ValuesQuerySetToDict(post)
        print(post_dict)
        dic["posts"] = post_dict
        self.flag = StatusCode.HTTP_200_OK
        return JsonWrapper(dic, self.flag)

    
# when testing with postman.like and dislike api will return Anonymous user so it won't work
# to test api with postman change request.user with 1 or any other valid post id 
# add like && dislike in body when testing API

class post_detail(APIView):
    #Api to see details of a particular post
    def get(self,request,id):
        dic={}
        try:
            if Post.objects.filter(pk=id):
                post = Post.objects.filter(pk=id).values()
                post_view = Post.objects.get(pk=id)
                post_dict= ValuesQuerySetToDict(post)
                dic["messages"] = "Valid Post Object"
                dic["posts"]= post_dict
                dic["likes_count"] = post_view.total_likes()
                dic["dislike_count"] = post_view.total_dislikes()
                self.flag = StatusCode.HTTP_200_OK
                return JsonWrapper(dic, self.flag)
            else:
                raise ValueError
        except ValueError:
            dic["messages"] = "Post doesn't exists"
            self.flag = StatusCode.HTTP_404_NOT_FOUND
            return JsonWrapper(dic, self.flag)
            
    # API for liking and disliking a post 
    def put(self,request,id):
        dic={}
        received_data=json.loads(request.body)
        post = Post.objects.get(pk=id)
        try:
            if received_data['like'] == True:
                post.likes.add(request.user)
                post.dislikes.remove(request.user)
                post.save()
            elif received_data['dislike'] == True:
                post.dislikes.add(request.user)
                post.likes.remove(request.user)
                post.save()
            else:
                pass
        except TypeError:
            dic["messages"] = "Anonymous User Detected"
            self.flag = StatusCode.HTTP_401_UNAUTHORIZED
            return JsonWrapper(dic, self.flag)

        #to retain all tags attached with post
        liked_post = post.tags.all().values()    
        liked_post_tags = ValuesQuerySetToDict(liked_post)
        tag_list=[]
        for item in liked_post_tags:
            tag_list.append(item['id'])
        #to get all post with same tags
        querylist = []
        for tags in tag_list:
            qry = Post.objects.filter(tags=tags).values()
            dic_qry = ValuesQuerySetToDict(qry)
            querylist.append(dic_qry)
        query_value_list = []
        for item in querylist:
            for subitem in item:
                if subitem not in query_value_list:
                    query_value_list.append(subitem) 
        dic["posts"] = query_value_list
        self.flag = StatusCode.HTTP_200_OK
        return JsonWrapper(dic, self.flag)

#API that returns a list of all the users who liked a post (/posts/reactions/:id)
class Reactionlist(APIView):

    def get(self,request,id):
        dic={}
        try:
            if Post.objects.filter(pk=id) :
                post = Post.objects.get(pk=id)
                post_likeset = post.likes.all().values()
                post_dislikeset = post.dislikes.all().values()
                likes = ValuesQuerySetToDict(post_likeset)
                dislikes = ValuesQuerySetToDict(post_dislikeset)

                like_list=[]
                for user in likes:
                    data={}
                    data['username'] = user['username']
                    like_list.append(data)

                dislike_list=[]
                for user in dislikes:
                    data={}
                    data['username'] = user['username']
                    dislike_list.append(data)

                dic["likes"] = like_list
                dic["total_likes"] = len(like_list)
                dic["dislikes"] = dislike_list
                dic["total_dislikes"] = len(dislike_list)

                self.flag = StatusCode.HTTP_200_OK
                return JsonWrapper(dic, self.flag)
            else:
                raise ValueError
        except ValueError :
            dic["messages"] = "Post doesn't exists"
            self.flag = StatusCode.HTTP_404_NOT_FOUND
            return JsonWrapper(dic, self.flag)


        

        
    
