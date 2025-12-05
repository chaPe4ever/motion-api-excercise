from rest_framework_simplejwt.authentication import JWTAuthentication


class JWTAuthenticationWithoutBearer(JWTAuthentication):
    """
    Custom JWT Authentication that accepts tokens with or without 'Bearer' prefix
    """
    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token

    def get_raw_token(self, header):
        """
        Extracts the token from the Authorization header.
        Accepts both 'Bearer <token>' and just '<token>'
        """
        # header is already bytes, decode it to string first
        if isinstance(header, bytes):
            header = header.decode('utf-8')

        parts = header.split()

        if len(parts) == 0:
            return None

        # If token is provided with 'Bearer' prefix
        if parts[0].lower() == 'bearer':
            if len(parts) == 1:
                return None
            # Return as bytes for JWT validation
            return parts[1].encode('utf-8') if isinstance(parts[1], str) else parts[1]

        # If token is provided without 'Bearer' prefix (for Swagger convenience)
        if len(parts) == 1:
            # Return as bytes for JWT validation
            return parts[0].encode('utf-8') if isinstance(parts[0], str) else parts[0]

        return None
