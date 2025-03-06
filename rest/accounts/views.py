from django.contrib.auth import get_user_model
from rest_framework.mixins import ListModelMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserSerializer
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

User = get_user_model()


class UserRegisterView(APIView):
    """
    crate a user./
    """
    def post(self, request):
        ser_data = UserRegisterSerializer(data=request.data)
        if ser_data.is_valid(raise_exception=True):
            ser_data.save()

            return Response(
                {'message': 'sent otp code.'},
                status=status.HTTP_200_OK
            )


class UserLoginView(GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        ser_data = self.get_serializer(data=request.data)
        if ser_data.is_valid(raise_exception=True):
            user = authenticate(
                phone_number=ser_data.validated_data['phone_number'],
                password=ser_data.validated_data['password']
            )
            if user:
                refresh = RefreshToken.for_user(user)
                return Response(
                    {
                        'user_data': ser_data.data,
                        'refresh': str(refresh),
                        'access': str(refresh.access_token)
                    }
                )
            return Response({'message': 'user information is invalid'}, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
    pass


class UserListView(ListModelMixin, GenericAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get(self, request):
        return self.list(request)

