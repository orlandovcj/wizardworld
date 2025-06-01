import logging
import time, requests
from datetime import datetime, timedelta

from telegram import Update, InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import MessageHandler, ApplicationBuilder, CallbackQueryHandler, ContextTypes, CommandHandler, InlineQueryHandler, filters

from csv import writer
from daltonapi.api import Atom

import json
import requests
import mysql.connector
import constants, responses, random, wizardworld

atom = Atom()
jokenpo_result=3

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Inicia o WizardBot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    usuario = "@" + update.message.from_user['username']
    user_name = str(usuario).lower()
    text = "📣 NEWS! All material templates are now stakable in Wizards World NFT Farm at WaxDao.\nStake it here: https://waxdao.io/farm/wizardsworld \n"
    text = text + "\n/HELP        /MISSION      /MYSTATS"
    await context.bot.send_message(chat_id=update.effective_chat.id,text=text, parse_mode="HTML")
    chat_id = update.effective_chat.id
    user_id = update.message.from_user['id']
    user_firstname = update.message.from_user['first_name']
    username = "@" + update.message.from_user['username']
    #print(chat_id)

# Envia mensagem para todos usuários
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #message = "🆕 Hello everyone!\n All material templates are now stakable in Wizards World NFT Farm at WaxDao.\nStake it here: https://waxdao.io/farm/wizardsworld"

    message = "📣Hello wizards!!! 📣\n"
    message = message+"I have some great news.\n"
    message = message+"As I've already mentioned here, the Wizards World NFT farm was created when I was developing the minigame so that the NFTs wouldn't just sit there uselessly in your wallet. With the normal functioning of the game, it became very annoying to have to stake and unstake NFTs from the farm.\n"
    message = message+"So I've made some changes that will make our experience easier and better:\n\n"

    message = message+"1. The Wizards Word NFT Farm has been closed. All stakers have been kicked, received their rewards and their NFTs returned to their wallets.\n\n"

    message = message+"2. All players will now receive rewards in SKART tokens daily in their in-game accounts at the end of their missions. In the case of players who have purple potions, the reward will be paid at the end of the mission that completes the 24-hour period.\n\n"

    message = message+"3. You can use the /mystats command to check your SKART token balance in the game. This balance does not mix with the balance you have in the Sketch Art Telegram group.\n\n"

    message = message+"4. You can use your SKART token balance to:\n"
    message = message+"a) Buy items directly in the Wizards World Bot  using the /buy command (use the /list command to see the available items).\n"
    message = message+"b) Transfer to your WAX wallet with the /withdraw command and use it to buy NFTs on NFTHive.\n"
    message = message+"c) Transfer it to your WAX wallet with the /withdraw command and stake it in the SKART-WAX Token Pool on WAXDAO and receive rewards in WAX. \n"
    message = message+"The remaining balance of the Wizards World NFT Farm was transferred to the SKART-WAX Token Pool to continue the rewards payments. Check it out here: https://waxdao.io/pool/skartwaxpool\n\n"

    message = message+"I hope everything goes well in this transition and if you find any bugs, please let me know.\n"
    message = message+"Have a great weekend! ❤️❤️"


    
    #conecta com o banco de dados MySQL
    connection = mysql.connector.connect(
        host="localhost",
        user="orlando",
        password="M@guila1969",
        database="wizardworld"
    )
    cursor = connection.cursor()
    sql = "SELECT chat_id FROM userinfo"
    cursor.execute(sql)
    chats = cursor.fetchall()
    # Fecha conexão com banco de dados
    cursor.close()
    connection.close()

    if len(chats)>0:
        await context.bot.send_message(chat_id="392483976",text= message, parse_mode="HTML")
        for chat in chats:
            try:
                #await context.bot.send_message(chat_id=chat,text= message, parse_mode="HTML")
                print("sent message to chat_id = ",chat,"  ",message)
            except Exception as e:
                print(f"Error: {e}")


