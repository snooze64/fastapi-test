#!/usr/bin/env python
"""
FastAPI版 Modal Processors Example

元のmodalprocessors_example.pyをFastAPI経由で実行するように書き換えたスクリプト
/multimodal-query エンドポイントを使用してマルチモーダルコンテンツ処理を実行する
"""

import os
import argparse
import asyncio
import logging
from pathlib import Path
import requests
import aiohttp
import json
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


async def insert_base_content(api_base_url: str):
    """
    基本的なコンテンツを挿入してモーダルプロセッサーのデモ用ベースを作成
    """
    try:
        content_url = f"{api_base_url}/content"
        
        # Basic content to provide context for modal processing examples
        base_content = [
            {
                "type": "text",
                "text": "This document demonstrates the use of different modal processors for handling multimodal content including images, tables, and equations in RAGAnything system.",
                "page_idx": 0
            },
            {
                "type": "text", 
                "text": "Modal processors are specialized components designed to extract meaningful information from different types of content modalities and integrate them into the knowledge graph.",
                "page_idx": 1
            }
        ]
        
        payload = {
            "content_list": base_content,
            "file_path": "modal_processors_demo.pdf",
            "doc_id": "modal-demo-base",
            "display_stats": True
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(content_url, json=payload) as response:
                if response.status == 200:
                    result = await response.json()
                    logging.info(f"✅ Base content inserted: {result['message']}")
                    return result
                else:
                    error_text = await response.text()
                    logging.error(f"❌ Base content insertion failed: {response.status} - {error_text}")
                    return None
                    
    except Exception as e:
        logging.error(f"Error inserting base content: {str(e)}")
        return None


async def process_image_example(api_base_url: str):
    """Example of processing an image via multimodal query"""
    try:
        logging.info("\n📸 Image Modal Processor Example")
        logging.info("-" * 40)
        
        # Since we don't have actual image files, we'll simulate image processing
        # by using multimodal queries that would typically include image data
        
        query = "Analyze this image caption and relate it to the modal processing capabilities described in the documentation"
        
        multimodal_content = [
            {
                "type": "image",
                "image_caption": "A sample system architecture diagram showing RAGAnything's multimodal processing pipeline with separate processors for text, images, tables, and equations"
            }
        ]
        
        query_url = f"{api_base_url}/multimodal-query"
        payload = {
            "query": query,
            "multimodal_content": multimodal_content,
            "mode": "hybrid"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(query_url, json=payload) as response:
                if response.status == 200:
                    result = await response.json()
                    logging.info(f"[Image Query]: {query}")
                    logging.info(f"📸 Image Processing Result: {result['answer']}")
                    logging.info(f"⏱️  Processing time: {result['processing_time']:.2f} seconds\n")
                    return result
                else:
                    error_text = await response.text()
                    logging.error(f"❌ Image processing failed: {response.status} - {error_text}")
                    return None
        
    except Exception as e:
        logging.error(f"Error in image processing example: {str(e)}")
        return None


async def process_table_example(api_base_url: str):
    """Example of processing a table via multimodal query"""
    try:
        logging.info("📊 Table Modal Processor Example")
        logging.info("-" * 40)
        
        query = "Analyze this employee information table and extract key insights about the team composition"
        
        multimodal_content = [
            {
                "type": "table",
                "table_data": """Name,Age,Occupation,Experience
John,25,Engineer,3 years
Mary,30,Designer,5 years
Alex,28,Data Scientist,4 years
Sarah,32,Product Manager,7 years""",
                "table_caption": "Employee Information Table"
            }
        ]
        
        query_url = f"{api_base_url}/multimodal-query"
        payload = {
            "query": query,
            "multimodal_content": multimodal_content,
            "mode": "hybrid"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(query_url, json=payload) as response:
                if response.status == 200:
                    result = await response.json()
                    logging.info(f"[Table Query]: {query}")
                    logging.info(f"📊 Table Processing Result: {result['answer']}")
                    logging.info(f"⏱️  Processing time: {result['processing_time']:.2f} seconds\n")
                    return result
                else:
                    error_text = await response.text()
                    logging.error(f"❌ Table processing failed: {response.status} - {error_text}")
                    return None
        
    except Exception as e:
        logging.error(f"Error in table processing example: {str(e)}")
        return None


async def process_equation_example(api_base_url: str):
    """Example of processing a mathematical equation via multimodal query"""
    try:
        logging.info("🧮 Equation Modal Processor Example")
        logging.info("-" * 40)
        
        query = "Explain this mathematical equation and its significance in the context of machine learning"
        
        multimodal_content = [
            {
                "type": "equation",
                "latex": "E = mc^2",
                "equation_caption": "Einstein's Mass-Energy Equivalence Formula"
            }
        ]
        
        query_url = f"{api_base_url}/multimodal-query"
        payload = {
            "query": query,
            "multimodal_content": multimodal_content,
            "mode": "hybrid"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(query_url, json=payload) as response:
                if response.status == 200:
                    result = await response.json()
                    logging.info(f"[Equation Query]: {query}")
                    logging.info(f"🧮 Equation Processing Result: {result['answer']}")
                    logging.info(f"⏱️  Processing time: {result['processing_time']:.2f} seconds\n")
                    return result
                else:
                    error_text = await response.text()
                    logging.error(f"❌ Equation processing failed: {response.status} - {error_text}")
                    return None
        
    except Exception as e:
        logging.error(f"Error in equation processing example: {str(e)}")
        return None


async def process_complex_multimodal_example(api_base_url: str):
    """Example of processing multiple modal types in a single query"""
    try:
        logging.info("🔄 Complex Multimodal Processing Example")
        logging.info("-" * 50)
        
        query = "Compare the performance data in this table with the mathematical relationship shown in the equation, and relate both to the system architecture described in the image"
        
        multimodal_content = [
            {
                "type": "table",
                "table_data": """System,Accuracy,Speed,Memory
RAGAnything,95.2%,120ms,2.1GB
Traditional,87.3%,180ms,3.2GB
Baseline,82.1%,220ms,4.1GB""",
                "table_caption": "Performance Comparison Results"
            },
            {
                "type": "equation",
                "latex": "Performance = \\frac{Accuracy \\times Speed}{Memory\\_Usage} \\times Scalability\\_Factor",
                "equation_caption": "Performance calculation formula"
            },
            {
                "type": "image", 
                "image_caption": "System architecture diagram showing the relationship between processing components, memory usage, and throughput optimization"
            }
        ]
        
        query_url = f"{api_base_url}/multimodal-query"
        payload = {
            "query": query,
            "multimodal_content": multimodal_content,
            "mode": "hybrid"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(query_url, json=payload) as response:
                if response.status == 200:
                    result = await response.json()
                    logging.info(f"[Complex Multimodal Query]: {query}")
                    logging.info(f"🔄 Complex Processing Result: {result['answer']}")
                    logging.info(f"⏱️  Processing time: {result['processing_time']:.2f} seconds\n")
                    return result
                else:
                    error_text = await response.text()
                    logging.error(f"❌ Complex multimodal processing failed: {response.status} - {error_text}")
                    return None
        
    except Exception as e:
        logging.error(f"Error in complex multimodal processing: {str(e)}")
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


async def run_modalprocessors_example(api_base_url: str):
    """
    Modal Processors example をFastAPI経由で実行
    
    Args:
        api_base_url: FastAPI server base URL
    """
    try:
        logging.info("=" * 60)
        logging.info("Modal Processors FastAPI Example")
        logging.info("=" * 60)
        logging.info("This example demonstrates modal processor capabilities:")
        logging.info("  - Image processing and analysis")
        logging.info("  - Table data extraction and insights")
        logging.info("  - Mathematical equation interpretation")
        logging.info("  - Complex multimodal content integration")

        # Health check
        if not check_api_health(api_base_url):
            return

        # Insert base content for context
        logging.info("\n📝 Inserting base content for modal processing context...")
        base_insert = await insert_base_content(api_base_url)
        
        if not base_insert:
            logging.error("Failed to insert base content. Continuing anyway...")
        
        # Wait for content to be processed
        await asyncio.sleep(2)

        results = {}

        # Run modal processor examples
        logging.info("\n🚀 Starting modal processor demonstrations...")
        
        # Image processing
        results["image"] = await process_image_example(api_base_url)
        await asyncio.sleep(1)
        
        # Table processing
        results["table"] = await process_table_example(api_base_url)
        await asyncio.sleep(1)
        
        # Equation processing
        results["equation"] = await process_equation_example(api_base_url)
        await asyncio.sleep(1)
        
        # Complex multimodal processing
        results["complex"] = await process_complex_multimodal_example(api_base_url)

        # Summary
        logging.info("=" * 60)
        logging.info("MODAL PROCESSORS SUMMARY")
        logging.info("=" * 60)

        successful_demos = 0
        for demo_name, result in results.items():
            if result:
                logging.info(f"✅ {demo_name.upper()}: Modal processing completed successfully")
                successful_demos += 1
            else:
                logging.info(f"❌ {demo_name.upper()}: Failed or had limitations")

        logging.info(f"\n📊 Modal processors tested: {successful_demos}/{len(results)}")
        
        logging.info("\n💡 Key Features Demonstrated:")
        logging.info("  - Image modal processing via API endpoints")
        logging.info("  - Table data analysis and extraction")
        logging.info("  - Mathematical equation interpretation")
        logging.info("  - Multi-modal content integration in single queries")
        logging.info("  - Context-aware multimodal reasoning")

        logging.info("\n✅ Modal Processors FastAPI example completed!")

    except Exception as e:
        logging.error(f"Error in modal processors FastAPI example: {str(e)}")
        import traceback
        logging.error(traceback.format_exc())


def main():
    """Main function to run the modal processors FastAPI example"""
    parser = argparse.ArgumentParser(description="Modal Processors FastAPI Example")
    parser.add_argument(
        "--api-url", 
        default="http://localhost:8000", 
        help="FastAPI server URL (default: http://localhost:8000)"
    )
    
    args = parser.parse_args()
    
    # Run the example
    asyncio.run(run_modalprocessors_example(args.api_url))


if __name__ == "__main__":
    # Configure logging first
    configure_logging()
    
    print("Modal Processors FastAPI Example")
    print("=" * 45)
    print("Demonstrating multimodal content processing via FastAPI")
    print("=" * 45)
    print("Make sure to start the FastAPI server first:")
    print("  python simple_api.py")
    print("=" * 45)
    
    main()