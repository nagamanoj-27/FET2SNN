import os

def list_files(dir_path):
    for root, dirs, files in os.walk(dir_path):
        for f in files:
            full_path = os.path.join(root, f)
            print(f"{full_path} -> size: {os.path.getsize(full_path)} bytes")

print("Checking media directory:")
if os.path.exists('media'):
    list_files('media')
else:
    print("media directory does not exist!")
