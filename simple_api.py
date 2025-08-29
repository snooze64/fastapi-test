#!/usr/bin/env python3
"""
Simple RAG-Anything API Server
基本的なドキュメント処理とクエリ機能のみ提供
env.exampleの全環境変数に対応
"""

import os
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any, Union
import logging

import uvicorn
from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from raganything import RAGAnything, RAGAnythingConfig


# 環境変数のデフォルト値を設定（env.example準拠）
def get_env_value(key: str, default: str, var_type=str):
    """環境変数を取得し、型変換する"""
    value = os.getenv(key, default)
    if var_type == bool:
        return value.lower() in ('true', '1', 'yes', 'on')
    elif var_type == int:
        return int(value)
    elif var_type == float:
        return float(value)
    elif var_type == list:
        return [item.strip() for item in value.split(',') if item.strip()]
    return var_type(value)


# サーバー設定
HOST = get_env_value("HOST", "0.0.0.0")
PORT = get_env_value("PORT", "8000", int)
WEBUI_TITLE = get_env_value("WEBUI_TITLE", "Simple RAG-Anything API")
WEBUI_DESCRIPTION = get_env_value("WEBUI_DESCRIPTION", "簡素化されたRAG-Anything API")
WORKERS = get_env_value("WORKERS", "1", int)
CORS_ORIGINS = get_env_value("CORS_ORIGINS", "*", list)

# 認証設定
AUTH_ACCOUNTS = get_env_value("AUTH_ACCOUNTS", "", list)
TOKEN_SECRET = get_env_value("TOKEN_SECRET", "")
TOKEN_EXPIRE_HOURS = get_env_value("TOKEN_EXPIRE_HOURS", "48", int)

# ディレクトリ設定
INPUT_DIR = get_env_value("INPUT_DIR", "./uploads")
OUTPUT_DIR = get_env_value("OUTPUT_DIR", "./output")
WORKING_DIR = get_env_value("WORKING_DIR", "./rag_storage")
LOG_DIR = get_env_value("LOG_DIR", "./logs")

# RAGAnything設定
PARSE_METHOD = get_env_value("PARSE_METHOD", "auto")
PARSER = get_env_value("PARSER", "mineru")
DISPLAY_CONTENT_STATS = get_env_value("DISPLAY_CONTENT_STATS", "true", bool)
ENABLE_IMAGE_PROCESSING = get_env_value("ENABLE_IMAGE_PROCESSING", "true", bool)
ENABLE_TABLE_PROCESSING = get_env_value("ENABLE_TABLE_PROCESSING", "true", bool)
ENABLE_EQUATION_PROCESSING = get_env_value("ENABLE_EQUATION_PROCESSING", "true", bool)
MAX_CONCURRENT_FILES = get_env_value("MAX_CONCURRENT_FILES", "1", int)

# コンテキスト設定
CONTEXT_WINDOW = get_env_value("CONTEXT_WINDOW", "1", int)
CONTEXT_MODE = get_env_value("CONTEXT_MODE", "page")
MAX_CONTEXT_TOKENS = get_env_value("MAX_CONTEXT_TOKENS", "2000", int)

# LLM設定
LLM_BINDING = get_env_value("LLM_BINDING", "openai")
LLM_MODEL = get_env_value("LLM_MODEL", "gpt-4o-mini")
LLM_BINDING_HOST = get_env_value("LLM_BINDING_HOST", "https://api.openai.com/v1")
LLM_BINDING_API_KEY = get_env_value("LLM_BINDING_API_KEY", os.getenv("OPENAI_API_KEY", ""))
TEMPERATURE = get_env_value("TEMPERATURE", "0", float)
MAX_TOKENS = get_env_value("MAX_TOKENS", "32768", int)
TIMEOUT = get_env_value("TIMEOUT", "240", int)

# 埋め込み設定
EMBEDDING_BINDING = get_env_value("EMBEDDING_BINDING", "openai")
EMBEDDING_MODEL = get_env_value("EMBEDDING_MODEL", "text-embedding-3-large")
EMBEDDING_DIM = get_env_value("EMBEDDING_DIM", "3072", int)
EMBEDDING_BINDING_HOST = get_env_value("EMBEDDING_BINDING_HOST", "https://api.openai.com/v1")
EMBEDDING_BINDING_API_KEY = get_env_value("EMBEDDING_BINDING_API_KEY", LLM_BINDING_API_KEY)

