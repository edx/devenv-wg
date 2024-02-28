ALLOWED_HOSTS = [
    "*",
    # "exams",
    # "{{ EXAMS_HOST }}"
]

PLATFORM_NAME = "{{ PLATFORM_NAME }}"

DATABASES = {
    'default': {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "{{ EXAMS_MYSQL_DATABASE }}",
        "USER": "{{ EXAMS_MYSQL_USERNAME }}",
        "PASSWORD": "{{ EXAMS_MYSQL_PASSWORD }}",
        "HOST": "{{ MYSQL_HOST }}",
        "PORT": "{{ MYSQL_PORT }}",
        'ATOMIC_REQUESTS': False,
        'CONN_MAX_AGE': 60,
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "KEY_PREFIX": "exams",
        "LOCATION": "redis://{% if REDIS_USERNAME and REDIS_PASSWORD %}{{ REDIS_USERNAME }}:{{ REDIS_PASSWORD }}{% endif %}@{{ REDIS_HOST }}:{{ REDIS_PORT }}/{{ EXAMS_CACHE_REDIS_DB }}",
    }
}

{% set jwt_rsa_key | rsa_import_key %}{{ JWT_RSA_PRIVATE_KEY }}{% endset %}
import json
JWT_AUTH["JWT_ISSUER"] = "{{ JWT_COMMON_ISSUER }}"
JWT_AUTH["JWT_AUDIENCE"] = "{{ JWT_COMMON_AUDIENCE }}"
JWT_AUTH["JWT_SECRET_KEY"] = "{{ JWT_COMMON_SECRET_KEY }}"
# TODO assign a exams-specific public key
JWT_AUTH["JWT_PUBLIC_SIGNING_JWK_SET"] = json.dumps(
    {
        "keys": [
            {
                "kid": "openedx",
                "kty": "RSA",
                "e": "{{ jwt_rsa_key.e|long_to_base64 }}",
                "n": "{{ jwt_rsa_key.n|long_to_base64 }}",
            }
        ]
    }
)
JWT_AUTH["JWT_ISSUERS"] = [
    {
        "ISSUER": "{{ JWT_COMMON_ISSUER }}",
        "AUDIENCE": "{{ JWT_COMMON_AUDIENCE }}",
        "SECRET_KEY": "{{ OPENEDX_SECRET_KEY }}"
    }
]

{{ patch("exams-common-settings") }}
