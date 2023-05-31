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


'''Algorithm to SORT List of Articles according to greater number of vote'''


class ListArticles(APIView):
    def get(self, request):
        articles = Article.objects.all()
        sorted_articles = self.merge_sort(articles)
        serializer = ArticleSerializer(sorted_articles, many=True)
        return Response(serializer.data)

    def merge_sort(self, articles):
        if len(articles) <= 1:
            return articles

        mid = len(articles) // 2
        left = self.merge_sort(articles[:mid])
        right = self.merge_sort(articles[mid:])

        return self.merge(left, right)

    def merge(self, left, right):
        result = []
        i = j = 0

        while i < len(left) and j < len(right):
            if left[i].vote > right[j].vote:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        result.extend(left[i:])
        result.extend(right[j:])
        return result


class RetrieveArticle(APIView):
    def get(self, request, article_id):
        article = get_object_or_404(Article, pk=article_id)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)


from django.http import HttpResponse


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

        return Response({"Article deleted successfully."})


class VoteArticle(APIView):
    def post(self, request, article_id):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            article = Article.objects.get(pk=article_id)
        except Article.DoesNotExist:
            raise Http404

        vote_type = request.data.get('vote_type')

        if vote_type == 'upvote':
            article.vote += 1
        elif vote_type == 'downvote':
            article.vote -= 1
        else:
            return Response({'error': 'Invalid vote_type'}, status=status.HTTP_400_BAD_REQUEST)

        article.save()

        return Response(status=status.HTTP_200_OK)
