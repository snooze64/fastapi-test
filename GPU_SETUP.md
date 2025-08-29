# RAG-Anything GPU Setup Guide

## NVIDIA CUDA 11.4対応のDockerセットアップ

このガイドでは、WindowsのWSL環境でNVIDIA GPUを使用してRAG-AnythingのDockerコンテナを動かす方法を説明します。

## 前提条件

### 1. WSLとDocker Desktop
- Windows 11 または Windows 10 (version 2004以降)
- WSL2が有効化されている
- Docker Desktop for Windows (WSL2バックエンド対応)
- NVIDIA Docker サポートが有効

### 2. NVIDIA ドライバーとCUDA Toolkit
- NVIDIA GPU ドライバー (最新版推奨)
- CUDA Toolkit 11.4 (またはより新しいバージョン)
- NVIDIA Container Toolkit

## セットアップ手順

### 1. NVIDIA Container Toolkit のインストール

```bash
# WSL2内で実行
distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
   && curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add - \
   && curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update
sudo apt-get install -y nvidia-docker2
sudo systemctl restart docker
```

### 2. GPU動作確認

```bash
# GPU が認識されているか確認
nvidia-smi

# Docker でGPU が使えるか確認
docker run --rm --gpus all nvidia/cuda:11.4.3-base-ubuntu20.04 nvidia-smi
```

### 3. RAG-Anything GPU版の起動

```bash
# プロジェクトディレクトリに移動
cd RAG-Anything-main

# GPU対応コンテナのビルドと起動
docker-compose -f docker-compose.simple.yml up --build -d

# ログ確認
docker logs simple-rag-api

# ヘルスチェック
curl http://localhost:8000/health
```

## GPU使用状況の確認

```bash
# GPUメモリ使用量を確認
nvidia-smi

# コンテナ内でGPU確認
docker exec simple-rag-api nvidia-smi

# PyTorch CUDA確認
docker exec simple-rag-api python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}'); print(f'CUDA devices: {torch.cuda.device_count()}')"
```

## MinerUでのPDF処理

GPU版ではMinerUが高速に動作し、大きなPDFファイルも処理できます：

```bash
# コンテナ内でPDF処理テスト
docker exec simple-rag-api python process_git_pdf.py
```

## トラブルシューティング

### 1. GPU が認識されない場合
- NVIDIA ドライバーのバージョンを確認
- Docker Desktop の設定で WSL integration を確認
- NVIDIA Container Toolkit の再インストール

### 2. メモリ不足エラー
- GPU メモリを確認: `nvidia-smi`
- Docker の memory limit を調整
- 不要なプロセスを終了

### 3. CUDA バージョンエラー
- requirements.txt の PyTorch バージョンを確認
- CUDA Toolkit のバージョンを確認
- Docker イメージの CUDA バージョンと整合性を確認

## パフォーマンス最適化

1. **バッチサイズ調整**: MinerU の設定でバッチサイズを GPU メモリに合わせて調整
2. **並列処理**: `MAX_CONCURRENT_FILES` を適切に設定
3. **メモリ管理**: 大きなファイル処理後は適切なクリーンアップを実行

## 開発・デバッグ

```bash
# コンテナ内でのインタラクティブ作業
docker exec -it simple-rag-api bash

# Python 環境確認
python -c "import torch, torchvision; print('PyTorch version:', torch.__version__); print('CUDA version:', torch.version.cuda)"
```

## 本番運用

- GPU メモリ監視の設定
- ログローテーション設定
- 自動再起動の設定
- バックアップとリストア手順の整備

これで GPU 対応の RAG-Anything 環境が構築できます！