import sys
import cv2

def convert_brg_to_rgb(input_path):
    # Read the BRG image
    img_brg = cv2.imread(input_path)

    if img_brg is None:
        print("Error: Could not open or find the image.")
        return

    # Convert BRG to RGB
    img_rgb = cv2.cvtColor(img_brg, cv2.COLOR_BGR2RGB)

    # Create the output path
    output_path = f"{input_path.rsplit('.', 1)[0]}_rgb.png"

    # Save the RGB image
    cv2.imwrite(output_path, img_rgb)
    print(f"Converted image saved as: {output_path}")

if __name__ == "__main__":
    # if len(sys.argv) != 2:
    #     print("Usage: python convert_brg_to_rgb.py <input_path>")
    #     sys.exit(1)

    # input_path = sys.argv[1]
    for i in range(33):
        convert_brg_to_rgb(f"{i}.png")

