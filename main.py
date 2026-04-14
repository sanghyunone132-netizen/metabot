from datetime import datetime
import discord
from discord.ext import commands
import json
import random
import asyncio
import requests
import threading
import time
import os

# ========================
# KEEP ALIVE (Render 유지용)
# ========================
def keep_alive():
    url = "https://metabot-am7j.onrender.com"  # Render URL

    while True:
        try:
            requests.get(url)
            print("ping success")
        except:
            print("ping failed")

        time.sleep(300)

threading.Thread(target=keep_alive, daemon=True).start()

# ========================
# TOKEN
# ========================
TOKEN = os.getenv("TOKEN")

# ========================
# Discord 설정
# ========================
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ========================
# 운세 45개
# ========================
luck_list = [
    "오늘은 두리가 컨디션이 좋은 것 같아요! 인챈트를 시도해보세요!",
    "오늘은 두리가 컨디션이 안 좋은 것 같아요! 인챈트는 미루는 게 어떨까요?",
    "오늘은 로니가 컨디션이 좋은 것 같아요! 세이지 도구를 강화해보세요!",
    "오늘은 로니가 컨디션이 안 좋은 것 같아요! 강화는 미루는 게 좋겠어요!",
    "알바가 사고를 칠 것 같아요! 알바 고용은 신중하게 하는 게 좋겠어요!",
    "보스가 좋은 무기를 떨어뜨릴 것 같은 느낌이에요! 보스전에 도전해보세요!",
    "오늘따라 하늘이 파란색이네요! 블루캡슐에 도전해보는 건 어떨까요?",
    "신화 상자에 좋은 아이템이 들어있는 것 같아요! 열쇠가 있다면 열어보세요!",
    "도구 상태가 좋지 않아 보여요! 수리에 신경 쓰세요!",
    "오늘은 운이 없어 보여요! 확률성 뽑기는 하지 않는 게 좋을 것 같아요!",
    "오늘은 운이 좋아 보여요! 모든 일에 행운이 따를 거예요!",
    "오늘따라 깜빡하는 일이 생길 것 같아요! 스태미나 소모, 접속 보상 등 해야 할 일을 미루지 마세요!",
    "이번 주 마을에 납부할 등록금이 부족할 수 있어요! 골드를 아끼고 미리 모아두세요!",
    "현질을 생각 중이신가요? 오늘이 기회예요!",
    "누군가가 지켜보고 있어요! 서버 규칙을 준수하세요!",
    "채팅 실수를 할 수 있어요! 채팅 채널 전환에 신경 쓰세요!",
    "무심코 아이템을 버릴 수 있어요! 쓰레기통 사용에 주의하세요!",
    "오늘은 많이 맞을 것 같아요! 갑옷 내구도에 신경 쓰세요!",
    "마을원과 갈등이 생길 수 있어요! 싸움으로 번지지 않게 주의하세요!",
    "구할 수 있는 재료는 직접 구하세요! 뜻밖의 행운이 찾아올 수도 있어요!",
    "오늘은 물이 깨끗해 보여요! 오션 오더에 도전해보세요!",
    "판매할 아이템이 있나요? 오늘보다 내일 팔면 더 비싸게 팔 수 있을 것 같아요!",
    "구매하고 싶은 아이템이 있나요? 오늘보다 내일 사면 더 싸게 살 수 있을 것 같아요!",
    "RPG 장신구 강화에 도전해보세요! 행운이 따를 거예요!",
    "RPG 스킬 강화에 도전해보세요! 행운이 따를 거예요!",
    "마을원과의 협력이 큰 도움이 될 거예요! 힘을 합쳐보세요!",
    "오늘 시도할 인챈트가 있다면 마을원에게 맡겨보세요! 당신보다 운이 좋을 거예요!",
    "세이지 도구 강화를 시도한다면 누구에게도 말하지 마세요! 운이 날아가 버릴 거예요!",
    "오늘따라 배 상태가 좋아 보여요! 항해를 해보는 건 어떨까요?",
    "억울한 일이 생길 수 있어요! 중요한 일에는 증거나 기록을 남겨두세요!",
    "쓸데없는 아이템이라고 생각되어도 버리지 마세요! 꼭 필요할 거예요!",
    "지니가 기분이 좋은가 봐요! 램프 효과 부여에 도전해보세요!",
    "할까 말까 하는 일은 하세요! 안 하면 후회할 거예요!",
    "부업이 있다면 오늘은 부업에 집중하세요! 더 많은 골드를 벌 수 있을 거예요!",
    "크루시오 마을의 규칙을 준수하세요! 잘못하면 벌점이 부여될 수 있어요!",
    "계산 실수를 할 수 있어요! 계산할 때는 다시 한 번 확인하세요!",
    "다음 사람에게 운을 맡기세요! 다음 사람의 운세가 동일하게 적용될 거예요!",
    "공기가 좋아 보여요! 풍선에서 좋은 아이템이 나올 수 있어요!",
    "오늘 신화 상자는 열지 마세요! 그건 스킬 프리즘이에요!",
    "오늘은 각인을 시도해보세요! 오늘따라 잘 새겨질 것 같아요!",
    "오늘은 골드 사용을 최소한으로 하세요! 모아두면 좋잖아요!",
    "일일 제한이 있는 아이템은 미리 사 두세요! 나중에 부족할 거예요!",
    "현재 날짜가 31에 가까울수록 운이 좋을 거예요! 31일이면 초럭키!",
    "전체 채팅을 주시하세요! 재미있는 채팅이 오고 갈 거예요!",
    "희귀한 지형을 찾았다면 필요 없더라도 홈으로 설정해두세요! 나중에 찾게 될 거예요!"
]

