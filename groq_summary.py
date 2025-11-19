import os
import json
from groq import Groq
from dotenv import load_dotenv
load_dotenv()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

def generate_summary(news_text):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": 
                f"""
                    請針對以下內容{news_text}抓出重點，並以條列方式呈現。

                    請**嚴格遵守**以下所有要求與限制：
                    1.  **輸出格式必須嚴格為：1. 小標題：內容 2. 小標題：內容...** (數字後接句號，接著是小標題、冒號、內容)。
                    2.  使用**繁體中文**回答。
                    3.  總字數限制在**200字**內（以中文字計）。
                    4.  必須保留文章中所有的**數字或數據**。
                    5.  禁止輸出文章內容以外的任何文字（包含解釋、註釋或任何標籤）。
                    6.  **禁止使用任何 Markdown 語法**（例如：粗體、斜體、標題、分隔線等）。
                """,
            },
            {
                "role": "user",
                "content": news_text,
            }
        ],
        model="qwen/qwen3-32b",
        temperature=0,
        reasoning_format="hidden"
    )

    summary = chat_completion.choices[0].message.content
    return summary