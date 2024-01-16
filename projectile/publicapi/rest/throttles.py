from rest_framework import throttling


class EmailThrottle(throttling.SimpleRateThrottle):
    # Limiting the rate to 1 request per 10 seconds for non-authorized users
    scope = "email"

    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            return None  # No throttling for authenticated users
        else:
            return self.cache_format % {
                "scope": self.scope,
                "ident": self.get_ident(request),
            }
