import os
import requests
from typing import Optional, Dict, Any, List
import redis
import logging
import json

from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicNumbers
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend

import base64
import jwt
from datetime import datetime
from py_linq import Enumerable


logger = logging.getLogger(__name__)


class JWTHandler:
    def __init__(self):
        pass
    
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        try:
            public_key = self.get_redis_pkey()
            if public_key is None:
                public_key = self.retrieve_public_key()
                
            if public_key is None:
                logger.error("Public key could not be retrieved.")
                return None
            
            jwt_content = self.decode_token(token, public_key)
            if jwt_content is None:
                logger.error("JWT token could not be decoded.")
                return None
            
            return jwt_content
        except jwt.DecodeError:
            logger.error("Error decoding JWT token.")
            return None
    
    def decode_token(self, token: str, public_key) -> Optional[Dict[str, Any]]:
        try:
            n_bytes = base64.urlsafe_b64decode(public_key['n'] + '==')
            e_bytes = base64.urlsafe_b64decode(public_key['e'] + '==')

            n = int.from_bytes(n_bytes, 'big')
            e = int.from_bytes(e_bytes, 'big')
            public_numbers = rsa.RSAPublicNumbers(e, n)
            pk_data= public_numbers.public_key(backend=default_backend())


            jwt_content = jwt.decode(token, pk_data, algorithms=[os.getenv("OAUTH_ALGORITHM")], audience=os.getenv("AUDIENCE"), issuer=os.getenv("OAUTH_ISSUER"))
            return jwt_content
        except jwt.ExpiredSignatureError as e:
            logger.error(f"JWT token has expired: {e}")
        except jwt.InvalidAudienceError as e:
            logger.error(f"Invalid audience in JWT token: {e}")
        except jwt.InvalidTokenError as e:
            logger.error(f"Invalid JWT token: {e}")
        except Exception as e:
            logger.error(f"Error decoding JWT token: {e}")
        return None
        
    def retrieve_public_key(self) -> Optional[Dict[str, Any]]:
        try:
            oauth_api_url = os.getenv("JWT_PUBLIC_KEY")
            
            if not oauth_api_url:
                logger.error("Public key not found in environment variables.")
                return None
            
            session  = requests.Session()
            session.verify = False
            session.headers.update({
                'User-Agent': 'BugTracker/1.0',
                'Accept': 'application/json',
                'Connection': 'close'
            })
            
            response = session.get(oauth_api_url, timeout=10)
            response.raise_for_status()
            
            keys = response.json().get("keys", [])
            if not keys:
                logger.error("No keys found in the JWKS response.")
                return None
            
            public_key = Enumerable(keys).where(lambda u: u.get('alg') == os.getenv("OAUTH_ALGORITHM")).first_or_default(None)
            
            if public_key is None:
                logger.error(f"No matching key found for algorithm {os.getenv('OAUTH_ALGORITHM')}.")
                return None
            self.set_redis_pkey(json.dumps(public_key))
            return public_key
        except Exception as e:
            logger.error(f"Error retrieving public key: {e}")
            return None
        
    def set_redis_pkey(self, public_key: str) -> None:
        try:
            host = os.getenv("REDIS_HOST", "localhost")
            port = int(os.getenv("REDIS_PORT", 6379))
            r = redis.Redis(host=host, port=port, db=0, ssl=False)
            r.set("public_key", public_key, ex=int(os.getenv("JWT_CACHE_TTL",3600)))  # Cache for 1 hour
        except Exception as e:
            logger.error(f"Error setting public key in Redis: {e}")

    def get_redis_pkey(self) ->  Optional[Dict[str, Any]]:
        try:
            host = os.getenv("REDIS_HOST", "localhost")
            port = int(os.getenv("REDIS_PORT", 6379))
            r = redis.Redis(host=host, port=port, db=0, ssl=False)
            public_key = r.get("public_key")
            if public_key:
                public_key_json = public_key.decode('utf-8')
                return json.loads(public_key_json)
            else:
                logger.error("Public key not found in Redis.")
                return None
        except Exception as e:
            logger.error(f"Error retrieving public key: {e}")
            return None
    