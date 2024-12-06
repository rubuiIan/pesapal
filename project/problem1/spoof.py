from PIL import Image
import hashlib
import random
import os

# Function to load an image
def load_image(image_path):
    try:
        img = Image.open(image_path)
        return img
    except Exception as e:
        print(f"Error loading image: {e}")
        return None

# Function to manipulate the image (adjusting metadata or pixels)
def manipulate_image(img):
    pixels = img.load()
    width, height = img.size
    
    # Change random pixels slightly to alter the image
    for i in range(random.randint(50, 100)):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        r, g, b = pixels[x, y]
        
        # Modify the pixel values slightly
        r = (r + random.randint(-5, 5)) % 256
        g = (g + random.randint(-5, 5)) % 256
        b = (b + random.randint(-5, 5)) % 256
        
        pixels[x, y] = (r, g, b)
    
    return img

# Function to hash the image and check if it matches the desired prefix
def hash_image(img):
    img_bytes = img.tobytes()
    
    sha256_hash = hashlib.sha256(img_bytes).hexdigest()
    return sha256_hash

# Function to adjust the image until the hash prefix matches
def adjust_until_hash_matches(img, target_prefix="0000", max_attempts=10000):
    attempts = 0
    while attempts < max_attempts:
        img = manipulate_image(img)  
        hashed_value = hash_image(img) 
        if hashed_value.startswith(target_prefix):
            print(f"Match found after {attempts} attempts!")
            print(f"Hash: {hashed_value}")
            break
        attempts += 1
        if attempts % 100 == 0:
            print(f"Attempt {attempts}...")

    if attempts >= max_attempts:
        print(f"Max attempts reached without a match.")

# Main function to load, manipulate and hash the image
def main():
    image_path = "images/Lambo.jpg"
    target_prefix = "0000" 
    
    img = load_image(image_path)
    if img:
        print("Image loaded successfully.")
        adjust_until_hash_matches(img, target_prefix)
    else:
        print("Failed to load image.")

if __name__ == "__main__":
    main()
