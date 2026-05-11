import json
from pywebpush import webpush, WebPushException
from sqlalchemy.orm import Session
from backend.models.models import Pengaturan
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
import base64

def get_or_create_vapid_keys(db: Session):
    private_key_record = db.query(Pengaturan).filter(Pengaturan.kunci == "vapid_private_key").first()
    public_key_record = db.query(Pengaturan).filter(Pengaturan.kunci == "vapid_public_key").first()

    if private_key_record and public_key_record:
        return {
            "private": private_key_record.nilai,
            "public": public_key_record.nilai
        }

    # Generate new VAPID keys
    private_key = ec.generate_private_key(ec.SECP256R1())
    public_key = private_key.public_key()

    priv_bytes = private_key.private_numbers().private_value.to_bytes(32, 'big')
    priv_b64 = base64.urlsafe_b64encode(priv_bytes).decode('utf-8').rstrip('=')

    # https://datatracker.ietf.org/doc/html/rfc7515#appendix-C
    # ANSI X9.62 uncompressed representation
    pub_bytes = b'\x04' + \
                public_key.public_numbers().x.to_bytes(32, 'big') + \
                public_key.public_numbers().y.to_bytes(32, 'big')
    pub_b64 = base64.urlsafe_b64encode(pub_bytes).decode('utf-8').rstrip('=')

    keys = {"private": priv_b64, "public": pub_b64}
    
    # Save to db
    if not private_key_record:
        db.add(Pengaturan(kunci="vapid_private_key", nilai=priv_b64))
    if not public_key_record:
        db.add(Pengaturan(kunci="vapid_public_key", nilai=pub_b64))
    
    db.commit()
    return keys

def send_push_notification(subscription_info: dict, message: str, db: Session):
    keys = get_or_create_vapid_keys(db)
    
    try:
        webpush(
            subscription_info=subscription_info,
            data=message,
            vapid_private_key=keys["private"],
            vapid_claims={
                "sub": "mailto:admin@poldakalsel.go.id"
            }
        )
        return True
    except WebPushException as ex:
        print("Push error:", ex)
        return False