# Mostra opções do Wizards World
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # print(update.effective_chat.id)
    help_text= "<b>WIZARDS WORLDS</b> \n<i>Help your wizard face incredible adventures and fulfill dangerous quests to become the greatest of all wizards.</i>\n"
    help_text=help_text+ "<i>You can send your wizard on daily missions and, if you manage to complete them, you receive items that can be useful for the next quests or in special blends that will help your wizard become more and more powerful</i>.\n"
    help_text=help_text+ "\n<b>How to Play</b> \n"

    help_text=help_text+ "1. Register your account and wax wallet with <b>/wax</b> <i>wallet.wam</i> command.\n"
    help_text=help_text+ "2. Read the details of your mission  with <b>/mission</b> command.\n"
    help_text=help_text+ "3. Attack the enemies by casting a spell against them with <b>/spell</b> command.\n"
    help_text=help_text+ "4. Discover secret passwords with the <b>/pass</b> command.\n"
    help_text=help_text+ "5. Use the <b>blue magic potion</b> to recover 50 magic powers from your wizard with <b>/useblue</b> command. Each blue potion gives you a 10% bonus point with every victory.\n"
    help_text=help_text+ "6. Use the <b>red magic potion</b> to reduce your enemy's 50 magic powers with <b>/usered</b> command. Each red potion increases the damage of your attacks by 10%.\n"
    help_text=help_text+ "7. Use the <b>yellow magic potion</b> to protect your wizard for 3 attacks with <b>/useyellow</b> command.\n"
    help_text=help_text+ "   <i>Each type of magic potion is limited to 10 and is recovered at the start of each mission.</i>.\n"
    help_text=help_text+ "8. Check your inventory and SKART token balance with <b>/mystats</b> command.\n"
    help_text=help_text+ "9. Check your in game SKART tokens balance and your daily reward with <b>/balance</b> command.\n"
    help_text=help_text+ "10. Send your SKART tokens to your Wax wallet with <b>/withdraw</b> <i>999999</i> (replace <i>999999</i> with the amount you wish to withdraw.\n"
    help_text=help_text+ "11. Check the Leaderboard with <b>/stats</b> command.\n"
    help_text=help_text+ "12. View the available NFT in the Wizard Store with <b>/list</b> \n"
    help_text=help_text+ "13. Use your SKART balance to buy items on the <i>Wizards Store</i> with <b>/buy</b> <i>999999</i> (replace 999999 with the template ID.\n"
    help_text=help_text+ "14. Once you finish all the missions you can use the /claim command to continue receiving your daily wizard rewards! 😉\n"
    help_text=help_text+ "\n🧙🏼 <b><i>Good Luck Wizard!!</i></b>"

    await context.bot.send_message(chat_id=update.effective_chat.id, text=help_text, parse_mode="HTML")
    help_text="\nYou can learn more about the Wizards World minigame on this guide:\nhttps://watercolor-sketch-art.gitbook.io/wizards-world/"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=help_text, parse_mode="HTML")


# Apenas repete a mensagem digitada. Esta função pode ser usada para responder perguntas
# que contenham palavras específicas
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:
        palavra = update.message.text
        if palavra == 'wizard':
            await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('teste.png', 'rb'))
    except Exception as e:
        error = e
        print("Echo ", f"Error: {e}")


# Converte a mensagem em texto maiúsculo
async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


# Registra a Wax Wallet to jogador
async def wax_wallet_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:
        chat_id = update.effective_chat.id
        user_id = update.message.from_user['id']
        txt = str(update.message.text).lower()
        usuario = "@" + update.message.from_user['username']

        status = wizardworld.mywax(usuario, txt)
        userinfo_update = wizardworld.my_userdata(user_id, chat_id)
        print(userinfo_update)
        #print(status)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=status, parse_mode="HTML")
        # await context.bot.reply.text(chat_id=update.effective_chat.id, text=status)
    except Exception as e:
        error = e
        print("Wax ", f"Error: {e}")

# THIS FUNCTION IS NOT IN USE.
async def magic_attack(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:
        txt = str(update.message.text).lower()
        usuario = "@" + update.message.from_user['username']
        #global minionKiller

        # if (update.effective_chat.id==(-1001568057335)) or (usuario=="@orlandovcj") :
        status = wizardworld.spell(usuario,txt)
        if status =="wizardlost":
            await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('teste.png', 'rb'))
            mensagem = "Hi "+usuario+"\n☠️ You don't have magic power. \nYour wizard was defeated after 10 rounds. It's better to get some rest and recover your powers before the next match!"
            await context.bot.send_message(chat_id=update.effective_chat.id, text=mensagem, parse_mode="HTML")
        elif status=="minionlost":
            await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('minion.png', 'rb'))
            mensagem = "⚔️ GAME OVER ⚔️ \nThe minion has been defeated!"
            await context.bot.send_message(chat_id=update.effective_chat.id, text=mensagem, parse_mode="HTML")
        elif status=="gameover":
            await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('wwlogo.jpg', 'rb'))
            mensagem = "<b>⚔️ TO BE CONTINUED... ⚔️</b> \nYou have managed to complete all the missions available so far. \nRelax a bit for now. Soon your wizard will be challenged again."
            await context.bot.send_message(chat_id=update.effective_chat.id, text=mensagem, parse_mode="HTML")
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=status, parse_mode="HTML")
        #else:
        #    await context.bot.send_message(chat_id=update.effective_chat.id, text="You must be in a group to use this command.")

    except Exception as e:
        error=e
        print("magic_attack ", f"Error: {e}")

# Starts the next round
async def next_round(update: Update, context: ContextTypes.DEFAULT_TYPE):
    txt = str(update.message.text).lower()
    usuario = "@" + update.message.from_user['username']
    #if (update.effective_chat.id==(-1001568057335)) or (usuario=="@orlandovcj") :
    status = wizardworld.nextround(usuario,txt)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=status, parse_mode="HTML")
    #else:
    #    await context.bot.send_message(chat_id=update.effective_chat.id, text="You must be in a group to use this command.", parse_mode="HTML")

# Uses the Blue Magic Potion.
async def use_bluepotion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    txt = str(update.message.text).lower()
    usuario = "@" + update.message.from_user['username']
    status = wizardworld.use_blue_potion(usuario,txt)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=status, parse_mode="HTML")

# Uses the Red Magic Potion.
async def use_redpotion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    txt = str(update.message.text).lower()
    usuario = "@" + update.message.from_user['username']
    status = wizardworld.use_red_potion(usuario,txt)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=status, parse_mode="HTML")

# Uses the Yellow Magic Potion.
async def use_yellowpotion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    txt = str(update.message.text).lower()
    usuario = "@" + update.message.from_user['username']
    status = wizardworld.use_yellow_potion(usuario,txt)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=status, parse_mode="HTML")

# Shows the stats for the WIZARD WORLDS.
async def show_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    txt = str(update.message.text).lower()
    usuario = "@" + update.message.from_user['username']
    status = wizardworld.leaderboard(usuario,txt)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=status, parse_mode="HTML")

# Shows the balance of ingame account
async def show_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    txt = str(update.message.text).lower()
    usuario = "@" + update.message.from_user['username']

    try:
        status = wizardworld.my_balance(usuario)
        await context.bot.send_message(chat_id=update.effective_chat.id, message_thread_id = update.message.message_thread_id, text=status, parse_mode="HTML")

        messageID = update.message.message_id
        #time.sleep(10)
        #await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=messageID)
        #await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=messageID+1)

    except Exception as e:
        error = e
        print("Balance ", f"Error: {e}")


# Shows the user stats for the WIZARDS WORLDS.
async def my_wizard_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    txt = str(update.message.text).lower()
    usuario = "@" + update.message.from_user['username']
    status = wizardworld.my_stats(usuario,txt)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=status, parse_mode="HTML")

# Claim reward when there is no new missions.
async def claim_reward(update: Update, context: ContextTypes.DEFAULT_TYPE):
    txt = str(update.message.text).lower()
    usuario = "@" + update.message.from_user['username']
    status = wizardworld.claim_daily_reward(usuario)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=status, parse_mode="HTML")

# Withdraw tokens to a Wax wallet.
async def withdraw_token(update: Update, context: ContextTypes.DEFAULT_TYPE):
    txt = str(update.message.text).lower()
    usuario = "@" + update.message.from_user['username']

    try:
        
        status = wizardworld.withdrawn_tokens(usuario, txt)

        await context.bot.send_message(chat_id=update.effective_chat.id, message_thread_id = update.message.message_thread_id, text=status, parse_mode="HTML")

        #messageID = update.message.message_id
        #time.sleep(10)
        #await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=messageID)
        #await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=messageID+1)

    except Exception as e:
        error = e
        print("withdraw ", f"Error: {e}")    

# Reset the WIZARDS WORLDS leaderboard for a new season.
async def reset_wizard_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    txt = str(update.message.text).lower()
    usuario = "@" + update.message.from_user['username']
    if usuario=="@orlandovcj":
        status = wizardworld.new_wizard_season(usuario,txt)
    else:
        status="🧙🏼‍ This command is for the Great Wizard Administrator only."
    await context.bot.send_message(chat_id=update.effective_chat.id, text=status, parse_mode="HTML")

# Send the WIZARDS WORLDS NFT Farm rewards.
async def payoff(update: Update, context: ContextTypes.DEFAULT_TYPE):
    txt = str(update.message.text).lower()
    usuario = "@" + update.message.from_user['username']
    if usuario=="@orlandovcj":
        status = wizardworld.payoff(usuario,txt)
    else:
        status="🧙🏼‍ This command is for the Great Wizard Administrator only."
    await context.bot.send_message(chat_id=update.effective_chat.id, text=status, parse_mode="HTML")

# Lista os NFT disponíveis para compra
async def list_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    txt = str(update.message.text).lower()
    usuario = "@" + update.message.from_user['username']

    try:
        status = wizardworld.list_NFT(usuario)
        await context.bot.send_message(chat_id=update.effective_chat.id, message_thread_id = update.message.message_thread_id, text=status, parse_mode="HTML")

        messageID = update.message.message_id
        #time.sleep(10)
        #await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=messageID)
        #await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=messageID+1)

    except Exception as e:
        error = e
        print("list ", f"Error: {e}")

# Compra NFT (o usuário deve usar o comando /buy <template_ID> e receberá seu NFT na wallet registrada)
async def buy_NFT_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    txt = str(update.message.text).lower()
    usuario = "@" + update.message.from_user['username']

    try:
        status = wizardworld.buy_NFT(usuario, txt)
        await context.bot.send_message(chat_id=update.effective_chat.id, message_thread_id = update.message.message_thread_id, text=status, parse_mode="HTML")

        #messageID = update.message.message_id
        #time.sleep(5)
        #await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=messageID)
        #await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=messageID+1)

    except Exception as e:
        error = e
        print("buy ", f"Error: {e}")

# Mission informations.
async def show_mission(update: Update, context: ContextTypes.DEFAULT_TYPE):
    txt = str(update.message.text).lower()
    usuario = "@" + update.message.from_user['username']
    status = wizardworld.mission(usuario)

    if status=="gameover":
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('wwlogo.jpg', 'rb'))
        mensagem = "<b>⚔️ TO BE CONTINUED... ⚔️</b> \nYou have managed to complete all the missions available so far. \nRelax a bit for now. Soon your wizard will be challenged again."
        await context.bot.send_message(chat_id=update.effective_chat.id, text=mensagem, parse_mode="HTML")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=status, parse_mode="HTML")

