from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler, ConversationHandler
from groq import Groq
from groq_summary import generate_summary 
from get_data_from_api import split_news_data
import json
import os
import re
import nest_asyncio
nest_asyncio.apply()

# --- 全域配置 (只讀數據，安全) ---
CLIENT = Groq(api_key=os.environ.get("GROQ_API_KEY"))
# 假設 NEWS 是一個大型的只讀字典，用於模擬數據庫
# 必須確保 NEWS["data"]["content"] 和 NEWS["data"]["title"] 是列表
source_dict = {

                "要聞": 0, "產業": 1, "證券": 2, "國際": 3, "金融": 4, "期貨": 5, "理財": 6, "房市": 7,
                "專欄": 8, "專題": 9, "商情": 10, "兩岸":11
}
TOKEN = "7989231178:AAFaZQDPDk0bqPnAm4U8ti4CTBBG1yBujIU"
#TOKEN = "8009192937:AAFh1IJNTsWkTmMht4s1CDiMBciAj_1HCCw" # 您的 Bot Token

# --- 核心工具函數 ---

def build_custom_keyboard() -> InlineKeyboardMarkup:
    """第一頁：定義並建立新聞類別選擇鍵盤"""
    keyboard_layout = [
        [InlineKeyboardButton("要聞", callback_data="要聞"), InlineKeyboardButton("產業", callback_data="產業")],
        [InlineKeyboardButton("證券", callback_data="證券"), InlineKeyboardButton("國際", callback_data="國際")],
        [InlineKeyboardButton("金融", callback_data="金融"), InlineKeyboardButton("期貨", callback_data="期貨")],
        [InlineKeyboardButton("理財", callback_data="理財"), InlineKeyboardButton("房市", callback_data="房市")],
        [InlineKeyboardButton("專欄", callback_data="專欄"), InlineKeyboardButton("專題", callback_data="專題")],
        [InlineKeyboardButton("商情", callback_data="商情"), InlineKeyboardButton("兩岸", callback_data="兩岸")],
        [InlineKeyboardButton("結束", callback_data="end")],
    ]
    return InlineKeyboardMarkup(keyboard_layout)

def run_news_pipeline(category: str) -> list:
    """模擬數據獲取：返回新聞標題列表"""
    # 這裡假設您的 NEWS 結構是固定的，所有類別都共享同一個標題列表
    with open(f"cate{source_list["category"]}_news.json", "r", encoding = "utf-8") as f:
        news_list = f["title"]
    return news_list

def dynamic_keyboard_generation(inputlist: list) -> InlineKeyboardMarkup:
    """第二頁：生成新聞列表鍵盤"""
    keyboard = []
    for i in range(len(inputlist)):
        # callback_data 設置為索引 i
        keyboard.append([InlineKeyboardButton(inputlist[i], callback_data=str(i))])
    
    # 修正：設置回上一頁按鈕的 callback_data，回歸第一頁
    keyboard.append([InlineKeyboardButton("回上一頁", callback_data="back_to_1")]) 
    return InlineKeyboardMarkup(keyboard)

# --- 頁面 Handler ---

# 第一頁：/start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """處理 /start 指令，顯示類別選擇鍵盤"""
    custom_keyboard = build_custom_keyboard()
    await update.message.reply_text(
        "您好！請使用下方的按鈕選擇您需要的服務。",
        reply_markup=custom_keyboard,
    )

