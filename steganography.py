from PIL import Image

class Steganography:
    def __init__(self):
        pass

    def _text_to_binary(self, text):
        # Convert text to binary
        return ''.join(format(ord(char), '08b') for char in text)

    def _binary_to_text(self, binary):
        # Convert binary to text
        text = ''.join(chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8))
        return text

    def perform_encryption(self, image_path, hidden_text):
        # Open the image
        image = Image.open(image_path)
        encoded_image = image.convert('RGB')  # Convert image to RGB
        width, height = encoded_image.size
        pixels = encoded_image.load()

        # Convert hidden text to binary
        binary_text = self._text_to_binary(hidden_text) + '1111111111111110'  # EOF marker

        binary_index = 0
        for y in range(height):
            for x in range(width):
                if binary_index < len(binary_text):
                    r, g, b = pixels[x, y]
                    r = (r & ~1) | int(binary_text[binary_index])
                    if binary_index + 1 < len(binary_text):
                        g = (g & ~1) | int(binary_text[binary_index + 1])
                    if binary_index + 2 < len(binary_text):
                        b = (b & ~1) | int(binary_text[binary_index + 2])
                    pixels[x, y] = (r, g, b)
                    binary_index += 3
                else:
                    break
            if binary_index >= len(binary_text):
                break

        # Save the encoded image
        encoded_image_path = 'encoded_image.png'
        encoded_image.save(encoded_image_path)
        return encoded_image_path

    def perform_decryption(self, image_path):
        # Open the encoded image
        encoded_image = Image.open(image_path).convert('RGB')
        width, height = encoded_image.size
        pixels = encoded_image.load()

        binary_text = ""
        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
                binary_text += str(r & 1)
                binary_text += str(g & 1)
                binary_text += str(b & 1)

        # Split by 8 bits and convert to characters
        binary_text = binary_text.split('1111111111111110')[0]  # Remove the EOF marker
        hidden_text = self._binary_to_text(binary_text)
        return hidden_text
