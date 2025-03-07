from kavenegar import *


def send_otp_code(phone_number, code):
    try:

        api = KavenegarAPI('3863534D2B474B6153627835396538734B4256416261433069353672545453706F326C48697363366437733D')
        params = {
            'sender': '2000660110',
            'receptor': phone_number,
            'message': f'کد تایید شما \n {code}'
        }
        response = api.sms_send(params)
        print(response)
    except APIException as e: 
        print(e)
    except HTTPException as e: 
        print(e)
