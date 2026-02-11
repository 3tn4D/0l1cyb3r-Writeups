import zipfile
import os

for i in range(3000, 0, -1):
    with zipfile.ZipFile(f"flag{i}.zip", 'r') as z:
        z.extractall(".")

    if i != 0 :
        os.remove(f"flag{i}.zip")
    