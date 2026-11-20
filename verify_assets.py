import os
import subprocess
import time

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
OUTPUT_DIR = r"D:\code_injectors\screenshots"

# We can test that the images exist and are accessible
for img_name in ['guardian_illustration.jpg', 'supply_chain_illustration.jpg', 'code_illustration.jpg']:
    p = os.path.join(r"D:\code_injectors\static\images", img_name)
    print(img_name, "exists in static/images:", os.path.exists(p), os.path.getsize(p) if os.path.exists(p) else 0)

print("Images verification complete!")
