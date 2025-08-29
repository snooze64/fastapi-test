#!/usr/bin/env python
"""
FastAPI版 Insert Content List Example

元のinsert_content_list_example.pyをFastAPI経由で実行するように書き換えたスクリプト
/content エンドポイントを使用してコンテンツリストを直接挿入し、クエリを実行する
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


def create_sample_content_list():
    """
    Create a simple content list for testing insert_content_list functionality
    
    Returns:
        List[Dict]: Sample content list with various content types
    """
    content_list = [
        # Introduction text
        {
            "type": "text",
            "text": "Welcome to the RAGAnything System Documentation. This guide covers the advanced multimodal document processing capabilities and features of our comprehensive RAG system.",
            "page_idx": 0
        },
        # Performance comparison table
        {
            "type": "table",
            "table_body": """| System | Accuracy | Processing Speed | Memory Usage |
|--------|----------|------------------|--------------|
| RAGAnything | 95.2% | 120ms | 2.1GB |
| Traditional RAG | 87.3% | 180ms | 3.2GB |
| Baseline System | 82.1% | 220ms | 4.1GB |
| Simple Retrieval | 76.5% | 95ms | 1.8GB |""",
            "table_caption": ["Table 1: Performance Comparison of Different RAG Systems"],
            "table_footnote": ["All tests conducted on the same hardware with identical test datasets"],
            "page_idx": 2
        },
        # Mathematical formula
        {
            "type": "equation",
            "latex": "Relevance(d, q) = \\sum_{i=1}^{n} w_i \\cdot sim(t_i^d, t_i^q) \\cdot \\alpha_i",
            "text": "Document relevance scoring formula where w_i are term weights, sim() is similarity function, and α_i are modality importance factors",
            "page_idx": 3
        },
        # Feature description
        {
            "type": "text",
            "text": "The system supports multiple content modalities including text, images, tables, and mathematical equations. Each modality is processed using specialized processors optimized for that content type.",
            "page_idx": 4
        },
        # Technical specifications table
        {
            "type": "table",
            "table_body": """| Feature | Specification |
|---------|---------------|
| Supported Formats | PDF, DOCX, PPTX, XLSX, Images |
| Max Document Size | 100MB |
| Concurrent Processing | Up to 8 documents |
| Query Response Time | <200ms average |
| Knowledge Graph Nodes | Up to 1M entities |""",
            "table_caption": ["Table 2: Technical Specifications"],
            "table_footnote": ["Specifications may vary based on hardware configuration"],
            "page_idx": 5
        },
        # Conclusion
        {
            "type": "text",
            "text": "RAGAnything represents a significant advancement in multimodal document processing, providing comprehensive solutions for complex knowledge extraction and retrieval tasks.",
            "page_idx": 6
        }
    ]
    
    return content_list


async def insert_content_list(api_base_url: str, content_list: list, file_path: str, doc_id: str = None):
    """
    FastAPI サーバーにコンテンツリストを挿入
    
    Args:
        api_base_url: FastAPI server base URL
        content_list: Content list to insert
        file_path: Reference file path for citation
        doc_id: Custom document ID
    """
    try:
        content_url = f"{api_base_url}/content"
        
        payload = {
            "content_list": content_list,
            "file_path": file_path,
            "doc_id": doc_id,
            "display_stats": True
        }
        
        async with aiohttp.ClientSession() as session:
            logging.info(f"📝 Inserting content list with {len(content_list)} items...")
            
            async with session.post(content_url, json=payload) as response:
                if response.status == 200:
                    result = await response.json()
                    logging.info(f"✅ Content insertion successful: {result['message']}")
                    logging.info(f"⏱️  Processing time: {result['processing_time']:.2f} seconds")
                    return result
                else:
                    error_text = await response.text()
                    logging.error(f"❌ Content insertion failed: {response.status} - {error_text}")
                    return None
                    
    except Exception as e:
        logging.error(f"Error inserting content list: {str(e)}")
        return None


async def query_content(api_base_url: str, query: str, mode: str = "hybrid"):
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
        logging.error(f"Error querying content: {str(e)}")
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


async def run_insert_content_list_example(api_base_url: str):
    """
    Insert Content List example をFastAPI経由で実行
    
    Args:
        api_base_url: FastAPI server base URL
    """
    try:
        logging.info("=" * 55)
        logging.info("Insert Content List FastAPI Example")
        logging.info("=" * 55)
        
        # Health check
        if not check_api_health(api_base_url):
            return
        
        # Create sample content list
        logging.info("\n📋 Creating sample content list...")
        content_list = create_sample_content_list()
        logging.info(f"Created content list with {len(content_list)} items")
        
        # Insert content list
        logging.info("\n📝 Inserting content list into RAGAnything via FastAPI...")
        insert_result = await insert_content_list(
            api_base_url,
            content_list,
            "raganything_documentation.pdf",
            "demo-doc-001"
        )
        
        if not insert_result:
            logging.error("Content list insertion failed. Exiting.")
            return
        
        # Wait a moment for processing to complete
        await asyncio.sleep(2)
        
        # Example queries - demonstrating different query approaches
        logging.info("\n🔍 Querying inserted content:")
        
        # 1. Pure text queries using /query endpoint
        text_queries = [
            "What is RAGAnything and what are its main features?",
            "How does RAGAnything compare to traditional RAG systems?",
            "What are the technical specifications of the system?",
        ]
        
        for query in text_queries:
            await query_content(api_base_url, query, "hybrid")
            await asyncio.sleep(1)
        
        # 2. Multimodal query with specific multimodal content
        logging.info("🔍 Running multimodal queries:")
        
        multimodal_result = await multimodal_query(
            api_base_url,
            "Compare this new performance data with the existing benchmark results in the documentation",
            multimodal_content=[
                {
                    "type": "table",
                    "table_data": """Method,Accuracy,Speed,Memory
