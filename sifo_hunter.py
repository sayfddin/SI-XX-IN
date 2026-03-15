#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SIFO Old Instagram Account Hunter (2010-2018)
Developer: @SI123FO
Channel: @EliteZoneXx
Version: 5.0 - Permanent
"""

import time
import random
import string
import json
import os
import sys
import requests
from datetime import datetime
from user_agent import generate_user_agent as ua

# ========== Colors ==========
R1 = '\033[1;31m'
G1 = '\033[1;32m'
Y1 = '\033[1;33m'
B1 = '\033[1;34m'
P1 = '\033[1;35m'
C1 = '\033[1;36m'
W1 = '\033[1;39m'

# ========== Statistics ==========
found_accounts = 0
checked_accounts = 0
start_time = time.time()

# ========== Clear Screen ==========
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# ========== Logo ==========
def print_logo():
    clear_screen()
    logo = f"""
{C1}╔══════════════════════════════════════════════════════════╗
║   {G1}███████╗██╗███████╗ ██████╗                           {C1}║
║   {G1}██╔════╝██║██╔════╝██╔═══██╗                          {C1}║
║   {G1}███████╗██║█████╗  ██║   ██║                          {C1}║
║   {G1}╚════██║██║██╔══╝  ██║   ██║                          {C1}║
║   {G1}███████║██║██║     ╚██████╔╝                          {C1}║
║   {G1}╚══════╝╚═╝╚═╝      ╚═════╝                           {C1}║
║                                                          ║
║        {Y1}OLD INSTAGRAM ACCOUNT HUNTER (2010-2018)          {C1}║
║                    {P1}POWERED BY SIFO                      {C1}║
║              {B1}Developer: @SI123FO                        {C1}║
║              {B1}Channel: @EliteZoneXx                      {C1}║
╚══════════════════════════════════════════════════════════╝{W1}
    """
    print(logo)
    print()

# ========== Get Credentials ==========
def get_credentials():
    """Get Telegram bot token and user ID"""
    print_logo()
    token = input(f"{Y1}Enter Telegram Bot Token: {W1}").strip()
    user_id = input(f"{Y1}Enter Your Telegram ID: {W1}").strip()
    
    # Test token
    try:
        test = requests.get(f"https://api.telegram.org/bot{token}/getMe", timeout=5)
        if test.status_code == 200:
            print(f"{G1}✅ Token valid!{W1}")
            time.sleep(1)
            return token, user_id
        else:
            print(f"{R1}❌ Invalid token!{W1}")
            sys.exit()
    except:
        print(f"{R1}❌ Failed to validate token!{W1}")
        sys.exit()

# ========== Send Start Message ==========
def send_start_message(token, user_id):
    """Send message that hunting started"""
    try:
        start_msg = f"""🚀 SIFO Old Instagram Hunter Started!
═══════════════════════════
📅 Hunting accounts from: 2010-2018
🔍 Medium speed (3 checks/sec)
⏱️ Permanent Version - No Time Limit
⏱️ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
═══════════════════════════
✅ Results will be sent here when found"""
        
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = {'chat_id': user_id, 'text': start_msg}
        requests.post(url, data=data, timeout=5)
        print(f"{G1}✅ Start message sent!{W1}")
    except:
        print(f"{R1}❌ Failed to send start message!{W1}")

# ========== Generate Random Username ==========
def generate_random_username():
    """Generate completely random username"""
    length = random.randint(5, 8)
    chars = string.ascii_lowercase + string.digits
    username = ''.join(random.choices(chars, k=length))
    # Make sure it starts with a letter
    if username[0].isdigit():
        username = random.choice(string.ascii_lowercase) + username[1:]
    return username

# ========== Calculate Account Age ==========
def calculate_account_year(user_id):
    """Estimate account creation year from user ID"""
    try:
        uid = int(user_id)
        id_ranges = [
            (1000000, 5000000, 2010), (5000000, 15000000, 2011),
            (15000000, 50000000, 2012), (50000000, 150000000, 2013),
            (150000000, 300000000, 2014), (300000000, 500000000, 2015),
            (500000000, 800000000, 2016), (800000000, 1200000000, 2017),
            (1200000000, 1700000000, 2018)
        ]
        for min_id, max_id, year in id_ranges:
            if min_id <= uid <= max_id:
                return year
        return None
    except:
        return None

# ========== Check Instagram Account ==========
def check_instagram_account(username):
    """Check if Instagram account exists"""
    try:
        url = f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}"
        headers = {
            'user-agent': str(ua()),
            'x-ig-app-id': '936619743392459',
        }
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and 'user' in data['data']:
                return data['data']['user']
        return None
    except:
        return None

# ========== Send Result to Telegram ==========
def send_result_to_telegram(token, user_id, username, user_data):
    """Send found account info to Telegram"""
    global found_accounts
    
    try:
        user_id_num = user_data.get('id', 'Unknown')
        full_name = user_data.get('full_name', 'No name')
        followers = user_data.get('edge_followed_by', {}).get('count', 0)
        following = user_data.get('edge_follow', {}).get('count', 0)
        posts = user_data.get('edge_owner_to_timeline_media', {}).get('count', 0)
        is_private = user_data.get('is_private', False)
        account_year = calculate_account_year(user_id_num)
        
        found_accounts += 1
        
        msg = f"""
