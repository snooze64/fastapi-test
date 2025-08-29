#!/usr/bin/env python3
"""
FastAPI版 Image Format Test

元のimage_format_test.pyをFastAPI経由で実行するように書き換えたスクリプト
様々な画像フォーマット（JPG、PNG、BMP、TIFF、GIF、WebP）のアップロードと処理をテストする
"""

import os
import argparse
import asyncio
import logging
from pathlib import Path
import requests
import aiohttp
import json
import tempfile
import base64

# Add project root directory to Python path
import sys
sys.path.append(str(Path(__file__).parent.parent))

from dotenv import load_dotenv

load_dotenv(dotenv_path=".env", override=False)


def configure_logging():
    """Configure logging for the application"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )


def check_pillow_installation():
    """Check if PIL/Pillow is installed and available"""
    try:
        from PIL import Image
        print(f"✅ PIL/Pillow found: PIL version {getattr(Image, '__version__', 'Unknown')}")
        return True
    except ImportError:
        print("❌ PIL/Pillow not found. Please install Pillow:")
        print("  pip install Pillow")
        return False


def get_image_info(image_path: Path):
    """Get detailed image information"""
    try:
        from PIL import Image
        
        with Image.open(image_path) as img:
            return {
                "format": img.format,
                "mode": img.mode,
                "size": img.size,
                "has_transparency": img.mode in ("RGBA", "LA") or "transparency" in img.info,
            }
    except Exception as e:
        return {"error": str(e)}


def create_sample_images():
    """Create sample images for testing different formats"""
    try:
        from PIL import Image, ImageDraw
        
        temp_dir = Path(tempfile.mkdtemp())
        sample_images = []
        
        # Create a simple test image
        img = Image.new('RGB', (400, 300), color='white')
        draw = ImageDraw.Draw(img)
        
        # Draw some content
        draw.rectangle([50, 50, 350, 250], outline='blue', width=3)
        draw.text((70, 70), "RAGAnything Image Format Test", fill='black')
        draw.text((70, 100), "This image tests different formats:", fill='black')
        draw.text((70, 130), "• JPG/JPEG - Lossy compression", fill='red')
        draw.text((70, 160), "• PNG - Lossless with transparency", fill='green')
        draw.text((70, 190), "• BMP - Uncompressed bitmap", fill='blue')
        draw.text((70, 220), "FastAPI Integration Test", fill='purple')
        
        # Save in different formats
        formats = {
            'jpg': {'format': 'JPEG', 'ext': '.jpg'},
            'png': {'format': 'PNG', 'ext': '.png'},
            'bmp': {'format': 'BMP', 'ext': '.bmp'},
        }
        
        # Add transparency for PNG
        img_with_alpha = Image.new('RGBA', (400, 300), color=(255, 255, 255, 200))
        draw_alpha = ImageDraw.Draw(img_with_alpha)
        draw_alpha.rectangle([50, 50, 350, 250], outline=(0, 0, 255, 255), width=3)
        draw_alpha.text((70, 70), "PNG with Transparency", fill=(0, 0, 0, 255))
        
        for name, config in formats.items():
            file_path = temp_dir / f"test_image{config['ext']}"
            
            if name == 'png':
                # Save PNG with transparency
                img_with_alpha.save(file_path, config['format'])
            else:
                img.save(file_path, config['format'])
            
            sample_images.append(str(file_path))
            logging.info(f"Created sample image: {file_path}")
        
        return sample_images, temp_dir
        
    except Exception as e:
        logging.error(f"Error creating sample images: {str(e)}")
        return [], None


async def upload_image(api_base_url: str, image_path: str):
    """
    FastAPI サーバーに画像ファイルをアップロード
    
    Args:
        api_base_url: FastAPI server base URL
        image_path: Path to image file
    """
    try:
        upload_url = f"{api_base_url}/upload"
        
        # Get image info before upload
        image_path_obj = Path(image_path)
        img_info = get_image_info(image_path_obj)
        
        logging.info(f"📸 Uploading image: {image_path_obj.name}")
        logging.info(f"   Format: {img_info.get('format', 'Unknown')}")
        logging.info(f"   Size: {img_info.get('size', 'Unknown')}")
        logging.info(f"   Mode: {img_info.get('mode', 'Unknown')}")
        if 'error' not in img_info:
            logging.info(f"   Has transparency: {img_info.get('has_transparency', False)}")
        
        async with aiohttp.ClientSession() as session:
            with open(image_path, 'rb') as f:
                data = aiohttp.FormData()
                data.add_field('file', f, filename=image_path_obj.name)
                
                async with session.post(upload_url, data=data) as response:
                    if response.status == 200:
                        result = await response.json()
                        logging.info(f"✅ Upload successful: {result['message']}")
                        logging.info(f"⏱️  Processing time: {result['processing_time']:.2f} seconds")
                        return result
                    else:
                        error_text = await response.text()
                        logging.error(f"❌ Upload failed: {response.status} - {error_text}")
                        return None
                        
    except Exception as e:
        logging.error(f"Error uploading image: {str(e)}")
        return None


async def query_image_content(api_base_url: str, query: str, mode: str = "hybrid"):
    """
    FastAPI サーバーで画像コンテンツにクエリ実行
    
    Args:
        api_base_url: FastAPI server base URL
        query: Query text
        mode: Query mode
    """
    try:
        query_url = f"{api_base_url}/query"
        
        payload = {
            "query": query,
            "mode": mode
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(query_url, json=payload) as response:
                if response.status == 200:
                    result = await response.json()
                    logging.info(f"[Image Query]: {query}")
                    logging.info(f"Answer: {result['answer']}")
                    logging.info(f"⏱️  Query time: {result['processing_time']:.2f} seconds\n")
                    return result
                else:
                    error_text = await response.text()
                    logging.error(f"❌ Query failed: {response.status} - {error_text}")
                    return None
                    
    except Exception as e:
        logging.error(f"Error querying image content: {str(e)}")
        return None


async def test_image_format_via_api(api_base_url: str, image_path: str):
    """Test single image format via FastAPI"""
    try:
        image_path_obj = Path(image_path)
        
        logging.info(f"\n🧪 Testing image format: {image_path_obj.suffix.upper()}")
        logging.info(f"📏 File size: {image_path_obj.stat().st_size / 1024:.1f} KB")
        
        # Check format support
        supported_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif", ".gif", ".webp"}
        if image_path_obj.suffix.lower() not in supported_extensions:
            logging.error(f"❌ Unsupported file format: {image_path_obj.suffix}")
            logging.error(f"   Supported formats: {', '.join(supported_extensions)}")
            return False
        
        # Upload and process image
        upload_result = await upload_image(api_base_url, image_path)
        
        if not upload_result:
            logging.error("❌ Image upload/processing failed")
            return False
        
        # Wait for processing
        await asyncio.sleep(2)
        
        # Query the processed image content
        image_queries = [
            "What text or content can you see in this image?",
            "Describe what is shown in the processed image",
            "Are there any tables, diagrams, or structured content in this image?",
        ]
        
        logging.info("🔍 Querying processed image content:")
        
        for query in image_queries:
            await query_image_content(api_base_url, query)
            await asyncio.sleep(1)
        
        return True
        
    except Exception as e:
        logging.error(f"Error testing image format via API: {str(e)}")
        return False


async def batch_test_image_formats(api_base_url: str, image_paths: list):
    """Test multiple image formats via batch processing"""
    try:
        logging.info(f"\n📦 Testing batch image processing with {len(image_paths)} images...")
        
        # Use batch endpoint for multiple images
        batch_url = f"{api_base_url}/batch"
        batch_config = {
            "parse_method": "auto",  # Auto-detect best method for images
            "max_workers": 2,
            "display_stats": True
        }
        
        async with aiohttp.ClientSession() as session:
            data = aiohttp.FormData()
            data.add_field('request_data', json.dumps(batch_config))
            
            # Add all image files
            file_handles = []
            for image_path in image_paths:
                file_handle = open(image_path, 'rb')
                file_handles.append(file_handle)
                data.add_field('files', file_handle, filename=Path(image_path).name)
            
            try:
                logging.info(f"📤 Uploading {len(image_paths)} images for batch processing...")
                
                async with session.post(batch_url, data=data) as response:
                    if response.status == 200:
                        result = await response.json()
                        logging.info(f"✅ Batch processing successful: {result['message']}")
                        logging.info(f"⏱️  Total processing time: {result['processing_time']:.2f} seconds")
                        
                        # Wait for processing to complete
                        await asyncio.sleep(3)
                        
                        # Query the batch processed content
                        batch_queries = [
                            "What different image formats were processed in this batch?",
                            "Summarize the text content found across all the processed images",
                            "Compare the quality or content differences between the different image formats",
                        ]
                        
                        logging.info("\n🔍 Querying batch processed image content:")
                        
                        for query in batch_queries:
                            await query_image_content(api_base_url, query)
                            await asyncio.sleep(1)
                        
                        return result
                    else:
                        error_text = await response.text()
                        logging.error(f"❌ Batch processing failed: {response.status} - {error_text}")
                        return None
            finally:
                # Close file handles
                for file_handle in file_handles:
                    file_handle.close()
                        
    except Exception as e:
        logging.error(f"Error in batch image format testing: {str(e)}")
        return None


def check_api_health(api_base_url: str):
    """FastAPI サーバーのヘルスチェック"""
    try:
        health_url = f"{api_base_url}/health"
        response = requests.get(health_url, timeout=10)
        
        if response.status_code == 200:
            health_data = response.json()
            logging.info(f"✅ API Server is healthy: {health_data['message']}")
            return True
        else:
            logging.error(f"❌ API Server health check failed: {response.status_code}")
            return False
            
    except Exception as e:
        logging.error(f"❌ Cannot connect to API server: {str(e)}")
        logging.error(f"Make sure the FastAPI server is running at {api_base_url}")
        return False


async def run_image_format_test(api_base_url: str, image_path: str = None):
    """
    Image Format Test をFastAPI経由で実行
    
    Args:
        api_base_url: FastAPI server base URL  
        image_path: Optional specific image file to test
    """
    try:
        logging.info("=" * 65)
        logging.info("Image Format Processing FastAPI Test")
        logging.info("=" * 65)
        logging.info("This test demonstrates image format processing:")
        logging.info("  - Multiple image format support (JPG, PNG, BMP, etc.)")
        logging.info("  - OCR text extraction from images")
        logging.info("  - Image content analysis and queries")
        logging.info("  - Batch image processing")

        # Health check
        if not check_api_health(api_base_url):
            return

        # Check PIL/Pillow installation
        logging.info("\n🔧 Checking PIL/Pillow installation...")
        if not check_pillow_installation():
            logging.error("PIL/Pillow is required for image processing")
            return

        results = {}

        if image_path:
            # Test specific image file
            logging.info(f"\n📄 Testing specific image file: {image_path}")
            
            if not Path(image_path).exists():
                logging.error(f"❌ File not found: {image_path}")
                return
            
            results["single_file"] = await test_image_format_via_api(api_base_url, image_path)
            
        else:
            # Create and test sample images
            logging.info("\n🖼️  Creating sample images for format testing...")
            sample_images, temp_dir = create_sample_images()
            
            if not sample_images:
                logging.error("❌ Failed to create sample images")
                return
            
            # Test individual formats
            logging.info("\n📄 Testing individual image formats...")
            individual_results = []
            
            for image_path in sample_images:
                success = await test_image_format_via_api(api_base_url, image_path)
                individual_results.append(success)
                await asyncio.sleep(2)
            
            results["individual_formats"] = individual_results
            
            # Test batch processing
            logging.info("\n📦 Testing batch image processing...")
            batch_result = await batch_test_image_formats(api_base_url, sample_images)
            results["batch_processing"] = batch_result is not None

        # Summary
        logging.info("\n" + "=" * 65)
        logging.info("IMAGE FORMAT TEST SUMMARY")
        logging.info("=" * 65)

        if image_path:
            if results.get("single_file"):
                logging.info(f"✅ Single file test: SUCCESS")
                logging.info(f"   File: {Path(image_path).name}")
            else:
                logging.info(f"❌ Single file test: FAILED")
        else:
            individual_success = sum(results.get("individual_formats", []))
            total_formats = len(results.get("individual_formats", []))
            logging.info(f"📊 Individual format tests: {individual_success}/{total_formats} successful")
            
            if results.get("batch_processing"):
                logging.info("✅ Batch processing test: SUCCESS")
            else:
                logging.info("❌ Batch processing test: FAILED")

        logging.info("\n💡 Key Features Tested:")
        logging.info("  - Multiple image format upload and processing")
        logging.info("  - OCR text extraction from images") 
        logging.info("  - Image content analysis via natural language queries")
        logging.info("  - Batch processing of multiple image formats")
        logging.info("  - FastAPI integration for image processing workflows")

        logging.info("\n✅ Image Format FastAPI test completed!")

    except Exception as e:
        logging.error(f"Error in image format FastAPI test: {str(e)}")
        import traceback
        logging.error(traceback.format_exc())


def main():
    """Main function to run the image format FastAPI test"""
    parser = argparse.ArgumentParser(description="Image Format FastAPI Test")
    parser.add_argument(
        "--api-url", 
        default="http://localhost:8000", 
        help="FastAPI server URL (default: http://localhost:8000)"
    )
    parser.add_argument(
        "--file",
        help="Path to specific image file to test (optional)"
    )
    parser.add_argument(
        "--check-pillow", 
        action="store_true", 
        help="Only check PIL/Pillow installation"
    )
    
    args = parser.parse_args()
    
    # Check PIL/Pillow installation
    if args.check_pillow:
        if check_pillow_installation():
            print("✅ PIL/Pillow installation check passed!")
            return 0
        else:
            return 1
    
    # Run the test
    asyncio.run(run_image_format_test(args.api_url, args.file))
    return 0


if __name__ == "__main__":
    # Configure logging first
    configure_logging()
    
    print("Image Format Processing FastAPI Test")
    print("=" * 50)
    print("Testing various image formats via FastAPI")
    print("=" * 50)
    print("Make sure to start the FastAPI server first:")
    print("  python simple_api.py")
    print("=" * 50)
    
    sys.exit(main())