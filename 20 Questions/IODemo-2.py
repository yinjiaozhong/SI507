
# IOdemo.py

# This file demonstrates reading and writing files

def demo():
    f1 = open("foods.txt", "w") # Open file foods.txt for writing
    foods = ["spam", "chocolate", "ice cream", "pizza"]
    for food in foods:
        print(food, file = f1)  # Automatically adds newline after each food
    f1.close()  # It's always good to close the file when you're done!

    f2 = open("foods.txt", "r") # Open file foods.txt for reading
    inputList = f2.readlines()  # Generate a list with lines from foods.txt
    f2.close() # It's always good to close the file when you're done!

    print(inputList)  # Notice the \n newline characters

    # Now we'll remove the \n symbols and print it again
    cleanList = [x.strip("\n") for x in inputList]
    print(cleanList)

    # Often, it's simpler to process a file one line at a time
    f2 = open("foods.txt")      # Open file for reading (default) again
    while True:
        line = f2.readline()
        if line == '':          # An empty line means the end of the file
            break
        line = line.strip()     # Get rid of that pesky \n symbol
        print(line)             # Print the line
    f2.close() # It's always good to close the file when you're done!