# ========================
# 데이터 저장
# ========================
DATA_FILE = "luck_data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

last_luck = load_data()

# ========================
# 채널 제한
# ========================
allowed_channel_ids = [
    1488183193298407484,
    1493530735347368087
]

tax_check = set()
tax_active = False

# ========================
# 메시지 이벤트
# ========================
@bot.event
async def on_message(message):
    global tax_active

    if message.author.bot:
        return

    if message.channel.id not in allowed_channel_ids:
        return

    # 운세
    if message.content == "오늘의 운세":
        user_id = str(message.author.id)
        today = str(datetime.now().date())

        if user_id in last_luck and last_luck[user_id] == today:
            await message.channel.send(f"{message.author.mention} ❗ 오늘 이미 운세를 봤어요!")
            return

        last_luck[user_id] = today
        save_data(last_luck)

        await message.channel.send(
            f"{message.author.mention} 🎲 {random.choice(luck_list)}"
        )

    # 등록금 납부
    if message.content == "등록금 납부":
        if tax_active:
            tax_check.add(message.author.id)
            await message.add_reaction("✅")

    await bot.process_commands(message)

# ========================
# 채널 전송
# ========================
async def send_all_channels(text):
    for guild in bot.guilds:
        for channel in guild.text_channels:
            if channel.id in allowed_channel_ids:
                try:
                    await channel.send(text)
                except:
                    pass

# ========================
# 시간 스케줄러
# ========================
async def time_scheduler():
    global tax_active

    while True:
        now = datetime.now()
        hour = now.hour
        minute = now.minute
        day = now.day
        weekday = now.weekday()

        if hour == 11 and minute == 50:
            await send_all_channels("🎁 곧 접속 시간이 초기화됩니다! 접속 보상을 받는 걸 잊지 마세요!")

        if hour == 3 and minute == 0:
            await send_all_channels("💪 스태미나가 초기화되었습니다! 오늘도 파이팅!")

        if hour == 3 and minute == 0 and (day == 1 or day % 3 == 0):
            await send_all_channels("🍳 요리 시세가 변동되었습니다! 이번엔 어떤 요리가 좋을까요?")

        if weekday == 6 and hour == 0 and minute == 0:
            tax_active = True
            tax_check.clear()
            await send_all_channels(
                "💰 오늘은 크루시오 마을의 등록금 납부일이에요!\n등록금 납부 후, 이 메시지에 체크해주세요!"
            )

        await asyncio.sleep(30)

# ========================
# 실행
# ========================
@bot.event
async def on_ready():
    print("bot ready")
    asyncio.create_task(time_scheduler())

bot.run(TOKEN)
