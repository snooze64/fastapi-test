#!/usr/bin/env python
"""
FastAPI版 Batch Processing Example

元のbatch_processing_example.pyをFastAPI経由で実行するように書き換えたスクリプト
/batch エンドポイントを使用して複数ドキュメントの一括処理を実行する
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
import time

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


def create_sample_documents():
    """Create sample documents for batch processing testing"""
    temp_dir = Path(tempfile.mkdtemp())
    sample_files = []

    # Create various document types
    documents = {
        "document1.txt": "This is a simple text document for testing batch processing.",
        "document2.txt": "Another text document with different content about machine learning.",
        "document3.md": """# Markdown Document

## Introduction
This is a markdown document for testing batch processing capabilities.

### Features
- Markdown formatting
- Code blocks
- Lists

```python
def example():
    return "Hello from markdown"
```
""",
        "report.txt": """Business Report

Executive Summary:
This report demonstrates batch processing capabilities for document analysis.

Key Findings:
1. Parallel processing improves throughput significantly
2. Progress tracking enhances user experience
3. Error handling ensures reliability and robustness

Conclusion:
Batch processing is essential for large-scale document processing workflows.
""",
        "notes.md": """# Meeting Notes

## Date: 2024-01-15

### Attendees
- Alice Johnson (Project Manager)
- Bob Smith (Lead Developer)
- Carol Williams (Data Scientist)

### Discussion Topics
1. **Batch Processing Implementation**
   - Parallel document processing architecture
   - Progress tracking mechanisms
   - Error handling strategies

2. **Performance Metrics**
   - Target: 100 documents/hour processing rate
   - Memory usage: < 4GB maximum
   - Success rate: > 95% reliability

### Action Items
- [ ] Implement batch processing functionality
- [ ] Add progress bars for user feedback
- [ ] Test with large document sets
- [ ] Optimize memory usage patterns

### Next Steps
Continue development and comprehensive testing of batch processing features.
"""
    }

    # Create files
    for filename, content in documents.items():
        file_path = temp_dir / filename
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        sample_files.append(str(file_path))

    return sample_files, temp_dir


async def batch_upload_documents(api_base_url: str, file_paths: list, batch_config: dict = None):
    """
    FastAPI サーバーに複数ドキュメントをバッチアップロード
    
    Args:
        api_base_url: FastAPI server base URL
        file_paths: List of file paths to upload
        batch_config: Batch processing configuration
    """
    try:
        batch_url = f"{api_base_url}/batch"
        
        # Default batch configuration
        if batch_config is None:
            batch_config = {
                "parse_method": "auto",
                "max_workers": 2,
                "display_stats": True
            }
        
        async with aiohttp.ClientSession() as session:
            # Create form data with files and configuration
            data = aiohttp.FormData()
            
            # Add configuration as JSON string
            data.add_field('request_data', json.dumps(batch_config))
            
            # Add files
            file_handles = []
            for file_path in file_paths:
                file_handle = open(file_path, 'rb')
                file_handles.append(file_handle)
                data.add_field('files', file_handle, filename=Path(file_path).name)
            
            try:
                logging.info(f"📦 Starting batch upload of {len(file_paths)} documents...")
                for file_path in file_paths:
                    logging.info(f"  - {Path(file_path).name}")
                
                start_time = time.time()
                
                async with session.post(batch_url, data=data) as response:
                    processing_time = time.time() - start_time
                    
                    if response.status == 200:
                        result = await response.json()
                        logging.info(f"✅ Batch upload successful: {result['message']}")
                        logging.info(f"⏱️  Total processing time: {processing_time:.2f} seconds")
                        logging.info(f"📊 Server processing time: {result['processing_time']:.2f} seconds")
                        return result
                    else:
                        error_text = await response.text()
                        logging.error(f"❌ Batch upload failed: {response.status} - {error_text}")
                        return None
            
            finally:
                # Close all file handles
                for file_handle in file_handles:
                    file_handle.close()
                        
    except Exception as e:
        logging.error(f"Error in batch upload: {str(e)}")
        return None


async def query_batch_content(api_base_url: str, query: str, mode: str = "hybrid"):
    """
    FastAPI サーバーでバッチ処理されたコンテンツにクエリ実行
    
    Args:
        api_base_url: FastAPI server base URL
        query: Query text
        mode: Query mode (hybrid, local, global)
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
                    logging.info(f"[Batch Query]: {query}")
                    logging.info(f"Answer: {result['answer']}")
                    logging.info(f"⏱️  Query time: {result['processing_time']:.2f} seconds\n")
                    return result
                else:
                    error_text = await response.text()
                    logging.error(f"❌ Query failed: {response.status} - {error_text}")
                    return None
                    
    except Exception as e:
        logging.error(f"Error querying batch content: {str(e)}")
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


