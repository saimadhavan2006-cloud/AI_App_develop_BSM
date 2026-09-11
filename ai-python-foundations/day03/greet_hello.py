def greet(name: str) -> str:
    """Return a greeting for the given name."""
    return f"Hello, {name}!"

name_input = input("Enter your name: ")
greeting = greet(name_input)
print(greeting)