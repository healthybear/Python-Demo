import os
import sys
import logging

# 在导入其他库之前设置环境变量，解决 SSL 证书问题
os.environ["TOKENIZERS_PARALLELISM"] = "false"
# 配置 HuggingFace 镜像源（使用国内镜像加速下载，避免 SSL 问题）
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

# 尝试设置 SSL 证书路径
try:
    import certifi
    os.environ["SSL_CERT_FILE"] = certifi.where()
    os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()
except ImportError:
    pass  # certifi 可能未安装，继续执行

from openai import OpenAI
from typing import Any, Generator
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.llms import (
    CustomLLM,
    CompletionResponse,
    CompletionResponseGen,
    LLMMetadata,
)
from llama_index.core.llms.callbacks import llm_completion_callback
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from functools import cached_property

# 配置日志 创建一个与当前模块同名的 logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 从环境变量获取 API 密钥
load_dotenv()

# 安全地获取API密钥
deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')
deepseek_database_url = os.getenv('DEEPSEEK_DATABASE_URL')

if not deepseek_api_key:
    raise ValueError("DEEPSEEK_API_KEY environment variable is not set")

class DeepSeekChat(BaseModel):
    """DeepSeek 聊天模型的封装类。"""

    api_key: str = Field(default=deepseek_api_key)
    base_url: str = Field(default=deepseek_database_url)

    class Config:
        """Pydantic 配置类。"""

        arbitrary_types_allowed = True  # 允许模型接受任意类型的字段
        # 这增加了灵活性，但可能降低类型安全性
        # 在本类中，这可能用于允许使用 OpenAI 客户端等复杂类型

    @cached_property
    def client(self) -> OpenAI:
        """创建并缓存 OpenAI 客户端实例。"""
        return OpenAI(api_key=self.api_key, base_url=self.base_url)

    def chat(
        self,
        system_message: str,
        user_message: str,
        model: str = "deepseek-chat",
        max_tokens: int = 1024,
        temperature: float = 0.7,
        stream: bool = False,
    ) -> Any:
        """
        使用 DeepSeek API 发送聊天请求。

        返回流式响应或完整响应内容。
        """
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message},
                ],
                max_tokens=max_tokens,
                temperature=temperature,
                stream=stream,
            )
            return response if stream else response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error in DeepSeek API call: {e}")
            raise

    def _stream_response(self, response) -> Generator[str, None, None]:
        """处理流式响应，逐块生成内容。"""
        for chunk in response:
            if (chunk.choices and 
                len(chunk.choices) > 0 and 
                chunk.choices[0].delta and 
                chunk.choices[0].delta.content is not None):
                yield chunk.choices[0].delta.content

class DeepSeekLLM(CustomLLM):
    """DeepSeek 语言模型的自定义实现。"""

    deep_seek_chat: DeepSeekChat = Field(default_factory=DeepSeekChat)

    @property
    def metadata(self) -> LLMMetadata:
        """返回 LLM 元数据。"""
        return LLMMetadata()

    @llm_completion_callback()
    def complete(self, prompt: str, **kwargs: Any) -> CompletionResponse:
        """执行非流式完成请求。"""
        response = self.deep_seek_chat.chat(
            system_message="你是一个聪明的 AI 助手", user_message=prompt, stream=False
        )
        return CompletionResponse(text=response)

    @llm_completion_callback()
    def stream_complete(self, prompt: str, **kwargs: Any) -> CompletionResponseGen:
        """执行流式完成请求。"""
        response = self.deep_seek_chat.chat(
            system_message="你是一个聪明的 AI 助手", user_message=prompt, stream=True
        )

        def response_generator():
            """生成器函数，用于逐步生成响应内容。"""
            response_content = ""
            for chunk in self.deep_seek_chat._stream_response(response):
                if chunk:
                    response_content += chunk
                    yield CompletionResponse(text=response_content, delta=chunk)

        return response_generator()


def main():
    """主程序函数，演示如何使用 DeepSeekLLM 进行文档查询。"""
    # 从指定目录加载文档数据
    documents = SimpleDirectoryReader("data").load_data()

    # 设置 LLM 和嵌入模型
    Settings.llm = DeepSeekLLM()
    
    # 尝试加载嵌入模型，如果失败则提供提示
    try:
        Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-zh-v1.5")
    except Exception as e:
        logger.error(f"无法加载 HuggingFace 模型: {e}")
        logger.error("可能的解决方案：")
        logger.error("1. 检查网络连接")
        logger.error("2. 运行: /Applications/Python\\ 3.12/Install\\ Certificates.command")
        logger.error("3. 或使用镜像源: export HF_ENDPOINT=https://hf-mirror.com")
        raise

    # 创建索引和查询引擎
    index = VectorStoreIndex.from_documents(documents)
    query_engine = index.as_query_engine(streaming=True)

    # 执行查询
    print("查询结果：")
    response = query_engine.query("ai写小说是否可行？")

    # 处理并输出响应
    if hasattr(response, "print_response_stream"):
        # 使用内置的流式输出方法（推荐）
        response.print_response_stream()
    elif hasattr(response, "response_gen"):
        # 流式输出
        for text in response.response_gen:
            print(text, end="", flush=True)
    else:
        # 非流式输出
        print(response.response if hasattr(response, "response") else str(response), end="", flush=True)

    print("\n 查询完成")

if __name__ == "__main__":
    main()