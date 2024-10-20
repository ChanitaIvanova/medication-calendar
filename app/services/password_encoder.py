import bcrypt
import base64

class PasswordEncoder:
    """
    A utility class for encoding and verifying passwords using bcrypt.

    Attributes:
        UTF8_ENCODING (str): The encoding format used for strings (UTF-8).
    """
    UTF8_ENCODING = 'utf-8'

    @staticmethod
    def encode_password(password, salt_rounds=12):
        """
        Encode a password using bcrypt with a specified number of salt rounds.

        :param password: The password to be encoded.
        :type password: str
        :param salt_rounds: The number of rounds to use for generating the salt (default is 12).
        :type salt_rounds: int
        :return: The Base64-encoded hashed password.
        :rtype: str
        :raises ValueError: If the password is not a non-empty string.
        """
        if not isinstance(password, str) or not password:
            raise ValueError("Password must be a non-empty string.")
        
        salt = bcrypt.gensalt(rounds=salt_rounds)
        hashed_password = bcrypt.hashpw(password.encode(PasswordEncoder.UTF8_ENCODING), salt)
        hashed_password_str = base64.b64encode(hashed_password).decode(PasswordEncoder.UTF8_ENCODING)
        return hashed_password_str

    @staticmethod
    def check_password(password, hashed_password_str):
        """
        Verify a password against a given Base64-encoded hashed password.

        :param password: The password to be verified.
        :type password: str
        :param hashed_password_str: The Base64-encoded hashed password to verify against.
        :type hashed_password_str: str
        :return: True if the password matches the hashed password, False otherwise.
        :rtype: bool
        :raises ValueError: If the hashed password is not a valid Base64-encoded string.
        """
        try:
            hashed_password = base64.b64decode(hashed_password_str.encode(PasswordEncoder.UTF8_ENCODING))
        except base64.binascii.Error as e:
            raise ValueError("Invalid hashed password format. Must be a valid Base64-encoded string.") from e
        
        return bcrypt.checkpw(password.encode(PasswordEncoder.UTF8_ENCODING), hashed_password)
