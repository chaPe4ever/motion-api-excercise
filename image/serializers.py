from rest_framework.serializers import ModelSerializer

from image.models import Image


class ImageSerializer(ModelSerializer):
    class Meta:
        model = Image
        fields = ["id", "image"]
