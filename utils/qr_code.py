import qrcode

def generate_qr_code(url, file_name="qrcode.png"):
    # Create a QR Code object
    qr = qrcode.QRCode(
        version=1,  # controls the size of the QR code (1 is 21x21, can go up to 40)
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # less error correction, more data storage
        box_size=10,  # size of each box in pixels
        border=4,  # thickness of the border (minimum is 4)
    )
    
    # Add data to the QR code
    qr.add_data(url)
    qr.make(fit=True)
    
    # Create an image from the QR code
    img = qr.make_image(fill='black', back_color='white')
    
    # Save the image to a file
    img.save(file_name)

# Call the function to generate the QR code
generate_qr_code("https://docs.openwebui.com/tutorial/functions", "site_qrcode.png")
