from rest_framework import serializers
from .models import Country

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name', 'capital']

class QuizQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name']  # Only send country name, not capital

class AnswerCheckSerializer(serializers.Serializer):
    country_id = serializers.IntegerField()
    user_answer = serializers.CharField(max_length=100)