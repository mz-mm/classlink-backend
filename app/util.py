from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_passowrd, hashed_password):
    return pwd_context.verify(plain_passowrd, hashed_password)

def getCurrentDay(current_day: str):
    if current_day == "Tuesday":
        return 2
    elif current_day == "Wednesday":
        return 3
    elif current_day == "Thursday":
        return 4
    elif current_day == "Friday":
        return 5
    elif current_day == "Saturday":
        return 6
    
    return 1