# ログ設定
LOG_LEVEL = get_env_value("LOG_LEVEL", "INFO")
VERBOSE = get_env_value("VERBOSE", "false", bool)

# ディレクトリ作成
Path(INPUT_DIR).mkdir(exist_ok=True, parents=True)
Path(OUTPUT_DIR).mkdir(exist_ok=True, parents=True)
Path(WORKING_DIR).mkdir(exist_ok=True, parents=True)
Path(LOG_DIR).mkdir(exist_ok=True, parents=True)

# ログ設定
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL.upper()),
    format='%(asctime)s - %(levelname)s - %(message)s'
)


# Response models
class HealthResponse(BaseModel):
    status: str
    timestamp: str
    message: str


class ProcessResponse(BaseModel):
    success: bool
    message: str
    document_id: Optional[str] = None
    processing_time: Optional[float] = None


class QueryRequest(BaseModel):
    query: str
    mode: str = "hybrid"


class QueryResponse(BaseModel):
    success: bool
    message: str
    answer: Optional[str] = None
    processing_time: Optional[float] = None


class ContentItem(BaseModel):
    type: str
    text: Optional[str] = None
    img_path: Optional[str] = None
    img_caption: Optional[List[str]] = None
    img_footnote: Optional[List[str]] = None
    table_body: Optional[str] = None
    table_caption: Optional[List[str]] = None
    table_footnote: Optional[List[str]] = None
    latex: Optional[str] = None
    page_idx: Optional[int] = 0


class ContentRequest(BaseModel):
    content_list: List[ContentItem]
    file_path: str
    doc_id: Optional[str] = None
    split_by_character: Optional[str] = None
    split_by_character_only: Optional[bool] = False
    display_stats: Optional[bool] = True


class MultimodalContentItem(BaseModel):
    type: str
    table_data: Optional[str] = None
    table_caption: Optional[str] = None
    latex: Optional[str] = None
    equation_caption: Optional[str] = None
    image_data: Optional[str] = None
    image_caption: Optional[str] = None


class MultimodalQueryRequest(BaseModel):
    query: str
    multimodal_content: List[MultimodalContentItem]
    mode: str = "hybrid"


class BatchProcessRequest(BaseModel):
    parse_method: Optional[str] = "auto"
    max_workers: Optional[int] = 2
    display_stats: Optional[bool] = True


# FastAPI app
app = FastAPI(
    title=WEBUI_TITLE,
    version="1.0.0",
    description=WEBUI_DESCRIPTION
)

# CORS設定（環境変数対応）
cors_origins = CORS_ORIGINS if isinstance(CORS_ORIGINS, list) else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global variables
rag_system: Optional[RAGAnything] = None


async def initialize_rag():
    """RAGシステムを初期化（環境変数対応）"""
    global rag_system
    
    if rag_system is None:
        # APIキー設定
        api_key = LLM_BINDING_API_KEY
        if not api_key:
            raise ValueError("LLM_BINDING_API_KEY or OPENAI_API_KEY environment variable is required")
        
        # LLM設定に応じた関数設定
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
            
            def vision_model_func(prompt, system_prompt=None, history_messages=[], 
                                image_data=None, messages=None, **kwargs):
                return openai_complete_if_cache(
                    "gpt-4o",  # ビジョンモデルは固定
                    prompt if not messages else messages,
                    system_prompt=system_prompt,
                    history_messages=history_messages,
                    api_key=api_key,
                    base_url=LLM_BINDING_HOST,
                    **kwargs,
                )
            
            # 埋め込み関数
            if EMBEDDING_BINDING == "openai":
                def embedding_func(texts):
                    return openai_embed(
                        texts,
                        model=EMBEDDING_MODEL,
                        api_key=EMBEDDING_BINDING_API_KEY,
                        base_url=EMBEDDING_BINDING_HOST
                    )
            else:
                # Ollamaやその他の埋め込みサービス用の実装は必要時に追加
                def embedding_func(texts):
                    logging.warning(f"Embedding binding {EMBEDDING_BINDING} not implemented, using OpenAI")
                    return openai_embed(
                        texts,
                        model=EMBEDDING_MODEL,
                        api_key=EMBEDDING_BINDING_API_KEY
                    )
        
        else:
            raise ValueError(f"LLM binding {LLM_BINDING} not supported in simple API")
        
        # 環境変数に基づく設定
        config = RAGAnythingConfig(
            working_dir=WORKING_DIR,
            parser_output_dir=OUTPUT_DIR,
            parser=PARSER,
            parse_method=PARSE_METHOD
        )
        
        # RAGAnythingインスタンス作成（dataclassとして直接関数を渡す）
        rag_system = RAGAnything(
            config=config,
            llm_model_func=llm_model_func,
            vision_model_func=vision_model_func,
            embedding_func=embedding_func
        )


