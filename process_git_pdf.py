#!/usr/bin/env python3
"""
Git PDF Processing Script for Docker Container
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, '/app')

from raganything import RAGAnything, RAGAnythingConfig

def initialize_rag_system():
    """Initialize RAGAnything with proper LLM and embedding functions"""
    
    # Environment variables (same as simple_api.py)
    LLM_BINDING = os.getenv("LLM_BINDING", "openai")
    LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")
    EMBEDDING_BINDING = os.getenv("EMBEDDING_BINDING", "openai")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-large")
    LLM_BINDING_HOST = os.getenv("LLM_BINDING_HOST", "https://api.openai.com/v1")
    EMBEDDING_BINDING_HOST = os.getenv("EMBEDDING_BINDING_HOST", "https://api.openai.com/v1")
    api_key = os.getenv("OPENAI_API_KEY")
    EMBEDDING_BINDING_API_KEY = os.getenv("EMBEDDING_BINDING_API_KEY") or api_key
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0"))
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "32768"))
    TIMEOUT = int(os.getenv("TIMEOUT", "240"))
    WORKING_DIR = os.getenv("WORKING_DIR", "./rag_storage")
    OUTPUT_DIR = os.getenv("OUTPUT_DIR", "./output")
    PARSER = os.getenv("PARSER", "mineru")
    PARSE_METHOD = os.getenv("PARSE_METHOD", "auto")
    
    if LLM_BINDING == "openai":
        from lightrag.llm.openai import openai_complete_if_cache, openai_embed
        
        def llm_model_func(prompt, system_prompt=None, history_messages=[], **kwargs):
            return openai_complete_if_cache(
                LLM_MODEL,
                prompt,
                system_prompt=system_prompt,
                history_messages=history_messages,
                api_key=api_key,
                base_url=LLM_BINDING_HOST,
                temperature=TEMPERATURE,
                max_tokens=MAX_TOKENS,
                timeout=TIMEOUT,
                **kwargs,
            )
        
        def vision_model_func(prompt, images, system_prompt=None, history_messages=[], **kwargs):
            return openai_complete_if_cache(
                LLM_MODEL,
                prompt,
                system_prompt=system_prompt,
                history_messages=history_messages,
                images=images,
                api_key=api_key,
                base_url=LLM_BINDING_HOST,
                temperature=TEMPERATURE,
                max_tokens=MAX_TOKENS,
                timeout=TIMEOUT,
                **kwargs,
            )
        
        # 埋め込み関数
        EMBEDDING_DIM = int(os.getenv("EMBEDDING_DIM", "3072"))  # Default for text-embedding-3-large
        
        if EMBEDDING_BINDING == "openai":
            def embedding_func(texts):
                return openai_embed(
                    texts,
                    model=EMBEDDING_MODEL,
                    api_key=EMBEDDING_BINDING_API_KEY,
                    base_url=EMBEDDING_BINDING_HOST
                )
            # Add embedding_dim attribute to the function
            embedding_func.embedding_dim = EMBEDDING_DIM
        else:
            def embedding_func(texts):
                return openai_embed(
                    texts,
                    model=EMBEDDING_MODEL,
                    api_key=EMBEDDING_BINDING_API_KEY
                )
            # Add embedding_dim attribute to the function
            embedding_func.embedding_dim = EMBEDDING_DIM
    else:
        raise ValueError(f"LLM binding {LLM_BINDING} not supported")
    
    # Create config
    config = RAGAnythingConfig(
        working_dir=WORKING_DIR,
        parser_output_dir=OUTPUT_DIR,
        parser=PARSER,
        parse_method=PARSE_METHOD
    )
    
    # Initialize RAGAnything with functions
    rag_system = RAGAnything(
        config=config,
        llm_model_func=llm_model_func,
        vision_model_func=vision_model_func,
        embedding_func=embedding_func
    )
    
    return rag_system

async def main():
    """Process Git PDF and add to knowledge base"""
    
    print("🚀 Starting Git PDF processing...")
    print(f"📂 Working directory: {os.getcwd()}")
    
    # Check if PDF exists
    pdf_path = "/tmp/git_pdf.pdf"
    if not os.path.exists(pdf_path):
        print(f"❌ PDF file not found: {pdf_path}")
        return False
    
    file_size = os.path.getsize(pdf_path)
    print(f"📄 PDF found: {file_size:,} bytes")
    
    try:
        # Initialize RAGAnything with proper functions
        print("🔄 Initializing RAGAnything with LLM and embedding functions...")
        rag = initialize_rag_system()
        print("✅ RAGAnything initialized with all functions")
        
        # Process the document
        print("🔄 Processing PDF document...")
        result = await rag.process_document_complete(pdf_path)
        
        print("✅ PDF processing completed successfully!")
        print(f"📊 Processing result: {result}")
        
        # Try a simple query to test the knowledge base
        print("\n🔍 Testing knowledge base with a query...")
        query_result = await rag.aquery("Gitとは何ですか？")
        print(f"💬 Query result: {query_result}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during processing: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    if success:
        print("\n🎉 Git PDF successfully added to knowledge base!")
        sys.exit(0)
    else:
        print("\n💥 Failed to process Git PDF")
        sys.exit(1)