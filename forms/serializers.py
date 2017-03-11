from rest_framework import serializers
from forms.models import Form

class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        fields = ('id', 'title')