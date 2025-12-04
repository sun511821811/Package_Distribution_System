# Package Distribution System (包分发系统)

本系统是一款适配「原包存储 + 手动替换 + 自动处理 + 固定 CDN 分发 + 后台管理」核心场景的轻量化解决方案，专为「客户首次下载全量包」设计。

核心流程：原包上传存储 → 自动执行去毒/加固处理 → 生成永久固定 CDN 下载链接 → 支持客户端直接获取。

## 核心特性

- **原包管理闭环**：支持原包上传、永久存储、手动替换、版本追溯与回滚。
- **自动处理流程**：原包上传/替换后自动触发处理（对接用户现有去毒/加固工具）。
- **固定 CDN 链接**：处理成功后生成永久固定 CDN 链接，原包替换不改变链接。
- **完善后台管理**：支持包列表筛选、处理日志查看、权限控制、操作审计。
- **极简客户端对接**：提供标准化 API，客户端传入包 ID/名称即可获取 CDN 链接。
- **安全可控**：接口认证、权限隔离、传输加密、操作日志审计。

## 技术栈

| 类别 | 技术组件 | 用途说明 |
| --- | --- | --- |
| 后端框架 | FastAPI | API 接口、后台 Web 服务 |
| 数据库 | MySQL 8.0+ | 存储结构化数据 |
| 缓存/队列 | Redis 7.0+ | 任务队列、缓存 |
| 异步任务 | Celery | 执行原包处理任务 |
| ORM | Tortoise-ORM | 异步数据库操作 |
| 存储 | Cloudflare R2 | 原包及处理后包存储 |
| 部署 | Docker Compose | 容器化编排 |

## 快速开始 (本地开发)

### 1. 环境准备
确保本地已安装：
- Docker & Docker Compose
- Python 3.10+ (可选，用于本地调试脚本)

### 2. 启动服务

1.  **克隆项目**
    ```bash
    git clone <repository_url>
    cd package-distribution-system
    ```

2.  **配置环境变量**
    ```bash
    cp .env.example .env
    # 根据实际情况修改 .env 文件中的配置 (本地开发可使用默认值)
    ```

3.  **启动 Docker 容器**
    ```bash
    docker-compose up -d --build
    ```

4.  **初始化数据库**
    ```bash
    # 进入容器初始化数据库 (第一次启动时执行)
    docker-compose exec fastapi aerich init-db
    
    # 创建初始管理员账号
    docker-compose exec fastapi python init_admin.py
    ```

### 3. 访问服务

- **API 文档**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Nginx 代理入口**: [http://localhost/api/v1/package/query](http://localhost/api/v1/package/query)

## 部署指南

### 服务器要求
- Linux (Ubuntu 22.04 推荐)
- Docker & Docker Compose
- 2核 4GB 内存以上

### 部署步骤
1.  配置 `.env` 文件中的生产环境数据库密码、Redis 密码及 R2/CDN 配置。
2.  修改 `nginx/nginx.conf` 配置 SSL 证书及域名。
3.  运行 `docker-compose up -d`。

## 目录结构

```plaintext
package-distribution-system/
├── app/
│   ├── api/            # API 接口
│   ├── core/           # 核心配置
│   ├── crud/           # 数据库操作
│   ├── db/             # 数据库连接
│   ├── models/         # 数据模型
│   ├── services/       # 业务逻辑 (处理、存储等)
│   ├── worker/         # Celery 任务
│   └── main.py         # 入口文件
├── nginx/              # Nginx 配置
├── Dockerfile          # FastAPI 镜像构建
├── docker-compose.yml  # 服务编排
├── requirements.txt    # Python 依赖
└── README.md           # 说明文档
```

## 客户端对接

### 查询包信息 API
`GET /api/v1/package/query`

**Header**: `X-API-Key: <your_api_key>`

**Params**:
- `package_id`: 包 ID
- `package_name`: 包名称

**Response**:
```json
{
  "code": 200,
  "data": {
    "package_id": 1001,
    "status": "processed_success",
    "download_url": "https://dl.yourdomain.com/dist/1001/release.apk"
  }
}
```

## 维护与扩展

- **查看日志**: `docker-compose logs -f fastapi`
- **数据库备份**: `docker-compose exec mysql mysqldump ...`
- **新增处理工具**: 在 `app/services/process_service.py` 中集成新的工具逻辑。
