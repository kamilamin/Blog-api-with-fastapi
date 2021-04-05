from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hash():
    def passwordHash(password: str):
        return pwd_context.hash(password)
    
    def verifyPassword(hashedPassword, requestedPassword):
        return pwd_context.verify(requestedPassword, hashedPassword)
