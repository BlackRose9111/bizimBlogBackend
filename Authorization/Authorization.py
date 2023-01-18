class Authorization():
    instance = None
    jwt_secret = None
    def __init__(self):
        from environment import getconfig
        self.instance = self
        self.jwt_secret = getconfig("JWT_SECRET")
    def generate_token(self,user):
        import jwt
        from datetime import datetime, timedelta
        payload = {
            'id': user.id,
            'exp': datetime.utcnow() + timedelta(days=30),
            'iat': datetime.utcnow()

        }
        token = jwt.encode(payload, self.jwt_secret, algorithm='HS256')
        return token
    def decode_token(self,token):
        import jwt
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=['HS256'])
            return payload['id']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'
    def get_user(self,token):
        from Models.Models import User
        id = self.decode_token(token)
        if id == None:
            return None
        return User.get(id)


    @staticmethod
    def get_instance():
        if Authorization.instance == None:
            Authorization.instance = Authorization()
        return Authorization.instance
