from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
import requests
from django.db.models import Count
from rest_framework import permissions
from utils.api_response import api_success_response, api_error_response
from datetime import datetime
from .serializers import NewsSerializer
from .models import News

NEWS_BASE_URL = settings.NEWS_API_BASE_URL
NEWS_API_KEY = settings.NEWS_API_KEY

class SearchNewsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        Handles the HTTP POST request for searching news.

        Parameters:
            request (HttpRequest): The HTTP request object.

        Returns:
            Response: The HTTP response object containing the search results.

        Raises:
            None

        Description:
            This function handles the HTTP POST request for searching news. It expects the request data to contain a
            'key_phrase' field. If the 'key_phrase' field is missing or empty, it returns an error response.

            The function first strips the 'key_phrase' field and assigns the user ID from the request to the 'user' field
            of the data dictionary.

            If the search type is 'past' and the key phrase exists in the database for the current user, the function
            retrieves the existing news record from the database and returns the API response data. The 'publishedAt'
            field of each article in the response data is formatted as a human-readable date.

            If the search type is 'new', the function constructs a URL to query the news API with the key phrase and
            other parameters. It sends a GET request to the API and saves the API response data in the 'api_response'
            field of the data dictionary. The function then validates and saves the data using the NewsSerializer. If
            the response status code is 200, the function formats the 'publishedAt' field of each article in the
            response data and returns a success response with the formatted data. Otherwise, it returns an error
            response with the API response data.

            If the search type is 'latest', the function checks if a news record exists in the database for the current
            user and the specified key phrase. If a record exists, the function constructs a new URL to query the news
            API with the key phrase and a 'from' parameter set to the creation date of the existing record. It sends a
            GET request to the API and retrieves the new articles. The existing articles are extended with the new
            articles, and the 'articles' and 'totalResults' fields of the API response are updated in the existing
            record. The function then saves the updated record and returns a success response with the API response
            data.
        """
        data = request.data
        if 'key_phrase' not in data:
            return api_error_response('key_phrase is required')
        if data['key_phrase'].strip() == '':
            return api_error_response('key_phrase cannot be empty')

        data['key_phrase'] = data['key_phrase'].strip()
        data['user'] = request.user.id

        # Check if the search_type is past and the key_phrase exists in the database, is yes then return the data from the database
        if News.objects.filter(key_phrase=data['key_phrase'], user=data['user']).exists() and data['search_type'] == 'past':
            news = News.objects.filter(key_phrase=data['key_phrase'], user=data['user']).first()
            serializer_data = NewsSerializer(news).data
            data = serializer_data['api_response']
            for article in data['articles']:
                    new_date = datetime.strptime(article['publishedAt'], "%Y-%m-%dT%H:%M:%SZ")
                    formatted_date = new_date.strftime("%B %d, %Y %H:%M:%S")
                    article['publishedAt'] = formatted_date
            return api_success_response(data)
        
        if data['search_type'] == 'new':
            url = NEWS_BASE_URL + 'everything?q=' + data['key_phrase'] + '&lang=en&sortBy=publishedAt&pageSize=25&apiKey=' + NEWS_API_KEY            
            response = requests.get(url)
            data['api_response'] = response.json()
            serializer = NewsSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            if response.status_code == 200:
                data = response.json()
                for article in data['articles']:
                    new_date = datetime.strptime(article['publishedAt'], "%Y-%m-%dT%H:%M:%SZ")
                    formatted_date = new_date.strftime("%B %d, %Y %H:%M:%S")
                    article['publishedAt'] = formatted_date
                return api_success_response(data)
            else:
                return api_error_response(data)
            
        # If the search_type is latest, then first get the existing record from the database with the matching key_phrase and user and then pull the latest news from the API and update the record in the database
        if data['search_type'] == 'latest':
            if News.objects.filter(key_phrase=data['key_phrase'], user=data['user']).exists():
                news = News.objects.filter(key_phrase=data['key_phrase'], user=data['user']).first()
                existing_articles = news.api_response['articles']
                url = NEWS_BASE_URL + 'everything?q=' + data['key_phrase'] + '&from=' + news.created_at.strftime("%Y-%m-%d") + '&lang=en&sortBy=publishedAt&pageSize=25&apiKey=' + NEWS_API_KEY
                response = requests.get(url)
                new_articles = response.json()['articles']
                existing_articles.extend(new_articles)
                news.api_response['articles'] = existing_articles
                news.api_response['totalResults'] = len(existing_articles)
                news.save()
                return api_success_response(news.api_response)
                

    def get(self, request):
        """
        Retrieves the news articles associated with the currently authenticated user.

        Parameters:
            request (Request): The HTTP request object.

        Returns:
            Response: The API response containing a list of serialized news articles.
        """
        user = request.user.id
        news = News.objects.filter(user=user)
        serializer = NewsSerializer(news, many=True)
        return api_success_response(serializer.data)       
        

class TrendingKeyPhrasesView(APIView):
    """
    View for retrieving trending key phrases from the database.
    """

    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    permission_classes = (permissions.AllowAny,)
    authentication_classes = []
    def get(self, request):
        """
        Retrieves the trending key phrases from the database based on count. 

        Parameters:
            request (Request): The HTTP request object.

        Returns:
            Response: The API response containing a list of trending key phrases.
        """
        key_phrases = News.objects.values('key_phrase').annotate(count=Count('key_phrase')).order_by('-count')[:3]
        return api_success_response(key_phrases)