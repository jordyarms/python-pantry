"""
Generate QR Code

This script generates a QR code for a given input data (URL or text) and saves it as an image file (PNG by default, with optional SVG output).

Usage:
    python generate_qr_code.py <data> <output_file>

Example:
    python generate_qr_code.py "https://example.com" example_qr.png
    python generate_qr_code.py "https://example.com" example_qr.svg

Dependencies:
    - qrcode[pil]
    - qrcode[svg] (if using SVG output)

Install dependencies:
    pip install qrcode[pil] qrcode[svg]

Author: @jordyarms, gpt-4o
"""

import qrcode
import argparse
import os

def generate_qr_code(data, output_file):
    """
    Generate a QR Code from the given data and save it as an image.
    
    Args:
        data (str): The data to encode in the QR code.
        output_file (str): The output file path for the generated QR code image.
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    
    qr.add_data(data)
    qr.make(fit=True)
    
    file_extension = os.path.splitext(output_file)[1].lower()
    
    if file_extension == ".svg":
        from qrcode.image.svg import SvgImage
        img = qr.make_image(image_factory=SvgImage)
    else:
        img = qr.make_image(fill_color="black", back_color="white")
    
    img.save(output_file)
    print(f"QR code generated and saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate a QR Code from input data.')
    parser.add_argument('data', type=str, help='The data (URL or text) to encode in the QR code')
    parser.add_argument('output_file', type=str, help='The output file path for the QR code image (supports .png and .svg)')
    
    args = parser.parse_args()
    
    generate_qr_code(args.data, args.output_file)
