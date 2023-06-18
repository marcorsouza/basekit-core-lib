from flasgger import Swagger

def swagger_init_app(app, title, version, description):
    TEMPLATE = {
        "swagger": "2.0",
        "info": {
            "title": title,
            "version": version,
            "description": description
        },
        "securityDefinitions": {
            "Bearer":
                {
                    "type": "apiKey",
                    "name": "Authorization",
                    "in": "header"
                }
        },
        "security": [
            {"Bearer": []}
        ], 
    }
    swagger = Swagger(app, template=TEMPLATE)
    return swagger