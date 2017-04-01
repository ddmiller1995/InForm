# from django.contrib.auth.models import User
from api.models import Youth
from rest_framework import serializers

# class YouthSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     youth_name = serializers.CharField(max_length=100)
#     date_of_birth = serializers.DateField()
#     ethnicity = serializers.CharField(max_length=64)

#     def create(self, validated_data):
#         """
#         Create and return a new `Snippet` instance, given the validated data.
#         """
#         return Youth.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         """
#         Update and return an existing `Snippet` instance, given the validated data.
#         """
#         instance.youth_name = validated_data.get('youth_name', instance.youth_name)
#         instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
#         instance.ethnicity = validated_data.get('ethnicity', instance.ethnicity)

#         instance.save()
#         return instance

class YouthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Youth
        fields = ('id', 'youth_name', 'date_of_birth', 'ethnicity')