async def demonstrate_basic_batch_processing(api_base_url: str):
    """Basic batch processing demonstration"""
    logging.info("\n" + "=" * 60)
    logging.info("BASIC BATCH PROCESSING DEMONSTRATION")
    logging.info("=" * 60)

    # Create sample documents
    sample_files, temp_dir = create_sample_documents()

    try:
        logging.info(f"📁 Created {len(sample_files)} sample documents in: {temp_dir}")
        for file_path in sample_files:
            logging.info(f"  - {Path(file_path).name}")

        # Basic batch configuration
        batch_config = {
            "parse_method": "auto",
            "max_workers": 2,
            "display_stats": True
        }

        logging.info("\n📦 Batch processing configuration:")
        logging.info(f"  - Parse method: {batch_config['parse_method']}")
        logging.info(f"  - Max workers: {batch_config['max_workers']}")
        logging.info(f"  - Display stats: {batch_config['display_stats']}")

        # Process batch via FastAPI
        result = await batch_upload_documents(api_base_url, sample_files, batch_config)

        if result:
            logging.info("\n" + "-" * 40)
            logging.info("BATCH PROCESSING RESULTS")
            logging.info("-" * 40)
            logging.info(f"✅ {result['message']}")
            logging.info(f"📄 Document ID: {result['document_id']}")
            
            # Wait for processing to stabilize
            await asyncio.sleep(3)
            
            # Test queries on batch processed content
            logging.info("\n🔍 Querying batch processed content:")
            
            queries = [
                "What types of documents were processed in the batch?",
                "Summarize the key topics from all the processed documents",
                "What are the main findings mentioned in the business report?",
                "List the action items from the meeting notes"
            ]
            
            for query in queries:
                await query_batch_content(api_base_url, query)
                await asyncio.sleep(1)
                
            return result
        else:
            logging.error("❌ Batch processing failed")
            return None

    except Exception as e:
        logging.error(f"❌ Batch processing demonstration failed: {str(e)}")
        return None


async def demonstrate_error_handling(api_base_url: str):
    """Demonstrate error handling with problematic files"""
    logging.info("\n" + "=" * 60)
    logging.info("ERROR HANDLING DEMONSTRATION")
    logging.info("=" * 60)

    temp_dir = Path(tempfile.mkdtemp())

    # Create files with various issues
    files_with_issues = {
        "valid_file.txt": "This is a valid file that should process successfully.",
        "empty_file.txt": "",  # Empty file
        "large_file.txt": "x" * 100000,  # Large file (100KB of 'x')
    }

    created_files = []
    for filename, content in files_with_issues.items():
        file_path = temp_dir / filename
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        created_files.append(str(file_path))

    try:
        logging.info(f"🧪 Testing error handling with {len(created_files)} files:")
        for file_path in created_files:
            name = Path(file_path).name
            size = Path(file_path).stat().st_size
            logging.info(f"  - {name}: {size} bytes")

        # Batch processing with short timeout for demonstration
        batch_config = {
            "parse_method": "auto",
            "max_workers": 1,
            "display_stats": True
        }

        # Process files and handle errors
        result = await batch_upload_documents(api_base_url, created_files, batch_config)

        if result:
            logging.info("\n" + "-" * 40)
            logging.info("ERROR HANDLING RESULTS")
            logging.info("-" * 40)
            logging.info(f"📊 {result['message']}")
            
            # The API already handles errors internally and reports success/failure rates
            return result
        else:
            logging.info("❌ Error handling demonstration completed with expected failures")
            return None

    except Exception as e:
        logging.error(f"❌ Error handling demonstration failed: {str(e)}")
        return None


async def run_batch_processing_example(api_base_url: str):
    """
    Batch Processing example をFastAPI経由で実行
    
    Args:
        api_base_url: FastAPI server base URL
    """
    try:
        logging.info("=" * 70)
        logging.info("Batch Processing FastAPI Example")
        logging.info("=" * 70)
        logging.info("This example demonstrates batch processing capabilities:")
        logging.info("  - Multiple document upload and processing")
        logging.info("  - Batch configuration options")
        logging.info("  - Error handling and recovery")
        logging.info("  - Query processing on batch results")

        # Health check
        if not check_api_health(api_base_url):
            return

        results = {}

        # Basic batch processing
        logging.info("\n🚀 Starting batch processing demonstrations...")
        results["basic"] = await demonstrate_basic_batch_processing(api_base_url)
        
        # Error handling demonstration
        results["error_handling"] = await demonstrate_error_handling(api_base_url)

        # Summary
        logging.info("\n" + "=" * 70)
        logging.info("BATCH PROCESSING SUMMARY")
        logging.info("=" * 70)

        successful_demos = 0
        for demo_name, result in results.items():
            if result:
                logging.info(f"✅ {demo_name.upper()}: Completed successfully")
                successful_demos += 1
            else:
                logging.info(f"❌ {demo_name.upper()}: Failed or had limitations")

        logging.info(f"\n📊 Demonstrations completed: {successful_demos}/{len(results)}")
        
        logging.info("\n💡 Key Features Demonstrated:")
        logging.info("  - Multiple file upload via FastAPI endpoints")
        logging.info("  - Batch processing with configurable parameters")
        logging.info("  - Error handling and success rate reporting")
        logging.info("  - Query processing on batch processed content")
        logging.info("  - Real-time processing feedback")

        logging.info("\n✅ Batch Processing FastAPI example completed!")

    except Exception as e:
        logging.error(f"Error in FastAPI batch example: {str(e)}")
        import traceback
        logging.error(traceback.format_exc())


def main():
    """Main function to run the FastAPI batch example"""
    parser = argparse.ArgumentParser(description="Batch Processing FastAPI Example")
    parser.add_argument(
        "--api-url", 
        default="http://localhost:8000", 
        help="FastAPI server URL (default: http://localhost:8000)"
    )
    
    args = parser.parse_args()
    
    # Run the example
    asyncio.run(run_batch_processing_example(args.api_url))


if __name__ == "__main__":
    # Configure logging first
    configure_logging()
    
    print("Batch Processing FastAPI Example")
    print("=" * 45)
    print("Demonstrating batch document processing via FastAPI")
    print("=" * 45)
    print("Make sure to start the FastAPI server first:")
    print("  python simple_api.py")
    print("=" * 45)
    
    main()