# Function for /spell command
async def play_jokenpo(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:
        usuario = "@" + update.message.from_user['username']
        user_name = str(usuario).lower()
        print(user_name)
        #conecta com o banco de dados MySQL
        connection = mysql.connector.connect(
            host="localhost",
            user="orlando",
            password="M@guila1969",
            database="wizardworld"
        )
        cursor = connection.cursor()

        sql = "SELECT * FROM battlefield WHERE username='"+user_name+"'"
        cursor.execute(sql)
        results = cursor.fetchall()
        # Fecha conexão com banco de dados
        cursor.close()
        connection.close()

        if len(results)>0:
            # Localiza o registro do usuário
            row = results[0]
            db_id, db_username, db_wallet, db_adventure, db_mission, db_level, db_round, db_magic, db_enemymp, db_bluepotions, db_redpotions, db_yellowpotions, db_purplepotions, db_invisible, db_updated, db_nextmission, db_password, db_skart, db_acum_skart, db_last_reward = row

            if db_nextmission>datetime.now():
                next_mission_time = db_nextmission - datetime.now()
                hours = int(next_mission_time.seconds/3600)
                minutes = int((next_mission_time.seconds/3600-hours)*60)
                
                mensagem = "Hello "+ user_name+"! Your wizard needs some rest. 😉\nThere are <b>"+str(hours)+" hours and "+str(minutes)+" minutes</b> remaining until next mission."
                await context.bot.send_message(chat_id=update.effective_chat.id, text=mensagem, parse_mode="HTML")

            else:

                password_levels = [17, 18, 19, 20, 23, 24, 25, 26, 27, 28, 30, 34]
                if db_adventure in password_levels:    
                    status = "In this mission you must use the /pass command. Check your /mission information."
                    # await context.bot.send_message(chat_id=update.effective_chat.id, message_thread_id = update.message.message_thread_id, text=status, parse_mode="HTML")
                    await context.bot.send_message(chat_id=update.effective_chat.id, text=status, parse_mode="HTML")
                    
                else:
                
                    if db_magic==0 and db_updated=="y":
                        mensagem = "Hi "+user_name+"\n☠️ Your wizard doesn't have magic power. \nUse /nextround command to restart this mission."
                        await context.bot.send_message(chat_id=update.effective_chat.id, text=mensagem, parse_mode="HTML")
                        

                    else:
                        #Sends a message with three inline buttons attached.
                        keyboard = [
                            [
                                InlineKeyboardButton("🪨 Rock", callback_data="1"),
                                InlineKeyboardButton("📃 Paper", callback_data="2"),
                                InlineKeyboardButton("✂️ Scissor", callback_data="3"),
                            ]
                        ]
                        reply_markup = InlineKeyboardMarkup(keyboard)

                        await update.message.reply_text("🧟 Your enemy is ready for battle!\nMake your choice or make a /deal with him.", reply_markup=reply_markup)

        else:
            mensagem = "Hi "+ user_name+"! Please, register your wax wallet with <b>/wax <i>wallet.wam</i></b> command (replace <i>wallet.wam</i> with your wax wallet)."
            await context.bot.send_message(chat_id=update.effective_chat.id, text=mensagem, parse_mode="HTML")
        # Fecha conexão com banco de dados
        #cursor.close()
        #connection.close()

    except Exception as e:
        error = e
        print("play ", f"Error: {e}")

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    usuario = "@" + update.callback_query.from_user['username']
    jokenpo_result=""
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()

    #Player's choices
    if query.data=="1":
        player_choice = "🪨 Rock"
    if query.data=="2":
        player_choice = "📃 Paper"
    if query.data=="3":
        player_choice = "✂️ Scissor"
    if query.data=="4":
        player_choice = "🕊 Make a deal"
    if query.data=="5":
        player_choice = "No deal"

    if player_choice == "🕊 Make a deal":
        print("Deal")
        result = "<b>🕊 You want to make a deal and pay your opponent 3.0 SKART tokens to avoid a fight.</b>"
        jokenpo_result = "4"
        player_choice = "🕊 Make a deal"

    elif player_choice == "No deal":
        print("No Deal")

        result = "<b>There was no deal. Let the fighting continue!</b>"
        jokenpo_result = "5"
        player_choice = "No deal"

    else:  
        # Enemy's choices
        enemy = list(range(1,4))
        # Embaralha a lista de números
        random.shuffle(enemy)

        if enemy[1]==1:
            enemy_choice = "🪨 Rock"
        elif enemy[1]==2:
            enemy_choice = "📃 Paper"
        elif enemy[1]==3:
            enemy_choice = "✂️ Scissor"

        # Possible results
        if enemy[1]==1 and query.data=="2":
            result = "<b>🥳 You won!</b>"
            jokenpo_result = "3"
        elif enemy[1]==1 and query.data=="3":
            result = "<b>🧟 Your enemy won!</b>"
            jokenpo_result = "1"
        elif enemy[1]==2 and query.data=="1":
            result = "<b>🧟 Your enemy won!</b>"
            jokenpo_result = "1"
        elif enemy[1]==2 and query.data=="3":
            result = "<b>🥳 You won!</b>"
            jokenpo_result = "3"
        elif enemy[1]==3 and query.data=="1":
            result = "<b>🥳 You won!</b>"
            jokenpo_result = "3"
        elif enemy[1]==3 and query.data=="2":
            result = "<b>🧟 Your enemy won!</b>"
            jokenpo_result = "1"
        else:
            result = "<b>⚖️ It's a draw!</b>"
            jokenpo_result = "2"

        result = result + "\nYour choice: "+player_choice+"\nSketchBot's choice: "+enemy_choice

    await query.edit_message_text(text=result, parse_mode="HTML")

    txt = str(jokenpo_result)
    if jokenpo_result=="5":
        status = "🧙🏼‍♂️ Use the /spell command to continue your mission. \nUse the /deal command to negotiate with your opponent (It costs 3 SKART)."
    else:
        status = wizardworld.fight(usuario, txt)

    if status=="gameover":
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('wwlogo.jpg', 'rb'))
        mensagem = "<b>⚔️ TO BE CONTINUED... ⚔️</b> \nYou have managed to complete all the missions available so far. \nRelax a bit for now. Soon your wizard will be challenged again."
        await context.bot.send_message(chat_id=update.effective_chat.id, text=mensagem, parse_mode="HTML")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=status, parse_mode="HTML")


