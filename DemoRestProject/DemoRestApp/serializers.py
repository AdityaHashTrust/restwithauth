
from django.db.models import fields
from rest_framework import serializers, validators
from rest_framework.exceptions import Throttled

from DemoRestApp.models import Article, Author,User
        
## Normal Serializer

# class ArticleSerializer(serializers.Serializer):
#     title=serializers.CharField(max_length=121)
#     description=serializers.CharField()
#     body=serializers.CharField()
#     author_id=serializers.IntegerField()
    
#     def create(self,validated_data):
#         return Article.objects.create(**validated_data)
        
#     def update(self,instance,validated_data):
#         instance.title=validated_data.get('title',instance.title)
#         instance.description=validated_data.get('description',instance.description)
#         instance.body=validated_data.get('body',instance.body)
#         instance.author_id=validated_data.get('author_id',instance.author_id)
#         instance.save()
#         return instance
    
# class AuthorSerializer(serializers.Serializer):
#     name=serializers.CharField(max_length=121)
#     email=serializers.EmailField()
    
#     def create(self,validated_data):
#         return Author.objects.create(**validated_data)
    
#     def update(self,validated_data,instance):
#         instance.name=validated_data.get('name',instance.name)
#         instance.email=validated_data.get('email',instance.email)
#         instance.save()
#         return instance

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model=Article
        fields='__all__'
        
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Author
        fields='__all__'
        
class UserSerializer(serializers.ModelSerializer):
    # password2=serializers.HiddenField(default='abc')
    class Meta:
        model=User
        fields=['username','password','password2'] 
        # validators=[]       
    def create(self, validated_data):
        # user=User.objects.create(username=validated_data['username'])
        user=User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
    def validate_password(self,value):
        if len(value)<8 or len(value)>51:
            raise serializers.ValidationError("Password length must be between 8 and 51")
        if value.isalnum() and value.isalpha():
            raise serializers.ValidationError("Password must be combination of Words and Numeric Digits")
        return value
    def validate(self,data):
        if data['password']!=data['password2']:
            raise serializers.ValidationError("Password 1 and Password 2 are not Same")
        return data

# class LoginSerializer(serializers.Serializer):
#     username=serializers.CharField()
#     password=serializers.CharField()
#     # try:
#     #     user=User.objects.get(username=username)
#     # except Exception as e:
#     #     print("User Not Found")
#     def validate_username(self,value):
#         user=User.objects.filter(username=value)
#         if user==[]:
#             raise serializers.ValidationError("Username not Found")
#         return value
#     def validate(self,data):
#         user=User.objects.get(username=data['username'])
#         if user.password!=data['password']:
#             raise serializers.ValidationError("Wrong Password")
#         return data  
      
