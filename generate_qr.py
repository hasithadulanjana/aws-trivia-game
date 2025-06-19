#!/usr/bin/env python3
"""
Generate QR Code for AWS Trivia Game
"""
import qrcode
from PIL import Image
import os

def generate_qr_code():
    # Game URL
    game_url = "https://aws-trivia-game.netlify.app/"
    
    # Create QR code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    
    # Add data
    qr.add_data(game_url)
    qr.make(fit=True)
    
    # Create image
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save to static/img directory
    output_path = "static/img/qr-code.png"
    img.save(output_path)
    print(f"QR code saved to: {output_path}")
    print(f"QR code points to: {game_url}")
    
    # Also create a smaller version
    img_small = img.resize((150, 150), Image.Resampling.LANCZOS)
    img_small.save("static/img/qr-code-small.png")
    print("Small QR code saved to: static/img/qr-code-small.png")

if __name__ == "__main__":
    generate_qr_code()
