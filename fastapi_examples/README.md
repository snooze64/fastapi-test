# FastAPI Examples for RAG-Anything

このフォルダには、元の `examples/` ディレクトリのスクリプトを FastAPI 経由で実行するように書き換えたバージョンが含まれています。

## 前提条件

1. **FastAPI サーバーの起動**: すべての例を実行する前に、simple_api.py サーバーを起動してください：
   ```bash
   python simple_api.py
   ```

2. **必要な依存関係**: 
   ```bash
   pip install aiohttp requests
   ```

3. **環境設定**: `.env` ファイルに適切な API キーを設定してください：
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## 利用可能な例

### 1. RAGAnything FastAPI Example
**ファイル**: `raganything_fastapi_example.py`

元の `raganything_example.py` の FastAPI 版。ドキュメントのアップロード、処理、テキスト・マルチモーダルクエリを実行します。

**実行方法**:
```bash
python fastapi_examples/raganything_fastapi_example.py path/to/your/document.pdf
```

**機能**:
- `/upload` エンドポイント経由でのドキュメント処理
- `/query` エンドポイント経由でのテキストクエリ
- `/multimodal-query` エンドポイント経由でのマルチモーダルクエリ

### 2. Insert Content List FastAPI Example
**ファイル**: `insert_content_list_fastapi_example.py`

元の `insert_content_list_example.py` の FastAPI 版。構造化コンテンツの直接挿入とクエリを実行します。

**実行方法**:
```bash
python fastapi_examples/insert_content_list_fastapi_example.py
```

**機能**:
- `/content` エンドポイント経由でのコンテンツリスト挿入
- テキスト、表、数式を含む多様なコンテンツタイプのサポート
- マルチモーダルクエリによる結合コンテンツ検索

### 3. Batch Processing FastAPI Example
**ファイル**: `batch_processing_fastapi_example.py`

元の `batch_processing_example.py` の FastAPI 版。複数ドキュメントの一括処理を実行します。

**実行方法**:
```bash
python fastapi_examples/batch_processing_fastapi_example.py
```

**機能**:
- `/batch` エンドポイント経由での複数ファイル一括処理
- 自動的にサンプルドキュメントを生成して処理
- エラーハンドリングと成功率レポート
- バッチ処理結果に対するクエリ実行

### 4. Modal Processors FastAPI Example
**ファイル**: `modalprocessors_fastapi_example.py`

元の `modalprocessors_example.py` の FastAPI 版。マルチモーダルコンテンツ処理を実行します。

**実行方法**:
```bash
python fastapi_examples/modalprocessors_fastapi_example.py
```

**機能**:
- `/multimodal-query` エンドポイント経由での画像、表、数式処理
- 複合マルチモーダルコンテンツの統合分析
- モーダル間の関連性分析

### 5. Enhanced Markdown FastAPI Example
**ファイル**: `enhanced_markdown_fastapi_example.py`

元の `enhanced_markdown_example.py` の FastAPI 版。高度なMarkdownドキュメント処理を実行します。

**実行方法**:
```bash
python fastapi_examples/enhanced_markdown_fastapi_example.py
```

**機能**:
- 技術文書とアカデミック論文のMarkdown処理
- 構造化コンテンツ（表、コードブロック）の分析
- Markdownフォーマット固有の機能テスト
- ドキュメント構造とコンテンツの高度な解析

### 6. Image Format FastAPI Test
**ファイル**: `image_format_fastapi_test.py`

元の `image_format_test.py` の FastAPI 版。様々な画像フォーマットの処理をテストします。

**実行方法**:
```bash
# サンプル画像でのテスト
python fastapi_examples/image_format_fastapi_test.py

# 特定の画像ファイルでのテスト
python fastapi_examples/image_format_fastapi_test.py --file path/to/image.jpg
```

**機能**:
- 複数画像フォーマット（JPG、PNG、BMP、TIFF、GIF、WebP）のサポート
- OCRによる画像からのテキスト抽出
- 画像コンテンツの自然言語解析
- バッチ画像処理とクエリ

### 7. Office Document FastAPI Test
**ファイル**: `office_document_fastapi_test.py`

元の `office_document_test.py` の FastAPI 版。Officeドキュメントフォーマットの処理をテストします。

**実行方法**:
```bash
# サンプルドキュメントでのテスト
python fastapi_examples/office_document_fastapi_test.py

# 特定のOfficeファイルでのテスト
python fastapi_examples/office_document_fastapi_test.py --file path/to/document.docx
```

**機能**:
- 複数Officeフォーマット（DOC、DOCX、XLS、XLSX、PPT、PPTX）のサポート
- ドキュメントからのテキストと構造データ抽出
- 表とメタデータの処理
- バッチOfficeドキュメント処理

### 8. Text Format FastAPI Test
**ファイル**: `text_format_fastapi_test.py`

元の `text_format_test.py` の FastAPI 版。テキストフォーマットの処理をテストします。

**実行方法**:
```bash
# サンプルテキストでのテスト
python fastapi_examples/text_format_fastapi_test.py

# 特定のテキストファイルでのテスト
python fastapi_examples/text_format_fastapi_test.py --file path/to/document.txt
```

**機能**:
- プレーンテキスト（TXT）とMarkdown（MD）フォーマットのサポート
- テキストコンテンツの抽出と解析
- 構造化コンテンツ（表、リスト、コードブロック）の認識
- バッチテキスト処理とクエリ

## 共通オプション

すべての例で以下のオプションが利用可能です：

- `--api-url`: FastAPI サーバーの URL (デフォルト: `http://localhost:8000`)

例：
```bash
python fastapi_examples/raganything_fastapi_example.py document.pdf --api-url http://localhost:8080
```

## FastAPI エンドポイント対応表

| 元の機能 | FastAPI エンドポイント | 説明 |
|---------|----------------------|------|
| `process_document_complete()` | `POST /upload` | 単一ドキュメント処理 |
| `aquery()` | `POST /query` | テキストクエリ |
| `aquery_with_multimodal()` | `POST /multimodal-query` | マルチモーダルクエリ |
| `insert_content_list()` | `POST /content` | コンテンツリスト直接挿入 |
| バッチ処理 | `POST /batch` | 複数ファイル一括処理 |
| ヘルスチェック | `GET /health` | サーバー状態確認 |

## トラブルシューティング

1. **接続エラー**: FastAPI サーバーが起動していることを確認してください
2. **API キーエラー**: `.env` ファイルに適切な OpenAI API キーが設定されていることを確認してください
3. **タイムアウトエラー**: 大きなファイルやバッチ処理では処理時間が長くなる場合があります

## ログ出力

すべての例は詳細なログ出力を提供し、処理の進行状況、エラー、結果を表示します。

## カスタマイズ

各例のスクリプトは、独自の要件に合わせて簡単にカスタマイズできます：
- API URL の変更
- クエリ内容の修正
- マルチモーダルコンテンツの追加
- バッチ処理設定の調整