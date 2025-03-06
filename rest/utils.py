from kavenegar import *


def send_otp_code(phone_number, code):
    try:
        api = KavenegarAPI('2F412F3477512F4A6C674C6257795A6379686E4B5A4636384731724B514F30392F424F31646B4E446279453D')
        params = {
            'sender': '',
            'receptor': phone_number,
            'message': f'کد تایید شما \n {code}'
        }
        response = api.sms_send(params)
        print(response)
    except APIException as e: 
        print(e)
    except HTTPException as e: 
        print(e)