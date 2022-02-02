from functools import partial
from urllib import request
from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
# from rest_framework import generics
# from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import action, authentication_classes, permission_classes
from rest_framework import filters
from .serializers import ArticleSerializer,AuthorSerializer
from .models import Article,Author,User
from django.contrib.auth import logout 
from .serializers import UserSerializer
from rest_framework.authtoken.models import Token
from rest_framework import authentication
from rest_framework.authtoken.views import ObtainAuthToken
# Create your views here.


## APIVIEW

# class ArticleAPIView(APIView):
#     def get(self,request,pk=None):
#         if pk:
#             article=get_object_or_404(Article.objects.all(),pk=pk)
#             serializer=ArticleSerializer(article)
#         else:
#             articles=Article.objects.all()
#             serializer=ArticleSerializer(articles,many=True)
#         return Response({"articles":serializer.data})
    
#     def post(self,request):
#         serializer=ArticleSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#         return Response({"success":"Article Created Successfully"})
    
#     def put(self,request,pk):
#         article=get_object_or_404(Article.objects.all(),pk=pk)
#         serializer=ArticleSerializer(data=request.data,instance=article,partial=True)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#         return Response({"success":"Article was Updated Successfully"})    
    
#     def delete(self,request,pk):
#         article=get_object_or_404(Article.objects.all(),pk=pk)
#         article.delete()
#         return Response({"message":"Article was Deleted"})
    
    
# class AuthorAPIView(APIView):
#     def get(self,request,pk=None):
#         if pk:
#             author=get_object_or_404(Author.objects.all(),pk=pk)
#             serializer=AuthorSerializer(author)
#         else:
#             authors=Author.objects.all()
#             serializer=AuthorSerializer(authors,many=True)
#         return Response({"authors":serializer.data})

#     def post(self,request):
#         serializer=AuthorSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#         return Response({"success":"Author Created Successfully"})
    
#     def put(self,request,pk):
#         author=get_object_or_404(Author.objects.all(),pk=pk)
#         serializer=AuthorSerializer(data=request.data,instance=author,partial=True)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#         return Response({"success":"Author was Updated Successfully"})
    
#     def delete(self,request,pk):
#         author=get_object_or_404(Author.objects.all(),pk=pk)
#         author.delete()
#         return Response({"message":"Author was Deleted"})
    
## GenericAPIView with mixins

# class ArticleGenericView(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
#     queryset=Article.objects.all()
#     serializer_class=ArticleSerializer
    
#     def get(self,request,*args,**kwargs):
#         return self.list(request,*args,**kwargs)
#     def post(self,request,*args,**kwargs):
#         return self.create(request,*args,**kwargs)
 

## GenericAPIView

# class ArticleListView(generics.ListCreateAPIView):
#     queryset=Article.objects.all()
#     serializer_class=ArticleSerializer

# class ArticleDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset=Article.objects.all()
#     serializer_class=ArticleSerializer

# ViewSets

class ArticleViewSet(viewsets.ModelViewSet):
    queryset=Article.objects.all()
    serializer_class=ArticleSerializer
    authentication_classes=[authentication.TokenAuthentication,]
    permission_classes=[permissions.IsAuthenticated]
    # permission_classes=[permissions.AllowAny,]


class AuthorViewSet(viewsets.ModelViewSet):
    queryset=Author.objects.all()
    serializer_class=AuthorSerializer
    authentication_classes=[authentication.TokenAuthentication,]
    permission_classes=[permissions.IsAuthenticated,]
    
    
    @action(detail=False,methods=['get'],url_path='my-action',name="ABC")#,suffix="XYZ")
    def id_lt_three(self,request,*args,**kwargs):
        return Response({"a":'sda'})
    
    
class RegisterUser(APIView):
    def post(self,request):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        # user=serializer.validated_data['user']
        user=User.objects.get(username=serializer.data['username'])
        token,created=Token.objects.get_or_create(user=user)
        return Response({'status':200,'payload':serializer.data,'token':str(token),'msg':'Success Message'})
    

class CustomAuthToken(ObtainAuthToken):
    def post(self,request,*args,**kwargs):
        serializer=self.serializer_class(data=request.data,context={'request':request})
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data['user']
        token,created=Token.objects.get_or_create(user=user)
        return Response({
            'token':token.key,
            'user_id':user.pk,
            'email':user.email
        })

class LogoutUser(APIView):
    authentication_classes=[authentication.TokenAuthentication,]
    permission_classes=[permissions.IsAuthenticated,]
    def post(self,request):
        try:
            request.user.auth_token.delete()
        except Exception as e:
            pass
        logout(request)
        return Response({'msg':"You have been logged out"})