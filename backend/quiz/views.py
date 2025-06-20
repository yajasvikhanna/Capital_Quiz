import requests
import random
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Country
from .serializers import CountrySerializer, QuizQuestionSerializer, AnswerCheckSerializer

def fetch_and_store_countries():
    """Fetch countries from API and store in database"""
    try:
        response = requests.get('https://countriesnow.space/api/v0.1/countries/capital')
        if response.status_code == 200:
            data = response.json()
            countries_data = data.get('data', [])
            
            # Clear existing data and adding  new data
            Country.objects.all().delete()
            
            for country_data in countries_data:
                country_name = country_data.get('name', '').strip()
                capital_city = country_data.get('capital', '').strip()
                
                # Skip entries where data is missing
                if country_name and capital_city:
                    Country.objects.get_or_create(
                        name=country_name,
                        defaults={'capital': capital_city}
                    )
            
            return True
    except Exception as e:
        print(f"Error fetching countries: {e}")
        return False

@api_view(['GET'])
def get_random_question(request):
    """Get a random country for the quiz"""
    # Ensure we have countries in database
    if Country.objects.count() == 0:
        success = fetch_and_store_countries()
        if not success:
            return Response(
                {'error': 'Failed to fetch countries data'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    # Get random country
    countries = Country.objects.all()
    if not countries:
        return Response(
            {'error': 'No countries available'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    random_country = random.choice(countries)
    serializer = QuizQuestionSerializer(random_country)
    
    return Response({
        'question': f"What is the capital of {random_country.name}?",
        'country': serializer.data
    })

@api_view(['POST'])
def check_answer(request):
    """Check if the provided answer is correct"""
    serializer = AnswerCheckSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    country_id = serializer.validated_data['country_id']
    user_answer = serializer.validated_data['user_answer'].strip().lower()
    
    try:
        country = Country.objects.get(id=country_id)
        correct_answer = country.capital.strip().lower()
        
        is_correct = user_answer == correct_answer
        
        return Response({
            'is_correct': is_correct,
            'correct_answer': country.capital,
            'user_answer': serializer.validated_data['user_answer']
        })
        
    except Country.DoesNotExist:
        return Response(
            {'error': 'Country not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['GET'])
def refresh_countries(request):
    """Manually refresh countries data from API"""
    success = fetch_and_store_countries()
    if success:
        count = Country.objects.count()
        return Response({
            'message': f'Successfully loaded {count} countries'
        })
    else:
        return Response(
            {'error': 'Failed to refresh countries data'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )