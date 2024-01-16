from rest_framework_simplejwt.tokens import RefreshToken

from typing import Dict


# Generate and return JWT tokens
def get_tokens_for_user(user) -> Dict[str, str]:
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }