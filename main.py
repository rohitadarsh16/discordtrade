import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
import time
import re
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()
driver.get("https://www.taptools.io/?Tokens=Recently+Added")
def get_token_liquidity():
    try:
        driver.refresh()
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//table/tbody/tr[1]/td[8]/div[1]")))
        tagname = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//table/tbody/tr[1]/td[1]")))
        driver.execute_script("window.scrollBy(0, 600);")
        driver.save_screenshot("screenshot.png")
        liquidity = element.text
        tagname=tagname.text
        liquidity = re.sub("[^0-9.]", "", liquidity)
        liquidity = float(re.sub("[^0-9.]", "", liquidity))
        return liquidity, tagname
    except:
        driver.get("https://www.taptools.io/?Tokens=Recently+Added")
        return 0,0

intents = discord.Intents.all()
intents.members = True
intents.messages = True
bot = commands.Bot(command_prefix='!', intents=intents)
@tasks.loop(seconds=10)
async def check_events():
    
    channel = bot.get_channel(1201987611661705237)
    liquidity, tagname = get_token_liquidity()
    if liquidity > 50000:
        messagedata = f"liquidity alert , is over 50,000   {tagname} @everyone"
        reminder_message = f"liquidity = {liquidity}@everyone"
        embed = discord.Embed(
            title=f"{messagedata} Reminder",
            description=reminder_message,
            color=discord.Color.green()
        )
        file = discord.File("screenshot.png", filename="image.png")
        embed.add_field(name='Reminder', value=f'liquidity is   {liquidity} ', inline=False)
        await channel.send(embed=embed, file=file)
    
            


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    check_events.start()


bot.run('MTIwMTYwMzc0NTgwNTUxNjk1MA.Gop5w2.illf9OYPlgGRljqdlAmO4jf4cgrqrYuoTWNgN0')
