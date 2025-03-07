from django.contrib.auth import get_user_model
from rest_framework.mixins import ListModelMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserSerializer, OTPSerializer
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import OTP
from utils import send_otp_code

User = get_user_model()


class UserRegisterView(APIView):
    """
    crate a user./
    """
    def post(self, request):
        ser_data = UserRegisterSerializer(data=request.data)
        phone_numebr = ser_data.validated_data['phone_number']
        if ser_data.is_valid(raise_exception=True):
            otp = OTP.create_otp(phone_numebr)
            send_otp_code(phone_numebr, otp)
            request.session['user_register_info'] = {
                'phone_number': phone_numebr,
                'email': ser_data.validated_data['email'],
                'full_name': ser_data.validated_data['full_name'],
                'password': ser_data.validated_data['password'],
            }
            return Response({
                'message': 'we sent you a verify code.'
            }, status=status.HTTP_200_OK)
    

class VerifyOTPView(GenericAPIView):
    serializer_class = OTPSerializer
    def post(self, request):
        user_session = request.session['user_register_info']
        ser_data = self.serializer_class(data=request.data)
        if ser_data.is_valid():
            code = ser_data.validated_data['code']
            otp_code = OTP.objects.filter(code=code, phone_number=user_session['phone_number']).first()
            

            
        




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

