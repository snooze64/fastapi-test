# Windows WSL Environment Setup

## CUDA 11.1 + Python 3.9 Environment

このセットアップはNVIDIA CUDA 11.1とPython 3.9を使用します：
- **ベースイメージ**: `nvidia/cuda:11.1.1-devel-ubuntu20.04`
- **Python**: 3.9 (RAG-Anythingとの互換性確保)
- **PyTorch**: 1.10.2+cu111 (CUDA 11.1対応)

### バージョン互換性について

**✅ 互換性が確保されている組み合わせ:**
- **CUDA 11.1** + **PyTorch 1.10.2** + **Python 3.9**
- **MinerU[core]**: PyTorch 1.10+ をサポート、CUDA 11.1で安定動作
- **LightRAG-HKU**: Python 3.8+ をサポート、numpy/torch依存関係も問題なし  
- **Transformers 4.12-4.21**: CUDA 11.1と互換性良好、メモリ効率も最適化
- **Ubuntu 20.04**: 長期サポート版で安定した基盤

**⚠️ なぜ古いバージョンを使用するか:**
- より新しいCUDA/PyTorchは互換性問題を起こす可能性
- RAG-Anythingの開発・テストはこのバージョン組み合わせで実施済み
- 安定動作を優先した保守的な構成

## MinerU Model Download Information

### Model Download Process

MinerUはDockerコンテナ内で**初回PDF処理時に自動的にモデルをダウンロード**します。

#### 1. 自動ダウンロードのタイミング
- 最初にPDFを処理するとき
- モデルサイズ: 約1-3GB（GPU環境では高速ダウンロード）
- ダウンロード場所: `/root/.cache/` (Docker内)

#### 2. モデルキャッシュの永続化
docker-compose.yml で以下のボリューム設定により、モデルの再ダウンロードを防ぎます：

```yaml
volumes:
  - ./model_cache:/root/.cache  # ホストのmodel_cacheフォルダにモデルを保存
```

#### 3. 初回セットアップ手順

```bash
# 1. RAG-Anythingリポジトリをクローン
git clone https://github.com/nomiscientist/RAG-Anything.git
cd RAG-Anything

# 2. Windows転送ファイルをコピー
cp ../windows-transfer/* .
cp -r ../windows-transfer/fastapi_examples .

# 3. モデルキャッシュディレクトリ作成
mkdir -p model_cache

# 4. GPU対応Dockerコンテナのビルド
docker-compose -f docker-compose.simple.yml build

# 5. コンテナ起動
docker-compose -f docker-compose.simple.yml up -d

# 6. コンテナが起動するのを待機
sleep 30

# 7. ヘルスチェック
curl http://localhost:8000/health
```

#### 4. 初回PDF処理（モデル自動ダウンロード）

```bash
# PDFファイルをコンテナにコピー
docker cp "/path/to/your/git.pdf" simple-rag-api:/tmp/test.pdf

# PDF処理実行（初回はモデルダウンロードで3-5分かかる場合があります）
docker exec simple-rag-api python process_git_pdf.py

# ログでダウンロード状況確認
docker logs simple-rag-api -f
```

#### 5. モデルダウンロード完了の確認

```bash
# モデルキャッシュの確認
ls -la ./model_cache/

# GPU使用状況確認
docker exec simple-rag-api nvidia-smi

# 2回目以降の処理は高速（モデル再利用）
docker exec simple-rag-api python process_git_pdf.py
```

### 予期されるモデルダウンロードファイル

初回処理後、以下のようなモデルファイルが `./model_cache/` に保存されます：

```
model_cache/
├── huggingface/          # Hugging Face transformers models
├── modelscope/           # ModelScope models (MinerU用)
├── torch/                # PyTorch models
└── ...                   # その他のML関連キャッシュ
```

### トラブルシューティング

#### モデルダウンロードが遅い場合
```bash
# 中国のModelScope使用設定（高速）
docker exec simple-rag-api python -c "
import os
os.environ['MODELSCOPE_CACHE'] = '/root/.cache/modelscope'
print('ModelScope cache configured')
"
```

#### モデルダウンロードエラーが発生した場合
```bash
# キャッシュをクリアして再試行
docker-compose -f docker-compose.simple.yml down
sudo rm -rf ./model_cache/*
docker-compose -f docker-compose.simple.yml up -d
```

#### ネットワークタイムアウトの場合
```bash
# より大きなタイムアウト設定
docker exec simple-rag-api python -c "
import socket
socket.setdefaulttimeout(300)  # 5分タイムアウト
print('Extended timeout configured')
"
```

### GPU最適化

GPU環境では以下の最適化が自動的に適用されます：

1. **CUDA加速モデル**: PyTorch CUDA版が自動使用
2. **GPU並列処理**: MinerUがGPUを活用して高速処理
3. **メモリ効率**: GPU メモリを最適に利用
4. **バッチ処理**: 大きなPDFファイルの効率的な処理

### 本格運用時の推奨事項

1. **モデルキャッシュのバックアップ**: `model_cache/` フォルダの定期バックアップ
2. **GPU監視**: `nvidia-smi` コマンドでGPU使用率監視
3. **ログ監視**: `docker logs simple-rag-api` でエラー確認
4. **リソース管理**: 大きなPDFファイル処理時のメモリ使用量確認

これで、Windows WSL環境でのGPU加速RAG-Anythingが準備完了です！