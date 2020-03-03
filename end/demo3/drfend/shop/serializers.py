from rest_framework import serializers
from .models import *

class GoodSerializer(serializers.ModelSerializer):
    category_super = serializers.CharField(source='category.name',read_only=True)
    class Meta:
        model = Good
        fields = ('name','desc','category','category_super')


class CustomSerializer(serializers.RelatedField):


    def to_representation(self, value):

        return str(value.id)+"--"+value.name+"--"+value.desc

class CategorySerializer(serializers.ModelSerializer):
    # goods = serializers.StringRelatedField(many=True)
    # goods = serializers.PrimaryKeyRelatedField(many=True,read_only=True)
    # goods = CustomSerializer(many=True,read_only=True)
    goods = GoodSerializer(many=True,read_only=True)
    class Meta:
        model = Category
        fields = ('name','goods')



class CategorySerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=10,min_length=3,error_messages={
        "max_length":"最多十个字",
        "min_length":"最少三个字"
    })
    category = CategorySerializer(label="分类")


    def validate(self, attrs):
        print("收到的数据为",attrs)
        try:
            c = Category.objects.get(name = attrs["category"]["name"])
        except:
            c = Category.objects.create(name = attrs["category"]["name"])

        attrs["categoory"] = c
        print("更改后的数据",attrs)
        return attrs




    def create(self, validated_data):
        instance = Category.objects.create(**validated_data)
        return instance

    def update(self, instance, validated_data):

        instance.name = validated_data.get('name')
        instance.save()
        return instance