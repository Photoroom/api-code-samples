#!/usr/bin/env python3
"""
Batch Background Removal Script

Process multiple images in a directory using the Photoroom API.
Useful for e-commerce, catalog processing, or bulk image editing.

Usage:
    python batch_remove_background.py /path/to/input/folder /path/to/output/folder

Requirements:
    pip install tqdm
    
    Or use the standard library version (without progress bars):
    python batch_remove_background_no_tqdm.py /path/to/input /path/to/output
"""

import os
import sys
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# Import the remove_background function from the existing module
from remove_background import remove_background

# Supported image formats
SUPPORTED_FORMATS = ('.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff')


def process_single_image(input_path: str, output_path: str) -> tuple:
    """
    Process a single image and return the result.
    
    Returns:
        tuple: (input_path, success: bool, error_message: str or None)
    """
    try:
        remove_background(input_path, output_path)
        return (input_path, True, None)
    except Exception as e:
        return (input_path, False, str(e))


def batch_remove_background(
    input_dir: str,
    output_dir: str,
    max_workers: int = 3,
    delay_between_requests: float = 0.5
):
    """
    Process all images in input_dir and save to output_dir.
    
    Args:
        input_dir: Directory containing input images
        output_dir: Directory to save processed images
        max_workers: Number of concurrent workers (default: 3)
        delay_between_requests: Delay between API calls in seconds (default: 0.5)
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    
    # Validate input directory
    if not input_path.exists():
        print(f"Error: Input directory '{input_dir}' does not exist.")
        sys.exit(1)
    
    if not input_path.is_dir():
        print(f"Error: '{input_dir}' is not a directory.")
        sys.exit(1)
    
    # Create output directory if it doesn't exist
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Find all image files
    image_files = [
        f for f in input_path.iterdir()
        if f.is_file() and f.suffix.lower() in SUPPORTED_FORMATS
    ]
    
    if not image_files:
        print(f"No supported images found in '{input_dir}'.")
        print(f"Supported formats: {', '.join(SUPPORTED_FORMATS)}")
        sys.exit(1)
    
    print(f"Found {len(image_files)} images to process.")
    print(f"Output directory: {output_path}")
    print(f"Concurrent workers: {max_workers}")
    print("-" * 50)
    
    # Process images
    successful = 0
    failed = 0
    failed_files = []
    
    # Try to use tqdm for progress bars, fallback to simple printing
    try:
        from tqdm import tqdm
        progress_bar = tqdm(total=len(image_files), desc="Processing")
    except ImportError:
        progress_bar = None
        print("Note: Install 'tqdm' for progress bars: pip install tqdm")
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_file = {}
        for image_file in image_files:
            output_file = output_path / f"{image_file.stem}_no_bg.png"
            
            # Add delay between submissions to avoid rate limiting
            time.sleep(delay_between_requests)
            
            future = executor.submit(
                process_single_image,
                str(image_file),
                str(output_file)
            )
            future_to_file[future] = image_file
        
        # Process completed tasks
        for future in as_completed(future_to_file):
            input_file = future_to_file[future]
            input_path_str, success, error = future.result()
            
            if progress_bar:
                progress_bar.update(1)
            
            if success:
                successful += 1
                if not progress_bar:
                    print(f"✓ {input_file.name}")
            else:
                failed += 1
                failed_files.append((input_file.name, error))
                if not progress_bar:
                    print(f"✗ {input_file.name}: {error}")
    
    if progress_bar:
        progress_bar.close()
    
    # Print summary
    print("-" * 50)
    print(f"Processing complete!")
    print(f"  Successful: {successful}")
    print(f"  Failed: {failed}")
    print(f"  Total: {len(image_files)}")
    
    if failed_files:
        print("\nFailed files:")
        for filename, error in failed_files:
            print(f"  - {filename}: {error}")
    
    return successful, failed


def main():
    """Main entry point"""
    # Check command line arguments
    if len(sys.argv) < 3:
        print("Usage: python batch_remove_background.py <input_folder> <output_folder>")
        print("\nExample:")
        print('  python batch_remove_background.py ./product-photos ./processed')
        print("\nOptional environment variables:")
        print("  MAX_WORKERS=5        Number of concurrent workers (default: 3)")
        print("  API_DELAY=1.0        Delay between requests in seconds (default: 0.5)")
        sys.exit(1)
    
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    
    # Get optional settings from environment
    max_workers = int(os.getenv('MAX_WORKERS', 3))
    api_delay = float(os.getenv('API_DELAY', 0.5))
    
    # Run batch processing
    batch_remove_background(input_dir, output_dir, max_workers, api_delay)


if __name__ == "__main__":
    main()
