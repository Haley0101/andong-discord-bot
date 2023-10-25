from Modules.Module_Basic import *

def randomNum(_LENGTH = 11):
    result = ""
    string_pool = string.digits 
    
    for i in range(_LENGTH):
        result += random.choice(string_pool)
    
    return result

def randomText(_LENGTH = 14):
    result = ""
    string_pool = string.ascii_letters # 대소문자
    
    for i in range(_LENGTH):
        result += random.choice(string_pool)
    
    return result

def randomNumText(_LENGTH = 20):
    string_pool = string.ascii_letters + string.digits
    result = "" 

    for i in range(_LENGTH):
        result += random.choice(string_pool)
    
    return result

def randomPw(_LENGTH = 24):
    # 숫자 + 대소문자 + 특수문자
    string_pool = string.ascii_letters + string.digits + string.punctuation
    result = "" 

    for i in range(_LENGTH):
        result += random.choice(string_pool)
    
    return result

def randomIl():
    length = random.randint(10, 14)
    return ''.join(random.choice('Il') for _ in range(length))