New_Approach,97.1%,110ms,1.9GB
Enhanced_RAG,91.4%,140ms,2.5GB""",
                    "table_caption": "Latest experimental results"
                }
            ],
            mode="hybrid"
        )
        
        await asyncio.sleep(1)
        
        # 3. Another multimodal query with equation content
        equation_result = await multimodal_query(
            api_base_url,
            "How does this similarity formula relate to the relevance scoring mentioned in the documentation?",
            multimodal_content=[
                {
                    "type": "equation",
                    "latex": "sim(a, b) = \\frac{a \\cdot b}{||a|| \\times ||b||} + \\beta \\cdot context\\_weight",
                    "equation_caption": "Enhanced cosine similarity with context weighting"
                }
            ],
            mode="hybrid"
        )
        
        await asyncio.sleep(1)
        
        # 4. Insert additional content list with different document ID
        logging.info("\n📝 Inserting additional content list...")
        additional_content = [
            {
                "type": "text",
                "text": "This is additional documentation about advanced features and configuration options.",
                "page_idx": 0
            },
            {
                "type": "table",
                "table_body": """| Configuration | Default Value | Range |
|---------------|---------------|-------|
| Chunk Size | 512 tokens | 128-2048 |
| Context Window | 4096 tokens | 1024-8192 |
| Batch Size | 32 | 1-128 |""",
                "table_caption": ["Advanced Configuration Parameters"],
                "page_idx": 1
            }
        ]
        
        additional_insert = await insert_content_list(
            api_base_url,
            additional_content,
            "advanced_configuration.pdf",
            "demo-doc-002"
        )
        
        await asyncio.sleep(2)
        
        # Query combined knowledge base
        if additional_insert:
            await query_content(
                api_base_url,
                "What configuration options are available and what are their default values?",
                "hybrid"
            )
        
        logging.info("✅ Insert Content List FastAPI example completed successfully!")
        
    except Exception as e:
        logging.error(f"Error in FastAPI example: {str(e)}")
        import traceback
        logging.error(traceback.format_exc())


def main():
    """Main function to run the FastAPI example"""
    parser = argparse.ArgumentParser(description="Insert Content List FastAPI Example")
    parser.add_argument(
        "--api-url", 
        default="http://localhost:8000", 
        help="FastAPI server URL (default: http://localhost:8000)"
    )
    
    args = parser.parse_args()
    
    # Run the example
    asyncio.run(run_insert_content_list_example(args.api_url))


if __name__ == "__main__":
    # Configure logging first
    configure_logging()
    
    print("Insert Content List FastAPI Example")
    print("=" * 45)
    print("Demonstrating direct content list insertion via FastAPI")
    print("=" * 45)
    print("Make sure to start the FastAPI server first:")
    print("  python simple_api.py")
    print("=" * 45)
    
    main()