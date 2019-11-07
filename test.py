import sys
say_hello = lambda: (
    message := "Hello world",
    print(message + "\n")
)
say_hello()