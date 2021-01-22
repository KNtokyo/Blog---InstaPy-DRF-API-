from django.db.models import Q
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from .models import *
from .serializers import *
from .permissions import *


# @api_view(['GET'])
# def categories(request):
#     categories = Category.objects.all()
#     serializer = CategorySerializer(categories, many=True)
#     return Response(serializer.data)
#
#
# class PostListView(APIView):
#     def get(self, request):
#         posts = Post.objects.all()
#         serializers = PostSerializer(posts, many=True)
#         return Response(serializers.data)
#
#     def post(self, request):
#         posts = request.data
#         print(posts)
#         serializers = PostSerializer(data=posts)
#         if serializers.is_valid(raise_exception=True):
#             posts_saved = serializers.save()
#         return Response(serializers.data)




# class PostView(generics.ListCreateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#
#
# class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer


class MyPaginationClass(PageNumberPagination):
    page_size = 3

    def get_paginated_response(self, data):
        for i in range(self.page_size):
            text = data[i]['text']
            data[i]['text'] = text[:15] + '...'
        return super().get_paginated_response(data)


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny, ]


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # permission_classes = [IsAuthenticated, ]
    pagination_class = MyPaginationClass

    def get_serializer_context(self):
        return {'request': self.request}

    # def get_permissions(self):
    #     """Переопределил этот метод"""
    #     print(self.action)
    #     if self.action in ['update', 'partial_update', 'destroy']:
    #         permissions = [IsAuthorPost, ]
    #     else:
    #         permissions = [IsAuthenticated, ]
    #     return [permission() for permission in permissions]

    # @action(detail=False, method=['get'])
    # def own(self, request, pk=None):
    #     queryset = self.get_queryset()
    #     queryset = queryset.filter(author=request.user)
    #     serializers = PostSerializer(queryset, many=True, context={'request': request})
    #     return Response(serializers.data, status=status.HTTP_200_OK)


    @action(detail=False, methods=['get'])
    def search(self, request, pk=None):
        # print(request.query_params)
        s = request.query_params.get('s')
        queryset = self.get_queryset()
        queryset = queryset.filter(Q(text__icontains=s) |
                                   Q(title__icontains=s))
        serializers = PostSerializer(queryset, many=True, context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)

    # @action(detail=False, methods=['get'])
    # def myfilter(self, request, pk=None):
    #     f = request.query_params.get('f')
    #     queryset = self.get_queryset()
    #     queryset = queryset.filter(category__icontains=f)
    #     serializers = PostSerializer
    #     return Response(serializers.data, status=status.HTTP_200_OK)


class PostImageView(generics.ListCreateAPIView):
    queryset = PostImage.objects.all()
    serializer_class = PostImageSerializer

    def get_serializer_context(self):
        return {'request': self.request}

