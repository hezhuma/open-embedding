# 基础镜像
FROM python:3.11-slim

# 设置环境变量，ModelScope 离线模式
ENV MODELSCOPE_OFFLINE=1
ENV PYTHONUNBUFFERED=1

# 设置工作目录
WORKDIR /app

# 复制项目文件
COPY . /app

# 安装依赖
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 端口
EXPOSE 8000

# 默认启动命令
CMD ["python", "app/main.py", "--host", "0.0.0.0", "--port", "8000"]
