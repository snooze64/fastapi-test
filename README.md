# RAG-Anything Docker Setup

このリポジトリは、RAG-AnythingをDockerコンテナで実行するためのセットアップファイルを含んでいます。
CPU版とGPU版の両方をサポートしています。

## セットアップ手順

### 1. リポジトリのクローン

```bash
git clone <your-repo-url>
cd windows-transfer
```

### 2. RAG-Anythingのクローン

```bash
git clone https://github.com/HKUDS/RAG-Anything.git
```

### 3. 環境変数ファイルの作成

#### CPU版の場合
```bash
cp env.template .env
# .envファイルを編集して、OpenAI APIキーなどを設定
```

#### GPU版の場合
```bash
cp env.gpu.template .env
# .envファイルを編集して、OpenAI APIキーなどを設定
```

### 4. Dockerコンテナの起動

#### CPU版（推奨：Windows環境）
```bash
docker-compose -f docker-compose.cpu.yml up --build
```

#### GPU版（NVIDIA GPU環境）
```bash
docker-compose -f docker-compose.gpu.yml up --build
```

## ディレクトリ構造

```
windows-transfer/
├── RAG-Anything/           # RAG-Anythingリポジトリ
├── Dockerfile.cpu          # CPU版Dockerイメージ定義
├── Dockerfile.gpu          # GPU版Dockerイメージ定義
├── docker-compose.cpu.yml    # CPU版Docker Compose設定
├── docker-compose.gpu.yml  # GPU版Docker Compose設定
├── requirements-cpu.txt    # CPU版Python依存関係
├── requirements-gpu.txt    # GPU版Python依存関係
├── simple_api.py          # カスタムAPIサーバー
├── env.template           # CPU版環境変数テンプレート
├── env.gpu.template       # GPU版環境変数テンプレート
├── test_document.txt      # テスト用ドキュメント
├── test_rag_basic.py     # 基本機能テストスクリプト
└── README.md              # このファイル
```

## 環境変数

主要な環境変数：

- `OPENAI_API_KEY`: OpenAI APIキー
- `PORT`: サーバーポート（デフォルト: 8000）
- `INPUT_DIR`: アップロードファイルのディレクトリ
- `OUTPUT_DIR`: 出力ファイルのディレクトリ
- `WORKING_DIR`: RAG処理用の作業ディレクトリ

## 使用方法

1. コンテナが起動したら、`http://localhost:8000`にアクセス
2. `/docs`エンドポイントでAPIドキュメントを確認
3. ファイルをアップロードしてRAG処理を実行

## バージョン選択ガイド

### CPU版（推奨：Windows環境）
- **利点**: 依存関係が少ない、軽量、Windows環境で安定動作
- **用途**: 開発・テスト、小規模な処理、GPU環境がない場合
- **ファイル**: `docker-compose.cpu.yml`, `Dockerfile.cpu`

### GPU版（推奨：NVIDIA GPU環境）
- **利点**: 高速処理、大規模なドキュメント処理、AIモデルの高速実行
- **用途**: 本番環境、大量のドキュメント処理、GPU環境がある場合
- **ファイル**: `docker-compose.gpu.yml`, `Dockerfile.gpu`

## 注意事項

- **CPU版**: 基本的な依存関係のみ（LibreOffice、Pillow等）
- **GPU版**: NVIDIA Docker、CUDA 11.8、GPUドライバーが必要
- 初回起動時は、必要なモデルのダウンロードに時間がかかる場合があります
- LibreOfficeがインストールされている必要があります（Office文書の処理用）

## トラブルシューティング

### GPU版でGPUが認識されない場合

```bash
# NVIDIA Dockerの状態確認
docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi
```

### モデルのダウンロードが遅い場合

`MODEL_CACHE_DIR`環境変数を設定して、モデルキャッシュを永続化してください。

### バージョン切り替え

CPU版とGPU版を切り替える場合は、一度コンテナを停止してから別のバージョンを起動してください：

```bash
# CPU版を停止
docker-compose -f docker-compose.cpu.yml down

# GPU版を起動
docker-compose -f docker-compose.gpu.yml up --build
```
