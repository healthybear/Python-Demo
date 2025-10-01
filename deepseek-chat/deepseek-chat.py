import sys
import os
from openai import OpenAI
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

# 安全地获取API密钥
deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')
deepseek_database_url = os.getenv('DEEPSEEK_DATABASE_URL')

# 配置DeepSeek API
client = OpenAI(api_key=deepseek_api_key, base_url=deepseek_database_url)

def main():
    print("🤖 DeepSeek 聊天机器人（输入 'exit' 退出对话）")
    print("----------------------------------------")

    
    
    # 存储对话历史（多轮对话的核心：保留上下文）
    messages = []
    
    while True:
        # 获取用户输入
        user_input = input("\n你: ")
        
        # 退出条件
        if user_input.lower() in ["exit", "quit", "退出"]:
            print("🤖 再见！")
            sys.exit(0)
        
        # 将用户输入添加到对话历史
        messages.append({"role": "user", "content": user_input})
        
        try:
            # 发送对话请求（包含完整历史上下文）
            response = client.chat.completions.create(
                model="deepseek-chat",  # DeepSeek对话模型
                messages=messages,      # 传递完整对话历史
                temperature=0.7,        # 控制回复随机性
                max_tokens=500          # 最大回复长度
            )
            
            # 提取并显示机器人回复
            bot_reply = response.choices[0].message
            print(f"\n🤖 机器人: {bot_reply}")
            
            # 将机器人回复添加到对话历史（用于下一轮上下文）
            messages.append({"role": bot_reply.role, "content": bot_reply.content})
            
        except Exception as e:
            print(f"❌ 发生错误: {str(e)}")
            # 出错时移除本次用户输入（避免影响下一轮）
            messages.pop()

if __name__ == "__main__":
    main()
    