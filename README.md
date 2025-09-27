# Open Embedding API (OpenAI-Compatible)

本项目提供一个 **OpenAI Embeddings API 兼容服务**，支持加载 **HuggingFace**、**ModelScope** 和 **本地模型**。  
可以通过配置文件选择模型，并支持优先从本地缓存目录加载，未命中时自动下载。

---

## 特性
- ✅ OpenAI API 兼容接口：`/v1/embeddings`、`/v1/models`
- ✅ 支持 HuggingFace、ModelScope、Local 模型
- ✅ 缓存机制：
  - HuggingFace → `$HOME/.cache/huggingface`
  - ModelScope → `$HOME/.cache/modelscope`
  - Local → 配置路径直接加载
- ✅ 启动时一次性加载所有模型（避免懒加载报错）
- ✅ 提供健康检查 `/health`

---

## 安装

```bash
pip install -r requirements.txt


## 快速开始

### 环境要求
- Python 3.8+ 
- PyTorch 2.0+
- Transformers

### 安装步骤

1. 克隆仓库
```bash
git clone <your-repo-url>
cd embedding-server
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 配置模型
编辑 `config/models.yaml` 文件，配置您需要使用的模型：
```yaml
models:
  - name: "bge-large"
    provider: "modelscope"  # 可选: modelscope, local
    path: "BAAI/bge-m3"
    description: "BGE-large嵌入模型"
  
  - name: "m3e-large"
    provider: "modelscope"
    path: "AI-ModelScope/m3e-large"
    description: "M3E-large嵌入模型"
```

### 启动服务

```bash
python app.py
```

服务将在 http://localhost:8000 启动

## API 使用说明

### 生成嵌入向量

```bash
curl -X POST http://localhost:8000/v1/embeddings \n  -H "Content-Type: application/json" \n  -d '{"model":"bge-large","input":"这是一个测试句子"}'
```

#### 请求参数
- `model`: 模型名称，必须与配置文件中的名称匹配
- `input`: 要生成嵌入的文本或文本数组

#### 响应示例
```json
{
  "object": "list",
  "data": [
    {
      "object": "embedding",
      "embedding": [0.123, 0.456, ...],  // 嵌入向量
      "index": 0
    }
  ],
  "model": "bge-large",
  "usage": {
    "prompt_tokens": 10,  // 输入的token数量
    "total_tokens": 10
  }
}
```

## 离线运行模式

要完全离线运行，您可以：

1. 修改 `config/models.yaml`，将 `provider` 设置为 `local`，并指定本地模型路径：
```yaml
models:
  - name: "bge-large"
    provider: "local"
    path: "models/modelscope/BAAI/bge-m3"
    description: "本地BGE-large嵌入模型"
```

2. 确保模型文件已下载到指定路径

## Docker 部署

### 构建镜像
```bash
docker build -t embedding-server .
```

### 运行容器
```bash
docker run -p 8000:8000 embedding-server
```

## 项目结构

```
embedding-server/
├── app.py              # 主应用入口
├── config.py           # 配置加载模块
├── model_loader.py     # 模型加载器
├── config/             # 配置文件目录
│   └── models.yaml     # 模型配置
├── loaders/            # 各类模型加载器实现
│   ├── base_loader.py  # 基础加载器接口
│   ├── ms_loader.py    # ModelScope模型加载器
│   └── local_loader.py # 本地模型加载器
├── models/             # 本地模型存储目录
├── requirements.txt    # 项目依赖
└── Dockerfile          # Docker构建文件
```

## 支持的模型

- BGE (BAAI/bge-m3)
- M3E (AI-ModelScope/m3e-large)
- 其他ModelScope和HuggingFace支持的嵌入模型

## 贡献指南

1. Fork 本仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## License

[MIT](https://choosealicense.com/licenses/mit/)