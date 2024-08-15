import bcrypt
import base64

class PasswordEncoder:
    UTF8_ENCODING = 'utf-8'

    @staticmethod
    def encode_password(password):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode(PasswordEncoder.UTF8_ENCODING), salt)
        hashed_password_str = base64.b64encode(hashed_password).decode(PasswordEncoder.UTF8_ENCODING)
        return hashed_password_str


    @staticmethod
    def check_password(password, hashed_password_str):
        hashed_password = base64.b64decode(hashed_password_str.encode(PasswordEncoder.UTF8_ENCODING))
        return bcrypt.checkpw(password.encode(PasswordEncoder.UTF8_ENCODING), hashed_password)