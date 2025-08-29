#!/usr/bin/env python
"""
FastAPI版 Enhanced Markdown Example

元のenhanced_markdown_example.pyをFastAPI経由で実行するように書き換えたスクリプト
Markdownコンテンツをアップロードして処理し、マルチモーダルクエリを実行する
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


def create_sample_markdown_content():
    """Create comprehensive sample markdown content for testing"""
    
    # Technical documentation sample
    technical_content = """# Enhanced Markdown Processing with RAGAnything

## Table of Contents
- [Overview](#overview)
- [Architecture](#architecture)  
- [Implementation](#implementation)
- [Performance](#performance)

## Overview
This document demonstrates enhanced markdown processing capabilities using RAGAnything's multimodal document processing pipeline.

## Architecture

### Core Components
1. **Document Parser**: Processes markdown syntax and structure
2. **Content Extractor**: Extracts text, tables, and other elements
3. **Knowledge Graph**: Integrates content into searchable graph
4. **Query Engine**: Enables natural language queries

### Processing Pipeline
The system follows this processing flow:
1. Markdown parsing and structure analysis
2. Content extraction and categorization
3. Multimodal content processing (tables, code, etc.)
4. Knowledge graph integration
5. Index creation for fast retrieval

## Implementation

### FastAPI Integration
```python
# Upload markdown document to FastAPI server
import aiohttp

async def upload_markdown(file_path):
    async with aiohttp.ClientSession() as session:
        with open(file_path, 'rb') as f:
            data = aiohttp.FormData()
            data.add_field('file', f, filename='document.md')
            
            async with session.post('http://localhost:8000/upload', data=data) as response:
                result = await response.json()
                return result
```

### Configuration Options
The system supports various processing options:
- **Parse Method**: auto, ocr, or txt extraction
- **Image Processing**: Extract and analyze embedded images
- **Table Processing**: Structure table data for queries
- **Code Block Processing**: Syntax highlighting and analysis

## Performance

### Benchmark Results
| Document Type | Processing Time | Memory Usage | Accuracy |
|---------------|----------------|-------------|----------|
| Simple MD | 0.5-2s | 50MB | 95% |
| Technical MD | 2-5s | 100MB | 92% |
| Complex MD | 5-15s | 200MB | 88% |

### Processing Capabilities
- **Text Extraction**: High-accuracy text parsing
- **Table Processing**: Structured data extraction
- **Code Block Analysis**: Language detection and syntax parsing
- **Link Processing**: Reference and citation handling
- **Image Analysis**: Embedded image processing (if supported)

## Advanced Features

### Multimodal Query Support
The processed markdown supports advanced query types:

#### Table Queries
Query tables directly from markdown:
```markdown
| Feature | Status | Priority |
|---------|--------|----------|
| FastAPI Integration | ✅ Complete | High |
| Batch Processing | 🔄 In Progress | Medium |
| Advanced Analytics | ❌ Planned | Low |
```

#### Code Analysis Queries
Analyze code blocks within documents:
```python
def process_markdown(content):
    '''Process markdown content with RAGAnything'''
    # Parse markdown structure
    parsed = markdown_parser.parse(content)
    
    # Extract multimodal elements
    elements = extract_elements(parsed)
    
    # Process with RAG system
    result = rag_system.process(elements)
    
    return result
```

### Custom Processing Options
- **Syntax Highlighting**: Automatic language detection
- **Table Extraction**: CSV-style data processing
- **Metadata Extraction**: Title, authors, dates
- **Cross-References**: Link and citation processing

## Integration Examples

### Basic Processing
Process a markdown file and query its content:

```python
# 1. Upload and process
result = await upload_markdown('technical_doc.md')

# 2. Query the processed content  
query_result = await query_document('What are the core components?')
```

### Advanced Multimodal Queries
Combine markdown content with additional data:

```python
# Query with additional context
multimodal_result = await multimodal_query(
    'Compare the benchmark results with this new data',
    multimodal_content=[{
        'type': 'table',
        'table_data': 'New,Results,Here',
        'table_caption': 'Latest benchmark data'
    }]
)
```

## Conclusion
RAGAnything's enhanced markdown processing provides comprehensive document analysis capabilities with FastAPI integration for scalable document processing workflows.

### Key Benefits
- ✅ **Fast Processing**: Optimized parsing and extraction
- ✅ **Multimodal Support**: Tables, code, images, text
- ✅ **API Integration**: RESTful interface for easy integration
- ✅ **Flexible Queries**: Natural language and structured queries
- ✅ **Scalable Architecture**: Handles documents of varying complexity

### Use Cases
- **Technical Documentation**: API docs, user guides, specifications
- **Academic Papers**: Research documents with tables and formulas
- **Content Management**: Wiki-style knowledge bases
- **Report Processing**: Business reports with mixed content types

---

*Generated for RAGAnything FastAPI Integration Example*
*Document Version: 1.0 | Last Updated: 2024*
"""

    # Academic paper sample with complex structure
    academic_content = """# Research Paper: Advanced Multimodal Document Processing

**Authors:** Dr. Alice Johnson¹, Prof. Bob Smith², Dr. Carol Williams¹  
**Affiliations:**  
¹ Advanced Computing Research Lab, Tech University  
² Institute for Document Sciences, Research University

## Abstract

This paper presents a comprehensive analysis of multimodal document processing techniques using enhanced RAGAnything framework. Our research demonstrates significant improvements in processing accuracy and query performance through integrated FastAPI architecture and advanced content extraction methods.

**Keywords:** document processing, multimodal analysis, RAGAnything, FastAPI, knowledge graphs

## 1. Introduction

The proliferation of complex document formats has created new challenges for automated document processing systems. Traditional approaches often fail to capture the rich semantic relationships present in multimodal content including text, tables, code blocks, and embedded media.

### 1.1 Research Objectives

Our research addresses the following key objectives:

1. **Performance Optimization**: Improve processing speed for large markdown documents
2. **Accuracy Enhancement**: Increase extraction accuracy for structured content
3. **API Integration**: Develop scalable REST API interface
4. **Query Capabilities**: Enable sophisticated multimodal queries

### 1.2 Contributions

This work makes the following novel contributions:

- Integration of enhanced markdown processing with RAGAnything framework
- FastAPI-based architecture for scalable document processing
- Advanced multimodal query capabilities for markdown content
- Comprehensive performance benchmarking across document types

## 2. Methodology

### 2.1 System Architecture

Our enhanced markdown processing system consists of four main components:

```python
class MarkdownProcessor:
    def __init__(self):
        self.parser = AdvancedMarkdownParser()
        self.extractor = MultimodalExtractor()
        self.rag_system = RAGAnything()
        self.api_server = FastAPIServer()
    
    async def process_document(self, markdown_content):
        # Parse markdown structure
        parsed = await self.parser.parse(markdown_content)
        
        # Extract multimodal elements
        elements = await self.extractor.extract(parsed)
        
        # Process with RAG system
        result = await self.rag_system.process(elements)
        
        return result
```

### 2.2 Experimental Setup

We evaluated our system using three categories of markdown documents:

| Category | Document Count | Avg Size (KB) | Complexity Score |
|----------|----------------|---------------|------------------|
| Simple | 100 | 15 | 2.3 |
| Technical | 75 | 85 | 6.8 |
| Academic | 50 | 150 | 9.1 |

### 2.3 Performance Metrics

Our evaluation focuses on four key metrics:

1. **Processing Speed**: Time to complete full document processing
2. **Extraction Accuracy**: Percentage of correctly extracted elements
3. **Query Performance**: Response time for multimodal queries
4. **Memory Efficiency**: Peak memory usage during processing

## 3. Results

### 3.1 Processing Performance

The enhanced system demonstrates significant performance improvements:

```python
# Performance comparison results
results = {
    'traditional_approach': {
        'speed': '45.2s ± 12.1s',
        'accuracy': '78.3%',
        'memory': '450MB'
    },
    'enhanced_raganything': {
        'speed': '12.8s ± 3.4s', 
        'accuracy': '94.7%',
        'memory': '230MB'
    }
}
```

### 3.2 Multimodal Query Analysis

Our multimodal query system achieves remarkable results across different content types:

#### 3.2.1 Table Processing
- **Extraction Accuracy**: 96.8% for structured tables
- **Query Response Time**: 0.3s average
- **Supported Formats**: Markdown tables, CSV-style data

#### 3.2.2 Code Block Analysis  
- **Language Detection**: 98.2% accuracy across 20+ languages
- **Syntax Analysis**: Full AST parsing for supported languages
- **Documentation Links**: Automatic API reference linking

### 3.3 API Performance

The FastAPI integration provides excellent scalability:

| Concurrent Requests | Avg Response Time | Throughput (req/s) |
|-------------------|------------------|-------------------|
| 1 | 1.2s | 0.83 |
| 10 | 2.8s | 3.57 |
| 50 | 6.4s | 7.81 |
| 100 | 12.1s | 8.26 |

## 4. Discussion

### 4.1 Technical Insights

The integration of enhanced markdown processing with RAGAnything provides several key advantages:

**Processing Pipeline Optimization**:
- Parallel processing of multimodal elements
- Intelligent content type detection
- Optimized memory usage patterns

**Knowledge Graph Integration**:
- Semantic relationship extraction
- Cross-document reference resolution
- Enhanced query capabilities

### 4.2 Practical Applications

Our enhanced system excels in several practical scenarios:

1. **Technical Documentation Processing**:
   - API documentation with code examples
   - User guides with embedded media
   - Specification documents with tables

2. **Academic Paper Analysis**:
   - Research papers with complex formatting
   - Mathematical content processing
   - Citation and reference analysis

3. **Business Report Processing**:
   - Financial reports with data tables
   - Market analysis with charts
   - Strategic documents with mixed content

## 5. Future Work

### 5.1 Enhanced Capabilities

Future development will focus on:

- **Real-time Collaborative Processing**: Multi-user document editing
- **Advanced Media Support**: Video and audio content analysis
- **Cross-Language Processing**: Multi-language document support
- **Automated Content Generation**: AI-assisted document creation

### 5.2 Integration Improvements

- **Cloud-native Architecture**: Kubernetes deployment support
- **Microservices Design**: Modular component architecture
- **Advanced Caching**: Distributed caching for improved performance
- **Monitoring Integration**: Comprehensive observability features

## 6. Conclusion

This research demonstrates the significant potential of integrating enhanced markdown processing capabilities with the RAGAnything framework. The FastAPI-based architecture provides scalable, high-performance document processing suitable for production environments.

### Key Findings

1. **Performance**: 3.5x faster processing compared to traditional approaches
2. **Accuracy**: 94.7% extraction accuracy across multimodal content
3. **Scalability**: Linear scaling up to 100 concurrent requests  
4. **Versatility**: Support for diverse document types and query patterns

### Impact

Our enhanced system enables new possibilities for automated document analysis, intelligent content extraction, and sophisticated multimodal queries, making it valuable for academic, technical, and business applications.

## References

1. Johnson, A., et al. (2024). "Multimodal Document Processing in Modern Systems." *Journal of Information Processing*, 28(3), 145-167.

2. Smith, B. (2024). "FastAPI Architecture Patterns for Document Services." *Web API Design Quarterly*, 15(2), 78-92.

3. Williams, C., et al. (2024). "RAGAnything Framework: Advanced Document Understanding." *AI Research Review*, 41(1), 234-251.

4. Brown, D. (2023). "Performance Optimization in Document Processing Systems." *Computing Performance Analysis*, 19(4), 88-105.

---

**Manuscript Information**
- Received: March 15, 2024
- Revised: March 28, 2024  
- Accepted: April 5, 2024
- Published: April 12, 2024
"""

    return {
        "technical": technical_content,
        "academic": academic_content
    }


async def upload_markdown_document(api_base_url: str, markdown_content: str, filename: str):
    """
    FastAPI サーバーにMarkdownドキュメントをアップロード
    
    Args:
        api_base_url: FastAPI server base URL
        markdown_content: Markdown content to upload
        filename: Name for the markdown file
    """
    try:
        upload_url = f"{api_base_url}/upload"
        
        # Create temporary file with markdown content
        temp_dir = Path(tempfile.mkdtemp())
        temp_file = temp_dir / filename
        
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        async with aiohttp.ClientSession() as session:
            with open(temp_file, 'rb') as f:
                data = aiohttp.FormData()
                data.add_field('file', f, filename=filename)
                
                logging.info(f"📝 Uploading markdown document: {filename}")
                
                async with session.post(upload_url, data=data) as response:
                    if response.status == 200:
                        result = await response.json()
                        logging.info(f"✅ Upload successful: {result['message']}")
                        logging.info(f"⏱️  Processing time: {result['processing_time']:.2f} seconds")
                        
                        # Clean up temp file
                        temp_file.unlink()
                        temp_dir.rmdir()
                        
                        return result
                    else:
                        error_text = await response.text()
                        logging.error(f"❌ Upload failed: {response.status} - {error_text}")
                        return None
        
    except Exception as e:
        logging.error(f"Error uploading markdown document: {str(e)}")
        return None


async def query_markdown_content(api_base_url: str, query: str, mode: str = "hybrid"):
    """
    FastAPI サーバーでMarkdownコンテンツにクエリ実行
    
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
                    logging.info(f"[Markdown Query]: {query}")
                    logging.info(f"Answer: {result['answer']}")
                    logging.info(f"⏱️  Query time: {result['processing_time']:.2f} seconds\n")
                    return result
                else:
                    error_text = await response.text()
                    logging.error(f"❌ Query failed: {response.status} - {error_text}")
                    return None
                    
    except Exception as e:
        logging.error(f"Error querying markdown content: {str(e)}")
        return None


async def markdown_table_analysis(api_base_url: str):
    """Demonstrate table analysis from markdown content"""
    try:
        logging.info("📊 Analyzing tables from markdown content...")
        
        # Query about performance table from the academic paper
        table_query = "What are the performance comparison results between traditional approach and enhanced RAGAnything?"
        
        result = await query_markdown_content(api_base_url, table_query)
        return result
        
    except Exception as e:
        logging.error(f"Error in markdown table analysis: {str(e)}")
        return None


async def markdown_code_analysis(api_base_url: str):
    """Demonstrate code block analysis from markdown content"""
    try:
        logging.info("💻 Analyzing code blocks from markdown content...")
        
        # Query about code examples in the documents
        code_query = "Explain the MarkdownProcessor class implementation shown in the code examples. What are its main components and methods?"
        
        result = await query_markdown_content(api_base_url, code_query)
        return result
        
    except Exception as e:
        logging.error(f"Error in markdown code analysis: {str(e)}")
        return None


async def markdown_structure_analysis(api_base_url: str):
    """Demonstrate document structure analysis"""
    try:
        logging.info("🏗️  Analyzing document structure...")
        
        # Query about document organization
        structure_query = "What are the main sections and topics covered in the research paper? Provide a summary of the paper's structure."
        
        result = await query_markdown_content(api_base_url, structure_query)
        return result
        
    except Exception as e:
        logging.error(f"Error in markdown structure analysis: {str(e)}")
        return None


async def advanced_markdown_queries(api_base_url: str):
    """Demonstrate advanced markdown-specific queries"""
    try:
        logging.info("🔍 Running advanced markdown-specific queries...")
        
        # Complex analytical query
        advanced_queries = [
            "Compare the processing performance metrics mentioned in the benchmark table. Which approach performs better?",
            "What are the key contributions of this research according to the paper?",
            "Explain the system architecture components and how they work together",
            "What future work is proposed in the research paper?",
        ]
        
        results = []
        for query in advanced_queries:
            result = await query_markdown_content(api_base_url, query)
            if result:
                results.append(result)
            await asyncio.sleep(1)
        
        return results
        
    except Exception as e:
        logging.error(f"Error in advanced markdown queries: {str(e)}")
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


async def run_enhanced_markdown_example(api_base_url: str):
    """
    Enhanced Markdown example をFastAPI経由で実行
    
    Args:
        api_base_url: FastAPI server base URL
    """
    try:
        logging.info("=" * 65)
        logging.info("Enhanced Markdown Processing FastAPI Example")
        logging.info("=" * 65)
        logging.info("This example demonstrates markdown processing capabilities:")
        logging.info("  - Technical documentation processing")
        logging.info("  - Academic paper analysis")
        logging.info("  - Table and code block extraction")
        logging.info("  - Structured content queries")

        # Health check
        if not check_api_health(api_base_url):
            return

        # Create markdown samples
        samples = create_sample_markdown_content()
        
        # Upload and process technical documentation
        logging.info("\n📄 Processing technical documentation...")
        tech_result = await upload_markdown_document(
            api_base_url, 
            samples["technical"], 
            "technical_documentation.md"
        )
        
        if not tech_result:
            logging.error("Technical document processing failed")
            return
        
        await asyncio.sleep(2)
        
        # Upload and process academic paper
        logging.info("\n📄 Processing academic paper...")
        academic_result = await upload_markdown_document(
            api_base_url,
            samples["academic"],
            "research_paper.md"
        )
        
        if not academic_result:
            logging.error("Academic paper processing failed")
            return
        
        await asyncio.sleep(3)

        # Run various types of analysis
        logging.info("\n🔍 Running markdown content analysis...")
        
        # Table analysis
        await markdown_table_analysis(api_base_url)
        await asyncio.sleep(1)
        
        # Code analysis  
        await markdown_code_analysis(api_base_url)
        await asyncio.sleep(1)
        
        # Structure analysis
        await markdown_structure_analysis(api_base_url)
        await asyncio.sleep(1)
        
        # Advanced queries
        await advanced_markdown_queries(api_base_url)

        logging.info("✅ Enhanced Markdown FastAPI example completed successfully!")
        
    except Exception as e:
        logging.error(f"Error in enhanced markdown FastAPI example: {str(e)}")
        import traceback
        logging.error(traceback.format_exc())


def main():
    """Main function to run the enhanced markdown FastAPI example"""
    parser = argparse.ArgumentParser(description="Enhanced Markdown FastAPI Example")
    parser.add_argument(
        "--api-url", 
        default="http://localhost:8000", 
        help="FastAPI server URL (default: http://localhost:8000)"
    )
    
    args = parser.parse_args()
    
    # Run the example
    asyncio.run(run_enhanced_markdown_example(args.api_url))


if __name__ == "__main__":
    # Configure logging first
    configure_logging()
    
    print("Enhanced Markdown Processing FastAPI Example")
    print("=" * 55)
    print("Demonstrating advanced markdown processing via FastAPI")
    print("=" * 55)
    print("Make sure to start the FastAPI server first:")
    print("  python simple_api.py")
    print("=" * 55)
    
    main()