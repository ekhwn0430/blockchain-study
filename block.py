from hashlib import sha256
import random
import string


a = sha256(str("hello").encode()).hexdigest()
b = sha256(str("1234").encode()).hexdigest()
c = sha256(str("home").encode()).hexdigest()

print(a)
print(b)
print(c)
print()


problem_word = "a"
problem_difficulty = 2

start_nonce = random.choice(string.ascii_letters)

i = 0
while True:
    nonce = start_nonce + str(i)
    nonce_result = sha256((nonce).encode()).hexdigest()
    print(i, nonce, nonce_result)
    
    if nonce_result[0:problem_difficulty] == problem_word * problem_difficulty:
        nonce = nonce_result
        break
    
    i += 1

print("\n" + nonce)
