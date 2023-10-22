import bcrypt

def hash_password(password):
    # Hash a password for the first time
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed

def check_password(hashed_password, user_password):
    # Check hashed password. Using bcrypt.checkpw()
    if bcrypt.checkpw(user_password.encode('utf-8'), hashed_password):
        return True
    return False

# password = input("Enter your password: ")
# hashed_password = hash_password(password)
# # Save `hashed_password` in your database
# print(hashed_password)
# # When a user logs in
# entered_password = input("Enter your password: ")

# # Check if the entered password matches the one in the database
# if check_password(hashed_password, entered_password):
#     print("Password is correct")
# else:
#     print("Password is incorrect")