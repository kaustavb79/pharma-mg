import random
from django.conf import settings
import logging

logger = logging.getLogger("app_account")


def send_otp(mobile):
    otp = random.randint(100000, 999999)
    message = settings.SMS_CLIENT.messages.create(
        body=f'Your PharmaMG verification OTP: {otp}',
        from_=settings.REGISTERED_NUMBER,
        to=f'+91{mobile}'
    )

    logger.info("MESSAGE SID: %s", message.sid)
    logger.info("MESSAGE STATUS: %s", message.status)
    return {"sid": message.sid, "status": message.status, "otp": otp}
