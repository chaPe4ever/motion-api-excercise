from drf_yasg.inspectors import SwaggerAutoSchema


class CustomSwaggerAutoSchema(SwaggerAutoSchema):
    """
    Custom schema to handle JWT token without requiring 'Bearer' prefix
    """

    def get_security(self):
        security = super().get_security()
        if security:
            return security
        return [{"Bearer": []}]
