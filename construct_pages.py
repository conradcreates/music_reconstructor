from PIL import Image
import os, sys

# Constants for A4 at 300 DPI
PAGE_WIDTH = 2480
PAGE_HEIGHT = 3508
MARGIN = 100
SPACING = 50

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <music_name>")
    sys.exit(1)

music_folder = sys.argv[1]
input_dir = "screenshots/processed"
output_dir = os.path.join(music_folder, "pdf_pages")
os.makedirs(output_dir, exist_ok=True)

def create_new_page():
    return Image.new("RGB", (PAGE_WIDTH, PAGE_HEIGHT), color="white")

def save_pdf_pages(pages, base_name="music_page"):
    for i, page in enumerate(pages):
        page.save(os.path.join(output_dir, f"{base_name}_{i+1:03}.png"))

def build_pages_from_images():
    images = [Image.open(os.path.join(input_dir, f)) 
              for f in sorted(os.listdir(input_dir)) if f.endswith(".png")]

    pages = []
    current_page = create_new_page()
    y_offset = MARGIN

    for img in images:
        # Resize if too wide
        if img.width > PAGE_WIDTH - 2 * MARGIN:
            scale = (PAGE_WIDTH - 2 * MARGIN) / img.width
            new_size = (int(img.width * scale), int(img.height * scale))
            img = img.resize(new_size, Image.Resampling.LANCZOS)

        if y_offset + img.height > PAGE_HEIGHT - MARGIN:
            pages.append(current_page)
            current_page = create_new_page()
            y_offset = MARGIN

        current_page.paste(img, (MARGIN, y_offset))
        y_offset += img.height + SPACING

    pages.append(current_page)
    return pages

# Build pages and save them
pages = build_pages_from_images()
save_pdf_pages(pages)
print(f"Saved {len(pages)} pages to '{output_dir}/'")

pages_folder = os.path.join(music_folder, "pdf_pages")
image_list = [Image.open(os.path.join(pages_folder, f)) 
              for f in sorted(os.listdir(pages_folder)) if f.endswith(".png")]

pdf_path = os.path.join(music_folder, "music_sheet.pdf")
image_list[0].save(pdf_path, save_all=True, append_images=image_list[1:])

