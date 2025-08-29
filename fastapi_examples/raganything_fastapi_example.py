#!/usr/bin/env python
"""
FastAPI版 RAGAnything Example

元のraganything_example.pyをFastAPI経由で実行するように書き換えたスクリプト
Simple APIサーバーと通信してドキュメント処理とクエリを実行する
"""

import os
import argparse
import asyncio
import logging
from pathlib import Path
import requests
import aiohttp
import json

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


async def upload_document(api_base_url: str, file_path: str):
    """
    FastAPI サーバーにドキュメントをアップロードして処理
    
    Args:
        api_base_url: FastAPI server base URL
        file_path: Path to the document
    """
    try:
        upload_url = f"{api_base_url}/upload"
        
        async with aiohttp.ClientSession() as session:
            with open(file_path, 'rb') as f:
                data = aiohttp.FormData()
                data.add_field('file', f, filename=Path(file_path).name)
                
                logging.info(f"Uploading document: {Path(file_path).name}")
                
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
        logging.error(f"Error uploading document: {str(e)}")
        return None


async def query_document(api_base_url: str, query: str, mode: str = "hybrid"):
    """
    FastAPI サーバーでテキストクエリを実行
    
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
                    logging.info(f"[Text Query]: {query}")
                    logging.info(f"Answer: {result['answer']}")
                    logging.info(f"⏱️  Query time: {result['processing_time']:.2f} seconds\n")
                    return result
                else:
                    error_text = await response.text()
                    logging.error(f"❌ Query failed: {response.status} - {error_text}")
                    return None
                    
    except Exception as e:
        logging.error(f"Error querying document: {str(e)}")
        return None


async def multimodal_query(api_base_url: str, query: str, multimodal_content: list, mode: str = "hybrid"):
    """
    FastAPI サーバーでマルチモーダルクエリを実行
    
    Args:
        api_base_url: FastAPI server base URL
        query: Query text
        multimodal_content: List of multimodal content
        mode: Query mode
    """
    try:
        query_url = f"{api_base_url}/multimodal-query"
        
        payload = {
            "query": query,
            "multimodal_content": multimodal_content,
            "mode": mode
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(query_url, json=payload) as response:
                if response.status == 200:
                    result = await response.json()
                    logging.info(f"[Multimodal Query]: {query}")
                    logging.info(f"Answer: {result['answer']}")
                    logging.info(f"⏱️  Query time: {result['processing_time']:.2f} seconds\n")
                    return result
                else:
                    error_text = await response.text()
                    logging.error(f"❌ Multimodal query failed: {response.status} - {error_text}")
                    return None
                    
    except Exception as e:
        logging.error(f"Error in multimodal query: {str(e)}")
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


async def run_raganything_example(
    api_base_url: str,
    file_path: str
):
    """
    RAGAnything example をFastAPI経由で実行
    
    Args:
        api_base_url: FastAPI server base URL
        file_path: Path to the document
    """
    try:
        logging.info("=" * 50)
        logging.info("RAGAnything FastAPI Example")
        logging.info("=" * 50)
        
        # Health check
        if not check_api_health(api_base_url):
            return
        
        # Document upload and processing
        logging.info("\n📄 Processing document with FastAPI server...")
        upload_result = await upload_document(api_base_url, file_path)
        
        if not upload_result:
            logging.error("Document processing failed. Exiting.")
            return
        
        # Wait a moment for processing to complete
        await asyncio.sleep(2)
        
        # Example queries - demonstrating different query approaches
        logging.info("\n🔍 Querying processed document:")
        
        # 1. Pure text queries using /query endpoint
        text_queries = [
            "What is the main content of the document?",
            "What are the key topics discussed?",
            "Summarize the document in 3 sentences"
        ]
        
        for query in text_queries:
            await query_document(api_base_url, query, "hybrid")
            await asyncio.sleep(1)  # Small delay between queries
        
        # 2. Multimodal query with performance table
        logging.info("🔍 Running multimodal queries:")
        
        multimodal_result = await multimodal_query(
            api_base_url,
            "Compare this performance data with any similar results mentioned in the document",
            multimodal_content=[
                {
                    "type": "table",
                    "table_data": """Method,Accuracy,Processing_Time
RAGAnything,95.2%,120ms
Traditional_RAG,87.3%,180ms
Baseline,82.1%,200ms""",
                    "table_caption": "Performance comparison results"
                }
            ],
            mode="hybrid"
        )
        
        await asyncio.sleep(1)
        
        # 3. Multimodal query with equation
        equation_result = await multimodal_query(
            api_base_url,
            "Explain this formula and relate it to any mathematical concepts in the document",
            multimodal_content=[
                {
                    "type": "equation",
                    "latex": "F1 = 2 \\cdot \\frac{precision \\cdot recall}{precision + recall}",
                    "equation_caption": "F1-score calculation formula"
                }
            ],
            mode="hybrid"
        )
        
        logging.info("✅ RAGAnything FastAPI example completed successfully!")
        
    except Exception as e:
        logging.error(f"Error in FastAPI example: {str(e)}")
        import traceback
        logging.error(traceback.format_exc())


def main():
    """Main function to run the FastAPI example"""
    parser = argparse.ArgumentParser(description="RAGAnything FastAPI Example")
    parser.add_argument("file_path", help="Path to the document to process")
    parser.add_argument(
        "--api-url", 
        default="http://localhost:8000", 
        help="FastAPI server URL (default: http://localhost:8000)"
    )
    
    args = parser.parse_args()
    
    # Check if file exists
    if not os.path.exists(args.file_path):
        logging.error(f"Error: File not found: {args.file_path}")
        return
    
    # Run the example
    asyncio.run(run_raganything_example(
        args.api_url,
        args.file_path
    ))


if __name__ == "__main__":
    # Configure logging first
    configure_logging()
    
    print("RAGAnything FastAPI Example")
    print("=" * 30)
    print("Processing document via FastAPI server")
    print("=" * 30)
    print("Make sure to start the FastAPI server first:")
    print("  python simple_api.py")
    print("=" * 30)
    
    main()