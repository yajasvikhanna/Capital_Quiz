from rest_framework import serializers
from .models import Country

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name', 'capital']

class QuizQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name']  # Only send the country name, not  the capitals

class AnswerCheckSerializer(serializers.Serializer):
    country_id = serializers.IntegerField()
    user_answer = serializers.CharField(max_length=100)