async def deal(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with three inline buttons attached."""
    keyboard = [
        [
            InlineKeyboardButton("🟢 YES", callback_data="4"),
            InlineKeyboardButton("🔴 NO", callback_data="5"),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("🕊 Make a deal (costs 3 SKART).\nPlease confirm.", reply_markup=reply_markup)


async def button2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()

    await query.edit_message_text(text=f"🇧🇷 Selected option: {query.data}")

# Minigame Senha
async def play_password(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try: 
        txt = str(update.message.text).lower()
        usuario = "@" + update.message.from_user['username']

        #conecta com o banco de dados MySQL
        connection = mysql.connector.connect(
            host="localhost",
            user="orlando",
            password="M@guila1969",
            database="wizardworld"
        )
        cursor = connection.cursor()

        sql = "SELECT * FROM battlefield WHERE username='"+usuario+"'"
        cursor.execute(sql)
        results = cursor.fetchall()
        # Fecha conexão com banco de dados
        cursor.close()
        connection.close()

        if len(results)>0:
            # Localiza o registro do usuário
            row = results[0]
            db_id, db_username, db_wallet, db_adventure, db_mission, db_level, db_round, db_magic, db_enemymp, db_bluepotions, db_redpotions, db_yellowpotions, db_purplepotions, db_invisible, db_updated, db_nextmission, db_password, db_skart, db_acum_skart, db_next_reward = row
            if db_nextmission>datetime.now():
                next_mission_time = db_nextmission - datetime.now()
                hours = int(next_mission_time.seconds/3600)
                minutes = int((next_mission_time.seconds/3600-hours)*60)
                
                mensagem = "Hello "+ usuario+"! Your wizard needs some rest. 😉\nThere are <b>"+str(hours)+" hours and "+str(minutes)+" minutes</b> remaining until next mission."
                await context.bot.send_message(chat_id=update.effective_chat.id, text=mensagem, parse_mode="HTML")

            else:

                password_levels = [17, 18, 19, 20, 23, 24, 25, 26, 27, 28, 30, 34]
                if db_adventure in password_levels: 

                    if len(txt)==11:
                        command, tentativa = txt.split()
                        status = wizardworld.senha(db_username,tentativa)
                        if status=="gameover":
                            await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('wwlogo.jpg', 'rb'))
                            mensagem = "<b>⚔️ TO BE CONTINUED... ⚔️</b> \nYou have managed to complete all the missions available so far. \nRelax a bit for now. Soon your wizard will be challenged again."
                            await context.bot.send_message(chat_id=update.effective_chat.id, text=mensagem, parse_mode="HTML")
                        else:
                            await context.bot.send_message(chat_id=update.effective_chat.id, text=status, parse_mode="HTML")
                        
                    else:
                        status = "The password has <b>5 digits</b> (numbers 1 to 9). \nUse the <b>/pass <i>99999</i> </b>command (replace <i>99999</i> with your password attempt)."

                        await update.message.reply_text("🧙🏼‍♂️In this mission your wizard must guess the password that opens the secret chamber.\n<b>Try to guess the password:</b>\n #️⃣#️⃣#️⃣#️⃣#️⃣",parse_mode="HTML")
                        await context.bot.send_message(chat_id=update.effective_chat.id, text=status, parse_mode="HTML")
                else:
                    status = "In this mission you must use the /spell command. Check your /mission information."
                    # await context.bot.send_message(chat_id=update.effective_chat.id, message_thread_id = update.message.message_thread_id, text=status, parse_mode="HTML")
                    await context.bot.send_message(chat_id=update.effective_chat.id, text=status, parse_mode="HTML")
                
        else:
            mensagem = "Hi "+ usuario+"! Please, register your wax wallet with <b>/wax <i>wallet.wam</i></b> command (replace <i>wallet.wam</i> with your wax wallet)."
            await context.bot.send_message(chat_id=update.effective_chat.id, text=mensagem, parse_mode="HTML")
        
    except Exception as e:
        error = e
        print("Senha ", f"Error: {e}")
         
async def inline_caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    if not query:
        return
    results = []
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    await context.bot.answer_inline_query(update.inline_query.id, results)


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


# Gera mensagem de erro
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #print("Error Message")
    erro = " "
    if context.error!="Message text is empty":
        erro = "Mensagem sem texto"
        #print(erro, f" Caused error: {context.error}")
    elif contex.error == "Invalid input ConnectionInputs.SEND_HEADERS in state ConnectionState.CLOSED":
        erro = "No activity"         
        #print("Error Message")
        #print(erro, f" Caused error: {context.error}")
    else:
        print(f"Update: {update.message.text} caused error: {context.error}")



if __name__ == '__main__':
    const_Token = constants.API_KEY
    application = ApplicationBuilder().token(const_Token).build()

    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    # caps_handler = CommandHandler('caps', caps)
    inline_caps_handler = InlineQueryHandler(inline_caps)
    
    start_handler = CommandHandler('start', start)
    broadcast_handler = CommandHandler('broad', broadcast)
    help_handler = CommandHandler('help', help_command)
    #spell_handler = CommandHandler('spell',magic_attack)
    round_handler = CommandHandler('nextround',next_round)
    stats_handler = CommandHandler('stats',show_stats)
    balance_handler = CommandHandler('balance',show_balance)
    mystats_handler = CommandHandler('mystats',my_wizard_stats)
    claim_handler = CommandHandler('claim',claim_reward)
    withdraw_handler = CommandHandler('withdraw', withdraw_token)
    usebluepotion_handler = CommandHandler('useblue',use_bluepotion)
    useredpotion_handler = CommandHandler('usered',use_redpotion)
    useyellowpotion_handler = CommandHandler('useyellow',use_yellowpotion)
    my_mission_handler = CommandHandler('mission', show_mission)
    reset_handler = CommandHandler('resetgame', reset_wizard_game)
    payoff_handler = CommandHandler('payoff', payoff)
    #price_handler = CommandHandler('price', price_crypto_command)
    list_NFT_handler = CommandHandler('list',list_command)
    buy_NFT_handler = CommandHandler('buy',buy_NFT_command)
    play_handler = CommandHandler('spell',play_jokenpo)
    deal_handler = CommandHandler('deal',deal)
    play_pass_handler = CommandHandler('pass',play_password)
    button_handler = CallbackQueryHandler(button)
    button2_handler = CallbackQueryHandler(button2)
    wax_handler = MessageHandler(filters.TEXT, wax_wallet_command)

    application.add_handler(start_handler)
    application.add_handler(broadcast_handler)
    application.add_handler(help_handler)

    application.add_handler(echo_handler)
    #application.add_handler(caps_handler)
    #application.add_handler(spell_handler)
    application.add_handler(round_handler)
    application.add_handler(stats_handler)
    application.add_handler(balance_handler)
    application.add_handler(mystats_handler)
    application.add_handler(claim_handler)
    application.add_handler(withdraw_handler)
    application.add_handler(usebluepotion_handler)
    application.add_handler(useredpotion_handler)
    application.add_handler(useyellowpotion_handler)
    application.add_handler(my_mission_handler)
    application.add_handler(reset_handler)
    application.add_handler(payoff_handler)
    #application.add_handler(price_handler)
    application.add_handler(list_NFT_handler)
    application.add_handler(buy_NFT_handler)
    application.add_handler(play_handler)
    application.add_handler(deal_handler)
    application.add_handler(play_pass_handler)
    application.add_handler(button_handler)
    application.add_handler(button2_handler)
    application.add_handler(wax_handler)

    application.add_handler(inline_caps_handler)

    # Other handlers
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    application.add_handler(unknown_handler)
    application.add_error_handler(error)

    
    application.run_polling()