✅ OLD INSTAGRAM ACCOUNT FOUND!
═══════════════════════════
📧 Email: {username}@gmail.com
👤 Username: @{username}
🆔 User ID: {user_id_num}
📅 Created: {account_year if account_year else 'Unknown'}
👥 Followers: {followers:,}
👣 Following: {following:,}
📷 Posts: {posts}
🔒 Private: {'Yes' if is_private else 'No'}
📝 Name: {full_name}
🔗 Link: https://www.instagram.com/{username}
═══════════════════════════
#️⃣ Found: {found_accounts}
"""
        
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = {'chat_id': user_id, 'text': msg}
        requests.post(url, data=data, timeout=5)
        
        print(f"{G1}✅ Found: {username} ({account_year}){W1}")
    except:
        pass

# ========== Display Progress ==========
def display_progress():
    """Show progress every 2 seconds"""
    global checked_accounts, found_accounts, start_time
    elapsed = int(time.time() - start_time)
    rate = checked_accounts / elapsed if elapsed > 0 else 0
    sys.stdout.write(f"\r{C1}[•] Checked: {G1}{checked_accounts}{C1} | Found: {G1}{found_accounts}{C1} | Rate: {G1}{rate:.1f}/s{C1} | Time: {G1}{elapsed}s{C1}  {W1}")
    sys.stdout.flush()

# ========== Main Hunting Function ==========
def hunt_old_accounts(token, user_id):
    """Main hunting loop - medium speed"""
    global checked_accounts
    
    print(f"\n{G1}Starting hunt for old accounts (medium speed)...{W1}")
    print(f"{Y1}Press Ctrl+C to stop{W1}\n")
    
    last_progress_time = time.time()
    
    try:
        while True:
            username = generate_random_username()
            user_data = check_instagram_account(username)
            checked_accounts += 1
            
            if user_data:
                user_id_num = user_data.get('id', '0')
                account_year = calculate_account_year(user_id_num)
                if account_year and 2010 <= account_year <= 2018:
                    send_result_to_telegram(token, user_id, username, user_data)
            
            if time.time() - last_progress_time >= 2:
                display_progress()
                last_progress_time = time.time()
            
            time.sleep(0.33)  # ~3 checks per second
            
    except KeyboardInterrupt:
        print(f"\n\n{R1}Hunt stopped.{W1}")
        print(f"{G1}Final Results:{W1}")
        print(f"  Checked: {checked_accounts}")
        print(f"  Found: {found_accounts}")
        print(f"  Time: {int(time.time() - start_time)} seconds")

# ========== Main ==========
def main():
    global start_time
    start_time = time.time()
    
    # Get credentials
    token, user_id = get_credentials()
    
    # Send start message
    send_start_message(token, user_id)
    
    # Clear screen and show logo
    clear_screen()
    print_logo()
    
    # Start hunting
    hunt_old_accounts(token, user_id)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{R1}Interrupted.{W1}")
    except Exception as e:
        print(f"{R1}Error: {e}{W1}")