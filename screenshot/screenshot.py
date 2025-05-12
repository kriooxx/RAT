import pyautogui
from PIL import Image

# Capture d'écran
screenshot = pyautogui.screenshot()

# Sauvegarder le screenshot en format .jpg
screenshot.save("screenshot.jpg", "JPEG")

print("Capture d'écran sauvegardée en format .jpg sous 'screenshot.jpg'.")
