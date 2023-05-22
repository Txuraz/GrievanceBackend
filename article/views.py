import datetime
import jwt
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404

from .models import Article
from .serializers import ArticleSerializer


class CreateArticle(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        serializer = ArticleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author_id=payload['id'])

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ListArticles(APIView):
    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)


class RetrieveArticle(APIView):
    def get(self, request, article_id):
        article = get_object_or_404(Article, pk=article_id)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)


class DeleteArticle(APIView):
    def delete(self, request, article_id):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            article = Article.objects.get(pk=article_id, author_id=payload['id'])
        except Article.DoesNotExist:
            raise Http404

        article.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
