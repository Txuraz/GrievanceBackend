import jwt
import spacy
from django.contrib.auth import get_user_model
from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from rest_framework.generics import get_object_or_404, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import User
from .models import Article
from .serializers import ArticleSerializer

nlp = spacy.load('en_core_web_sm')


class CreateArticle(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        author_id = payload['id']
        author_name = get_user_model().objects.get(id=author_id).name

        # Check if 'stay_anonymous' is provided in the request
        stay_anonymous = request.data.get('stay_anonymous', False)  # Default to False if not provided

        serializer = ArticleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Set 'stay_anonymous' to False if not provided
        serializer.save(author_id=author_id, author_name=author_name, stay_anonymous=stay_anonymous)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class IncompleteArticles(APIView):
    def get(self, request):
        all_articles = Article.objects.all()
        pending_articles = []
        completed_articles = []

        for article in all_articles:
            if article.is_completed:
                completed_articles.append(article)
            else:
                pending_articles.append(article)

        sorted_pending_articles = self.merge_sort(pending_articles)
        serializer = ArticleSerializer(sorted_pending_articles, many=True)
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
        article = self.get_article(article_id)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    def get_article(self, article_id):
        article = get_object_or_404(Article, pk=article_id)
        return article


class SimilarArticles(APIView):
    def get(self, request, article_id):
        article = self.get_article(article_id)
        similar_articles = self.get_similar_articles(article)
        serializer = ArticleSerializer(similar_articles, many=True)
        return Response(serializer.data)

    def get_article(self, article_id):
        article = get_object_or_404(Article, pk=article_id)
        return article

    def get_similar_articles(self, article, num_suggestions=4):
        unfiltered_articles = Article.objects.exclude(id=article.id)
        all_articles = [article for article in unfiltered_articles if not article.is_completed]

        # Combine the titles and contents of all articles
        all_text = [art.content for art in all_articles]

        # Load spaCy's English model for tokenization
        nlp = spacy.load('en_core_web_sm')

        # Tokenize and preprocess the text
        all_docs = [nlp(text) for text in all_text]
        article_doc = nlp(article.content)

        sentences = [[token.text for token in doc] for doc in all_docs]

        # Calculate similarity scores using spaCy's similarity method
        similarities = [article_doc.similarity(doc) for doc in all_docs]

        # Get the indices of top similar articles
        similar_indices = sorted(range(len(similarities)), key=lambda i: similarities[i], reverse=True)[
                          :num_suggestions]

        similar_articles = [all_articles[index] for index in similar_indices]
        return similar_articles


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
            article = Article.objects.get(pk=article_id)
        except Article.DoesNotExist:
            raise Http404

        user_id = payload.get('id')
        user = User.objects.get(pk=user_id)

        if user != article.author and not user.is_admin:
            raise PermissionDenied('You do not have permission to delete this article.')

        article.delete()

        return Response({"message": "Article deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


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

        user_id = payload['id']
        user = get_user_model().objects.get(pk=user_id)

        if vote_type == 'upvote':
            if article.upvoted_by.filter(id=user_id).exists():
                article.upvoted_by.remove(user)
                article.vote -= 1
            else:
                article.downvoted_by.remove(user)
                article.upvoted_by.add(user)
                article.vote += 1
        elif vote_type == 'downvote':
            if article.downvoted_by.filter(id=user_id).exists():
                article.downvoted_by.remove(user)
                article.vote += 1
            else:
                article.upvoted_by.remove(user)
                article.downvoted_by.add(user)
                article.vote -= 1
        else:
            return Response({'error': 'Invalid vote_type'}, status=status.HTTP_400_BAD_REQUEST)

        article.save()

        return Response(status=status.HTTP_200_OK)


class ArticleStatusUpdate(APIView):
    def put(self, request, article_id):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user_id = payload.get('id')
        user = User.objects.get(pk=user_id)

        if not user.is_admin:
            raise PermissionDenied('Only admin users can update the status of an article.')

        try:
            article = Article.objects.get(pk=article_id)
        except Article.DoesNotExist:
            raise Http404

        is_completed = request.data.get('is_completed', None)
        if is_completed is not None:
            article.is_completed = is_completed
            article.is_status_updatable = True
            article.save()

        serializer = ArticleSerializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CompletedArticleList(APIView):
    def get(self, request):
        completed_articles = Article.objects.filter(is_completed=True)
        serializer = ArticleSerializer(completed_articles, many=True)
        return Response(serializer.data)


class ListArticles(APIView):
    def get(self, request):
        all_articles = Article.objects.all()
        serializer = ArticleSerializer(all_articles, many=True)
        return Response(serializer.data)


class EditArticle(UpdateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def put(self, request, *args, **kwargs):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            # Verify and decode the JWT token
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user_id = payload['id']

        try:
            # Get the article from the database
            article = self.get_object()
        except Article.DoesNotExist:
            raise Http404

        if user_id != article.author.id:
            raise PermissionDenied('You do not have permission to edit this article.')

        request_data = request.data.copy()
        request_data.pop('author_name', None)

        serializer = self.get_serializer(article, data=request_data, partial=True)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
