import sys
import argparse
from PIL import Image, ImageOps
from pathlib import Path

def process_icon(source_path, output_dir, name, threshold=180, chroma_key=None, tolerance=60, padding=12):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    source_path = Path(source_path)
    if not source_path.exists():
        print(f"Error: Source image {source_path} does not exist.")
        sys.exit(1)

    im = Image.open(source_path).convert("RGBA")
    
    # 1. Chroma Keying (Background Removal)
    if chroma_key:
        # chroma_key is expected to be a tuple (R, G, B)
        data = im.getdata()
        new_data = []
        for item in data:
            # Check if color is close to chroma key (allowing some tolerance)
            # Default for green screen: (0, 255, 0)
            if abs(item[0] - chroma_key[0]) < tolerance and abs(item[1] - chroma_key[1]) < tolerance and abs(item[2] - chroma_key[2]) < tolerance:
                new_data.append((0, 0, 0, 0)) # Transparent
            else:
                new_data.append(item)
        im.putdata(new_data)
        print(f"✨ Chroma key removed: {chroma_key} (Tolerance: {tolerance})")

    # 2. Bounding Box & Crop
    # Convert to grayscale for mask (using alpha for transparency aware crop if chroma keyed)
    if chroma_key:
        alpha = im.split()[3]
        bbox = alpha.getbbox()
    else:
        gray = ImageOps.grayscale(im.convert("RGB"))
        mask = gray.point(lambda p: 255 if p < 245 else 0)
        bbox = mask.getbbox()
    
    if bbox:
        l, t, r, b = bbox
        im = im.crop((
            max(0, l - padding), 
            max(0, t - padding), 
            min(im.width, r + padding), 
            min(im.height, b + padding)
        ))
    
    # 3. Save Output PNG
    png_path = output_dir / f"{name}.png"
    im.save(png_path)
    
    # 4. Save PBM for potrace (only if not chroma keyed, as tracing multi-color is not recommended here)
    if not chroma_key:
        gray = ImageOps.grayscale(im.convert("RGB"))
        bw = gray.point(lambda p: 0 if p < threshold else 255, mode="1")
        pbm_path = output_dir / f"{name}.pbm"
        bw.save(pbm_path)
        print(f"   - PBM: {pbm_path} (Threshold: {threshold})")
    
    print(f"✅ Processed {name}")
    print(f"   - PNG: {png_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process icons: crop, binarize, or remove green screen.")
    parser.add_argument("source", help="Path to the source image")
    parser.add_argument("output_dir", help="Directory to save the processed files")
    parser.add_argument("name", help="Base name for the output files")
    parser.add_argument("--threshold", type=int, default=180, help="Threshold for binarization (default: 180)")
    parser.add_argument("--chroma", action="store_true", help="Remove green background (#00FF00)")
    parser.add_argument("--tolerance", type=int, default=60, help="Tolerance for chroma keying (default: 60)")
    parser.add_argument("--padding", type=int, default=12, help="Padding around the icon (default: 12)")
    
    args = parser.parse_args()
    
    key = (0, 255, 0) if args.chroma else None
    process_icon(args.source, args.output_dir, args.name, args.threshold, chroma_key=key, tolerance=args.tolerance, padding=args.padding)
