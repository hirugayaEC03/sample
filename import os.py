import os
if os.path.exists("/usr/bin/chromium-browser"):
    print("Chromium is installed.")
else:
    print("Chromium is missing.")