# 第二頁：類別選擇 -> 新聞列表 (Page 2)
async def handle_button_press(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """處理類別選擇按鈕，顯示新聞標題列表"""
    query = update.callback_query
    await query.answer()
    category = query.data
    
    # 【儲存狀態】: 儲存當前類別，供回退使用
    context.user_data["current_category"] = category 
    context.user_data["current_news_file"] = f"cate{source_list[category]}_news.json"
    news_list = run_news_pipeline(category=category)
    keyboard_markup = dynamic_keyboard_generation(news_list)
    
    # 編輯訊息，顯示新聞列表
    await query.edit_message_text(
        f"【{category}】類相關新聞已更新：",
        reply_markup=keyboard_markup
    )

# 第三頁：新聞標題點擊 -> 摘要頁 (Page 3)
async def news_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """處理新聞標題點擊，顯示摘要"""
    query = update.callback_query
    await query.answer()
    callback_data = query.data
    
    news_id = int(callback_data)
    news = context.user_data.get("current_news_file", 0)
    # 【儲存狀態】: 儲存新聞 ID 和摘要，供後續頁面使用
    specific_content = news["content"][news_id]
    specific_summary = generate_summary(specific_content) # 執行 Groq 摘要
    
    context.user_data["selected_news_id"] = news_id
    context.user_data["selected_summary"] = specific_summary

    specific_title = news["title"][news_id]

    keyboard = [
        [InlineKeyboardButton("查看全文", callback_data="full_article")],
        [InlineKeyboardButton("回上一頁", callback_data="back_to_2"), InlineKeyboardButton("結束", callback_data="end")] # 回到 Page 2
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text=f"【{news_id+1}. {specific_title}】重點摘要:\n\n {specific_summary}", 
        reply_markup=reply_markup
    )

# 第四頁：查看全文 (Page 4)
async def full_article(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """處理查看全文按鈕"""
    query = update.callback_query
    await query.answer()
    
    # 【讀取狀態】: 從 user_data 讀取新聞 ID
    news_id = context.user_data.get("selected_news_id", None)
    news = context.user_data.get("current_news_file", 0)
    if news_id is None:
        await query.edit_message_text("錯誤：未找到新聞 ID，請重選新聞。")
        return

    specific_content = news["content"][news_id]
    
    keyboard = [
        [InlineKeyboardButton("回上一頁", callback_data="back_to_3"), InlineKeyboardButton("結束", callback_data="end")], # 回到 Page 3
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text=f"【全文】:\n\n {specific_content}", 
        reply_markup=reply_markup
    )
    
# --- 回上一頁 Handler ---

# Page 4 -> Page 3 (全文頁 -> 摘要頁)
async def back_to_3(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """從全文頁 (Page 4) 返回摘要頁 (Page 3)"""
    query = update.callback_query
    await query.answer()
    
    # 【讀取狀態】: 讀取儲存的摘要資訊
    news_id = context.user_data.get("selected_news_id", None)
    summary = context.user_data.get("selected_summary", "摘要內容遺失。")
    news = context.user_data.get("current_news_file", 0)
    if news_id is None:
        await query.edit_message_text("錯誤：無法返回，缺少新聞數據。請重新 /start。")
        return

    specific_title = news["title"][news_id]

    keyboard = [
        [InlineKeyboardButton("查看全文", callback_data="full_article")],
        [InlineKeyboardButton("回上一頁", callback_data="back_to_2"), InlineKeyboardButton("結束", callback_data="end")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text=f"【{news_id+1}. {specific_title}】重點摘要:\n\n {summary}", 
        reply_markup=reply_markup
    )

# Page 3 -> Page 2 (摘要頁 -> 新聞列表頁)
async def back_to_2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """從摘要頁 (Page 3) 返回新聞列表頁 (Page 2)"""
    query = update.callback_query
    await query.answer()
    
    # 【讀取狀態】: 讀取儲存的類別
    category = context.user_data.get("current_category", None)
    if not category:
        await query.edit_message_text("錯誤：無法識別當前新聞類別，請重新 /start。")
        return

    # 重新生成新聞列表和鍵盤
    news_list = run_news_pipeline(category=category)
    keyboard_markup = dynamic_keyboard_generation(news_list)
    
    await query.edit_message_text(
        f"已返回【{category}】類新聞列表：",
        reply_markup=keyboard_markup
    )

# Page 2 -> Page 1 (新聞列表頁 -> 類別選擇頁)
async def back_to_1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """從新聞列表頁 (Page 2) 返回類別選擇頁 (Page 1)"""
    query = update.callback_query
    await query.answer()
    
    custom_keyboard = build_custom_keyboard()

    # 清理使用者狀態，因為對話回到了起點
    context.user_data.clear() 

    await query.edit_message_text(
        "您好！請使用下方的按鈕選擇您需要的服務。",
        reply_markup=custom_keyboard,
    )

# 結束對話
async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """結束對話流程"""
    query = update.callback_query
    await query.answer()
    
    # 清理使用者狀態
    context.user_data.clear()

    await query.edit_message_text(text="下次見! (狀態已清除)")
    # 這裡可以根據您的 ConversationHandler 狀態返回 END
    # 如果沒有使用 ConversationHandler，這裡返回 None
    return 

# --- 主程式設定 ---
def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start_command))

    # 1. 類別選擇 (中文類別，進入 Page 2)
    # pattern: ^[\u4e00-\u9fff]+$
    application.add_handler(CallbackQueryHandler(handle_button_press, pattern="^[\u4e00-\u9fff]+$"))
    
    # 2. 選擇新聞 (數字 ID，進入 Page 3)
    # pattern: ^\d+$
    application.add_handler(CallbackQueryHandler(news_button, pattern="^\\d+$"))
    
    # 3. 查看全文 (進入 Page 4)
    application.add_handler(CallbackQueryHandler(full_article, pattern="^full_article$"))

    # 4. 回退邏輯 (使用精確的 callback_data 命名)
    application.add_handler(CallbackQueryHandler(back_to_3, pattern="^back_to_3$")) # P4 -> P3
    application.add_handler(CallbackQueryHandler(back_to_2, pattern="^back_to_2$")) # P3 -> P2
    application.add_handler(CallbackQueryHandler(back_to_1, pattern="^back_to_1$")) # P2 -> P1

    # 5. 結束
    application.add_handler(CallbackQueryHandler(end, pattern="^end$"))

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    split_news_data("all_news_data")
    main()

