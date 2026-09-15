def greet_user(name):
    """
    Greet the user with a personalized message.

    Parameters:
    name (str): The name of the user.

    Returns:
    str: A greeting message.
    """
    return f"Hello, {name}! Welcome to the AI Python Foundations course."

name = input("Enter your name: ")
greeting_message = greet_user(name)
print(greeting_message)
#name is parameter and input is function to take input from user.
#And greet_user is function to greet user with personalized message.
