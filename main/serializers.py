from rest_framework import serializers
from .models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%d/%m/%Y %H:%M', read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'category', 'created_at', 'text')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['author'] = instance.author.email
        representation['categories'] = CategorySerializer(instance.category).data
        representation['images'] = PostImageSerializer(instance.images.all(),
                                                       many=True, context=self.context).data
        return representation

    def create(self, validated_data):
        request = self.context.get('request')
        user_id = request.user.id
        validated_data['author_id'] = user_id
        print(validated_data)
        post = Post.objects.create(**validated_data)
        return post


    #
    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation['author'] = instance.author.email
    #     representation['category'] = CategorySerializer(instance.category).data
    #     representation['images'] = PostImageSerializer(instance.images.all(),
    #                                                    many=True, context=self.context).data


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = '__all__'


    def _get_image_url(self, obj):
        if obj.image:
            url = obj.image.url
            request = self.context.get('request')
            if request is not None:
                url = request.build_absolute_uri(url)
        else:
            url = ''
        return url

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image'] = self._get_image_url(instance)
        return representation

