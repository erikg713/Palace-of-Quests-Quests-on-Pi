from flask_jwt_extended import JWTManager

jwt = JWTManager()

@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id