# Startup event
@app.on_event("startup")
async def startup_event():
    await initialize_rag()
    print("🚀 Simple RAG-Anything API started")


# Health check
@app.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        message="Simple RAG-Anything API is running"
    )


# Document upload and processing
@app.post("/upload", response_model=ProcessResponse)
async def upload_document(file: UploadFile = File(...)):
    """ドキュメントをアップロードして処理"""
    if not rag_system:
        await initialize_rag()
    
    try:
        # ファイル保存（環境変数ディレクトリ使用）
        file_path = Path(INPUT_DIR) / file.filename
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # ドキュメント処理（環境変数設定使用）
        import time
        start_time = time.time()
        
        result = await rag_system.process_document_complete(
            file_path=str(file_path),
            output_dir=OUTPUT_DIR,
            parser=PARSER,
            parse_method=PARSE_METHOD,
            enable_image_processing=ENABLE_IMAGE_PROCESSING,
            enable_table_processing=ENABLE_TABLE_PROCESSING,
            enable_equation_processing=ENABLE_EQUATION_PROCESSING,
            display_stats=DISPLAY_CONTENT_STATS
        )
        
        processing_time = time.time() - start_time
        
        # ファイル削除
        file_path.unlink()
        
        return ProcessResponse(
            success=True,
            message=f"Document '{file.filename}' processed successfully",
            document_id=file.filename,
            processing_time=processing_time
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Query
@app.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    """ドキュメントに対してクエリを実行"""
    if not rag_system:
        await initialize_rag()
    
    try:
        import time
        start_time = time.time()
        
        answer = await rag_system.aquery(request.query, mode=request.mode)
        processing_time = time.time() - start_time
        
        return QueryResponse(
            success=True,
            message="Query processed successfully",
            answer=answer,
            processing_time=processing_time
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Content list insertion
@app.post("/content", response_model=ProcessResponse)
async def insert_content_list(request: ContentRequest):
    """コンテンツリストを直接挿入"""
    if not rag_system:
        await initialize_rag()
    
    try:
        import time
        start_time = time.time()
        
        # Convert Pydantic models to dict format for RAGAnything
        content_list = []
        for item in request.content_list:
            content_dict = {"type": item.type, "page_idx": item.page_idx or 0}
            
            if item.type == "text" and item.text:
                content_dict["text"] = item.text
            elif item.type == "image":
                if item.img_path:
                    content_dict["img_path"] = item.img_path
                if item.img_caption:
                    content_dict["img_caption"] = item.img_caption
                if item.img_footnote:
                    content_dict["img_footnote"] = item.img_footnote
            elif item.type == "table":
                if item.table_body:
                    content_dict["table_body"] = item.table_body
                if item.table_caption:
                    content_dict["table_caption"] = item.table_caption
                if item.table_footnote:
                    content_dict["table_footnote"] = item.table_footnote
            elif item.type == "equation":
                if item.latex:
                    content_dict["latex"] = item.latex
                if item.text:
                    content_dict["text"] = item.text
            
            content_list.append(content_dict)
        
        # Insert content list
        await rag_system.insert_content_list(
            content_list=content_list,
            file_path=request.file_path,
            doc_id=request.doc_id,
            split_by_character=request.split_by_character,
            split_by_character_only=request.split_by_character_only,
            display_stats=request.display_stats
        )
        
        processing_time = time.time() - start_time
        
        return ProcessResponse(
            success=True,
            message=f"Content list with {len(content_list)} items inserted successfully",
            document_id=request.doc_id,
            processing_time=processing_time
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Multimodal query
@app.post("/multimodal-query", response_model=QueryResponse)
async def multimodal_query(request: MultimodalQueryRequest):
    """マルチモーダルコンテンツを含むクエリを実行"""
    if not rag_system:
        await initialize_rag()
    
    try:
        import time
        start_time = time.time()
        
        # Convert Pydantic models to dict format for RAGAnything
        multimodal_content = []
        for item in request.multimodal_content:
            content_dict = {"type": item.type}
            
            if item.type == "table":
                if item.table_data:
                    content_dict["table_data"] = item.table_data
                if item.table_caption:
                    content_dict["table_caption"] = item.table_caption
            elif item.type == "equation":
                if item.latex:
                    content_dict["latex"] = item.latex
                if item.equation_caption:
                    content_dict["equation_caption"] = item.equation_caption
            elif item.type == "image":
                if item.image_data:
                    content_dict["image_data"] = item.image_data
                if item.image_caption:
                    content_dict["image_caption"] = item.image_caption
            
            multimodal_content.append(content_dict)
        
        # Execute multimodal query
        answer = await rag_system.aquery_with_multimodal(
            request.query, 
            multimodal_content=multimodal_content,
            mode=request.mode
        )
        
        processing_time = time.time() - start_time
        
        return QueryResponse(
            success=True,
            message="Multimodal query processed successfully",
            answer=answer,
            processing_time=processing_time
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Batch processing
@app.post("/batch", response_model=ProcessResponse)
async def batch_process(files: List[UploadFile] = File(...), request_data: str = Form(...)):
    """複数ファイルのバッチ処理"""
    if not rag_system:
        await initialize_rag()
    
    try:
        import json
        import time
        from pathlib import Path
        
        # Parse request data
        try:
            request_dict = json.loads(request_data)
            batch_request = BatchProcessRequest(**request_dict)
        except:
            batch_request = BatchProcessRequest()
        
        start_time = time.time()
        
        # Save uploaded files
        file_paths = []
        for file in files:
            file_path = Path(INPUT_DIR) / file.filename
            with open(file_path, "wb") as buffer:
                content = await file.read()
                buffer.write(content)
            file_paths.append(str(file_path))
        
        # Process files sequentially (simplified batch processing)
        successful_files = []
        failed_files = []
        errors = {}
        
        for file_path in file_paths:
            try:
                await rag_system.process_document_complete(
                    file_path=file_path,
                    output_dir=OUTPUT_DIR,
                    parser=PARSER,
                    parse_method=batch_request.parse_method,
                    enable_image_processing=ENABLE_IMAGE_PROCESSING,
                    enable_table_processing=ENABLE_TABLE_PROCESSING,
                    enable_equation_processing=ENABLE_EQUATION_PROCESSING,
                    display_stats=batch_request.display_stats
                )
                successful_files.append(file_path)
                
                # Clean up uploaded file
                Path(file_path).unlink(missing_ok=True)
                
            except Exception as file_error:
                failed_files.append(file_path)
                errors[file_path] = str(file_error)
                
                # Clean up uploaded file even on error
                Path(file_path).unlink(missing_ok=True)
        
        processing_time = time.time() - start_time
        
        success_rate = (len(successful_files) / len(file_paths)) * 100 if file_paths else 0
        
        message = f"Batch processing completed: {len(successful_files)}/{len(file_paths)} files successful ({success_rate:.1f}%)"
        if failed_files:
            message += f". Failed files: {[Path(f).name for f in failed_files]}"
        
        return ProcessResponse(
            success=len(successful_files) > 0,
            message=message,
            document_id=f"batch-{len(file_paths)}-files",
            processing_time=processing_time
        )
        
    except Exception as e:
        # Clean up any remaining uploaded files on error
        for file in files:
            file_path = Path(INPUT_DIR) / file.filename
            file_path.unlink(missing_ok=True)
        raise HTTPException(status_code=500, detail=str(e))


def main():
    """サーバー起動（環境変数対応）"""
    logging.info(f"Starting {WEBUI_TITLE} on {HOST}:{PORT}")
    logging.info(f"Working directory: {WORKING_DIR}")
    logging.info(f"LLM Model: {LLM_MODEL} ({LLM_BINDING})")
    logging.info(f"Embedding Model: {EMBEDDING_MODEL} ({EMBEDDING_BINDING})")
    logging.info("Available endpoints:")
    logging.info("  GET  /health - Health check")
    logging.info("  POST /upload - Single document upload and processing")
    logging.info("  POST /query - Text query against documents")
    logging.info("  POST /content - Direct content list insertion")
    logging.info("  POST /multimodal-query - Multimodal query with content")
    logging.info("  POST /batch - Batch processing of multiple files")
    
    uvicorn.run(
        "simple_api:app",
        host=HOST,
        port=PORT,
        workers=WORKERS,
        reload=False,
        log_level=LOG_LEVEL.lower()
    )


if __name__ == "__main__":
    main()