import qrcode
from PIL import Image, ImageDraw, ImageFont

class Filter:
    def __init__(self):
        self.messages = []  # Simulates chat message history

    def inlet(self, user_input: str) -> None:
        """
        Simulates user input processing and responds with a QR code or other messages.
        """
        user_input = user_input.strip()

        if user_input.lower() == "/qr-share":
            # Simulate excluding the /qr-share command from messages
            messages = self.messages[:-1]

            if not messages:
                print("No messages available to generate a QR code.")
            else:
                # Use Anthony Bourdain's famous quote for the QR code
                famous_quote = (
                    "“Travel isn’t always pretty. It isn’t always comfortable. "
                    "Sometimes it hurts, it even breaks your heart. But that’s okay. "
                    "The journey changes you; it should change you.”\n"
                    "— Anthony Bourdain"
                )
                self.display_qr_code(famous_quote)
        else:
            # Store the message in the history
            self.messages.append(user_input)
            print(f"Message received: {user_input}")

    def generate_qr_code(self, data: str) -> Image:
        """
        Generate a QR code image from the given data with a custom background and style.
        :param data: The data to encode in the QR code.
        :return: The QR code image as a PIL Image object.
        """
        qr = qrcode.QRCode(
            version=1,  # Controls the size of the QR code
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        # Generate the QR code image with custom colors (black foreground, white background)
        img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

        return img

    def display_qr_code(self, data: str) -> None:
        """
        Generate and display the QR code with custom styling.
        :param data: The data to encode in the QR code.
        """
        img = self.generate_qr_code(data)

        # Resize the QR code image using the LANCZOS filter for high-quality resizing
        img = img.resize((400, 400), Image.LANCZOS)

        # Create a new background image (optional custom background color)
        background = Image.new('RGB', (500, 550), (255, 255, 255))  # White background
        background.paste(img, (50, 50))  # Paste the QR code in the center of the background

        # Draw text on the image
        draw = ImageDraw.Draw(background)
        
        try:
            # Load a nice font, using a system font or a TTF file
            font = ImageFont.truetype("arial.ttf", 20)
        except IOError:
            # Fallback to default font if custom font isn't available
            font = ImageFont.load_default()

        # Add Anthony Bourdain's quote under the QR code
        quote = (
            "“Travel isn’t always pretty. It isn’t always comfortable.\n"
            "Sometimes it hurts, it even breaks your heart.\n"
            "But that’s okay. The journey changes you; it should change you.”\n"
            "— Anthony Bourdain"
        )
        text_position = (50, 470)  # Position for the text
        draw.text(text_position, quote, font=font, fill="black")

        # Show the final image
        background.show()


# Simulating user input and the /qr-share command
if __name__ == "__main__":
    chat_filter = Filter()

    while True:
        user_input = input("Enter a message (or /qr-share to generate QR): ")
        chat_filter.inlet(user_input)

        # Stop the loop if the user types "exit"
        if user_input.lower() == "exit":
            break
