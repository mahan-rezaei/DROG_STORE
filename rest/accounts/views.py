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
from .util import send_otp_code

User = get_user_model()


class UserRegisterView(APIView):
    """
    crate a user./
    """
    def post(self, request):
        ser_data = UserRegisterSerializer(data=request.data)
        if ser_data.is_valid(raise_exception=True):
            phone_number = ser_data.validated_data['phone_number']
            otp = OTP.create_otp(phone_number)
            send_otp_code(phone_number, otp)
            request.session['user_register_info'] = {
                'phone_number': phone_number,
                'email': ser_data.validated_data['email'],
                'full_name': ser_data.validated_data['full_name'],
                'password': ser_data.validated_data['password'],
            }
            request.session.set_expiry(300)
            return Response({
                'message': 'we sent you a verify code.'
            }, status=status.HTTP_200_OK)
    

class VerifyOTPView(GenericAPIView):
    serializer_class = OTPSerializer

    def post(self, request):
        user_session = request.session.get('user_register_info')
        if not user_session:
            return Response({'error': 'session expired or invalid'}, status=status.HTTP_404_NOT_FOUND)
        ser_data = self.serializer_class(data=request.data)
        if ser_data.is_valid(raise_exception=True):
            code = ser_data.validated_data['code']
            otp_code = OTP.objects.filter(code=code, phone_number=user_session['phone_number']).first()
            if otp_code and otp_code.verify_otp(user_session['phone_number'], code):
                user_ser_data = UserRegisterSerializer(data=user_session)
                if user_ser_data.is_valid(raise_exception=True):
                    user_ser_data.save()
                    otp_code.delete()
                    del request.session['user_register_info']
                    return Response({'message': 'user created successfully.'}, status=status.HTTP_201_CREATED)
            return Response({'message': 'OTP code verification failed'}, status=status.HTTP_400_BAD_REQUEST)
            

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

