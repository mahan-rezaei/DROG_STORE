from rest_framework.serializers import RelatedField


class CustomUserPhoneField(RelatedField):
    def to_representation(self, value):
        return f'{value.phone_number}'