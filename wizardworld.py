import mysql.connector
from datetime import datetime, timedelta
import time
import pyntelope
from csv import writer
from daltonapi.api import Atom
from waxNFTdispatcher import AssetSender
import csv, random, requests, constants

atom = Atom()

isMinionAlive = True
minionKiller = ""
start = datetime.now()
timebetweenmissions = timedelta(hours=24)
timebetweenrewards = timedelta(hours=24)
aventuras_disponiveis = 36


# Inclui ou atualiza a wax wallet do player na base de dados
def mywax(name, wallet):
    user_name = str(name).lower()
    if wallet=="/wax" or wallet=="/wax@wizardsworldsbot":
        return "Hi "+user_name+" ! You can register your wax wallet with <b>/wax <i>wallet.wam</i></b> command (replace <i>wallet.wam</i> with your wax wallet)."
    else:
        command, user_wallet = wallet.split()

    #user_wallet = str(wallet[5:20]).lower()
    #user_name = str(name).lower()

    if command in ("wax", "/wax", "\wax"):

        if (len(user_wallet)==0) or (user_wallet=="wizardsworldsbot"):
            return "Hi "+user_name+" ! You can register your wax wallet with <b>/wax <i>wallet.wam</i></b> command (replace <i>wallet.wam</i> with your wax wallet)."

        my_blue_potions=0
        my_red_potions=0
        my_yellow_potions=0
        my_purple_potions=0
        my_wooden_keys=0
        my_iron_keys=0
        my_bronze_keys=0
        my_pickaxes=0
        my_wizards=0

        # Verifica quantas poções o jogador possui.
        #url = f"https://wax.api.atomicassets.io/atomicassets/v1/accounts/{user_wallet}/brsketchart1"
        #url = f"https://atomic.hivebp.io/atomicassets/v1/accounts/{user_wallet}/brsketchart1"
        url = f"https://wax.eosusa.io/atomicassets/v1/accounts/{user_wallet}/brsketchart1"

        # Send a GET request to the API endpoint
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()

        # Extract template_id and assets from the parsed data
        templates = data['data']['templates']
        for template in templates:
            template_id = template['template_id']
            assets = template['assets']

            #print("Template ID:", template_id)
            #print("Assets Count:", assets)

            if template_id=="665364":
                my_blue_potions=int(assets)
            elif template_id=="665365":
                my_red_potions=int(assets)
            elif template_id=="665366":
                my_yellow_potions=int(assets)
            elif template_id=="746407":
                my_purple_potions=int(assets)
            # Verifica de possui uma Wooden Magic Key
            elif template_id=="735319":
                my_wooden_keys=int(assets)
            # Verifica de possui uma Iron Magic Key
            elif template_id=="739075":
                my_iron_keys=int(assets)
            # Verifica de possui uma Bronze Magic Key
            elif template_id=="770360":
                my_bronze_keys=int(assets)
            # Verifica de possui uma Pickaxe
            elif template_id=="746673":
                my_pickaxes=int(assets)
            # Verifica se existem wizards na conta
            elif template_id=="761405" or template_id=="649929" or template_id=="649930" or template_id=="660835" or template_id=="660839" or template_id=="685511" or template_id=="750119" or template_id=="777207" or template_id=="781527":
                my_wizards=my_wizards+1

        # Max usable potions = 10
        if my_blue_potions>10:
            my_blue_potions=10

        if my_red_potions>10:
            my_red_potions=10

        if my_yellow_potions>10:
            my_yellow_potions=10

        if my_purple_potions>12:
            my_purple_potions=12


        # VERIFICA REQUISITOS
        # Tem um wizard
        if my_wizards==0:
            return "Hi "+user_name+" ! You don't seem to have a wizard to join the game.\nYou can get a wizard here: https://waxdao.io/collection/brsketchart1"

        max_wizard_MP = inventory(user_name, user_wallet)

        #conecta com o banco de dados MySQL
        connection = mysql.connector.connect(
            host="host",
            user="user",
            password=constants.DBACCESS,
            database="wizardworld"
        )

        cursor = connection.cursor()

        sql = "SELECT * FROM battlefield WHERE username='"+user_name+"'"
        cursor.execute(sql)
        results = cursor.fetchall()

        if len(results)>0:
            # Localiza o registro do usuário
            sql = "SELECT * FROM battlefield WHERE username='"+user_name+"'"
            cursor.execute(sql)
            results = cursor.fetchall()
            row = results[0]

            db_id, db_username, db_wallet, db_adventure, db_mission, db_level, db_round, db_magic, db_enemymp, db_bluepotions, db_redpotions, db_yellowpotions, db_purplepotions, db_invisible, db_updated, db_nextmission, db_password, db_skart, db_acum_skart, db_last_reward = row

            #verifica se possui uma wooden magic key (necessario para a aventura 2)
            if db_adventure==2:
                if my_wooden_keys==0:
                    return "🗝Hold on wizard!!\nIf you've made it this far, you already have the ingredients to make your <b>Magic Wooden Key</b>. It's needed for you to go on to the next adventure.\nBlend your <i>Wooden Magic Key</i> here:\n https://neftyblocks.com/collection/brsketchart1/blends/blend.nefty/30315 "
            #verifica se possui uma iron magic key (necessario para a aventura 3)
            if db_adventure==3:
                if my_iron_keys==0:
                    return "🗝Hold on wizard!!\nIf you've made it this far, you already have the ingredients to make your <b>Iron Magic Key</b>. It's needed for you to go on to the next adventure.\nBlend your <i>Iron Magic Key</i> here:\n https://neftyblocks.com/collection/brsketchart1/blends/blend.nefty/30549 "
            #verifica se possui uma iron pickaxe (necessario para a aventura 6)
            if db_adventure==6:
                if my_pickaxes==0:
                    return "⛏Hold on wizard!!\nIf you've made it this far, you already have the ingredients to make your <b>Iron Pickaxe</b>. It's needed for you to go on to the next adventure.\nBlend your <i>Iron Pickaxe</i> here:\n https://neftyblocks.com/collection/brsketchart1/blends/blend.nefty/31148 "
            #verifica se possui uma bronze magic key (necessario para a aventura 15)
            if db_adventure==15:
                if my_bronze_keys==0:
                    return "⛏Hold on wizard!!\nIf you've made it this far, you already have the ingredients to make your <b>Magic Bronze Key</b>. It's needed for you to open the Temple of the Elements door and go on to the next adventure.\nBlend your <i>Magic Bronze Key</i> here:\n https://neftyblocks.com/collection/brsketchart1/blends/blend.nefty/33123 "



            if db_updated=="y":
                return "Hi "+user_name+" ! You cannot synchronize again during a mission. Wait for the end of this mission and try again!"

            if db_wallet != user_wallet:
                return "Hi "+user_name+" ! You already have a different wax wallet in use! Please, contact the admin if you need to change you wallet."

            else:
                sql = "UPDATE battlefield SET username = %s, wallet = %s, adventure = %s, mission = %s, level = %s, round = %s, magic = %s, enemymp = %s, bluepotions = %s, redpotions = %s, yellowpotions = %s, purplepotions = %s, invisible = %s, updated = %s, nextmission = %s, password = %s, skart = %s, acum_skart = %s, last_reward = %s WHERE id = %s"
                data = (db_username, db_wallet,  db_adventure, db_mission, db_level, db_round, max_wizard_MP, db_enemymp, my_blue_potions, my_red_potions, my_yellow_potions, my_purple_potions, db_invisible, "y", db_nextmission, db_password, db_skart, db_acum_skart, db_last_reward, db_id)
                cursor.execute(sql, data)
                connection.commit()
                recordsaffected = cursor.rowcount

            # Fecha conexão com banco de dados
            cursor.close()
            connection.close()


        else:

            sql = "INSERT INTO battlefield (username, wallet, adventure, mission, level, round, magic, enemymp, bluepotions, redpotions, yellowpotions, purplepotions, invisible, updated, nextmission, password, skart, acum_skart, last_reward) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            data = (user_name, user_wallet, 1, 1, 1, 1, max_wizard_MP, 1000, my_blue_potions, my_red_potions, my_yellow_potions,my_purple_potions, 0,"y", start, create_password(),0,0, (datetime.now()+timebetweenrewards))
            cursor.execute(sql, data)
            connection.commit()
            cursor.close()
            connection.close()

        return "Hi "+user_name+" ! Your wax wallet "+user_wallet+" has been successfully updated and synced!"

# Lança feitiço e soma (ou reduz) os pontos
def fight(name,jokenpo):
    #command, jokepo_points = jokenpo.split()
    user_name = str(name).lower()
    jokenpo_result = int(jokenpo)

    global isMinionAlive
    global minionKiller

    if (isMinionAlive==False):
        return "minionlost"
        # return "⚔️ GAME OVER ⚔️ \nAll hail the great wizard "+minionKiller+" who defeated the minion!"


    #conecta com o banco de dados MySQL
    connection = mysql.connector.connect(
        host="host",
        user="user",
        password=constants.DBACCESS,
        database="wizardworld"
    )

    cursor = connection.cursor()

    sql = "SELECT * FROM battlefield WHERE username='"+user_name+"'"
    cursor.execute(sql)
    results = cursor.fetchall()

    if len(results)>0:
        # Localiza o registro do usuário

        row = results[0]
        #print(row)
        #print(points)
        db_id, db_username, db_wallet, db_adventure, db_mission, db_level, db_round, db_magic, db_enemymp, db_bluepotions, db_redpotions, db_yellowpotions, db_purplepotions, db_invisible, db_updated, db_nextmission, db_password, db_skart, db_acum_skart, db_last_reward = row

        if db_nextmission>datetime.now():
            next_mission_time = db_nextmission - datetime.now()
            return "Hello "+ user_name+"! Your wizard need some rest. 😉\nThere are <b>"+str(round(next_mission_time.seconds/3600,2))+" hours</b> remaining until next mission."

        # Check the number of available adventures
        if db_adventure>aventuras_disponiveis:
            return "gameover"
            # return "⚔️ TO BE CONTINUED... ⚔️' because there are not more levels.

        # Verifica quantas Poções Mágicas e itens obrigatórios o jogador possui.
        if db_updated=="n":
            my_blue_potions=0
            my_red_potions=0
            my_yellow_potions=0
            my_purple_potions=0
            my_wooden_keys=0
            my_iron_keys=0
            my_bronze_keys=0
            my_pickaxes=0
            my_wizards=0

            # Verifica quantas poções o jogador possui.
            #url = f"https://wax.api.atomicassets.io/atomicassets/v1/accounts/{db_wallet}/brsketchart1"
            #url = f"https://atomic.hivebp.io/atomicassets/v1/accounts/{db_wallet}/brsketchart1"
            url = f"https://wax.eosusa.io/atomicassets/v1/accounts/{db_wallet}/brsketchart1"


            # Send a GET request to the API endpoint
            response = requests.get(url)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                data = response.json()

            # Extract template_id and assets from the parsed data
            templates = data['data']['templates']

            for template in templates:
                template_id = template['template_id']
                assets = template['assets']

                #print("Template ID:", template_id)
                #print("Assets Count:", assets)

                if template_id=="665364":
                    my_blue_potions=int(assets)
                elif template_id=="665365":
                    my_red_potions=int(assets)
                elif template_id=="665366":
                    my_yellow_potions=int(assets)
                elif  template_id=="746407":
                    my_purple_potions=int(assets)
                # VERIFICA REQUISITOS
                #verifica se possui uma wooden magic key (necessario para a aventura 2)
                elif template_id=="735319":
                    my_wooden_keys=int(assets)
                # Verifica de possui uma Iron Magic Key
                elif template_id=="739075":
                    my_iron_keys=int(assets)
                # Verifica de possui uma Bronze Magic Key
                elif template_id=="770360":
                    my_bronze_keys=int(assets)
                # Verifica de possui uma Pickaxe
                elif template_id=="746673":
                    my_pickaxes=int(assets)
                # Verifica se existem wizards na conta
                elif template_id == "761405" or template_id=="649929" or template_id=="649930" or template_id=="660835" or template_id=="660839" or template_id=="685511" or template_id=="750119" or template_id=="777207" or template_id=="781527":
                    my_wizards=my_wizards+1


            # Max usable potions = 10
            if my_blue_potions>10:
                my_blue_potions=10

            if my_red_potions>10:
                my_red_potions=10

            if my_yellow_potions>10:
                my_yellow_potions=10

            if my_purple_potions>12:
                my_purple_potions=12


            # VERIFICA SE OS PRE-REQUISITOS PARAS AS AVENTURAS ESTÃO PRESENTES
            # Tem um wizard
            if my_wizards==0:
                return "Hi "+user_name+" ! You don't seem to have a wizard to join the game.\nYou can get a wizard here: https://waxdao.io/collection/brsketchart1"
            #verifica se possui uma wooden magic key (necessario para a aventura 2)
            if db_adventure==2:
                if my_wooden_keys==0:
                    return "🗝Hold on wizard!!\nIf you've made it this far, you already have the ingredients to make your <b>Magic Wooden Key</b>. It's needed for you to go on to the next adventure.\nBlend your <i>Wooden Magic Key</i> here:\n https://neftyblocks.com/collection/brsketchart1/blends/blend.nefty/30315 "
            #verifica se possui uma iron magic key (necessario para a aventura 3)
            if db_adventure==3:
                if my_iron_keys==0:
                    return "🗝Hold on wizard!!\nIf you've made it this far, you already have the ingredients to make your <b>Iron Magic Key</b>. It's needed for you to go on to the next adventure.\nBlend your <i>Iron Magic Key</i> here:\n https://neftyblocks.com/collection/brsketchart1/blends/blend.nefty/30549 "
            #verifica se possui uma iron pickaxe (necessario para a aventura 6)
            if db_adventure==6:
                if my_pickaxes==0:
                    return "⛏Hold on wizard!!\nIf you've made it this far, you already have the ingredients to make your <b>Iron Pickaxe</b>. It's needed for you to go on to the next adventure.\nBlend your <i>Iron Pickaxe</i> here:\n https://neftyblocks.com/collection/brsketchart1/blends/blend.nefty/31148 "
            #verifica se possui uma bronze magic key (necessario para a aventura 15)
            if db_adventure==15:
                if my_bronze_keys==0:
                    return "⛏Hold on wizard!!\nIf you've made it this far, you already have the ingredients to make your <b>Magic Bronze Key</b>. It's needed for you to open the Temple of the Elements door and go on to the next adventure.\nBlend your <i>Magic Bronze Key</i> here:\n https://neftyblocks.com/collection/brsketchart1/blends/blend.nefty/33123 "


            db_magic = inventory(db_username, db_wallet)

            db_updated="y"

            sql = "UPDATE battlefield SET username = %s, wallet = %s, adventure = %s, mission = %s, level = %s, round = %s, magic = %s, enemymp = %s, bluepotions = %s, redpotions = %s, yellowpotions = %s, purplepotions = %s, invisible = %s, updated = %s, nextmission = %s, password = %s, skart = %s, acum_skart = %s, last_reward = %s WHERE id = %s"
            data = (db_username, db_wallet, db_adventure, db_mission, db_level, db_round, db_magic, db_enemymp, my_blue_potions, my_red_potions, my_yellow_potions, my_purple_potions, db_invisible, "y", db_nextmission, db_password, db_skart, db_acum_skart, db_last_reward, db_id)
            cursor.execute(sql, data)
            connection.commit()
            recordsaffected = cursor.rowcount

        else:
            my_blue_potions = db_bluepotions
            my_red_potions = db_redpotions
            my_yellow_potions = db_yellowpotions
            my_purple_potions = db_purplepotions

        if my_blue_potions>10:
            my_blue_potions=10

        if my_red_potions>10:
            my_red_potions=10

        if my_yellow_potions>10:
            my_yellow_potions=10

        if my_purple_potions>12:
            my_purple_potions=12

        extrapower = my_red_potions*10


        if db_magic==0:
            # Fim de jogo porque atingiu 10 rounds
            if db_round==10:
                return "wizardlost"
                # return "Hi "+user_name+"\n☠️ You don't have magic power. \nYour wizard was defeated after 10 rounds. It's better to get some rest and recover your powers before the next match!"
            sql = "UPDATE battlefield SET username = %s, wallet = %s, adventure = %s, mission = %s, level = %s, round = %s, magic = %s, enemymp = %s, bluepotions = %s, redpotions = %s, yellowpotions = %s, purplepotions = %s, invisible = %s, updated = %s, nextmission = %s, password = %s, skart = %s, acum_skart = %s, last_reward = %s WHERE id = %s"
            data = (db_username, db_wallet, db_adventure, db_mission, db_level, db_round, db_magic, db_enemymp, my_blue_potions, my_red_potions, my_yellow_potions, my_purple_potions, db_invisible, db_updated, db_nextmission, db_password, db_skart, db_acum_skart, db_last_reward, db_id)
            cursor.execute(sql, data)
            connection.commit()
            recordsaffected = cursor.rowcount
            # Fecha conexão com banco de dados
            cursor.close()
            connection.close()
            return "Hi "+user_name+"\n☠️ Your wizard doesn't have magic power. \nUse /nextround command to start the round "+str(db_round+1)+"."


        if jokenpo_result==1:   # The minion hits you
            if db_invisible>0:
                db_invisible=db_invisible-1
                points = 0
                enemy_points=0
                registro = user_name +", The enemy was unable to attack because you used a 🟡yellow magic potion to protect your wizard.\nYou're safe for the next "+str(db_invisible)+" attacks."
            else:
                points = int(SwitchPoints(jokenpo_result))
                enemy_points=10
                registro = user_name +", "+ SwitchDados(jokenpo_result)

        if jokenpo_result==2: # You defended the minion attack
            points=0
            enemy_points=0
            if db_invisible>0:
                registro = user_name +", "+ SwitchDados(jokenpo_result)+"\nThe enemy cannot attack you for "+str(db_invisible)+" turns."
            else:
                registro = user_name +", "+ SwitchDados(jokenpo_result)

        if jokenpo_result==3:   # You have hit the minion
            # Quanto maior o MP do jogador maior o dano causado no inimigo.
            enemy_points = (int(SwitchPoints(jokenpo_result))+(db_magic/10))*(-1)    # minion perde 20 pontos + 10% dos MP do Wizard
            points = 20
            if db_invisible>0:
                registro = user_name +", "+ SwitchDados(jokenpo_result)+"\nThe enemy cannot attack you for "+str(db_invisible)+" turns."
            else:
                registro = user_name +", "+ SwitchDados(jokenpo_result)

        if jokenpo_result==4:   # You made a buy offer to the minion
            # O jogador decidiu fazer uma oferta ao minion pelo item que ele carrega.
            if db_skart>=float(3):
                db_enemymp=0   # Não haverá luta
                enemy_points=0
                points=0
                db_skart=float(db_skart)-float(3)
                registro = user_name +", "+ SwitchDados(jokenpo_result)
            else:
                registro = user_name +", You don't have enough SKART to make a deal with your enemy."
                # Fecha conexão com banco de dados
                cursor.close()
                connection.close()
                return registro


        # Incuir aqui uma ação para que uma poção ou extra power aumentem o poder do wizard
        if points>0:
            magicpotion = (db_bluepotions+db_redpotions+db_yellowpotions+db_purplepotions)*10
            total_points = int(db_magic+points+points*(magicpotion/100))
            registro = registro + "\n<b>Potions Bonus Points</b> = "+str(int(points*(magicpotion/100)))+ " MP."
            registro = registro + "\nYou've earned " +str(int(points+points*(magicpotion/100)))+ " MP."
        else:
            total_points = int(db_magic+points)

        if enemy_points<0:
            total_enemy_MP=int(db_enemymp+(enemy_points+enemy_points*(extrapower)/100))
            registro = registro + " The enemy has lost " +str(int((enemy_points+enemy_points*(extrapower)/100)*(-1)))+ " MP."
        elif enemy_points==0:
            total_enemy_MP=db_enemymp+enemy_points
        else:
            total_enemy_MP=db_enemymp+enemy_points
            registro = registro + " The enemy received "+str(enemy_points)+" MP."

        level = db_level

        # Evita pontuação negativa
        if total_points<=0:
            total_points=0

        # Passa para o próximo nível
        if total_enemy_MP<=0:

            print("********************* \n Sending rewards to :",db_username)
            # Envia o prêmio correspondente ao nível
            imagem_NFT = send_NFT(db_wallet, db_level)

            # Envia o SKART reward para a conta do jogador no jogo
            db_last_reward = datetime.now()
            player_reward = float(getRewardPlayer(db_username, db_wallet))
            db_skart = float(db_skart)+float(player_reward)
            db_acum_skart = float(db_acum_skart) + float(player_reward)

            if (db_level/db_adventure)==10:
                db_adventure=db_adventure+1
                registro = "🎉Congratulations, " +user_name +"!! You have finished this adventure! \nThis victory took you to the next level! \nBut beware! Your next adventure might not be so easy!\n"
            else:
                if jokenpo_result==4:   # You made a buy offer to the minion
                    registro = "🎉Congratulations, " +user_name +"!! You made a deal and paid your opponent 3.0 SKART to avoid a fight.\nThis deal took you to the next level! \nBut beware! Your next enemy is also stronger!\n"
                else:
                    registro = "🎉Congratulations, " +user_name +"!! You have defeated the enemy! \nThis victory took you to the next level! \nBut beware! Your next enemy is also stronger!\n"

            level=db_level+1
            db_level=level
            db_mission=db_mission+1
            total_enemy_MP=1000 + (level*100)
            db_round=1
            db_invisible=0
            db_updated="n"
            total_points=db_magic
            db_bluepotions=getCount("665364",db_wallet)
            db_redpotions=getCount("665365",db_wallet)
            db_yellowpotions=getCount("665366",db_wallet)
            db_purplepotions=getCount("746407",db_wallet)
            if db_purplepotions>12:
                db_purplepotions=12
            my_blue_potions=db_bluepotions
            my_red_potions=db_redpotions
            my_yellow_potions=db_yellowpotions
            my_purple_potions=db_purplepotions
            db_nextmission = datetime.now()+timebetweenmissions-timedelta(hours=db_purplepotions)

            # Max usable potions = 10
            if my_blue_potions>10:
                my_blue_potions=10

            if my_red_potions>10:
                my_red_potions=10

            if my_yellow_potions>10:
                my_yellow_potions=10

            if my_purple_potions>12:
                my_purple_potions=12

            #isMinionAlive=False
            #minionKiller=user_name

            registro = registro + "Your enemy dropped an item that was sent to your wallet. It will be useful in your next missions. Use it wisely."
            registro = registro + "\nTo see your next mission use the /mission command.\n"
            registro = registro + "🧙🏼‍ Your MP = "+str(total_points)+"      🧟 Enemy MP = "+ str(total_enemy_MP)
            registro = registro + "\n🎨 SKART this mission = "+str(round(player_reward,4))+"\n🎨 SKART balance = "+str(round(db_skart,4))+"   \n🎨 SKART earned so far = "+ str(round(db_acum_skart,4))
            registro = registro + "\n⭐️ Next Level = "+str(level)
            registro = registro + "\n"+imagem_NFT

        else:
            #registro = registro + "\n🧙🏼‍ You= "+str(total_points)+"  🧟 Enemy= "+ str(total_enemy_MP) +"\nMagic Potions:  🔵 = "+ str(my_blue_potions)+"  🔴 = "+ str(my_red_potions)+"  🟡 = "+str(db_yellowpotions)
            registro = registro + "\n✅ Level = "+str(level)+"      ⚔️ Round = "+ str(db_round)
            registro = registro +"\n<b>Magic Power</b>\n🧙🏼 You = "+str(total_points) + " 🧟 Enemy= "+str(total_enemy_MP)
            registro = registro +"\n<b>Magic Potions</b>\n🔵 = "+str(my_blue_potions)+" 🔴 = "+str(my_red_potions)+ " 🟡 = "+str(my_yellow_potions) + " 🟣 = "+str(my_purple_potions)
            registro = registro + "\n🎨 SKART = "+str(round(db_skart,4))+"   \n🎨 SKART earned so far = "+ str(round(db_acum_skart,4))

        sql = "UPDATE battlefield SET username = %s, wallet = %s, adventure = %s, mission = %s, level = %s, round = %s, magic = %s, enemymp = %s, bluepotions = %s, redpotions = %s, yellowpotions = %s, purplepotions = %s, invisible=%s, updated = %s, nextmission = %s, password = %s, skart = %s, acum_skart = %s, last_reward = %s WHERE id = %s"
        data = (db_username, db_wallet, db_adventure, db_mission, db_level, db_round, total_points, total_enemy_MP, my_blue_potions, my_red_potions, my_yellow_potions, my_purple_potions, db_invisible, db_updated, db_nextmission, db_password, db_skart, db_acum_skart, db_last_reward, db_id)

        cursor.execute(sql, data)
        connection.commit()
        recordsaffected = cursor.rowcount

        # Fecha conexão com banco de dados
        cursor.close()
        connection.close()

    else:
        return "Hi "+ user_name+"! Please, register your wax wallet with <b>/wax <i>wallet.wam</i></b> command (replace <i>wallet.wam</i> with your wax wallet)."

    return registro

# Switch-Case para a pontuação
def SwitchDados(argument):
    switcher = {
        1: " ☠️ The enemy hit you. You lost 20 magic point.",
        2: " 🛡 You defended the enemy's attack.",
        3: " 💥 Great! You have hit the enemy. You received 20 magic points and got stronger!",
        4: " 🕊 You made a deal and paid your opponent some SKART tokens to avoid a fight."
    }
    return switcher.get(argument, "You missed the enemy!")

# Tabela de pontos
def SwitchPoints(argument):
    switcher = {
        1: "-20",
        2: "0",
        3: "20",
        4: "0"
    }
    return switcher.get(argument, "0")

# Inicia próximo round
def nextround(name, wallet):
    user_wallet = str(wallet[5:20]).lower()
    user_name = str(name).lower()

    #conecta com o banco de dados MySQL
    connection = mysql.connector.connect(
        host="host",
        user="user",
        password=constants.DBACCESS,
        database="wizardworld"
    )
    cursor = connection.cursor()

    sql = "SELECT * FROM battlefield WHERE username='"+user_name+"'"
    cursor.execute(sql)
    results = cursor.fetchall()

    if len(results)>0:
        # Localiza o registro do usuário
        row = results[0]
        db_id, db_username, db_wallet, db_adventure, db_mission, db_level, db_round, db_magic, db_enemymp, db_bluepotions, db_redpotions, db_yellowpotions, db_purplepotions, db_invisible, db_updated, db_nextmission, db_password, db_skart, db_acum_skart, db_last_reward = row
        timebetweenmissions= timedelta(hours=24)-timedelta(hours=db_purplepotions)
        if db_magic==0:
            db_round = db_round + 1

            if db_round>10 and db_updated=="n":
                db_nextmission = datetime.now()+timebetweenmissions
                #db_round=1
                next_mission_time = db_nextmission - datetime.now()
                db_updated = "y"
                message = "Hold on Wizard! You have already played your 10 rounds! \n<b>Your wizard needs some rest.</b> 😉\nThere are <b>"+str(round(next_mission_time.seconds/3600,2))+" hours</b> remaining until next mission."
            else:
                db_updated="n"
                db_round=1
                message = "Hi "+user_name+"\n⚔️ You have recovered your magic power. \nLet's restart the round "+str(db_round)+". Use /spell command."

            sql = "UPDATE battlefield SET username = %s, wallet = %s, adventure = %s, mission = %s, level = %s, round = %s, magic = %s, enemymp = %s, bluepotions = %s, redpotions = %s, yellowpotions = %s, purplepotions = %s, invisible=%s, updated = %s, nextmission = %s, password = %s, skart = %s, acum_skart = %s, last_reward = %s WHERE id = %s"
            data = (db_username, db_wallet, db_adventure, db_mission, db_level, db_round, db_magic, db_enemymp, db_bluepotions, db_redpotions,db_yellowpotions, db_purplepotions, db_invisible, db_updated, db_nextmission, db_password, db_skart, db_acum_skart, db_last_reward, db_id)
            cursor.execute(sql, data)
            connection.commit()
            recordsaffected = cursor.rowcount
            # Fecha conexão com banco de dados
            cursor.close()
            connection.close()

        else:

            message = "Hold on Wizard! Finish the current round first. 😉"

    else:
        message = "Hi "+ user_name+"! Please, register your wax wallet with <b>/wax <i>wallet.wam</i></b> command (replace <i>wallet.wam</i> with your wax wallet)."

    return message

# Apresenta as pontuações de todos os jogadores
def leaderboard(name,wallet):
    user_name = str(name).lower()
    j=0
    #conecta com o banco de dados MySQL
    connection = mysql.connector.connect(
        host="host",
        user="user",
        password=constants.DBACCESS,
        database="wizardworld"
    )

    cursor = connection.cursor()

    sql = "SELECT * FROM battlefield ORDER BY level DESC, enemymp ASC, magic DESC LIMIT 100"
    cursor.execute(sql)
    results = cursor.fetchall()

    cursor.close()
    connection.close()
    stats = "<b>🏁🏁 TOP 20 PLAYERS 🏁🏁</b>" + "\n" + "User Name (Wallet)" + "\n"

    for result in results:
        j=j+1
        db_id, db_username, db_wallet, db_adventure, db_mission, db_level, db_round, db_magic, db_enemymp, db_bluepotions, db_redpotions, db_yellowpotions, db_purplepotions, db_invisible, db_updated, db_nextmission, db_password, db_skart, db_acum_skart, db_last_reward = result

        if j<=20:
        #if (db_level!=0) or (db_round!=1) or (db_magic != 100) or (db_enemymp !=1000):
            if db_wallet==None:
                stats = stats + str(j) + "<b> " + db_username + " </b>(empty)\n     Level=<b> " + str(db_level) + " </b>Magic Points=<b> "+str(db_magic)+ "</b>\n"
            else:
                stats = stats + str(j) + "<b> " + db_username + "</b> ("+db_wallet+")\n     Level=<b> " + str(db_level) + " </b>Magic Points=<b> "+str(db_magic)+ "</b>\n"

    return stats

# Reinicia as pontuações de todos os jogadores
def new_wizard_season(name,wallet):
    user_name = str(name).lower()
    j=0
    global isMinionAlive
    global minionKiller
    isMinionAlive = True
    minionKiller = ""
    #conecta com o banco de dados MySQL
    connection = mysql.connector.connect(
        host="host",
        user="user",
        password=constants.DBACCESS,
        database="wizardworld"
    )

    cursor = connection.cursor()

    sql = "SELECT * FROM battlefield ORDER BY level DESC, enemymp ASC, magic DESC"
    cursor.execute(sql)
    results = cursor.fetchall()


    stats = "The leaderboard was successfully reseted. \nAll set for a new season of Wizards Worlds."

    for result in results:

        row = results[j]
        db_id, db_username, db_wallet, db_adventure, db_mission, db_level, db_round, db_magic, db_enemymp, db_bluepotions, db_redpotions, db_yellowpotions, db_purplepotions, db_invisible, db_updated, db_nextmission, db_password, db_skart, db_acum_skart, db_last_reward = row
        #db_level=0
        #db_round=1
        #db_enemymp=1000
        db_updated="n"
        # Descomentar essas linhas para zerar a quantidade de MP e poções de todos os jogadores
        #db_magic=100
        #db_bluepotions=0
        #db_redpotions=0
        #db_yellowpotions=0
        db_invisible=0


        sql = "UPDATE battlefield SET username = %s, wallet = %s, adventure = %s, mission = %s, level = %s, round = %s, magic = %s, enemymp = %s, bluepotions = %s, redpotions = %s, yellowpotions = %s, purplepotions = %s, invisible=%s, updated = %s, nextmission = %s, password = %s, skart = %s, acum_skart = %s, last_reward = %s WHERE id = %s"
        data = (db_username, db_wallet, db_adventure, db_mission, db_level, db_round, db_magic, db_enemymp, db_bluepotions, db_redpotions, db_yellowpotions, db_purplepotions, db_invisible, db_updated, db_nextmission, db_password, db_skart, db_acum_skart, db_last_reward, db_id)

        cursor.execute(sql, data)
        connection.commit()
        recordsaffected = cursor.rowcount
        j=j+1

    cursor.close()
    connection.close()
    return stats

# Apresenta informações e pontuações do jogador
def my_stats(name,wallet):
    user_name = str(name).lower()
    j=0
    #conecta com o banco de dados MySQL
    connection = mysql.connector.connect(
        host="host",
        user="user",
        password=constants.DBACCESS,
        database="wizardworld"
    )

    cursor = connection.cursor()

    # Localiza o registro do usuário
    sql = "SELECT * FROM battlefield WHERE username='"+user_name+"'"
    cursor.execute(sql)
    results = cursor.fetchall()

    if len(results)>0:
        row = results[0]
        db_id, db_username, db_wallet, db_adventure, db_mission, db_level, db_round, db_magic, db_enemymp, db_bluepotions, db_redpotions, db_yellowpotions, db_purplepotions, db_invisible, db_updated, db_nextmission, db_password, db_skart, db_acum_skart, db_last_reward = row

        stats = "<b>📊 My Stats 📊</b>\n"
        my_magicSet = magic_Set(db_wallet)
        my_wizard = my_magicSet[0]
        my_spellbook = my_magicSet[1]
        my_wand = my_magicSet[2]


        if db_wallet==None:
            stats = stats+ "👤 - " + db_username + " (empty)"
        else:
            stats = stats +"👤 - " + db_username + " ("+db_wallet+") \n"


        if db_invisible>0:
            stats = stats + "\n🛡 Adventure = "+str(db_adventure)+"     🎯 /Mission = "+str(db_mission)
            stats = stats + "\n✅ Level = "+str(db_level)+"      ⚔️ Round = "+ str(db_round)
            stats = stats +"\n\n<b>Magic Power:</b>"
            stats = stats +"\n🧙🏼 You = "+str(db_magic) + " 🧟 Enemy= "+str(db_enemymp)
            stats = stats +"\n\n<b>My magical items in use:</b>\n"
            stats = stats +"🧙🏼 = "+ my_wizard+"\n📓 = "+my_spellbook+"\n🪄 = "+my_wand+"\n"
            stats = stats +"🧉 = Magic Potions ("+str(5*(db_bluepotions+db_redpotions+db_yellowpotions+db_purplepotions))+" Magic Points)\n"
            stats = stats + "\n<b>Magic Potions:</b> \n🔵 = "+str(db_bluepotions)+" 🔴 = "+str(db_redpotions)+ " 🟡 = "+str(db_yellowpotions)+ " 🟣 = "+str(db_purplepotions)
            stats = stats + "\n<i>Your magic potions give you <b>"+str(2*(db_bluepotions+db_redpotions+db_yellowpotions+db_purplepotions))+" Potion Bonus Points</b> when you hit the enemy</i>."
            #stats = stats +"\n\n<b>My SKART balance:</b>\n"
            #stats = stats + "🎨 SKART = "+str(round(db_skart,4))+"   \n🎨 SKART earned so far = "+ str(round(db_acum_skart,4))
            #stats = stats +"\n<i>You can use your SKART balance to /buy items. \nClick /list to see the available items.</i>"
            #stats = stats + "\n<i>You can also /withdraw your SKART tokens and stake it in the SKART token pool and earn WAX here: https://waxdao.io/pool/skartwaxpool </i>"
            stats=stats+"\n\n The enemy cannot attack you for "+str(db_invisible)+" turns."
        else:
            stats = stats + "\n🛡 Adventure = "+str(db_adventure)+"     🎯 /Mission = "+str(db_mission)
            stats = stats + "\n✅ Level = "+str(db_level)+"      ⚔️ Round = "+ str(db_round)
            stats = stats +"\n\n<b>Magic Power:</b>"
            stats = stats +"\n🧙🏼 You = "+str(db_magic) + "   🧟 Enemy= "+str(db_enemymp)
            stats = stats +"\n\n<b>My magical items in use:</b>\n"
            stats = stats +"🧙🏼 = "+ my_wizard+"\n📓 = "+my_spellbook+"\n🪄 = "+my_wand+"\n"
            stats = stats +"🧉 = Magic Potions ("+str(5*(db_bluepotions+db_redpotions+db_yellowpotions+db_purplepotions))+" Magic Points)\n"
            stats = stats + "\n<b>Magic Potions:</b> \n🔵 = "+str(db_bluepotions)+" 🔴 = "+str(db_redpotions)+ " 🟡 = "+str(db_yellowpotions)+ " 🟣 = "+str(db_purplepotions)
            stats = stats + "\n<i>Your magic potions give you <b>"+str(2*(db_bluepotions+db_redpotions+db_yellowpotions+db_purplepotions))+" Potion Bonus Points</b> when you hit the enemy</i>."
            #stats = stats +"\n\n<b>My SKART balance:</b>\n"
            #stats = stats + "🎨 SKART = "+str(round(db_skart,4))+"   \n🎨 SKART earned so far = "+ str(round(db_acum_skart,4))
            #stats = stats +"\n<i>You can use your SKART balance to /buy items. \nClick /list to see the available items.</i>"
            #stats = stats + "\n<i>You can also /withdraw your SKART tokens and stake it in the SKART token pool and earn WAX here: https://waxdao.io/pool/skartwaxpool </i>"

    else:
        stats="Hi "+ user_name+"! Please, register your wax wallet with <b>/wax <i>wallet.wam</i></b> command (replace <i>wallet.wam</i> with your wax wallet)."

    cursor.close()
    connection.close()

    return stats

# Apresenta o saldo ingame do jogador
def my_balance(name):
    user_name = str(name).lower()
    user_data = getData(user_name)
    user_wallet=user_data[2]

    # Verifica quais itens o jogador possui.
    #url = f"https://atomic.hivebp.io/atomicassets/v1/assets?collection_name=brsketchart1&schema_name=wizardsworld&owner={user_wallet}&page=1&limit=500&order=desc&sort=asset_id"
    url = f"https://wax.eosusa.io/atomicassets/v1/assets?collection_name=brsketchart1&schema_name=wizardsworld&owner={user_wallet}&page=1&limit=500&order=desc&sort=asset_id"

    # Send a GET request to the API endpoint
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        data = response.json()

    # Extract template_id and assets from the parsed data
    assets = data['data']
    total_assets=0
    player_reward=float(0)


    for asset in assets:
        asset_id = str(asset['asset_id'])
        collection = asset['collection']['collection_name']
        schema_name = asset['schema']['schema_name']
        template = asset['template']['template_id']
        total_assets = total_assets + 1

        player_reward = player_reward + float(getRewardTemplate(template))


    player_reward_daily = round(player_reward,4)
    player_reward_hourly = round((player_reward/24),4)
    magicpower = inventory(name, user_wallet)

    info_balance = "<b>WIZARD'S BALANCE</b>\n"
    info_balance = info_balance + "\n🧙🏼‍ Wizard : <b>"+user_name+"</b>"
    info_balance = info_balance + "\n💰 Wallet : <b>"+user_wallet+"</b>"
    info_balance = info_balance + "\n🖼 Assets : "+str(total_assets)+" NFT"
    info_balance = info_balance + "\n✨ Magic Power : "+str(magicpower)
    info_balance = info_balance + "\n🎨 Daily Reward : "+str(player_reward_daily)+ " SKART"
    info_balance = info_balance + "\n🎨 Hourly Reward : "+str(player_reward_hourly)+ " SKART"
    info_balance = info_balance + "\n\n🎨 Current Balance : <b>"+str(round(user_data[17],4))+ " SKART</b>"
    info_balance = info_balance + "\n🎨 Tokens received so far : "+str(round(user_data[18],4))+ " SKART"
    info_balance = info_balance + "\n\n<i>You can use SKART to /buy items. \nClick /list to see the available items.</i>"
    info_balance = info_balance + "\n<i>You can /withdraw SKART tokens, stake it in the SKART token pool and earn WAX at WaxDao:\nhttps://waxdao.io/pool/skartwaxpool </i>"


    print("** BALANCE INFORMATION **")
    print("User name: ", user_name)
    print("User wallet: ", user_wallet)
    print("Magic Power: ",magicpower)
    print("Total assets: ", total_assets)
    print("Daily reward: ",player_reward_daily, "SKART")
    print("Hourly reward: ",player_reward_hourly, "SKART")
    print("Current balance: ",round(user_data[17],4), "SKART")
    print("Tokens received so far: ", round(user_data[18],4), "SKART")
    print("*********************")

    return info_balance

# Usa a Poção Azul. Esta poção recupera 50 wizard power do jogador, mas cada poção só pode ser usada uma vez.
def use_blue_potion(name,wallet):
    user_name = str(name).lower()
    global isMinionAlive
    global minionKiller
    if (isMinionAlive==False):
        return "minionlost"
        # return "⚔️ GAME OVER ⚔️ \nAll hail the great wizard "+minionKiller+" who defeated the minion!"

    j=0
    #conecta com o banco de dados MySQL
    connection = mysql.connector.connect(
        host="host",
        user="user",
        password=constants.DBACCESS,
        database="wizardworld"
    )

    cursor = connection.cursor()

    # Localiza o registro do usuário
    sql = "SELECT * FROM battlefield WHERE username='"+user_name+"'"
    cursor.execute(sql)
    results = cursor.fetchall()

    if len(results)>0:
        row = results[0]
        db_id, db_username, db_wallet, db_adventure, db_mission, db_level, db_round, db_magic, db_enemymp, db_bluepotions, db_redpotions, db_yellowpotions, db_purplepotions, db_invisible, db_updated, db_nextmission, db_password, db_skart, db_acum_skart, db_last_reward = row

        if db_bluepotions>0:
            db_bluepotions=db_bluepotions-1
            db_magic=db_magic+50

            sql = "UPDATE battlefield SET username = %s, wallet = %s, adventure = %s, mission = %s, level = %s, round = %s, magic = %s, enemymp = %s, bluepotions = %s, redpotions = %s, yellowpotions = %s, purplepotions = %s, invisible = %s,updated = %s, nextmission = %s, password = %s, skart = %s, acum_skart = %s, last_reward = %s WHERE id = %s"
            data = (db_username, db_wallet, db_adventure, db_mission, db_level, db_round, db_magic, db_enemymp, db_bluepotions, db_redpotions, db_yellowpotions, db_purplepotions, db_invisible, db_updated, db_nextmission, db_password, db_skart, db_acum_skart, db_last_reward, db_id)
            cursor.execute(sql, data)
            connection.commit()
            recordsaffected = cursor.rowcount

            stats = "Hi "+ db_username+"! You used a 🔵blue magic potion and added 50 magic powers to your wizard.\nNow you have:"
            #stats = stats + "\n✅ Level = "+str(db_level)+"      ⚔️ Round = "+ str(db_round)+"\n🧙🏼 You = "+str(db_magic) + " 🧟 Enemy= "+str(db_enemymp)+"\nMagic Potions: \n🔵 = "+str(db_bluepotions)+" 🔴 = "+str(db_redpotions)+ " 🟡 = "+str(db_yellowpotions)
            stats = stats + "\n✅ Level = "+str(db_level)+"      ⚔️ Round = "+ str(db_round)
            stats = stats +"\n<b>Magic Power</b>\n🧙🏼 You = "+str(db_magic) + " 🧟 Enemy= "+str(db_enemymp)
            stats = stats +"\n<b>Magic Potions</b>\n🔵 = "+str(db_bluepotions)+" 🔴 = "+str(db_redpotions)+ " 🟡 = "+str(db_yellowpotions)+ " 🟣 = "+str(db_purplepotions)

        else:
            stats="Sorry, "+ db_username+". You don't have Blue Magic Potions."

    else:
        stats="Hi "+ user_name+"! Please, register your wax wallet with <b>/wax <i>wallet.wam</i></b> command (replace <i>wallet.wam</i> with your wax wallet)."


    cursor.close()
    connection.close()

    return stats

# Usa a Poção Vermelha. Esta poção recupera reduz 50 wizard powers do inimigo, mas cada poção só pode ser usada uma vez.
def use_red_potion(name,wallet):
    user_name = str(name).lower()
    global isMinionAlive
    global minionKiller
    if (isMinionAlive==False):
        return "minionlost"
        #return "⚔️ GAME OVER ⚔️ \nAll hail the great wizard "+minionKiller+" who defeated the minion!"

    j=0
    #conecta com o banco de dados MySQL
    connection = mysql.connector.connect(
        host="host",
        user="user",
        password=constants.DBACCESS,
        database="wizardworld"
    )

    cursor = connection.cursor()

    # Localiza o registro do usuário
    sql = "SELECT * FROM battlefield WHERE username='"+user_name+"'"
    cursor.execute(sql)
    results = cursor.fetchall()

    if len(results)>0:
        row = results[0]
        db_id, db_username, db_wallet, db_adventure, db_mission, db_level, db_round, db_magic, db_enemymp, db_bluepotions, db_redpotions, db_yellowpotions, db_purplepotions, db_invisible, db_updated, db_nextmission, db_password, db_skart, db_acum_skart, db_last_reward = row
        timebetweenmissions= timedelta(hours=24)-timedelta(hours=db_purplepotions)
        if db_redpotions>0:
            db_redpotions=db_redpotions-1
            if db_enemymp>=50:
                db_enemymp=db_enemymp-50
            else:
                db_enemymp=0

            # Passa para o próximo nível
            if db_enemymp<=0:

                print("********************* \n Sending rewards to :",db_username)
                # Envia o prêmio correspondente ao nível
                imagem_NFT = send_NFT(db_wallet, db_level)

                # Envia o SKART reward para a conta do jogador no jogo
                db_last_reward = datetime.now()
                player_reward = float(getRewardPlayer(db_username, db_wallet))
                db_skart = float(db_skart)+float(player_reward)
                db_acum_skart = float(db_acum_skart) + float(player_reward)

                if (db_level/db_adventure)==10:
                    db_adventure=db_adventure+1
                    registro = "🎉Congratulations, " +user_name +"!! You have finished this adventure! \nThis victory took you to the next level! \nBut beware! Your next adventure might not be so easy!\n"
                else:
                    registro = "🎉Congratulations, " +user_name +"!! You have defeated the enemy! \nThis victory took you to the next level! \nBut beware! Your next enemy is also stronger!\n"

                level=db_level+1
                db_level=level
                db_mission=db_mission+1
                db_invisible=0
                db_enemymp=1000 + (db_level*100)
                db_round=1
                db_updated="n"
                db_bluepotions=getCount("665364",db_wallet)
                db_redpotions=getCount("665365",db_wallet)
                db_yellowpotions=getCount("665366",db_wallet)
                db_purplepotions=getCount("746407",db_wallet)
                if db_purplepotions>12:
                    db_purplepotions=12
                timebetweenmissions= timedelta(hours=24)-timedelta(hours=db_purplepotions)
                db_nextmission = datetime.now()+timebetweenmissions

                # Max usable potions = 10
                if db_bluepotions>10:
                    db_bluepotions=10
                if db_redpotions>10:
                    db_redpotions=10
                if db_yellowpotions>10:
                    db_yellowpotions=10
                if db_purplepotions>12:
                    db_purplepotions=12
                #total_points=db_magic

                #isMinionAlive=False
                #minionKiller=user_name

                registro = registro + "Your enemy dropped an item that was sent to your wallet. It will be useful in your next missions. Use it wisely."
                registro = registro + "\nTo see your next mission use the /mission command.\n"
                registro = registro + "🧙🏼‍ Your MP = "+str(db_magic)+"      🧟 Enemy MP = "+ str(db_enemymp)
                registro = registro + "\n🎨 SKART this mission = "+str(round(player_reward,4))+"\n🎨 SKART balance = "+str(round(db_skart,4))+"   \n🎨 SKART earned so far = "+ str(round(db_acum_skart,4))
                registro = registro + "\n⭐️ Next Level = "+str(db_level)
                registro = registro + "\n"+imagem_NFT

            else:
                registro = "Hi "+ db_username+"! You used a 🔴 red magic potion and reduced your enemy's 50 magic powers.\nNow you have:"
                #registro = registro + "\n🧙🏼‍ You= "+str(db_magic)+"  🧟 Enemy= "+ str(db_enemymp) +"\nMagic Potions:  🔵 = "+ str(db_bluepotions)+"  🔴 = "+ str(db_redpotions)+"  🟡 = "+str(db_yellowpotions)
                registro = registro + "\n✅ Level = "+str(db_level)+"      ⚔️ Round = "+ str(db_round)
                registro = registro +"\n<b>Magic Power</b>\n🧙🏼 You = "+str(db_magic) + " 🧟 Enemy= "+str(db_enemymp)
                registro = registro +"\n<b>Magic Potions</b>\n🔵 = "+str(db_bluepotions)+" 🔴 = "+str(db_redpotions)+ " 🟡 = "+str(db_yellowpotions)+ " 🟣 = "+str(db_purplepotions)
                registro = registro + "\n🎨 SKART = "+str(round(db_skart,4))+"   \n🎨 SKART earned so far = "+ str(round(db_acum_skart,4))

        else:
            registro="Sorry, "+ db_username+". You don't have Red Magic Potions."

        sql = "UPDATE battlefield SET username = %s, wallet = %s, adventure = %s, mission = %s, level = %s, round = %s, magic = %s, enemymp = %s, bluepotions = %s, redpotions = %s, yellowpotions = %s, purplepotions = %s, invisible=%s, updated = %s, nextmission = %s, password = %s, skart = %s, acum_skart = %s, last_reward = %s WHERE id = %s"
        data = (db_username, db_wallet, db_adventure, db_mission, db_level, db_round, db_magic, db_enemymp, db_bluepotions, db_redpotions, db_yellowpotions, db_purplepotions, db_invisible, db_updated, db_nextmission, db_password, db_skart, db_acum_skart, db_last_reward, db_id)
        cursor.execute(sql, data)
        connection.commit()
        recordsaffected = cursor.rowcount

    else:
        registro="Hi "+ user_name+"! Please, register your wax wallet with <b>/wax <i>wallet.wam</i></b> command (replace <i>wallet.wam</i> with your wax wallet)."

    cursor.close()
    connection.close()

    return registro

# Usa a Poção Amarela. Esta poção anula os ataques do inimigo por 3 turnos, mas cada poção só pode ser usada uma vez.
def use_yellow_potion(name,wallet):
    user_name = str(name).lower()
    global isMinionAlive
    global minionKiller
    if (isMinionAlive==False):
        return "minionlost"
        # return "⚔️ GAME OVER ⚔️ \nAll hail the great wizard "+minionKiller+" who defeated the minion!"

    j=0
    #conecta com o banco de dados MySQL
    connection = mysql.connector.connect(
        host="host",
        user="user",
        password=constants.DBACCESS,
        database="wizardworld"
    )

    cursor = connection.cursor()

    # Localiza o registro do usuário
    sql = "SELECT * FROM battlefield WHERE username='"+user_name+"'"
    cursor.execute(sql)
    results = cursor.fetchall()

    if len(results)>0:
        row = results[0]
        db_id, db_username, db_wallet, db_adventure, db_mission, db_level, db_round, db_magic, db_enemymp, db_bluepotions, db_redpotions, db_yellowpotions, db_purplepotions, db_invisible, db_updated, db_nextmission, db_password, db_skart, db_acum_skart, db_last_reward = row

        if db_yellowpotions>0:
            db_yellowpotions=db_yellowpotions-1
            db_invisible=db_invisible+3

            sql = "UPDATE battlefield SET username = %s, wallet = %s, adventure = %s, mission = %s, level = %s, round = %s, magic = %s, enemymp = %s, bluepotions = %s,  redpotions = %s, yellowpotions = %s, purplepotions = %s, invisible = %s, updated = %s, nextmission = %s, password = %s, skart = %s, acum_skart = %s, last_reward = %s WHERE id = %s"
            data = (db_username, db_wallet, db_adventure, db_mission, db_level, db_round, db_magic, db_enemymp, db_bluepotions, db_redpotions, db_yellowpotions, db_purplepotions, db_invisible, db_updated, db_nextmission, db_password, db_skart, db_acum_skart, db_last_reward, db_id)
            cursor.execute(sql, data)
            connection.commit()
            recordsaffected = cursor.rowcount

            stats = "Hi "+ db_username+"! You used a 🟡yellow magic potion to protect your wizard.\nNow you have:"

            if db_invisible>0:
                stats = stats + "\nThe enemy cannot attack you for "+str(db_invisible)+" turns."

            stats = stats + "\n✅ Level = "+str(db_level)+"      ⚔️ Round = "+ str(db_round)
            stats = stats +"\n<b>Magic Power</b>\n🧙🏼 You = "+str(db_magic) + " 🧟 Enemy= "+str(db_enemymp)
            stats = stats +"\n<b>Magic Potions</b>\n🔵 = "+str(db_bluepotions)+" 🔴 = "+str(db_redpotions)+ " 🟡 = "+str(db_yellowpotions)+ " 🟣 = "+str(db_purplepotions)

        else:
            stats="Sorry, "+ db_username+". You don't have Yellow Magic Potions."

    else:
        stats="Hi "+ user_name+"! Please, register your wax wallet with <b>/wax <i>wallet.wam</i></b> command (replace <i>wallet.wam</i> with your wax wallet)."


    cursor.close()
    connection.close()

    return stats

# Atualiza a tabela de itens do jogador e retorna a máxima pontuação de seus NFT (Wizard + SpeelBook + Magic Wand)
def inventory(name, wallet):
    user_name = str(name).lower()
    user_wallet = str(wallet).lower()
    magic_list = ""
    j=0

    # Replace the informations "wallet", "collection" and "schema".
    my_magics = atom.get_assets(user_wallet,"brsketchart1","wizardsworld","",1,"desc",500)
    total_magics = len(my_magics)
    tipoNFT=""
    points=0
    total_magic_points=0
    maxpoint_wizard=0
    maxpoint_book=0
    maxpoint_wand=0
    maxpoints_potion=0
    maxpoints_key=0
    maxpoints_items=0
    maxpoints=0
    maxtemplate=""

    #conecta com o banco de dados MySQL
    connection = mysql.connector.connect(
        host="host",
        user="user",
        password=constants.DBACCESS,
        database="wizardworld"
    )

    #cursor = connection.cursor()

    if total_magics>0:

        for i in my_magics:

            cursor = connection.cursor()

            magic= my_magics[j]
            idasset = magic.get_id()
            template = magic.template.name
            imagem = magic.template.image

            points = int(MagicPoint(template)[2:6])
            codtipo = str((MagicPoint(template))[0:2])
            if codtipo=="WZ":
                tipoNFT= "wizard"
                if points>maxpoint_wizard:
                    maxpoint_wizard=points
            elif codtipo=="BK":
                tipoNFT = "book"
                if points>maxpoint_book:
                    maxpoint_book=points
            elif codtipo=="WD":
                tipoNFT = "wand"
                if points>maxpoint_wand:
                    maxpoint_wand=points
            elif codtipo=="PT":
                tipoNFT = "potion"
                maxpoints_potion=maxpoints_potion+points
            elif codtipo=="KY":
                tipoNFT = "key"
                maxpoints_key=maxpoints_key+points
            elif codtipo=="IT":
                tipoNFT = "item"
                maxpoints_items=maxpoints_items+points

            maxpoints = maxpoint_wizard + maxpoint_book + maxpoint_wand + maxpoints_potion + maxpoints_key + maxpoints_items

            # Localiza o registro do item no inventário
            sql = "SELECT * FROM inventory WHERE username='"+user_name+"' and wallet='"+user_wallet+"' and asset='"+idasset+"'"
            cursor.execute(sql)
            results = cursor.fetchall()

            if len(results)>0:
                row = results[0]
                db_id, db_username, db_wallet, db_asset, db_tipo, db_name_asset, db_img, db_mp = row
                if db_wallet != user_wallet:
                    return "Hi "+user_name+" ! You already have a different wax wallet in use! Please, contact the admin if you need to change you wallet."

                else:
                    sql = "UPDATE inventory SET username = %s, wallet = %s, asset = %s, tipo = %s, name_asset = %s, img = %s, mp = %s WHERE id = %s"
                    data = (db_username, db_wallet, idasset, tipoNFT, template, imagem, points, db_id)
                    cursor.execute(sql, data)
                    connection.commit()
                    recordsaffected = cursor.rowcount
            else:
                sql = "INSERT INTO inventory (username, wallet, asset, tipo, name_asset, img, mp) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                data = (user_name, user_wallet, idasset, tipoNFT, template, imagem, points)
                cursor.execute(sql, data)
                connection.commit()
                cursor.close()

            j=j+1
            # Fecha conexão com banco de dados
            connection.commit()
            cursor.close()
        connection.close()

    else:
        cursor = connection.cursor()
        sql = "INSERT INTO inventory (username, wallet, asset, tipo, name_asset, img, mp) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        data = (user_name, user_wallet, "", "", "", "", 0)
        cursor.execute(sql, data)
        connection.commit()
        cursor.close()
        connection.close()

    return maxpoints

# Verifica quais os maiores MP de Wizard, Spell Book e Magic Wand que o jogador possui em sua wallet.
def magic_Set(wallet):
    set_NFT = []
    #user_name = str(name).lower()
    my_aspiring_wizards=0
    my_apprentice_wizards=0
    my_journeywoman_souceress=0
    my_journeyman_wizards=0
    my_expert_wizards=0
    my_master_wizards=0
    my_supreme_wizards=0
    my_ethereal_wizards=0
    my_aspiring_spellbooks=0
    my_apprentice_spellbooks=0
    my_journeywoman_spellbooks=0
    my_expert_spellbooks=0
    my_master_spellbooks=0
    my_supreme_spellbooks=0
    my_ethereal_spellbooks=0
    my_wooden_wands=0
    my_iron_wands=0
    my_bronze_wands=0
    my_silver_wands=0
    my_golden_wands=0
    my_crystal_wands=0
    my_emerald_wands=0

    # Verifica quais itens o jogador possui.
    #url = f"https://wax.api.atomicassets.io/atomicassets/v1/accounts/{wallet}/brsketchart1"
    #url = f"https://atomic.hivebp.io/atomicassets/v1/accounts/{wallet}/brsketchart1"
    url = f"https://wax.eosusa.io/atomicassets/v1/accounts/{wallet}/brsketchart1"

    # Send a GET request to the API endpoint
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        data = response.json()

    # Extract template_id and assets from the parsed data
    templates = data['data']['templates']

    for template in templates:
        template_id = template['template_id']
        assets = template['assets']

        #print("Template ID:", template_id)
        #print("Assets Count:", assets)
        # WIZARDS
        if template_id=="649929":
            my_aspiring_wizards=int(assets)
        elif template_id=="649930":
            my_apprentice_wizards=int(assets)
        elif template_id=="660835":
            my_journeywoman_souceress=int(assets)
        elif template_id=="660839":
            my_journeyman_wizards=int(assets)
        elif template_id=="685511":
            my_expert_wizards=int(assets)
        elif template_id=="750119":
            my_master_wizards=int(assets)
        elif template_id=="761405":
            my_supreme_wizards=int(assets)
        elif template_id=="777207":
            my_ethereal_wizards=int(assets)
        # SPELL BOOKS
        if template_id=="649934":
            my_aspiring_spellbooks=int(assets)
        elif template_id=="649936":
            my_apprentice_spellbooks=int(assets)
        elif template_id=="660777":
            my_journeywoman_spellbooks=int(assets)
        elif template_id=="745208":
            my_expert_spellbooks=int(assets)
        elif template_id=="749104":
            my_master_spellbooks=int(assets)
        elif template_id=="761406":
            my_supreme_spellbooks=int(assets)
        elif template_id=="781527":
            my_ethereal_spellbooks=int(assets)
        # MAGIC WANDS
        elif template_id=="649938":
            my_wooden_wands=int(assets)
        elif template_id=="649939":
            my_iron_wands=int(assets)
        elif template_id=="649942":
            my_bronze_wands=int(assets)
        elif template_id=="649943":
            my_silver_wands=int(assets)
        elif template_id=="749105":
            my_golden_wands=int(assets)
        elif template_id=="749109":
            my_crystal_wands=int(assets)
        elif template_id=="749114":
            my_emerald_wands=int(assets)


    if my_emerald_wands>0:
        my_wand="Emerald Magic Wand (1000 Magic Points)"
    elif my_crystal_wands>0:
        my_wand="Crystal Magic Wand (500 Magic Points)"
    elif my_golden_wands>0:
        my_wand="Golden Magic Wand (250 Magic Points)"
    elif my_silver_wands>0:
        my_wand="Silver Magic Wand (125 Magic Points)"
    elif my_bronze_wands>0:
        my_wand="Bronze Magic Wand (60 Magic Points)"
    elif my_iron_wands>0:
        my_wand="Iron Magic Wand (30 Magic Points)"
    elif my_wooden_wands>0:
        my_wand="Wooden Magic Wand (15 Magic Points)"
    else:
        my_wand="No Magic Wands"


    if my_ethereal_wizards>0:
        my_wizard="Ethereal Wizard (1500 Magic Points)"
    elif my_supreme_wizards>0:
        my_wizard="Supreme Wizard (500 Magic Points)"
    elif my_master_wizards>0:
        my_wizard="Master Wizard (250 Magic Points)"
    elif my_expert_wizards>0:
        my_wizard="Expert Wizard (125 Magic Points)"
    elif my_journeyman_wizards>0:
        my_wizard="Journeyman Wizard (60 Magic Points)"
    elif my_journeywoman_souceress>0:
        my_wizard="Journeywoman Sourceress (60 Magic Points)"
    elif my_apprentice_wizards>0:
        my_wizard="Apprentice Wizard (30 Magic Points)"
    elif my_aspiring_wizards>0:
        my_wizard="Aspiring Wizard (15 Magic Points)"
    else:
        my_wizard="No Wizards"

    if my_ethereal_spellbooks>0:
        my_spellbook="Ethereal Spellbook (1500 Magic Points)"
    elif my_supreme_spellbooks>0:
        my_spellbook="Supreme Spellbook (500 Magic Points)"
    elif my_master_spellbooks>0:
        my_spellbook="Master Spellbook (250 Magic Points)"
    elif my_expert_spellbooks>0:
        my_spellbook="Expert Spellbook (125 Magic Points)"
    elif my_journeywoman_spellbooks>0:
        my_spellbook="Journeyman Spellbook (60 Magic Points)"
    elif my_apprentice_spellbooks>0:
        my_spellbook="Apprentice Spellbook (30 Magic Points)"
    elif my_aspiring_spellbooks>0:
        my_spellbook="Aspiring Spellbook (15 Magic Points)"
    else:
        my_spellbook="No Spellbooks"

    set_NFT.append(my_wizard)
    set_NFT.append(my_spellbook)
    set_NFT.append(my_wand)

    return (set_NFT)

# Conta o numero de assets de um determinado template em uma wax wallet.
def getCount(cod_template, wallet_add):
    #url = f"https://wax.api.atomicassets.io/atomicmarket/v1/assets?template_id={cod_template}&owner={wallet_add}&page=1&limit=300&order=desc&sort=asset_id"
    #url = f"https://atomic.hivebp.io/atomicassets/v1/assets?template_id={cod_template}&owner={wallet_add}&page=1&limit=300&order=desc&sort=asset_id"
    url = f"https://wax.eosusa.io/atomicmarket/v1/assets?template_id={cod_template}&owner={wallet_add}&page=1&limit=300&order=desc&sort=asset_id"
    # Send GET request
    response = requests.get(url)
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        count_Assets=len(data["data"])
        return(count_Assets)

    else:
        return(0)
        print("Error:", response.status_code)

# Inclui ou atualiza a informações de usuário Telegram do player na base de dados
def my_userdata(id_user, id_chat):
    my_UserID = id_user
    my_Chat = id_chat

    #conecta com o banco de dados MySQL
    connection = mysql.connector.connect(
        host="host",
        user="user",
        password=constants.DBACCESS,
        database="wizardworld"
    )

    cursor = connection.cursor()

    sql = "SELECT * FROM userinfo WHERE user_id='"+str(my_UserID)+"'"
    cursor.execute(sql)
    results = cursor.fetchall()

    if len(results)>0:
        # Localiza o registro do usuário para atualização
        row = results[0]
        db_cod, db_user_id, db_chatid = row
        sql = "UPDATE userinfo SET user_id = %s, chat_id = %s WHERE cod = %s"
        data = (my_UserID, my_Chat, db_cod)
        cursor.execute(sql, data)
        connection.commit()
        recordsaffected = cursor.rowcount

    else:
        # Insere novo usuário
        sql = "INSERT INTO userinfo (user_id, chat_id) VALUES (%s, %s)"
        data = (my_UserID, my_Chat)
        cursor.execute(sql, data)
        connection.commit()
        cursor.close()
        connection.close()

    # Fecha conexão com banco de dados
    cursor.close()
    connection.close()

    message = "Userinfo updated for Userid: "+str(my_UserID)+" Chat ID: "+ str(my_Chat)
    return message

#Atribuição de Magic Points para cada template
def MagicPoint(template):
    nome_template = template
    magicpoints=""

    if nome_template== "Aspiring Wizard":
        magicpoints="WZ15"
    elif nome_template=="Apprentice Wizard":
        magicpoints="WZ30"
    elif nome_template=="Journeyman Wizard":
        magicpoints="WZ60"
    elif nome_template=="Journeywoman Sorceress":
        magicpoints="WZ60"
    elif nome_template=="Expert Wizard":
        magicpoints="WZ125"
    elif nome_template=="Master Wizard":
        magicpoints="WZ250"
    elif nome_template=="Supreme Wizard":
        magicpoints="WZ500"
    elif nome_template=="Ethereal Wizard":
        magicpoints="WZ1500"
    elif nome_template=="Aspiring Spell Book":
        magicpoints="BK15"
    elif nome_template=="Apprentice Spell Book":
        magicpoints="BK30"
    elif nome_template=="Journeyman Spell Book":
        magicpoints="BK60"
    elif nome_template=="Expert Spell Book":
        magicpoints="BK125"
    elif nome_template=="Master Spell Book":
        magicpoints="BK250"
    elif nome_template=="Supreme Spell Book":
        magicpoints="BK500"
    elif nome_template=="Ethereal Spell Book":
        magicpoints="BK1500"
    elif nome_template=="Wooden Magic Wand":
        magicpoints="WD15"
    elif nome_template=="Iron Magic Wand":
        magicpoints="WD30"
    elif nome_template=="Bronze Magic Wand":
        magicpoints="WD60"
    elif nome_template=="Silver Magic Wand":
        magicpoints="WD125"
    elif nome_template=="Golden Magic Wand":
        magicpoints="WD250"
    elif nome_template=="Crystal Magic Wand":
        magicpoints="WD500"
    elif nome_template=="Emerald Magic Wand":
        magicpoints="WD1000"
    elif nome_template=="Blue Magic Potion":
        magicpoints="PT05"
    elif nome_template=="Red Magic Potion":
        magicpoints="PT05"
    elif nome_template=="Yellow Magic Potion":
        magicpoints="PT05"
    elif nome_template=="Purple Magic Potion":
        magicpoints="PT10"
    elif nome_template=="Basic Magic Key":
        magicpoints="KY05"
    elif nome_template=="Wooden Magic Key":
        magicpoints="KY10"
    elif nome_template=="Iron Magic Key":
        magicpoints="KY20"
    elif nome_template=="Bronze Magic Key":
        magicpoints="KY40"
    elif nome_template=="Spell Sheet":
        magicpoints="IT20"
    elif nome_template=="Rubi":
        magicpoints="IT10"
    elif nome_template=="Sapphire":
        magicpoints="IT10"
    elif nome_template=="Emerald":
        magicpoints="IT10"
    elif nome_template=="Amethyst":
        magicpoints="IT10"
    elif nome_template=="Silver":
        magicpoints="IT10"
    elif nome_template=="Gold":
        magicpoints="IT10"
    elif nome_template=="Air Spell Scroll":
        magicpoints="IT40"
    elif nome_template=="Water Spell Scroll":
        magicpoints="IT40"
    elif nome_template=="Wooden Magic Staff":
        magicpoints="IT20"
    elif nome_template=="Lunar Magic Staff":
        magicpoints="IT20"
    elif nome_template=="Magic Hat":
        magicpoints="IT05"
    elif nome_template=="Dagger":
        magicpoints="IT15"
    elif nome_template=="Silver Dagger":
        magicpoints="IT20"
    elif nome_template=="Golden Dagger":
        magicpoints="IT60"
    elif nome_template=="Magic Iron Cauldron":
        magicpoints="IT60"
    elif nome_template=="Magic Silver Cauldron":
        magicpoints="IT100"
    elif nome_template=="Magic Golden Cauldron":
        magicpoints="IT100"
    elif nome_template=="Pickaxe":
        magicpoints="IT60"
    elif nome_template=="Leather Magic Hat":
        magicpoints="IT40"
    elif nome_template=="Ventus":
        magicpoints="IT20"
    elif nome_template=="Terra":
        magicpoints="IT20"
    elif nome_template=="Aquae":
        magicpoints="IT50"
    elif nome_template=="Ignis":
        magicpoints="IT50"
    elif nome_template=="Eldoria Map":
        magicpoints="IT30"
    elif nome_template=="Sapphire Amulet":
        magicpoints="IT50"
    elif nome_template=="Ruby Amulet":
        magicpoints="IT50"
    elif nome_template=="Emerald Amulet":
        magicpoints="IT50"
    elif nome_template=="Amethyst Amulet":
        magicpoints="IT50"
    elif nome_template=="Dream Catcher":
        magicpoints="IT30"
    elif nome_template=="Magic Dust":
        magicpoints="IT50"
    elif nome_template=="Sun Stone Amulet":
        magicpoints="IT50"
    elif nome_template=="Moonstone Amulet":
        magicpoints="IT50"
    elif nome_template=="Mars Stone Amulet":
        magicpoints="IT50"
    elif nome_template=="Venus Stone Amulet":
        magicpoints="IT50"
    elif nome_template=="Saturn Stone Amulet":
        magicpoints="IT50"
    elif nome_template=="Jupiter Stone Amulet":
        magicpoints="IT50"
    elif nome_template=="Earth Elemental Amulet":
        magicpoints="IT50"
    elif nome_template=="Water Elemental Amulet":
        magicpoints="IT50"
    elif nome_template=="Fire Elemental Amulet":
        magicpoints="IT50"
    elif nome_template=="Wind Elemental Amulet":
        magicpoints="IT50"
    elif nome_template=="Time Keeper":
        magicpoints="IT50"
    elif nome_template=="Magic Hourglass":
        magicpoints="IT50"
    elif nome_template=="Time Machine":
        magicpoints="IT50"
    elif nome_template=="Skyship":
        magicpoints="IT50"
    elif nome_template=="Celestial Prism":
        magicpoints="IT50"
    elif nome_template=="Heart of Harmony":
        magicpoints="IT50"
    elif nome_template=="Anti-gravity device":
        magicpoints="IT50"
    elif nome_template=="Magic Flying Carpet":
        magicpoints="IT50"

    else:
        magicpoints="IT00"

    return magicpoints

# Game adventures and missions
def mission(name):
    user_name = str(name).lower()

    adventures = {
        1: " <b>🛡 Adventure One</b>\n     Ashraraziel, an evil dark master wizard, has stolen a precious scroll that contains an ancient spell capable of putting a person into a state of deep sleep for years. He plans to use this knowledge to put the leader of the village where you were born to sleep, and thus dominate your hometown for his own purposes.\n     This dark master wizard keeps the scroll in the highest tower of his castle. Your mission is to enter the castle and steal the scroll back. But this will not be an easy task, because each level of the castle is closely watched by minions working for Ashararaziel.\n",
        2: " <b>🛡 Adventure Two</b>\n     Upon hearing your fight against the minions, Ashraraziel fled the castle and took shelter in an old house in the middle of the <i>Whispering Forest</i>. It is known that Ashraraziel keeps in this house other scrolls with spells that can increase your wizard's powers.  So, you follow him in search of this house in the forest and maybe get some more spells.\n     However, the forest is home to <i>small goblins</i> who will not appreciate your intrusion. They have materials that can be useful in your journey, but you will need to defeat them to get these materials.\n     You will need a <b>magic iron key</b> to open the door to the house in the forest.\n",
        3: " <b>🛡 Adventure Three</b>\n     You managed to get into the forest house by using your magic iron key to open the door. In a corner of the room is an old, damaged magic cauldron.\n     Well... this is something really useful for a beginner wizard making his magic potions. But you'll need to find some <b>iron portions</b> to recover the cauldron.\n",
        4: " <b>🛡 Adventure Four</b>\n     Your wizard has managed to collect all the materials to repair a magical iron cauldron. It will be needed to produce some magic potions. Keep it well guarded.\n     Another item every wizard needs is a magic hat. In this new adventure you'll need to find the necessary materials to make a good magic hat.\n",
        5: " <b>🛡 Adventure Five</b>\n     Your wizard is in front of an ancient mine protected by dwarf miners. In this mine you will be able to extract some precious stones and minerals useful for your spells. But in order to extract materials from the mine, you first need to make a good pickaxe.\n     Luckily, the dwarf miners have the materials you need to make this pickaxe, but you'll have to convince them to give it to you.😉\n",
        6: " <b>🛡 Adventure Six</b>\n     <b>Ruby</b> is a stone of great energy, capable of strengthening us, increasing our vitality and opening the way to achieving our goals. It strengthens our motivation, awakens a love of life, eliminates tiredness and indisposition, strengthens the mind, reduces fears and gives us a strong sense of confidence.\n     Your wizard will set off on an adventure in search of this magical stone that can be extracted from a mine protected by <b>dwarf miners</b>.\n",
        7: " <b>🛡 Adventure Seven</b>\n     <b>Sapphire</b> produces peace of mind, equanimity; it chases away all evil thoughts, establishing a healthy circulation in man. <b>Sapphire</b> is also considered the stone of wisdom.\n     Your wizard now has the mission of finding some of these magical stones in the mine of the <b>dwarf miners</b>.\n",
        8: " <b>🛡 Adventure Eight</b>\n     By tradition, the <b>emerald</b> is considered to be a stone with the power to predict the future and combat enchantments in magical workings.\n     Your wizard now has the mission of finding some of these magical stones in the mine of the <b>dwarf miners</b>.\n",
        9: " <b>🛡 Adventure Nine</b>\n     <b>Amethyst</b> is attributed with the power to transmute negative energies into positive ones, protect against bad thoughts, calm the mind, heighten intuition and awaken creativity.\n     Your wizard now has the mission of finding some of these magical stones in the mine of the <b>dwarf miners</b>.\n",
        10: "<b>🛡 Adventure Ten</b>\n     Your wizard got some ruby stones from the dwarf mine. After making your ruby amulet, you have ruby residue left over in your house. This residue is useful for making magic potions. But the dust-eating spiders want to take it back to their nests.\n",
        11: "<b>🛡 Adventure Eleven</b>\n     Your wizard got some sapphire stones from the dwarf mine. After making your sapphire amulet, you have sapphire residue left over in your house. This residue is useful for making magic potions. But the dust-eating spiders want to take it back to their nests.\n",
        12: "<b>🛡 Adventure Twelve</b>\n     Your wizard got some emerald stones from the dwarf mine. After making your emerald amulet, you have emerald residue left over in your house. This residue is useful for making magic potions. But the dust-eating spiders want to take it back to their nests.\n",
        13: "<b>🛡 Adventure Thirteen</b>\n     Your wizard got some amethyst stones from the dwarf mine. After making your amethyst amulet, you have amethyst residue left over in your house. This residue is useful for making magic potions. But the dust-eating spiders want to take it back to their nests.\n",
        14: "<b>🗝 Adventure Fourteen</b>\n     Your wizard has to navigate through the Enchanted Forest to find the hidden entrance to the lost Temple of Elements. Beware of the forest's protective spirits along the way.\n",
        15: "<b>💧 Adventure Fifteen</b>\n     After crafting a bronze magic key your wizard entered the Temple of the Elements. The first chamber of this Temple is dedicated to the element of Water. At the end of this adventure you will be able to blend the <b>Water Element Badge</b>.\n",
        16: "<b>🔥 Adventure Sixteen</b>\n     The second chamber of the Temple of the Elements is dedicated to the <b>Fire element</b>. At the end of this adventure you will be able to blend the <b>Fire Element Badge</b>.\n",
        17: "<b>💧 Adventure Seventeen</b>\n     Your wizard has managed to enter the Temple of the Elements. Inside the chamber dedicated to the <b>Water Element</b> there is an ancient locker with 10 doors. Each door needs a password to be opened and inside is an elemental stone.",
        18: "<b>🌬 Adventure Eighteen</b>\n     Your wizard has managed to enter the Temple of the Elements. Inside the chamber dedicated to the <b>Wind Element</b> there is an ancient locker with 10 doors. Each door needs a password to be opened and inside is an elemental stone.",
        19: "<b>🌍 Adventure Nineteen</b>\n     Your wizard has managed to enter the Temple of the Elements. Inside the chamber dedicated to the <b>Earth Element</b> there is an ancient locker with 10 doors. Each door needs a password to be opened and inside is an elemental stone.",
        20: "<b>🔥 Adventure Twenty</b>\n     Your wizard has managed to enter the Temple of the Elements. Inside the chamber dedicated to the <b>Fire Element</b> there is an ancient locker with 10 doors. Each door needs a password to be opened and inside is an elemental stone.",
        21: "<b>🗺 Adventure Twenty-one</b>\n     The legendary island of <b>Eldoria</b>, whose location is a secret, is where your wizard will find the ruins of a very ancient civilization. To obtain this map you need to get its fragments from the pirates.\n     Defeat them on your way to the Port of Many Tears, collect the parts of the map and, with the map of Eldoria in hand, go on to new adventures in Wizards World.",
        22: "<b>🗺 Adventure Twenty-two</b>\n     The legendary island of <b>Eldoria</b>, whose location is a secret, is where your wizard will find the ruins of a very ancient civilization. To obtain this map you need to get its fragments from the pirates.\n     Defeat them on your way to the Port of Many Tears, collect the parts of the map and, with the map of Eldoria in hand, go on to new adventures in Wizards World.",
        23: "<b>🌞 Adventure Twenty-three</b>\n     In Eldoria, explore the ruins of the Temple of the Sun. Uncover clues and artifacts that lead to the fabled Sunstone, a powerful relic said to control daylight.",
        24: "<b>🌔 Adventure Twenty-four</b>\n     Your wizard discovered another ruined temple in Eldoria. It is the Temple of the Moon. Uncover clues and artifacts that lead to the fabled Moonstone, another powerful relic said to control moonlight.",
        25: "<b>🔵 Adventure Twenty-five</b>\n     New ruins appear during your exploration of the island of Eldoria. The ruins of the Temple of Venus appear in the middle of the sand. Uncover clues and artifacts that lead to the Venus stone, another powerful relic said to control the birds' sense of direction.",
        26: "<b>🔴 Adventure Twenty-six</b>\n     In the sands of the red desert of Eldoria your wizard found the ruins of the Temple of Mars. In these ruins you will find the stones of Mars that will be used to make the Amulet of Mars Stone, a mystical artifact that has the power to arouse the wrath of your enemies.",
        27: "<b>🟠 Adventure Twenty-seven</b>\n     Eldoria is full of ancient ruins of ancient temples. The ruins of the <b>Temple of Jupiter</b> are also hidden in the Whispering Forest. In these ruins your wizard will find the <b>Jupiter stones</b> that will be needed to manufacture an amulet capable of increasing the physical strength of its bearer.",
        28: "<b>🪐 Adventure Twenty-eight</b>\n     At the foot of the Magnetic Mountains, your wizard found the ruins of the Temple of Saturn. Several secret chambers need to be opened in order for him to collect all the stones that will allow him to make the Amulet of Saturn.",
        29: "<b>🪐 Adventure Twenty-nine</b>\n     Your wizard must set off in search of the Time Keeper, a wizard older than the known universe.",
        30: "<b>⏳ Adventure Thirty</b>\n     A magic hourglass is an enchanting and mystical artifact often depicted with an ornate and elaborate design. Inside the hourglass, instead of ordinary sand, there are tiny sparkling particles that resemble stardust. They are dark magical sparks. These particles move at a variable pace, sometimes flowing steadily like traditional sand and, at other times, spinning slowly or even stopping in mid-air, as if suspended by an invisible force.",
        31: "<b>⏳ Adventure Thirty-one</b>\n     The Time Keeper has given you the project to build a time machine. Although it only allows you to travel back in time for a few minutes, it will be very useful. Gather the necessary materials and make your own time machine.",
        32: "<b>☁️ Adventure Thirty-two</b>\n     Your wizard has been invited to an important convention of wizards from all over the world. This event will take place in Celestia, the floating capital of the Sky Kingdom. The journey to Celestia will take place aboard the Skyship, a majestic flying ship. However, your wizard needs to get a ticket to travel on this ship. Luckily, there is a magical tournament taking place near the pier and you have a chance of winning enough coins to buy your wizard's ticket.",
        33: "<b>☁️ Adventure Thirty-three</b>\n     The Celestial Prism, a resplendent artifact of unparalleled beauty, was stolen from the Cloud Citadel by the enigmatic Sky Serpents. This radiant jewel, once a cornerstone of the Sky Kingdoms’ power, shimmers with the captured essence of a thousand dawns, its facets refracting light into a mesmerizing dance of celestial colors. It is said to harness the energy of the stars themselves, granting its wielder dominion over weather and the very fabric of the sky. The Prism's theft has plunged the Sky Kingdoms into a tumultuous upheaval, as its absence disrupts the delicate balance of their atmospheric magic, leaving the realm shrouded in mysterious, ever-shifting storms and darkness.",
        34: "<b>☁️ Adventure Thirty-four</b>\n     The Wizards Convention will bring together the greatest representatives of the entire Wizards World. Your wizard has been followed by an evil sorcerer who wants to commit an act of terrorism in the middle of the convention.\n     To neutralize the evil sorcerer's attack on the magicians' convention, You will need an artifact called the “Heart of Harmony”. This artifact is a jewel that emanates a protective aura, capable of dispelling evil intentions and disarming hostile spells. It also amplifies the magic of the wizards around it, strengthening their defenses.\n     The Heart of Harmony should be placed in the center of the convention hall, creating a protective field that not only neutralizes attacks, but also reveals the presence of any disguised enemy. To activate it, a collective ritual is required in which the magicians unite their energies, further strengthening the artifact's power.\n     This jewel may have a history of being used in ancient times to maintain peace between magical kingdoms, making it a symbol of unity and resistance.",
        35: "<b>☁️ Adventure Thirty-five</b>\n     Celestia, the majestic floating capital of the Sky Kingdom, defies the laws of gravity by being built on a large gravitite reserve. This is an ore that has properties that nullify the effect of the force of gravity.\n     With a certain amount of gravitite, it is possible to make an anti-gravity device that could be very useful for a wizard.",
        36: "<b>☁️ Adventure Thirty-six</b>\n     There are several possible uses for the gravitite ore mined by the miners of Celestia.\n     With the right amount of gravitite, it's even possible to make a flying carpet that will allow a wizard to travel the skies."

    }

    missions = {
        # ADVENTURE 1 - Make a magic wooden key
        1: "🗝 <b>Mission 1 – <i>Steal the key to Ashraraziel’s castle</i></b> \n     Before you can enter the castle you must get its key. To do this, you must defeat the guardian minion and steal the key from him. \n     The Minion Doorman has 1000 magic power. You have 10 rounds to defeat him and steal the key. A round ends when your wizard's magic powers run out, so you will need to wait for your wizard to recover before trying a new round against the Minion Doorman.\n",
        2: "🪵 <b>Mission 2 – <i>Defeat the minion guarding the <b>second floor</b> of Ashraraziel's Castle.</i></b> \n     You defeated the gatekeeper minion and got a basic magic key. You used the key to open the main gate of Ashraraziel's castle.\n     This castle has 9 floors and on each floor there is a guard minion. You have to defeat these minions to reach the main room where Ashraraziel kept the <i>scroll containing the spell of eternal sleep</i>.\n     The room where the scroll is kept can only be opened with a <b>magical wooden key</b>.\n",
        3: "🪵 <b>Mission 3 – <i>Defeat the minion guarding the <b>third floor</b> of Ashraraziel's Castle.</i></b> \n     You defeated the second guard minion and got a portion of wood. Keep it in your wallet as this is an important ingredient for your quest.\n     Keep going up the floors and defeating the next minions. You have to defeat these minions to reach the main room where Ashraraziel kept the <i>scroll containing the spell of eternal sleep</i>.\n     The room where the scroll is kept can only be opened with a <b>magical wooden key</b>.\n",
        4: "🪵 <b>Mission 4 – <i>Defeat the minion guarding the <b>fourth floor</b> of Ashraraziel's Castle.</i></b> \n     You defeated the third guard minion and got a portion of wood. Keep it in your wallet as this is an important ingredient for your quest.\n     Keep going up the floors and defeating the next minions. You have to defeat these minions to reach the main room where Ashraraziel kept the <i>scroll containing the spell of eternal sleep</i>.\n     The room where the scroll is kept can only be opened with a <b>magical wooden key</b>.\n",
        5: "🪵 <b>Mission 5 – <i>Defeat the minion guarding the <b>fifth floor</b> of Ashraraziel's Castle.</i></b> \n     You defeated the fourth guard minion and got a portion of wood. Keep it in your wallet as this is an important ingredient for your quest.\n     Keep going up the floors and defeating the next minions. You have to defeat these minions to reach the main room where Ashraraziel kept the <i>scroll containing the spell of eternal sleep</i>.\n     The room where the scroll is kept can only be opened with a <b>magical wooden key</b>.\n",
        6: "🪵 <b>Mission 6 – <i>Defeat the minion guarding the <b>sixth floor</b> of Ashraraziel's Castle.</i></b> \n     You defeated the fifth guard minion and got a portion of wood. Keep it in your wallet as this is an important ingredient for your quest.\n     Keep going up the floors and defeating the next minions. You have to defeat these minions to reach the main room where Ashraraziel kept the <i>scroll containing the spell of eternal sleep</i>.\n     The room where the scroll is kept can only be opened with a <b>magical wooden key</b>.\n",
        7: "🪵 <b>Mission 7 – <i>Defeat the minion guarding the <b>seventh floor</b> of Ashraraziel's Castle.</i></b> \n     You defeated the sixth guard minion and got a portion of wood. Keep it in your wallet as this is an important ingredient for your quest.\n     Keep going up the floors and defeating the next minions. You have to defeat these minions to reach the main room where Ashraraziel kept the <i>scroll containing the spell of eternal sleep</i>.\n     The room where the scroll is kept can only be opened with a <b>magical wooden key</b>.\n",
        8: "🪵 <b>Mission 8 – <i>Defeat the minion guarding the <b>eighth floor</b> of Ashraraziel's Castle.</i></b> \n     You defeated the seventh guard minion and got a portion of wood. Keep it in your wallet as this is an important ingredient for your quest.\n     Keep going up the floors and defeating the next minions. You have to defeat these minions to reach the main room where Ashraraziel kept the <i>scroll containing the spell of eternal sleep</i>.\n     The room where the scroll is kept can only be opened with a <b>magical wooden key</b>.\n",
        9: "🪵 <b>Mission 9 – <i>Defeat the minion guarding the <b>nineth  floor</b> of Ashraraziel's Castle.</i></b> \n     You defeated the eighth guard minion and got a portion of wood. Keep it in your wallet as this is an important ingredient for your quest.\n     Keep going up the floors and defeating the next minions. You have to defeat these minions to reach the main room where Ashraraziel kept the <i>scroll containing the spell of eternal sleep</i>.\n     The room where the scroll is kept can only be opened with a <b>magical wooden key</b>.\n",
        10: "🗝 <b>Mission 10 – <i>Defeat the minion guarding the <b>tenth floor</b> of Ashraraziel's Castle and Blend the wooden Magic Key.</i></b> \n     You defeated the nineth guard minion and got a portion of wood. Keep it in your wallet as this is an important ingredient for your quest.\n     Keep going up the floors and defeating the next minions. You have to defeat these minions to reach the main room where Ashraraziel kept the <i>scroll containing the spell of eternal sleep</i>.\n     The room where the scroll is kept can only be opened with a <b>magical wooden key</b>.\n",
        # ADVENTURE 2 - Make a magic iron key
        11: "🗝 <b>Mission 11 – <i>Defeat the first little goblin of the Whispering Forest.</i></b>\n     Each little goblin has a material that will be useful in this adventure. This little goblin has a <b>basic magic key</b> that will need to be blended with other materials to be obtained from the other goblins to make an iron magic key that opens the door to Ashraraziel's forest home.\n",
        12: "🗝 <b>Mission 12 – <i>Defeat the second little goblin of the Whispering Forest.</i></b>\n     Each little goblin has a material that will be useful in this adventure. This little goblin has a piece of <b>wood</b> that will need to be blended with other materials to be obtained from the other goblins to make an iron magic key that opens the door to Ashraraziel's forest home.\n",
        13: "🗝 <b>Mission 13 – <i>Defeat the third little goblin of the Whispering Forest.</i></b>\n     Each little goblin has a material that will be useful in this adventure. This little goblin has a piece of <b>wood</b> that will need to be blended with other materials to be obtained from the other goblins to make an iron magic key that opens the door to Ashraraziel's forest home.\n",
        14: "🗝 <b>Mission 14 – <i>Defeat the fourth little goblin of the Whispering Forest.</i></b>\n     Each little goblin has a material that will be useful in this adventure. This little goblin has a piece of <b>wood</b> that will need to be blended with other materials to be obtained from the other goblins to make an iron magic key that opens the door to Ashraraziel's forest home.\n",
        15: "🗝 <b>Mission 15 – <i>Defeat the fifth little goblin of the Whispering Forest.</i></b>\n     Each little goblin has a material that will be useful in this adventure. This little goblin has a piece of <b>iron</b> that will need to be blended with other materials to be obtained from the other goblins to make an iron magic key that opens the door to Ashraraziel's forest home.\n",
        16: "🗝 <b>Mission 16 – <i>Defeat the sixth little goblin of the Whispering Forest.</i></b>\n     Each little goblin has a material that will be useful in this adventure. This little goblin has a piece of <b>iron</b> that will need to be blended with other materials to be obtained from the other goblins to make an iron magic key that opens the door to Ashraraziel's forest home.\n",
        17: "🗝 <b>Mission 17 – <i>Defeat the seventh little goblin of the Whispering Forest.</i></b>\n     Each little goblin has a material that will be useful in this adventure. This little goblin has a piece of <b>iron</b> that will need to be blended with other materials to be obtained from the other goblins to make an iron magic key that opens the door to Ashraraziel's forest home.\n",
        18: "🗝 <b>Mission 18 – <i>Defeat the eighth little goblin of the Whispering Forest.</i></b>\n     Each little goblin has a material that will be useful in this adventure. This little goblin has a piece of <b>iron</b> that will need to be blended with other materials to be obtained from the other goblins to make an iron magic key that opens the door to Ashraraziel's forest home.\n",
        19: "🗝 <b>Mission 19 – <i>Defeat the nineth little goblin of the Whispering Forest.</i></b>\n     Each little goblin has a material that will be useful in this adventure. This little goblin has a piece of <b>iron</b> that will need to be blended with other materials to be obtained from the other goblins to make an iron magic key that opens the door to Ashraraziel's forest home.\n",
        20: "🗝 <b>Mission 20 – <i>Defeat the tenth little goblin of the Whispering Forest.</i></b>\n     Each little goblin has a material that will be useful in this adventure. This little goblin has a piece of <b>iron</b> that will need to be blended with other materials to be obtained from the other goblins to make an iron magic key that opens the door to Ashraraziel's forest home.\n",
        # ADVENTURE 3 - Make a iron magic cauldron
        21: "🥘 <b>Mission 21 – <i>Try to get more iron from the forest goblins of the Whispering Forest.</i></b>\n     Each little goblin has a piece of <b>iron</b> that you'll need to restore the damaged old magic cauldron.\n",
        22: "🥘 <b>Mission 22 – <i>Try to get more iron from the forest goblins of the Whispering Forest.</i></b>\n     Each little goblin has a piece of <b>iron</b> that you'll need to restore the damaged old magic cauldron.\n",
        23: "🥘 <b>Mission 23 – <i>Try to get more iron from the forest goblins of the Whispering Forest.</i></b>\n     Each little goblin has a piece of <b>iron</b> that you'll need to restore the damaged old magic cauldron.\n",
        24: "🥘 <b>Mission 24 – <i>Try to get more iron from the forest goblins of the Whispering Forest.</i></b>\n     Each little goblin has a piece of <b>iron</b> that you'll need to restore the damaged old magic cauldron.\n",
        25: "🥘 <b>Mission 25 – <i>Try to get more iron from the forest goblins of the Whispering Forest.</i></b>\n     Each little goblin has a piece of <b>iron</b> that you'll need to restore the damaged old magic cauldron.\n",
        26: "🥘 <b>Mission 26 – <i>Try to get more iron from the forest goblins of the Whispering Forest.</i></b>\n     Each little goblin has a piece of <b>iron</b> that you'll need to restore the damaged old magic cauldron.\n",
        27: "🥘 <b>Mission 27 – <i>Try to get more iron from the forest goblins of the Whispering Forest.</i></b>\n     Each little goblin has a piece of <b>iron</b> that you'll need to restore the damaged old magic cauldron.\n",
        28: "🥘 <b>Mission 28 – <i>Try to get more iron from the forest goblins of the Whispering Forest.</i></b>\n     Each little goblin has a piece of <b>iron</b> that you'll need to restore the damaged old magic cauldron.\n",
        29: "🥘 <b>Mission 29 – <i>Try to get more iron from the forest goblins of the Whispering Forest.</i></b>\n     Each little goblin has a piece of <b>iron</b> that you'll need to restore the damaged old magic cauldron.\n",
        30: "🥘 <b>Mission 30 – <i>Try to get more iron from the forest goblins of the Whispering Forest.</i></b>\n     Each little goblin has a piece of <b>iron</b> that you'll need to restore the damaged old magic cauldron.\n",
        # ADVENTURE 4 - Make a leather magic hat
        31: "🥘 <b>Mission 31</b> – The blacksmith dwarf who repaired the cauldron noticed that your wizard didn't have a magic hat. He proposed a jo-ken-po challenge and, if you win, he will give you a <b>magic hat</b> made of fabric with star prints.\n",
        32: "🧙🏼‍♂️ <b>Mission 32</b> – <i>You can also make a beautiful magic leather hat</i>. To do this, you need to find some materials in town. Try to get a piece of <b>leather</b>.\n",
        33: "🧙🏼‍♂️ <b>Mission 33</b> – <i>You can also make a beautiful magic leather hat</i>. To do this, you need to find some materials in town. Try to get another piece of <b>leather</b>.\n",
        34: "🧙🏼‍♂️ <b>Mission 34</b> – <i>You can also make a beautiful magic leather hat</i>. To do this, you need to find some materials in town. Try to get another piece of <b>leather</b>.\n",
        35: "🧙🏼‍♂️ <b>Mission 35</b> – <i>You can also make a beautiful magic leather hat</i>. To do this, you need to find some materials in town. Try to get another piece of <b>leather</b>.\n",
        36: "🧙🏼‍♂️ <b>Mission 36</b> – <i>You can also make a beautiful magic leather hat</i>. To do this, you need to find some materials in town. Try to get another piece of <b>leather</b>.\n",
        37: "🧙🏼‍♂️ <b>Mission 37</b> – <i>You can also make a beautiful magic leather hat</i>. To do this, you need to find some materials in town. Try to get a piece of <b>iron</b> to make a beautiful buckle for your magic hat.\n",
        38: "🧙🏼‍♂️ <b>Mission 38</b> – <i>You can also make a beautiful magic leather hat</i>. To do this, you need to find some materials in town. Try to get a piece of <b>iron</b> to make a beautiful buckle for your magic hat.\n",
        39: "🧙🏼‍♂️ <b>Mission 39</b> – <i>You can also make a beautiful magic leather hat</i>. To do this, you need to find some materials in town. Try to get a piece of <b>iron</b> to make a beautiful buckle for your magic hat.\n",
        40: "🧙🏼‍♂️ <b>Mission 40</b> – <i>You can also make a beautiful magic leather hat</i>. To do this, you need to find some materials in town. Now you need a <b>needle and thread</b> to sew your magic leather hat.\n",
        # ADVENTURE 5 - Make a iron pickaxe
        41: "⛏ <b>Mission 41</b> – <i>For the next adventures you will need a pickaxe</i>. To do this, you need to find some materials on the way to the dwarves' mine. Try to get a piece of <b>wood</b> in the forest.\n",
        42: "⛏ <b>Mission 42</b> – <i>For the next adventures you will need a pickaxe</i>. To do this, you need to find some materials on the way to the dwarves' mine. Try to get a piece of <b>wood</b> in the forest.\n",
        43: "⛏ <b>Mission 43</b> – <i>For the next adventures you will need a pickaxe</i>. To do this, you need to find some materials on the way to the dwarves' mine. Try to get a piece of <b>wood</b> in the forest.\n",
        44: "⛏ <b>Mission 44</b> – <i>For the next adventures you will need a pickaxe</i>. To do this, you need to find some materials on the way to the dwarves' mine. Try to get a piece of <b>wood</b> in the forest.\n",
        45: "⛏ <b>Mission 45</b> – <i>For the next adventures you will need a pickaxe</i>. To do this, you need to find some materials on the way to the dwarves' mine. Try to get a piece of <b>wood</b> in the forest.\n",
        46: "⛏ <b>Mission 46</b> – <i>For the next adventures you will need a pickaxe</i>. Try to steal a piece of <b>iron</b> from the mining dwarves.\n",
        47: "⛏ <b>Mission 47</b> – <i>For the next adventures you will need a pickaxe</i>. Try to steal a piece of <b>iron</b> from the mining dwarves.\n",
        48: "⛏ <b>Mission 48</b> – <i>For the next adventures you will need a pickaxe</i>. Try to steal a piece of <b>iron</b> from the mining dwarves.\n",
        49: "⛏ <b>Mission 49</b> – <i>For the next adventures you will need a pickaxe</i>. Try to steal a piece of <b>iron</b> from the mining dwarves.\n",
        50: "⛏ <b>Mission 50</b> – <i>For the next adventures you will need a pickaxe</i>. Try to steal a piece of <b>iron</b> from the mining dwarves. At the end of this adventure, remember to make your pickaxe.\n",
        # ADVENTURE 6 - Mine ruby to make some new blends
        51: "♦️ <b>Mission 51</b> – With your pick you can extract some materials from the dwarf mine. Use it and see what ores you can mine.",
        52: "♦️ <b>Mission 52</b> – With your pick you can extract some materials from the dwarf mine. Use it and see what ores you can mine.",
        53: "♦️ <b>Mission 53</b> – With your pick you can extract some materials from the dwarf mine. Use it and see what ores you can mine.",
        54: "♦️ <b>Mission 54</b> – With your pick you can extract some materials from the dwarf mine. Use it and see what ores you can mine.",
        55: "♦️ <b>Mission 55</b> – With your pick you can extract some materials from the dwarf mine. Use it and see what ores you can mine.",
        56: "♦️ <b>Mission 56</b> – With your pick you can extract some materials from the dwarf mine. Use it and see what ores you can mine.",
        57: "♦️ <b>Mission 57</b> – With your pick you can extract some materials from the dwarf mine. Use it and see what ores you can mine.",
        58: "♦️ <b>Mission 58</b> – With your pick you can extract some materials from the dwarf mine. Use it and see what ores you can mine.",
        59: "♦️ <b>Mission 59</b> – With your pick you can extract some materials from the dwarf mine. Use it and see what ores you can mine.",
        60: "♦️ <b>Mission 60</b> – With your pick you can extract some materials from the dwarf mine. Use it and see what ores you can mine.",
        # ADVENTURE 7 - Mine Sapphire to make some new blends
        61: "🔹 <b>Mission 61</b> – Keep using your pickaxe to find some sapphires in the dwarf miners' mine. See which ores you can mine.",
        62: "🔹 <b>Mission 62</b> – Keep using your pickaxe to find some sapphires in the dwarf miners' mine. See which ores you can mine.",
        63: "🔹 <b>Mission 63</b> – Keep using your pickaxe to find some sapphires in the dwarf miners' mine. See which ores you can mine.",
        64: "🔹 <b>Mission 64</b> – Keep using your pickaxe to find some sapphires in the dwarf miners' mine. See which ores you can mine.",
        65: "🔹 <b>Mission 65</b> – Keep using your pickaxe to find some sapphires in the dwarf miners' mine. See which ores you can mine.",
        66: "🔹 <b>Mission 66</b> – Keep using your pickaxe to find some sapphires in the dwarf miners' mine. See which ores you can mine.",
        67: "🔹 <b>Mission 67</b> – Keep using your pickaxe to find some sapphires in the dwarf miners' mine. See which ores you can mine.",
        68: "🔹 <b>Mission 68</b> – Keep using your pickaxe to find some sapphires in the dwarf miners' mine. See which ores you can mine.",
        69: "🔹 <b>Mission 69</b> – Keep using your pickaxe to find some sapphires in the dwarf miners' mine. See which ores you can mine.",
        70: "🔹 <b>Mission 70</b> – Keep using your pickaxe to find some sapphires in the dwarf miners' mine. See which ores you can mine.",
        # ADVENTURE 8 - Mine Emerald to make some new blends
        71: "🟢 <b>Mission 71</b> – Keep using your pickaxe to find some emeralds in the dwarf miners' mine. See which ores you can mine.",
        72: "🟢 <b>Mission 72</b> – Keep using your pickaxe to find some emeralds in the dwarf miners' mine. See which ores you can mine.",
        73: "🟢 <b>Mission 73</b> – Keep using your pickaxe to find some emeralds in the dwarf miners' mine. See which ores you can mine.",
        74: "🟢 <b>Mission 74</b> – Keep using your pickaxe to find some emeralds in the dwarf miners' mine. See which ores you can mine.",
        75: "🟢 <b>Mission 75</b> – Keep using your pickaxe to find some emeralds in the dwarf miners' mine. See which ores you can mine.",
        76: "🟢 <b>Mission 76</b> – Keep using your pickaxe to find some emeralds in the dwarf miners' mine. See which ores you can mine.",
        77: "🟢 <b>Mission 77</b> – Keep using your pickaxe to find some emeralds in the dwarf miners' mine. See which ores you can mine.",
        78: "🟢 <b>Mission 78</b> – Keep using your pickaxe to find some emeralds in the dwarf miners' mine. See which ores you can mine.",
        79: "🟢 <b>Mission 79</b> – Keep using your pickaxe to find some emeralds in the dwarf miners' mine. See which ores you can mine.",
        80: "🟢 <b>Mission 80</b> – Keep using your pickaxe to find some emeralds in the dwarf miners' mine. See which ores you can mine.",
        # ADVENTURE 9 - Mine Amethyst to make some new blends
        81: "🟣 <b>Mission 81</b> – Keep using your pickaxe to find some amethyst in the dwarf miners' mine. See which ores you can mine.",
        82: "🟣 <b>Mission 82</b> – Keep using your pickaxe to find some amethyst in the dwarf miners' mine. See which ores you can mine.",
        83: "🟣 <b>Mission 83</b> – Keep using your pickaxe to find some amethyst in the dwarf miners' mine. See which ores you can mine.",
        84: "🟣 <b>Mission 84</b> – Keep using your pickaxe to find some amethyst in the dwarf miners' mine. See which ores you can mine.",
        85: "🟣 <b>Mission 85</b> – Keep using your pickaxe to find some amethyst in the dwarf miners' mine. See which ores you can mine.",
        86: "🟣 <b>Mission 86</b> – Keep using your pickaxe to find some amethyst in the dwarf miners' mine. See which ores you can mine.",
        87: "🟣 <b>Mission 87</b> – Keep using your pickaxe to find some amethyst in the dwarf miners' mine. See which ores you can mine.",
        88: "🟣 <b>Mission 88</b> – Keep using your pickaxe to find some amethyst in the dwarf miners' mine. See which ores you can mine.",
        89: "🟣 <b>Mission 89</b> – Keep using your pickaxe to find some amethyst in the dwarf miners' mine. See which ores you can mine.",
        90: "🟣 <b>Mission 90</b> – Keep using your pickaxe to find some amethyst in the dwarf miners' mine. See which ores you can mine.",
        # ADVENTURE 10 - Kill the spiders and collect all the ruby dust to use in new potions.
        91: "🔻 <b>Mission 91</b> – Kill the spiders and collect all the <b>ruby dust</b> to use in new potions.\n",
        92: "🔻 <b>Mission 92</b> – Kill the spiders and collect all the <b>ruby dust</b> to use in new potions.\n",
        93: "🔻 <b>Mission 93</b> – Kill the spiders and collect all the <b>ruby dust</b> to use in new potions.\n",
        94: "🔻 <b>Mission 94</b> – Kill the spiders and collect all the <b>ruby dust</b> to use in new potions.\n",
        95: "🔻 <b>Mission 95</b> – Kill the spiders and collect all the <b>ruby dust</b> to use in new potions.\n",
        96: "🔻 <b>Mission 96</b> – Kill the spiders and collect all the <b>ruby dust</b> to use in new potions.\n",
        97: "🔻 <b>Mission 97</b> – Kill the spiders and collect all the <b>ruby dust</b> to use in new potions.\n",
        98: "🔻 <b>Mission 98</b> – Kill the spiders and collect all the <b>ruby dust</b> to use in new potions.\n",
        99: "🔻 <b>Mission 99</b> – Kill the spiders and collect all the <b>ruby dust</b> to use in new potions.\n",
        100: "🔻 <b>Mission 100</b> – Kill the spiders and collect all the <b>ruby dust</b> to use in new potions.\n",
        # ADVENTURE 11 - Kill the spiders and collect all the sapphire dust to use in new potions.
        101: "🔹 <b>Mission 101</b> – Kill the spiders and collect all the <b>sapphire dust</b> to use in new potions.\n",
        102: "🔹 <b>Mission 102</b> – Kill the spiders and collect all the <b>sapphire dust</b> to use in new potions.\n",
        103: "🔹 <b>Mission 103</b> – Kill the spiders and collect all the <b>sapphire dust</b> to use in new potions.\n",
        104: "🔹 <b>Mission 104</b> – Kill the spiders and collect all the <b>sapphire dust</b> to use in new potions.\n",
        105: "🔹 <b>Mission 105</b> – Kill the spiders and collect all the <b>sapphire dust</b> to use in new potions.\n",
        106: "🔹 <b>Mission 106</b> – Kill the spiders and collect all the <b>sapphire dust</b> to use in new potions.\n",
        107: "🔹 <b>Mission 107</b> – Kill the spiders and collect all the <b>sapphire dust</b> to use in new potions.\n",
        108: "🔹 <b>Mission 108</b> – Kill the spiders and collect all the <b>sapphire dust</b> to use in new potions.\n",
        109: "🔹 <b>Mission 109</b> – Kill the spiders and collect all the <b>sapphire dust</b> to use in new potions.\n",
        110: "🔹 <b>Mission 110</b> – Kill the spiders and collect all the <b>sapphire dust</b> to use in new potions.\n",
        # ADVENTURE 12 - Kill the spiders and collect all the emerald dust to use in new potions.
        111: "🟢 <b>Mission 111</b> – Kill the spiders and collect all the <b>emerald dust</b> to use in new potions.\n",
        112: "🟢 <b>Mission 112</b> – Kill the spiders and collect all the <b>emerald dust</b> to use in new potions.\n",
        113: "🟢 <b>Mission 113</b> – Kill the spiders and collect all the <b>emerald dust</b> to use in new potions.\n",
        114: "🟢 <b>Mission 114</b> – Kill the spiders and collect all the <b>emerald dust</b> to use in new potions.\n",
        115: "🟢 <b>Mission 115</b> – Kill the spiders and collect all the <b>emerald dust</b> to use in new potions.\n",
        116: "🟢 <b>Mission 116</b> – Kill the spiders and collect all the <b>emerald dust</b> to use in new potions.\n",
        117: "🟢 <b>Mission 117</b> – Kill the spiders and collect all the <b>emerald dust</b> to use in new potions.\n",
        118: "🟢 <b>Mission 118</b> – Kill the spiders and collect all the <b>emerald dust</b> to use in new potions.\n",
        119: "🟢 <b>Mission 119</b> – Kill the spiders and collect all the <b>emerald dust</b> to use in new potions.\n",
        120: "🟢 <b>Mission 120</b> – Kill the spiders and collect all the <b>emerald dust</b> to use in new potions.\n",
        # ADVENTURE 13 - Kill the spiders and collect all the amethyst dust to use in new potions.
        121: "🟣 <b>Mission 121</b> – Kill the spiders and collect all the <b>amethyst dust</b> to use in new potions.\n",
        122: "🟣 <b>Mission 122</b> – Kill the spiders and collect all the <b>amethyst dust</b> to use in new potions.\n",
        123: "🟣 <b>Mission 123</b> – Kill the spiders and collect all the <b>amethyst dust</b> to use in new potions.\n",
        124: "🟣 <b>Mission 124</b> – Kill the spiders and collect all the <b>amethyst dust</b> to use in new potions.\n",
        125: "🟣 <b>Mission 125</b> – Kill the spiders and collect all the <b>amethyst dust</b> to use in new potions.\n",
        126: "🟣 <b>Mission 126</b> – Kill the spiders and collect all the <b>amethyst dust</b> to use in new potions.\n",
        127: "🟣 <b>Mission 127</b> – Kill the spiders and collect all the <b>amethyst dust</b> to use in new potions.\n",
        128: "🟣 <b>Mission 128</b> – Kill the spiders and collect all the <b>amethyst dust</b> to use in new potions.\n",
        129: "🟣 <b>Mission 129</b> – Kill the spiders and collect all the <b>amethyst dust</b> to use in new potions.\n",
        130: "🟣 <b>Mission 130</b> – Kill the spiders and collect all the <b>amethyst dust</b> to use in new potions.\n",
        # ADVENTURE 14 - Navigate through the Enchanted Forest to find the hidden entrance to the lost Temple of Elements.
        131: "🗝 <b>Mission 131</b> – Defend yourself from the spirits of the <b>Enchanted Forest</b> and find the entrance to the Temple of the Elements.\n     Collect prizes along the way to craft the magical bronze key needed to open the Temple's door.\n",
        132: "🗝 <b>Mission 132</b> – Defend yourself from the spirits of the <b>Enchanted Forest</b> and find the entrance to the Temple of the Elements.\n     Collect prizes along the way to craft the magical bronze key needed to open the Temple's door.\n",
        133: "🗝 <b>Mission 133</b> – Defend yourself from the spirits of the <b>Enchanted Forest</b> and find the entrance to the Temple of the Elements.\n     Collect prizes along the way to craft the magical bronze key needed to open the Temple's door.\n",
        134: "🗝 <b>Mission 134</b> – Defend yourself from the spirits of the <b>Enchanted Forest</b> and find the entrance to the Temple of the Elements.\n     Collect prizes along the way to craft the magical bronze key needed to open the Temple's door.\n",
        135: "🗝 <b>Mission 135</b> – Defend yourself from the spirits of the <b>Enchanted Forest</b> and find the entrance to the Temple of the Elements.\n     Collect prizes along the way to craft the magical bronze key needed to open the Temple's door.\n",
        136: "🗝 <b>Mission 136</b> – Defend yourself from the spirits of the <b>Enchanted Forest</b> and find the entrance to the Temple of the Elements.\n     Collect prizes along the way to craft the magical bronze key needed to open the Temple's door.\n",
        137: "🗝 <b>Mission 137</b> – Defend yourself from the spirits of the <b>Enchanted Forest</b> and find the entrance to the Temple of the Elements.\n     Collect prizes along the way to craft the magical bronze key needed to open the Temple's door.\n",
        138: "🗝 <b>Mission 138</b> – Defend yourself from the spirits of the <b>Enchanted Forest</b> and find the entrance to the Temple of the Elements.\n     Collect prizes along the way to craft the magical bronze key needed to open the Temple's door.\n",
        139: "🗝 <b>Mission 139</b> – Defend yourself from the spirits of the <b>Enchanted Forest</b> and find the entrance to the Temple of the Elements.\n     Collect prizes along the way to craft the magical bronze key needed to open the Temple's door.\n",
        140: "🗝 <b>Mission 140</b> – Defend yourself from the spirits of the <b>Enchanted Forest</b> and find the entrance to the Temple of the Elements.\n     Collect prizes along the way to craft the magical bronze key needed to open the Temple's door.\n",
        # ADVENTURE 15 - Master the Water Element.
        141: "💧 <b>Mission 141</b> – A water spirit must be defeated to give you the item you need to master the Water Element.\n",
        142: "💧 <b>Mission 142</b> – A water spirit must be defeated to give you the item you need to master the Water Element.\n",
        143: "💧 <b>Mission 143</b> – A water spirit must be defeated to give you the item you need to master the Water Element.\n",
        144: "💧 <b>Mission 144</b> – A water spirit must be defeated to give you the item you need to master the Water Element.\n",
        145: "💧 <b>Mission 145</b> – A water spirit must be defeated to give you the item you need to master the Water Element.\n",
        146: "💧 <b>Mission 146</b> – A water spirit must be defeated to give you the item you need to master the Water Element.\n",
        147: "💧 <b>Mission 147</b> – A water spirit must be defeated to give you the item you need to master the Water Element.\n",
        148: "💧 <b>Mission 148</b> – A water spirit must be defeated to give you the item you need to master the Water Element.\n",
        149: "💧 <b>Mission 149</b> – A water spirit must be defeated to give you the item you need to master the Water Element.\n",
        150: "💧 <b>Mission 150</b> – A water spirit must be defeated to give you the item you need to master the Water Element.\n",
        # ADVENTURE 16 - Master the Fire Element.
        151: "🔥 <b>Mission 151</b> – A fire spirit must be defeated to give you the item you need to master the Fire Element.\n",
        152: "🔥 <b>Mission 152</b> – A fire spirit must be defeated to give you the item you need to master the Fire Element.\n",
        153: "🔥 <b>Mission 153</b> – A fire spirit must be defeated to give you the item you need to master the Fire Element.\n",
        154: "🔥 <b>Mission 154</b> – A fire spirit must be defeated to give you the item you need to master the Fire Element.\n",
        155: "🔥 <b>Mission 155</b> – A fire spirit must be defeated to give you the item you need to master the Fire Element.\n",
        156: "🔥 <b>Mission 156</b> – A fire spirit must be defeated to give you the item you need to master the Fire Element.\n",
        157: "🔥 <b>Mission 157</b> – A fire spirit must be defeated to give you the item you need to master the Fire Element.\n",
        158: "🔥 <b>Mission 158</b> – A fire spirit must be defeated to give you the item you need to master the Fire Element.\n",
        159: "🔥 <b>Mission 159</b> – A fire spirit must be defeated to give you the item you need to master the Fire Element.\n",
        160: "🔥 <b>Mission 160</b> – A fire spirit must be defeated to give you the item you need to master the Fire Element.\n",
        # ADVENTURE 17 - Get all Water Elemental Stones.
        161: "💧 <b>Mission 161</b> – Open the door of the old locker and find a Water Elemental Stone.\nThe password has <b>5 digits</b> (numbers 1 to 9). \nUse the <b>/pass <i>99999</i> </b>command (replace <i>99999</i> with your password attempt).",
        162: "💧 <b>Mission 162</b> – Open the door of the old locker and find a Water Elemental Stone.\nThe password has <b>5 digits</b> (numbers 1 to 9). \nUse the <b>/pass <i>99999</i> </b>command (replace <i>99999</i> with your password attempt).",
        163: "💧 <b>Mission 163</b> – Open the door of the old locker and find a Water Elemental Stone.\nThe password has <b>5 digits</b> (numbers 1 to 9). \nUse the <b>/pass <i>99999</i> </b>command (replace <i>99999</i> with your password attempt).",
        164: "💧 <b>Mission 164</b> – Open the door of the old locker and find a Water Elemental Stone.\nThe password has <b>5 digits</b> (numbers 1 to 9). \nUse the <b>/pass <i>99999</i> </b>command (replace <i>99999</i> with your password attempt).",
        165: "💧 <b>Mission 165</b> – Open the door of the old locker and find a Water Elemental Stone.\nThe password has <b>5 digits</b> (numbers 1 to 9). \nUse the <b>/pass <i>99999</i> </b>command (replace <i>99999</i> with your password attempt).",
        166: "💧 <b>Mission 166</b> – Open the door of the old locker and find a Water Elemental Stone.\nThe password has <b>5 digits</b> (numbers 1 to 9). \nUse the <b>/pass <i>99999</i> </b>command (replace <i>99999</i> with your password attempt).",
        167: "💧 <b>Mission 167</b> – Open the door of the old locker and find a Water Elemental Stone.\nThe password has <b>5 digits</b> (numbers 1 to 9). \nUse the <b>/pass <i>99999</i> </b>command (replace <i>99999</i> with your password attempt).",
        168: "💧 <b>Mission 168</b> – Open the door of the old locker and find a Water Elemental Stone.\nThe password has <b>5 digits</b> (numbers 1 to 9). \nUse the <b>/pass <i>99999</i> </b>command (replace <i>99999</i> with your password attempt).",
        169: "💧 <b>Mission 169</b> – Open the door of the old locker and find a Water Elemental Stone.\nThe password has <b>5 digits</b> (numbers 1 to 9). \nUse the <b>/pass <i>99999</i> </b>command (replace <i>99999</i> with your password attempt).",
        170: "💧 <b>Mission 170</b> – Open the door of the old locker and find a Water Elemental Stone.\nThe password has <b>5 digits</b> (numbers 1 to 9). \nUse the <b>/pass <i>99999</i> </b>command (replace <i>99999</i> with your password attempt).",
        # ADVENTURE 18 - Get all Wind Elemental Stones.
        171: "🌬 <b>Mission 171</b> – Open the door of the old locker and find a Wind Elemental Stone.\nThe password has <b>5 digits</b> (numbers 1 to 9). \nUse the <b>/pass <i>99999</i> </b>command (replace <i>99999</i> with your password attempt).",
        172: "🌬 <b>Mission 172</b> – Open the door of the old locker and find a Wind Elemental Stone.\nThe password has <b>5 digits</b> (numbers 1 to 9). \nUse the <b>/pass <i>99999</i> </b>command (replace <i>99999</i> with your password attempt).",
        173: "🌬 <b>Mission 173</b> – Open the door of the old locker and find a Wind Elemental Stone.\nThe password has <b>5 digits</b> (numbers 1 to 9). \nUse the <b>/pass <i>99999</i> </b>command (replace <i>99999</i> with your password attempt).",
        174: "🌬 <b>Mission 174</b> – Open the door of the old locker and find a Wind Elemental Stone.\nThe password has <b>5 digits</b> (numbers 1 to 9). \nUse the <b>/pass <i>99999</i> </b>command (replace <i>99999</i> with your password attempt).",
        175: "🌬 <b>Mission 175</b> – Open the door of the old locker and find a Wind Elemental Stone.\nThe password has <b>5 digits</b> (numbers 1 to 9). \nUse the <b>/pass <i>99999</i> </b>command (replace <i>99999</i> with your password attempt).",
        176: "🌬 <b>Mission 176</b> – Open the door of the old locker and find a Wind Elemental Stone.\nThe password has <b>5 digits</b> (numbers 1 to 9). \nUse the <b>/pass <i>99999</i> </b>command (replace <i>99999</i> with your password attempt).",
        177: "🌬 <b>Mission 177</b> – Open the door of the old locker and find a Wind Elemental Stone.\nThe password has <b>5 digits</b> (numbers 1 to 9). \nUse the <b>/pass <i>99999</i> </b>command (replace <i>99999</i> with your password attempt).",
        178: "🌬 <b>Mission 178</b> – Open the door of the old locker and find a Wind Elemental Stone.\nThe password has <b>5 digits</b> (numbers 1 to 9). \nUse the <b>/pass <i>99999</i> </b>command (replace <i>99999</i> with your password attempt).",
        179: "🌬 <b>Mission 179</b> – Open the door of the old locker and find a Wind Elemental Stone.\nThe password has <b>5 digits</b> (numbers 1 to 9). \nUse the <b>/pass <i>99999</i> </b>command (replace <i>99999</i> with your password attempt).",
        180: "🌬 <b>Mission 180</b> – Open the door of the old locker and find a Wind Elemental Stone.\nThe password has <b>5 digits</b> (numbers 1 to 9). \nUse the <b>/pass <i>99999</i> </b>command (replace <i>99999</i> with your password attempt).",
        # ADVENTURE 19 - Get all Earth Elemental Stones.
        181: "🌍 <b>Mission 181</b> – Open the door of the old locker and find a Earth Elemental Stone.\nThe password has <b>5 digits</b> (numbers 1 to 9). \nUse the <b>/pass <i>99999</i> </b>command (replace <i>99999</i> with your password attempt).",
        182: "🌍 <b>Mission 182</b> – Open the door of the old locker and find a Earth Elemental Stone.\nThe password has <b>5 digits</b> (numbers 1 to 9). \nUse the <b>/pass <i>99999</i> </b>command (replace <i>99999</i> with your password attempt).",
        183: "🌍 <b>Mission 183</b> – Open the door of the old locker and find a Earth Elemental Stone.\nThe password has <b>5 digits</b> (numbers 1 to 9). \nUse the <b>/pass <i>99999</i> </b>command (replace <i>99999</i> with your password attempt).",
        184: "🌍 <b>Mission 184</b> – Open the door of the old locker and find a Earth Elemental Stone.\nThe password has <b>5 digits</b> (numbers 1 to 9). \nUse the <b>/pass <i>99999</i> </b>command (replace <i>99999</i> with your password attempt).",
        185: "🌍 <b>Mission 185</b> – Open the door of the old locker and find a Earth Elemental Stone.\nThe password has <b>5 digits</b> (numbers 1 to 9). \nUse the <b>/pass <i>99999</i> </b>command (replace <i>99999</i> with your password attempt).",
        186: "🌍 <b>Mission 186</b> – Open the door of the old locker and find a Earth Elemental Stone.\nThe password has <b>5 digits</b> (numbers 1 to 9). \nUse the <b>/pass <i>99999</i> </b>command (replace <i>99999</i> with your password attempt).",
        187: "🌍 <b>Mission 187</b> – Open the door of the old locker and find a Earth Elemental Stone.\nThe password has <b>5 digits</b> (numbers 1 to 9). \nUse the <b>/pass <i>99999</i> </b>command (replace <i>99999</i> with your password attempt).",
        188: "🌍 <b>Mission 188</b> – Open the door of the old locker and find a Earth Elemental Stone.\nThe password has <b>5 digits</b> (numbers 1 to 9). \nUse the <b>/pass <i>99999</i> </b>command (replace <i>99999</i> with your password attempt).",
        189: "🌍 <b>Mission 189</b> – Open the door of the old locker and find a Earth Elemental Stone.\nThe password has <b>5 digits</b> (numbers 1 to 9). \nUse the <b>/pass <i>99999</i> </b>command (replace <i>99999</i> with your password attempt).",
        190: "🌍 <b>Mission 190</b> – Open the door of the old locker and find a Earth Elemental Stone.\nThe password has <b>5 digits</b> (numbers 1 to 9). \nUse the <b>/pass <i>99999</i> </b>command (replace <i>99999</i> with your password attempt).",
        # ADVENTURE 20 - Get all Fire Elemental Stones.
        191: "🔥 <b>Mission 191</b> – Open the door of the old locker and find a Fire Elemental Stone.\nThe password has <b>5 digits</b> (numbers 1 to 9). \nUse the <b>/pass <i>99999</i> </b>command (replace <i>99999</i> with your password attempt).",
        192: "🔥 <b>Mission 192</b> – Open the door of the old locker and find a Fire Elemental Stone.\nThe password has <b>5 digits</b> (numbers 1 to 9). \nUse the <b>/pass <i>99999</i> </b>command (replace <i>99999</i> with your password attempt).",
        193: "🔥 <b>Mission 193</b> – Open the door of the old locker and find a Fire Elemental Stone.\nThe password has <b>5 digits</b> (numbers 1 to 9). \nUse the <b>/pass <i>99999</i> </b>command (replace <i>99999</i> with your password attempt).",
        194: "🔥 <b>Mission 194</b> – Open the door of the old locker and find a Fire Elemental Stone.\nThe password has <b>5 digits</b> (numbers 1 to 9). \nUse the <b>/pass <i>99999</i> </b>command (replace <i>99999</i> with your password attempt).",
        195: "🔥 <b>Mission 195</b> – Open the door of the old locker and find a Fire Elemental Stone.\nThe password has <b>5 digits</b> (numbers 1 to 9). \nUse the <b>/pass <i>99999</i> </b>command (replace <i>99999</i> with your password attempt).",
        196: "🔥 <b>Mission 196</b> – Open the door of the old locker and find a Fire Elemental Stone.\nThe password has <b>5 digits</b> (numbers 1 to 9). \nUse the <b>/pass <i>99999</i> </b>command (replace <i>99999</i> with your password attempt).",
        197: "🔥 <b>Mission 197</b> – Open the door of the old locker and find a Fire Elemental Stone.\nThe password has <b>5 digits</b> (numbers 1 to 9). \nUse the <b>/pass <i>99999</i> </b>command (replace <i>99999</i> with your password attempt).",
        198: "🔥 <b>Mission 198</b> – Open the door of the old locker and find a Fire Elemental Stone.\nThe password has <b>5 digits</b> (numbers 1 to 9). \nUse the <b>/pass <i>99999</i> </b>command (replace <i>99999</i> with your password attempt).",
        199: "🔥 <b>Mission 199</b> – Open the door of the old locker and find a Fire Elemental Stone.\nThe password has <b>5 digits</b> (numbers 1 to 9). \nUse the <b>/pass <i>99999</i> </b>command (replace <i>99999</i> with your password attempt).",
        200: "🔥 <b>Mission 200</b> – Open the door of the old locker and find a Fire Elemental Stone.\nThe password has <b>5 digits</b> (numbers 1 to 9). \nUse the <b>/pass <i>99999</i> </b>command (replace <i>99999</i> with your password attempt).",
        # ADVENTURE 21 - Collect the fragments of the map to Eldoria.
        201: "🗺 <b>Mission 201</b> – Collect the fragments of the map to Eldoria. You need to defeat the pirate to receive one of the map fragments.",
        202: "🗺 <b>Mission 202</b> – Collect the fragments of the map to Eldoria. You need to defeat the pirate to receive one of the map fragments.",
        203: "🗺 <b>Mission 203</b> – Collect the fragments of the map to Eldoria. You need to defeat the pirate to receive one of the map fragments.",
        204: "🗺 <b>Mission 204</b> – Collect the fragments of the map to Eldoria. You need to defeat the pirate to receive one of the map fragments.",
        205: "🗺 <b>Mission 205</b> – Collect the fragments of the map to Eldoria. You need to defeat the pirate to receive one of the map fragments.",
        206: "🗺 <b>Mission 206</b> – Collect the fragments of the map to Eldoria. You need to defeat the pirate to receive one of the map fragments.",
        207: "🗺 <b>Mission 207</b> – Collect the fragments of the map to Eldoria. You need to defeat the pirate to receive one of the map fragments.",
        208: "🗺 <b>Mission 208</b> – Collect the fragments of the map to Eldoria. You need to defeat the pirate to receive one of the map fragments.",
        209: "🗺 <b>Mission 209</b> – Collect the fragments of the map to Eldoria. You need to defeat the pirate to receive one of the map fragments.",
        210: "🗺 <b>Mission 210</b> – Collect the fragments of the map to Eldoria. You need to defeat the pirate to receive one of the map fragments.",
        # ADVENTURE 22 - Collect more fragments of the map to Eldoria.
        211: "🗺 <b>Mission 211</b> – Collect the fragments of the map to Eldoria. You need to defeat the pirate to receive one of the map fragments.",
        212: "🗺 <b>Mission 212</b> – Collect the fragments of the map to Eldoria. You need to defeat the pirate to receive one of the map fragments.",
        213: "🗺 <b>Mission 213</b> – Collect the fragments of the map to Eldoria. You need to defeat the pirate to receive one of the map fragments.",
        214: "🗺 <b>Mission 214</b> – Collect the fragments of the map to Eldoria. You need to defeat the pirate to receive one of the map fragments.",
        215: "🗺 <b>Mission 215</b> – Collect the fragments of the map to Eldoria. You need to defeat the pirate to receive one of the map fragments.",
        216: "🗺 <b>Mission 216</b> – Collect the fragments of the map to Eldoria. You need to defeat the pirate to receive one of the map fragments.",
        217: "🗺 <b>Mission 217</b> – Collect the fragments of the map to Eldoria. You need to defeat the pirate to receive one of the map fragments.",
        218: "🗺 <b>Mission 218</b> – Collect the fragments of the map to Eldoria. You need to defeat the pirate to receive one of the map fragments.",
        219: "🗺 <b>Mission 219</b> – Collect the fragments of the map to Eldoria. You need to defeat the pirate to receive one of the map fragments.",
        220: "🗺 <b>Mission 220</b> – Collect the fragments of the map to Eldoria. You need to defeat the pirate to receive one of the map fragments.",
        # ADVENTURE 23 - Collect all Celestial Sun Stones.
        221: "🌞 <b>Mission 221</b> – Collect the Sun Celestial Stones. You need to find the password that opens the compartment in the ruins of the Temple of the Sun where the stones are hidden.",
        222: "🌞 <b>Mission 222</b> – Collect the Sun Celestial Stones. You need to find the password that opens the compartment in the ruins of the Temple of the Sun where the stones are hidden.",
        223: "🌞 <b>Mission 223</b> – Collect the Sun Celestial Stones. You need to find the password that opens the compartment in the ruins of the Temple of the Sun where the stones are hidden.",
        224: "🌞 <b>Mission 224</b> – Collect the Sun Celestial Stones. You need to find the password that opens the compartment in the ruins of the Temple of the Sun where the stones are hidden.",
        225: "🌞 <b>Mission 225</b> – Collect the Sun Celestial Stones. You need to find the password that opens the compartment in the ruins of the Temple of the Sun where the stones are hidden.",
        226: "🌞 <b>Mission 226</b> – Collect the Sun Celestial Stones. You need to find the password that opens the compartment in the ruins of the Temple of the Sun where the stones are hidden.",
        227: "🌞 <b>Mission 227</b> – Collect the Sun Celestial Stones. You need to find the password that opens the compartment in the ruins of the Temple of the Sun where the stones are hidden.",
        228: "🌞 <b>Mission 228</b> – Collect the Sun Celestial Stones. You need to find the password that opens the compartment in the ruins of the Temple of the Sun where the stones are hidden.",
        229: "🌞 <b>Mission 229</b> – Collect the Sun Celestial Stones. You need to find the password that opens the compartment in the ruins of the Temple of the Sun where the stones are hidden.",
        230: "🌞 <b>Mission 230</b> – Collect the Sun Celestial Stones. You need to find the password that opens the compartment in the ruins of the Temple of the Sun where the stones are hidden.",
        # ADVENTURE 24 - Collect all Celestial Moon Stones.
        231: "🌔 <b>Mission 231</b> – Collect the Moon Celestial Stones. You need to find the password that opens the compartment in the ruins of the Temple of the Moon where the stones are hidden.",
        232: "🌔 <b>Mission 232</b> – Collect the Moon Celestial Stones. You need to find the password that opens the compartment in the ruins of the Temple of the Moon where the stones are hidden.",
        233: "🌔 <b>Mission 233</b> – Collect the Moon Celestial Stones. You need to find the password that opens the compartment in the ruins of the Temple of the Moon where the stones are hidden.",
        234: "🌔 <b>Mission 234</b> – Collect the Moon Celestial Stones. You need to find the password that opens the compartment in the ruins of the Temple of the Moon where the stones are hidden.",
        235: "🌔 <b>Mission 235</b> – Collect the Moon Celestial Stones. You need to find the password that opens the compartment in the ruins of the Temple of the Moon where the stones are hidden.",
        236: "🌔 <b>Mission 236</b> – Collect the Moon Celestial Stones. You need to find the password that opens the compartment in the ruins of the Temple of the Moon where the stones are hidden.",
        237: "🌔 <b>Mission 237</b> – Collect the Moon Celestial Stones. You need to find the password that opens the compartment in the ruins of the Temple of the Moon where the stones are hidden.",
        238: "🌔 <b>Mission 238</b> – Collect the Moon Celestial Stones. You need to find the password that opens the compartment in the ruins of the Temple of the Moon where the stones are hidden.",
        239: "🌔 <b>Mission 239</b> – Collect the Moon Celestial Stones. You need to find the password that opens the compartment in the ruins of the Temple of the Moon where the stones are hidden.",
        240: "🌔 <b>Mission 240</b> – Collect the Moon Celestial Stones. You need to find the password that opens the compartment in the ruins of the Temple of the Moon where the stones are hidden.",
        # ADVENTURE 25 - Collect all Celestial Venus Stones.
        241: "🔵 <b>Mission 241</b> – Collect the Venus Celestial Stones. You need to find the password that opens the compartment in the ruins of the Temple of Venus where the stones are hidden.",
        242: "🔵 <b>Mission 242</b> – Collect the Venus Celestial Stones. You need to find the password that opens the compartment in the ruins of the Temple of Venus where the stones are hidden.",
        243: "🔵 <b>Mission 243</b> – Collect the Venus Celestial Stones. You need to find the password that opens the compartment in the ruins of the Temple of Venus where the stones are hidden.",
        244: "🔵 <b>Mission 244</b> – Collect the Venus Celestial Stones. You need to find the password that opens the compartment in the ruins of the Temple of Venus where the stones are hidden.",
        245: "🔵 <b>Mission 245</b> – Collect the Venus Celestial Stones. You need to find the password that opens the compartment in the ruins of the Temple of Venus where the stones are hidden.",
        246: "🔵 <b>Mission 246</b> – Collect the Venus Celestial Stones. You need to find the password that opens the compartment in the ruins of the Temple of Venus where the stones are hidden.",
        247: "🔵 <b>Mission 247</b> – Collect the Venus Celestial Stones. You need to find the password that opens the compartment in the ruins of the Temple of Venus where the stones are hidden.",
        248: "🔵 <b>Mission 248</b> – Collect the Venus Celestial Stones. You need to find the password that opens the compartment in the ruins of the Temple of Venus where the stones are hidden.",
        249: "🔵 <b>Mission 249</b> – Collect the Venus Celestial Stones. You need to find the password that opens the compartment in the ruins of the Temple of Venus where the stones are hidden.",
        250: "🔵 <b>Mission 250</b> – Collect the Venus Celestial Stones. You need to find the password that opens the compartment in the ruins of the Temple of Venus where the stones are hidden.",
        # ADVENTURE 26 - Collect all Celestial Mars Stones.
        251: "🔴 <b>Mission 251</b> – Collect the Mars Celestial Stones. You need to find the password that opens the compartment in the ruins of the Temple of Mars where the stones are hidden.",
        252: "🔴 <b>Mission 252</b> – Collect the Mars Celestial Stones. You need to find the password that opens the compartment in the ruins of the Temple of Mars where the stones are hidden.",
        253: "🔴 <b>Mission 253</b> – Collect the Mars Celestial Stones. You need to find the password that opens the compartment in the ruins of the Temple of Mars where the stones are hidden.",
        254: "🔴 <b>Mission 254</b> – Collect the Mars Celestial Stones. You need to find the password that opens the compartment in the ruins of the Temple of Mars where the stones are hidden.",
        255: "🔴 <b>Mission 255</b> – Collect the Mars Celestial Stones. You need to find the password that opens the compartment in the ruins of the Temple of Mars where the stones are hidden.",
        256: "🔴 <b>Mission 256</b> – Collect the Mars Celestial Stones. You need to find the password that opens the compartment in the ruins of the Temple of Mars where the stones are hidden.",
        257: "🔴 <b>Mission 257</b> – Collect the Mars Celestial Stones. You need to find the password that opens the compartment in the ruins of the Temple of Mars where the stones are hidden.",
        258: "🔴 <b>Mission 258</b> – Collect the Mars Celestial Stones. You need to find the password that opens the compartment in the ruins of the Temple of Mars where the stones are hidden.",
        259: "🔴 <b>Mission 259</b> – Collect the Mars Celestial Stones. You need to find the password that opens the compartment in the ruins of the Temple of Mars where the stones are hidden.",
        260: "🔴 <b>Mission 260</b> – Collect the Mars Celestial Stones. You need to find the password that opens the compartment in the ruins of the Temple of Mars where the stones are hidden.",
        # ADVENTURE 27 - Collect all Celestial Jupiter Stones.
        261: "🟠 <b>Mission 261</b> – Collect the Jupiter Celestial Stones. You need to find the password that opens the compartment in the ruins of the Temple of Jupiter where the stones are hidden.",
        262: "🟠 <b>Mission 262</b> – Collect the Jupiter Celestial Stones. You need to find the password that opens the compartment in the ruins of the Temple of Jupiter where the stones are hidden.",
        263: "🟠 <b>Mission 263</b> – Collect the Jupiter Celestial Stones. You need to find the password that opens the compartment in the ruins of the Temple of Jupiter where the stones are hidden.",
        264: "🟠 <b>Mission 264</b> – Collect the Jupiter Celestial Stones. You need to find the password that opens the compartment in the ruins of the Temple of Jupiter where the stones are hidden.",
        265: "🟠 <b>Mission 265</b> – Collect the Jupiter Celestial Stones. You need to find the password that opens the compartment in the ruins of the Temple of Jupiter where the stones are hidden.",
        266: "🟠 <b>Mission 266</b> – Collect the Jupiter Celestial Stones. You need to find the password that opens the compartment in the ruins of the Temple of Jupiter where the stones are hidden.",
        267: "🟠 <b>Mission 267</b> – Collect the Jupiter Celestial Stones. You need to find the password that opens the compartment in the ruins of the Temple of Jupiter where the stones are hidden.",
        268: "🟠 <b>Mission 268</b> – Collect the Jupiter Celestial Stones. You need to find the password that opens the compartment in the ruins of the Temple of Jupiter where the stones are hidden.",
        269: "🟠 <b>Mission 269</b> – Collect the Jupiter Celestial Stones. You need to find the password that opens the compartment in the ruins of the Temple of Jupiter where the stones are hidden.",
        270: "🟠 <b>Mission 270</b> – Collect the Jupiter Celestial Stones. You need to find the password that opens the compartment in the ruins of the Temple of Jupiter where the stones are hidden.",
        # ADVENTURE 28 - Collect all Celestial Saturn Stones.
        271: "🪐 <b>Mission 271</b> – Collect the Saturn Celestial Stones. You need to find the password that opens the compartment in the ruins of the Temple of Jupiter where the stones are hidden.",
        272: "🪐 <b>Mission 272</b> – Collect the Saturn Celestial Stones. You need to find the password that opens the compartment in the ruins of the Temple of Jupiter where the stones are hidden.",
        273: "🪐 <b>Mission 273</b> – Collect the Saturn Celestial Stones. You need to find the password that opens the compartment in the ruins of the Temple of Jupiter where the stones are hidden.",
        274: "🪐 <b>Mission 274</b> – Collect the Saturn Celestial Stones. You need to find the password that opens the compartment in the ruins of the Temple of Jupiter where the stones are hidden.",
        275: "🪐 <b>Mission 275</b> – Collect the Saturn Celestial Stones. You need to find the password that opens the compartment in the ruins of the Temple of Jupiter where the stones are hidden.",
        276: "🪐 <b>Mission 276</b> – Collect the Saturn Celestial Stones. You need to find the password that opens the compartment in the ruins of the Temple of Jupiter where the stones are hidden.",
        277: "🪐 <b>Mission 277</b> – Collect the Saturn Celestial Stones. You need to find the password that opens the compartment in the ruins of the Temple of Jupiter where the stones are hidden.",
        278: "🪐 <b>Mission 278</b> – Collect the Saturn Celestial Stones. You need to find the password that opens the compartment in the ruins of the Temple of Jupiter where the stones are hidden.",
        279: "🪐 <b>Mission 279</b> – Collect the Saturn Celestial Stones. You need to find the password that opens the compartment in the ruins of the Temple of Jupiter where the stones are hidden.",
        280: "🪐 <b>Mission 280</b> – Collect the Saturn Celestial Stones. You need to find the password that opens the compartment in the ruins of the Temple of Jupiter where the stones are hidden.",
        # ADVENTURE 29 - Your wizard must set off in search of the Time Keeper, a wizard older than the known universe.
        281: "⏳ <b>Mission 281</b> – Defend yourself against the time spirits and collect their magical sparks.",
        282: "⏳ <b>Mission 282</b> – Defend yourself against the time spirits and collect their magical sparks.",
        283: "⏳ <b>Mission 283</b> – Defend yourself against the time spirits and collect their magical sparks.",
        284: "⏳ <b>Mission 284</b> – Defend yourself against the time spirits and collect their magical sparks.",
        285: "⏳ <b>Mission 285</b> – Defend yourself against the time spirits and collect their magical sparks.",
        286: "⏳ <b>Mission 286</b> – Defend yourself against the time spirits and collect their magical sparks.",
        287: "⏳ <b>Mission 287</b> – Defend yourself against the time spirits and collect their magical sparks.",
        288: "⏳ <b>Mission 288</b> – Defend yourself against the time spirits and collect their magical sparks.",
        289: "⏳ <b>Mission 289</b> – Defend yourself against the time spirits and collect their magical sparks.",
        290: "⏳ <b>Mission 290</b> – Defend yourself against the time spirits and collect their magical sparks.",
        # ADVENTURE 30 - Collect the materials you need to make your own magic hourglass.
        291: "⏳ <b>Mission 291</b> – Collect the materials you need to make your own Magic Hourglass.",
        292: "⏳ <b>Mission 292</b> – Collect the materials you need to make your own Magic Hourglass.",
        293: "⏳ <b>Mission 293</b> – Collect the materials you need to make your own Magic Hourglass.",
        294: "⏳ <b>Mission 294</b> – Collect the materials you need to make your own Magic Hourglass.",
        295: "⏳ <b>Mission 295</b> – Collect the materials you need to make your own Magic Hourglass.",
        296: "⏳ <b>Mission 296</b> – Collect the materials you need to make your own Magic Hourglass.",
        297: "⏳ <b>Mission 297</b> – Collect the materials you need to make your own Magic Hourglass.",
        298: "⏳ <b>Mission 298</b> – Collect the materials you need to make your own Magic Hourglass.",
        299: "⏳ <b>Mission 299</b> – Collect the materials you need to make your own Magic Hourglass.",
        300: "⏳ <b>Mission 300</b> – Collect the materials you need to make your own Magic Hourglass.",
        # ADVENTURE 31 - Collect the materials you need to make your own Time Machine.
        301: "⏳ <b>Mission 301</b> – Collect the materials you need to make your own Time Machine.",
        302: "⏳ <b>Mission 302</b> – Collect the materials you need to make your own Time Machine.",
        303: "⏳ <b>Mission 303</b> – Collect the materials you need to make your own Time Machine.",
        304: "⏳ <b>Mission 304</b> – Collect the materials you need to make your own Time Machine.",
        305: "⏳ <b>Mission 305</b> – Collect the materials you need to make your own Time Machine.",
        306: "⏳ <b>Mission 306</b> – Collect the materials you need to make your own Time Machine.",
        307: "⏳ <b>Mission 307</b> – Collect the materials you need to make your own Time Machine.",
        308: "⏳ <b>Mission 308</b> – Collect the materials you need to make your own Time Machine.",
        309: "⏳ <b>Mission 309</b> – Collect the materials you need to make your own Time Machine.",
        310: "⏳ <b>Mission 310</b> – Collect the materials you need to make your own Time Machine.",
        # ADVENTURE 32 - Collect enough gold coins to buy a ticket to travel on the Skyship.
        311: "🟡 <b>Mission 311</b> – Beat your opponent to win a gold coin. Collect 10 gold coins to buy a ticket to travel on the Skyship.",
        312: "🟡 <b>Mission 312</b> – Beat your opponent to win a gold coin. Collect 10 gold coins to buy a ticket to travel on the Skyship.",
        313: "🟡 <b>Mission 313</b> – Beat your opponent to win a gold coin. Collect 10 gold coins to buy a ticket to travel on the Skyship.",
        314: "🟡 <b>Mission 314</b> – Beat your opponent to win a gold coin. Collect 10 gold coins to buy a ticket to travel on the Skyship.",
        315: "🟡 <b>Mission 315</b> – Beat your opponent to win a gold coin. Collect 10 gold coins to buy a ticket to travel on the Skyship.",
        316: "🟡 <b>Mission 316</b> – Beat your opponent to win a gold coin. Collect 10 gold coins to buy a ticket to travel on the Skyship.",
        317: "🟡 <b>Mission 317</b> – Beat your opponent to win a gold coin. Collect 10 gold coins to buy a ticket to travel on the Skyship.",
        318: "🟡 <b>Mission 318</b> – Beat your opponent to win a gold coin. Collect 10 gold coins to buy a ticket to travel on the Skyship.",
        319: "🟡 <b>Mission 319</b> – Beat your opponent to win a gold coin. Collect 10 gold coins to buy a ticket to travel on the Skyship.",
        320: "🟡 <b>Mission 320</b> – Beat your opponent to win a gold coin. Collect 10 gold coins to buy a ticket to travel on the Skyship.",
        # ADVENTURE 33 - Find the Celestial Prism.
        321: "🐍 <b>Mission 321</b> – Explore the Cloud Citadel, the central hub of the Sky Kingdoms, to gather information about the stolen Celestial Prism. Encounter and negotiate with the sky serpents. Each sky serpent will give you its notes with clues to the location of the Celestial Prism after it has been defeated or through a deal.",
        322: "🐍 <b>Mission 322</b> – Explore the Cloud Citadel, the central hub of the Sky Kingdoms, to gather information about the stolen Celestial Prism. Encounter and negotiate with the sky serpents. Each sky serpent will give you its notes with clues to the location of the Celestial Prism after it has been defeated or through a deal.",
        323: "🐍 <b>Mission 323</b> – Explore the Cloud Citadel, the central hub of the Sky Kingdoms, to gather information about the stolen Celestial Prism. Encounter and negotiate with the sky serpents. Each sky serpent will give you its notes with clues to the location of the Celestial Prism after it has been defeated or through a deal.",
        324: "🐍 <b>Mission 324</b> – Explore the Cloud Citadel, the central hub of the Sky Kingdoms, to gather information about the stolen Celestial Prism. Encounter and negotiate with the sky serpents. Each sky serpent will give you its notes with clues to the location of the Celestial Prism after it has been defeated or through a deal.",
        325: "🐍 <b>Mission 325</b> – Explore the Cloud Citadel, the central hub of the Sky Kingdoms, to gather information about the stolen Celestial Prism. Encounter and negotiate with the sky serpents. Each sky serpent will give you its notes with clues to the location of the Celestial Prism after it has been defeated or through a deal.",
        326: "🐍 <b>Mission 326</b> – Explore the Cloud Citadel, the central hub of the Sky Kingdoms, to gather information about the stolen Celestial Prism. Encounter and negotiate with the sky serpents. Each sky serpent will give you its notes with clues to the location of the Celestial Prism after it has been defeated or through a deal.",
        327: "🐍 <b>Mission 327</b> – Explore the Cloud Citadel, the central hub of the Sky Kingdoms, to gather information about the stolen Celestial Prism. Encounter and negotiate with the sky serpents. Each sky serpent will give you its notes with clues to the location of the Celestial Prism after it has been defeated or through a deal.",
        328: "🐍 <b>Mission 328</b> – Explore the Cloud Citadel, the central hub of the Sky Kingdoms, to gather information about the stolen Celestial Prism. Encounter and negotiate with the sky serpents. Each sky serpent will give you its notes with clues to the location of the Celestial Prism after it has been defeated or through a deal.",
        329: "🐍 <b>Mission 329</b> – Explore the Cloud Citadel, the central hub of the Sky Kingdoms, to gather information about the stolen Celestial Prism. Encounter and negotiate with the sky serpents. Each sky serpent will give you its notes with clues to the location of the Celestial Prism after it has been defeated or through a deal.",
        330: "🐍 <b>Mission 330</b> – Explore the Cloud Citadel, the central hub of the Sky Kingdoms, to gather information about the stolen Celestial Prism. Encounter and negotiate with the sky serpents. Each sky serpent will give you its notes with clues to the location of the Celestial Prism after it has been defeated or through a deal.",
        # ADVENTURE 34 - Finde the elemental stones you need to blend the Heart of Harmony.
        331: "💎 <b>Mission 331</b> – Find the elemental stones you need to blend the Heart of Harmony and avoid the attack of the terrorist sorcerer.",
        332: "💎 <b>Mission 332</b> – Find the elemental stones you need to blend the Heart of Harmony and avoid the attack of the terrorist sorcerer.",
        333: "💎 <b>Mission 333</b> – Find the elemental stones you need to blend the Heart of Harmony and avoid the attack of the terrorist sorcerer.",
        334: "💎 <b>Mission 334</b> – Find the elemental stones you need to blend the Heart of Harmony and avoid the attack of the terrorist sorcerer.",
        335: "💎 <b>Mission 335</b> – Find the elemental stones you need to blend the Heart of Harmony and avoid the attack of the terrorist sorcerer.",
        336: "💎 <b>Mission 336</b> – Find the elemental stones you need to blend the Heart of Harmony and avoid the attack of the terrorist sorcerer.",
        337: "💎 <b>Mission 337</b> – Find the elemental stones you need to blend the Heart of Harmony and avoid the attack of the terrorist sorcerer.",
        338: "💎 <b>Mission 338</b> – Find the elemental stones you need to blend the Heart of Harmony and avoid the attack of the terrorist sorcerer.",
        339: "💎 <b>Mission 339</b> – Find the elemental stones you need to blend the Heart of Harmony and avoid the attack of the terrorist sorcerer.",
        340: "💎 <b>Mission 340</b> – Find the elemental stones you need to blend the Heart of Harmony and avoid the attack of the terrorist sorcerer.",
        # ADVENTURE 35 - Collect enough gravitite to make an anti-gravity device.
        341: "🟣 <b>Mission 341</b> – Collect enough gravitite to make an anti-gravity device. You'll need to negotiate with the miners in Celestia's gravitite mines.",
        342: "🟣 <b>Mission 342</b> – Collect enough gravitite to make an anti-gravity device. You'll need to negotiate with the miners in Celestia's gravitite mines.",
        343: "🟣 <b>Mission 343</b> – Collect enough gravitite to make an anti-gravity device. You'll need to negotiate with the miners in Celestia's gravitite mines.",
        344: "🟣 <b>Mission 344</b> – Collect enough gravitite to make an anti-gravity device. You'll need to negotiate with the miners in Celestia's gravitite mines.",
        345: "🟣 <b>Mission 345</b> – Collect enough gravitite to make an anti-gravity device. You'll need to negotiate with the miners in Celestia's gravitite mines.",
        346: "🟣 <b>Mission 346</b> – Collect enough gravitite to make an anti-gravity device. You'll need to negotiate with the miners in Celestia's gravitite mines.",
        347: "🟣 <b>Mission 347</b> – Collect enough gravitite to make an anti-gravity device. You'll need to negotiate with the miners in Celestia's gravitite mines.",
        348: "🟣 <b>Mission 348</b> – Collect enough gravitite to make an anti-gravity device. You'll need to negotiate with the miners in Celestia's gravitite mines.",
        349: "🟣 <b>Mission 349</b> – Collect enough gravitite to make an anti-gravity device. You'll need to negotiate with the miners in Celestia's gravitite mines.",
        350: "🟣 <b>Mission 350</b> – Collect enough gravitite to make an anti-gravity device. You'll need to negotiate with the miners in Celestia's gravitite mines.",
        # ADVENTURE 36 - Collect enough gravitite to make a flying carpet.
        351: "🟣 <b>Mission 351</b> – Collect enough gravitite to make a flying carpet. You'll need to negotiate with the miners in Celestia's gravitite mines.",
        352: "🟣 <b>Mission 352</b> – Collect enough gravitite to make a flying carpet. You'll need to negotiate with the miners in Celestia's gravitite mines.",
        353: "🟣 <b>Mission 353</b> – Collect enough gravitite to make a flying carpet. You'll need to negotiate with the miners in Celestia's gravitite mines.",
        354: "🟣 <b>Mission 354</b> – Collect enough gravitite to make a flying carpet. You'll need to negotiate with the miners in Celestia's gravitite mines.",
        355: "🟣 <b>Mission 355</b> – Collect enough gravitite to make a flying carpet. You'll need to negotiate with the miners in Celestia's gravitite mines.",
        356: "🟣 <b>Mission 356</b> – Collect enough gravitite to make a flying carpet. You'll need to negotiate with the miners in Celestia's gravitite mines.",
        357: "🟣 <b>Mission 357</b> – Collect enough gravitite to make a flying carpet. You'll need to negotiate with the miners in Celestia's gravitite mines.",
        358: "🟣 <b>Mission 358</b> – Collect enough gravitite to make a flying carpet. You'll need to negotiate with the miners in Celestia's gravitite mines.",
        359: "🟣 <b>Mission 359</b> – Collect enough gravitite to make a flying carpet. You'll need to negotiate with the miners in Celestia's gravitite mines.",
        360: "🟣 <b>Mission 360</b> – Collect enough gravitite to make a flying carpet. You'll need to negotiate with the miners in Celestia's gravitite mines."

    }

    #conecta com o banco de dados MySQL
    onnection = mysql.connector.connect(
        host="host",
        user="user",
        password=constants.DBACCESS,
        database="wizardworld"
    )


    cursor = connection.cursor()

    # Localiza o registro do usuário
    sql = "SELECT * FROM battlefield WHERE username='"+user_name+"'"
    cursor.execute(sql)
    results = cursor.fetchall()

    if len(results)>0:
        row = results[0]
        db_id, db_username, db_wallet, db_adventure, db_mission, db_level, db_round, db_magic, db_enemymp, db_bluepotions, db_redpotions, db_yellowpotions, db_purplepotions, db_invisible, db_updated, db_nextmission, db_password, db_skart, db_acum_skart, db_last_reward = row

        if db_adventure>aventuras_disponiveis:
            return "gameover"
            # return "⚔️ TO BE CONTINUED... ⚔️' because there are not more levels.

        my_adventure = adventures.get(db_adventure)
        my_mission = missions.get(db_level)

        mission_info = "Hello "+ db_username+"! This is your current mission.\n\n"+my_adventure+"\n"+my_mission+"\n"
        mission_info = mission_info+"\n Check your stats with /mystats  or  cast a /spell against your enemy"

    else:
        mission_info="Hi "+ user_name+"! Please, register your wax wallet with <b>/wax <i>wallet.wam</i></b> command (replace <i>wallet.wam</i> with your wax wallet)."

    cursor.close()
    connection.close()

    return mission_info

# Envia um NFT para uma Wax wallet
def send_NFT(wallet, level):
    try:
        recipient = wallet

        templates = {
            # ADVENTURE 1 - Make a magic wooden key
            1: "665825", # Basic Magic Key
            2: "735049", # Wood
            3: "735049", # Wood
            4: "735049", # Wood
            5: "735049", # Wood
            6: "735049", # Wood
            7: "735049", # Wood
            8: "735049", # Wood
            9: "735049", # Wood
            10: "735049", # Wood
            # ADVENTURE 2 - Make a magic iron key
            11: "665825", # Basic Magic Key
            12: "735049", # Wood
            13: "735049", # Wood
            14: "735049", # Wood
            15: "735051", # Iron
            16: "735049", # Wood
            17: "735051", # Iron
            18: "735051", # Iron
            19: "735051", # Iron
            20: "735051", # Iron
            # ADVENTURE 3 - Make a iron magic cauldron
            21: "735051", # Iron
            22: "735051", # Iron
            23: "735051", # Iron
            24: "735051", # Iron
            25: "735051", # Iron
            26: "735051", # Iron
            27: "735051", # Iron
            28: "735051", # Iron
            29: "735051", # Iron
            30: "735051", # Iron
            # ADVENTURE 4 - Make a leather magic hat
            31: "740817", # Magic Hat
            32: "735050", #Leather
            33: "735050", #Leather
            34: "735050", #Leather
            35: "735050", #Leather
            36: "735050", #Leather
            37: "735051", # Iron
            38: "735051", # Iron
            39: "735051", # Iron
            40: "735324", # Needle and Thread
            # ADVENTURE 5 - Make a iron pickaxe
            41: "735049", # Wood
            42: "735049", # Wood
            43: "735049", # Wood
            44: "735049", # Wood
            45: "735049", # Wood
            46: "735051", # Iron
            47: "735051", # Iron
            48: "735051", # Iron
            49: "735051", # Iron
            50: "735051", # Iron
            # ADVENTURE 6 - Mine ruby to make some new blends
            51: "735051", # Iron
            52: "735052", # Silver
            53: "735054", # Ruby
            54: "735051", # Iron
            55: "735052", # Silver
            56: "735054", # Ruby
            57: "735051", # Iron
            58: "735052", # Silver
            59: "735054", # Ruby
            60: "735058", # Gold
            # ADVENTURE 7 - Mine Sapphire to make some new blends
            61: "735051", # Iron
            62: "735052", # Silver
            63: "735055", # Sapphire
            64: "735051", # Iron
            65: "735052", # Silver
            66: "735055", # Sapphire
            67: "735051", # Iron
            68: "735052", # Silver
            69: "735055", # Sapphire
            70: "735058", # Gold
            # ADVENTURE 8 - Mine Emerald to make some new blends
            71: "735051", # Iron
            72: "735052", # Silver
            73: "735056", # Emerald
            74: "735051", # Iron
            75: "735052", # Silver
            76: "735056", # Emerald
            77: "735051", # Iron
            78: "735052", # Silver
            79: "735056", # Emerald
            80: "735058", # Gold
            # ADVENTURE 9 - Mine Amethyst to make some new blends
            81: "735051", # Iron
            82: "735052", # Silver
            83: "735057", # Amethyst
            84: "735051", # Iron
            85: "735052", # Silver
            86: "735057", # Amethyst
            87: "735051", # Iron
            88: "735052", # Silver
            89: "735057", # Amethyst
            90: "735058", # Gold
            # ADVENTURE 10 - Kill the spiders and collect all the ruby dust
            91: "759948", # Ruby Dust
            92: "735322", # Water
            93: "759948", # Ruby Dust
            94: "735049", # Wood
            95: "759948", # Ruby Dust
            96: "735322", # Water
            97: "759948", # Ruby Dust
            98: "735049", # Wood
            99: "759948", # Ruby Dust
            100: "735058", # Gold
            # ADVENTURE 11 - Kill the spiders and collect all the sapphire dust
            101: "759949", # Sapphire Dust
            102: "735322", # Water
            103: "759949", # Sapphire Dust
            104: "735049", # Wood
            105: "759949", # Sapphire Dust
            106: "735322", # Water
            107: "759949", # Sapphire Dust
            108: "735049", # Wood
            109: "759949", # Sapphire Dust
            110: "735058", # Gold
            # ADVENTURE 12 - Kill the spiders and collect all the emerald dust
            111: "759950", # Emerald Dust
            112: "735322", # Water
            113: "759950", # Emerald Dust
            114: "735049", # Wood
            115: "759950", # Emerald Dust
            116: "735322", # Water
            117: "759950", # Emerald Dust
            118: "735049", # Wood
            119: "759950", # Emerald Dust
            120: "735058", # Gold
            # ADVENTURE 13 - Kill the spiders and collect all the amethyst dust
            121: "759951", # Amethyst Dust
            122: "735322", # Water
            123: "759951", # Amethyst Dust
            124: "735049", # Wood
            125: "759951", # Amethyst Dust
            126: "735322", # Water
            127: "759951", # Amethyst Dust
            128: "735049", # Wood
            129: "759951", # Amethyst Dust
            130: "735058", # Gold
            # ADVENTURE 14 - Navigate through the Enchanted Forest to find the hidden entrance to the lost Temple of Elements.
            131: "665825", # Basic Magic Key
            132: "770369", # Bronze
            133: "735051", # Iron
            134: "770369", # Bronze
            135: "665825", # Basic Magic Key
            136: "735051", # Iron
            137: "770369", # Bronze
            138: "735054", # Ruby
            139: "770369", # Bronze
            140: "665825", # Basic Magic Key
            # ADVENTURE 15 - Master the Water Element.
            141: "735322", # Water
            142: "735322", # Water
            143: "735322", # Water
            144: "735322", # Water
            145: "735322", # Water
            146: "735322", # Water
            147: "735322", # Water
            148: "735322", # Water
            149: "735322", # Water
            150: "735322", # Water
            # ADVENTURE 16 - Master the Fire Element.
            151: "772191", # Magic Sparks
            152: "772191", # Magic Sparks
            153: "772191", # Magic Sparks
            154: "772191", # Magic Sparks
            155: "772191", # Magic Sparks
            156: "772191", # Magic Sparks
            157: "772191", # Magic Sparks
            158: "772191", # Magic Sparks
            159: "772191", # Magic Sparks
            160: "772191", # Magic Sparks
            # ADVENTURE 17 - Get all Water Elemental Stones.
            161: "773938", # Water Elemental Stone
            162: "773938", # Water Elemental Stone
            163: "773938", # Water Elemental Stone
            164: "773938", # Water Elemental Stone
            165: "773938", # Water Elemental Stone
            166: "773938", # Water Elemental Stone
            167: "773938", # Water Elemental Stone
            168: "773938", # Water Elemental Stone
            169: "773938", # Water Elemental Stone
            170: "773938", # Water Elemental Stone
            # ADVENTURE 18 - Get all Wind Elemental Stones.
            171: "773939", # Wind Elemental Stone
            172: "773939", # Wind Elemental Stone
            173: "773939", # Wind Elemental Stone
            174: "773939", # Wind Elemental Stone
            175: "773939", # Wind Elemental Stone
            176: "773939", # Wind Elemental Stone
            177: "773939", # Wind Elemental Stone
            178: "773939", # Wind Elemental Stone
            179: "773939", # Wind Elemental Stone
            180: "773939", # Wind Elemental Stone
            # ADVENTURE 19 - Get all Earth Elemental Stones.
            181: "773940", # Earth Elemental Stone
            182: "773940", # Earth Elemental Stone
            183: "773940", # Earth Elemental Stone
            184: "773940", # Earth Elemental Stone
            185: "773940", # Earth Elemental Stone
            186: "773940", # Earth Elemental Stone
            187: "773940", # Earth Elemental Stone
            188: "773940", # Earth Elemental Stone
            189: "773940", # Earth Elemental Stone
            190: "773940", # Earth Elemental Stone
            # ADVENTURE 20 - Get all Fire Elemental Stones.
            191: "773941", # Fire Elemental Stone
            192: "773941", # Fire Elemental Stone
            193: "773941", # Fire Elemental Stone
            194: "773941", # Fire Elemental Stone
            195: "773941", # Fire Elemental Stone
            196: "773941", # Fire Elemental Stone
            197: "773941", # Fire Elemental Stone
            198: "773941", # Fire Elemental Stone
            199: "773941", # Fire Elemental Stone
            200: "773941", # Fire Elemental Stone
            # ADVENTURE 21 - Collect the fragments of the map to Eldoria.
            201: "780676", # Eldoria map (fragment 1/20)
            202: "780681", # Eldoria map (fragment 2/20)
            203: "780684", # Eldoria map (fragment 3/20)
            204: "780685", # Eldoria map (fragment 4/20)
            205: "780687", # Eldoria map (fragment 5/20)
            206: "780688", # Eldoria map (fragment 6/20)
            207: "780694", # Eldoria map (fragment 7/20)
            208: "780693", # Eldoria map (fragment 8/20)
            209: "780695", # Eldoria map (fragment 9/20)
            210: "780697", # Eldoria map (fragment 10/20)
            # ADVENTURE 22 - Collect the fragments of the map to Eldoria.
            211: "780704", # Eldoria map (fragment 11/20)
            212: "780706", # Eldoria map (fragment 12/20)
            213: "780707", # Eldoria map (fragment 13/20)
            214: "780708", # Eldoria map (fragment 14/20)
            215: "780709", # Eldoria map (fragment 15/20)
            216: "780710", # Eldoria map (fragment 16/20)
            217: "780711", # Eldoria map (fragment 17/20)
            218: "780713", # Eldoria map (fragment 18/20)
            219: "780715", # Eldoria map (fragment 19/20)
            220: "780717", # Eldoria map (fragment 20/20)
            # ADVENTURE 23 - Collect all Celestial Sun Stones.
            221: "782745", # Sun Celestial Stone
            222: "782745", # Sun Celestial Stone
            223: "782745", # Sun Celestial Stone
            224: "782745", # Sun Celestial Stone
            225: "782745", # Sun Celestial Stone
            226: "782745", # Sun Celestial Stone
            227: "782745", # Sun Celestial Stone
            228: "782745", # Sun Celestial Stone
            229: "782745", # Sun Celestial Stone
            230: "782745", # Sun Celestial Stone
            # ADVENTURE 24 - Collect all Celestial Moon Stones.
            231: "782852", # Moon Celestial Stone
            232: "782852", # Moon Celestial Stone
            233: "782852", # Moon Celestial Stone
            234: "782852", # Moon Celestial Stone
            235: "782852", # Moon Celestial Stone
            236: "782852", # Moon Celestial Stone
            237: "782852", # Moon Celestial Stone
            238: "782852", # Moon Celestial Stone
            239: "782852", # Moon Celestial Stone
            240: "782852", # Moon Celestial Stone
            # ADVENTURE 25 - Collect all Celestial Venus Stones.
            241: "784270", # Venus Celestial Stone
            242: "784270", # Venus Celestial Stone
            243: "784270", # Venus Celestial Stone
            244: "784270", # Venus Celestial Stone
            245: "784270", # Venus Celestial Stone
            246: "784270", # Venus Celestial Stone
            247: "784270", # Venus Celestial Stone
            248: "784270", # Venus Celestial Stone
            249: "784270", # Venus Celestial Stone
            250: "784270", # Venus Celestial Stone
            # ADVENTURE 26 - Collect all Celestial Mars Stones.
            251: "784441", # Mars Celestial Stone
            252: "784441", # Mars Celestial Stone
            253: "784441", # Mars Celestial Stone
            254: "784441", # Mars Celestial Stone
            255: "784441", # Mars Celestial Stone
            256: "784441", # Mars Celestial Stone
            257: "784441", # Mars Celestial Stone
            258: "784441", # Mars Celestial Stone
            259: "784441", # Mars Celestial Stone
            260: "784441", # Mars Celestial Stone
            # ADVENTURE 27 - Collect all Celestial Jupiter Stones.
            261: "787287", # Jupiter Celestial Stone
            262: "787287", # Jupiter Celestial Stone
            263: "787287", # Jupiter Celestial Stone
            264: "787287", # Jupiter Celestial Stone
            265: "787287", # Jupiter Celestial Stone
            266: "787287", # Jupiter Celestial Stone
            267: "787287", # Jupiter Celestial Stone
            268: "787287", # Jupiter Celestial Stone
            269: "787287", # Jupiter Celestial Stone
            270: "787287", # Jupiter Celestial Stone
            # ADVENTURE 28 - Collect all Celestial Saturn Stones.
            271: "787866", # Saturn Celestial Stone
            272: "787866", # Saturn Celestial Stone
            273: "787866", # Saturn Celestial Stone
            274: "787866", # Saturn Celestial Stone
            275: "787866", # Saturn Celestial Stone
            276: "787866", # Saturn Celestial Stone
            277: "787866", # Saturn Celestial Stone
            278: "787866", # Saturn Celestial Stone
            279: "787866", # Saturn Celestial Stone
            280: "787866", # Saturn Celestial Stone
            # ADVENTURE 29 - Defend yourself against the time spirits and collect their magical sparks.
            281: "772191", # Magic Sparks
            282: "772191", # Magic Sparks
            283: "772191", # Magic Sparks
            284: "772191", # Magic Sparks
            285: "772191", # Magic Sparks
            286: "772191", # Magic Sparks
            287: "772191", # Magic Sparks
            288: "772191", # Magic Sparks
            289: "772191", # Magic Sparks
            290: "772191", # Magic Sparks
            # ADVENTURE 30 - Collect the materials you need to make your own Magic Hourglass.
            291: "808594", # Magic Dark Sparks
            292: "808594", # Magic Dark Sparks
            293: "808594", # Magic Dark Sparks
            294: "808594", # Magic Dark Sparks
            295: "808594", # Magic Dark Sparks
            296: "808594", # Magic Dark Sparks
            297: "808594", # Magic Dark Sparks
            298: "808594", # Magic Dark Sparks
            299: "808594", # Magic Dark Sparks
            300: "808594", # Magic Dark Sparks
            # ADVENTURE 31 - Collect the materials you need to make your own Time Machine.
            301: "808594", # Magic Dark Sparks
            302: "735051", # Iron
            303: "735055", # Sapphire
            304: "808594", # Magic Dark Sparks
            305: "735051", # Iron
            306: "735055", # Sapphire
            307: "808594", # Magic Dark Sparks
            308: "735051", # Iron
            309: "735055", # Sapphire
            310: "808594", # Magic Dark Sparks
            # ADVENTURE 32 - Collect enough gold coins to buy a ticket to travel on the Skyship.
            311: "825108", # Golden coin
            312: "825108", # Golden coin
            313: "825108", # Golden coin
            314: "825108", # Golden coin
            315: "825108", # Golden coin
            316: "825108", # Golden coin
            317: "825108", # Golden coin
            318: "825108", # Golden coin
            319: "825108", # Golden coin
            320: "825108", # Golden coin
            # ADVENTURE 33 - Find the Celestial Prism.
            321: "832310", # Notes
            322: "832310", # Notes
            323: "832310", # Notes
            324: "832310", # Notes
            325: "832310", # Notes
            326: "832310", # Notes
            327: "832310", # Notes
            328: "832310", # Notes
            329: "832310", # Notes
            330: "832310", # Notes
            # ADVENTURE 34 - Finde the elemental stones you need to blend the Heart of Harmony.
            331: "773938", # Water elemental stone
            332: "773939", # Wind elemental stone
            333: "773940", # Earth elemental stone
            334: "773941", # Fire elemental stone
            335: "773938", # Water elemental stone
            336: "773939", # Wind elemental stone
            337: "773940", # Earth elemental stone
            338: "773941", # Fire elemental stone
            339: "773938", # Water elemental stone
            340: "773941", # Fire elemental stone
            # ADVENTURE 35 - Collect enough gravitite to make an anti-gravity device.
            341: "857632", # Gravitite
            342: "857632", # Gravitite
            343: "857632", # Gravitite
            344: "857632", # Gravitite
            345: "857632", # Gravitite
            346: "857632", # Gravitite
            347: "857632", # Gravitite
            348: "857632", # Gravitite
            349: "857632", # Gravitite
            350: "857632", # Gravitite
            # ADVENTURE 36 - Collect enough gravitite to make a flying carpet.
            351: "857632", # Gravitite
            352: "857632", # Gravitite
            353: "857632", # Gravitite
            354: "857632", # Gravitite
            355: "857632", # Gravitite
            356: "857632", # Gravitite
            357: "857632", # Gravitite
            358: "857632", # Gravitite
            359: "857632", # Gravitite
            360: "857632" # Gravitite
        }

        template_NFT = templates.get(level)

        if template_NFT=="665825":
            image = "https://atomichub-ipfs.com/ipfs/QmchBJnFeXRr87uNNkCtbQuDmJu24azvzcM6cMAuuKesaa" # Basic Magic Key
        elif template_NFT=="735322":
            image = "https://atomichub-ipfs.com/ipfs/QmcWYeVauvyN2Mh6Deqi99bRAFLF1GPxoBcGkBP2fnqy3t" # Water
        elif template_NFT=="772191":
            image = "https://atomichub-ipfs.com/ipfs/QmTXsYr2W34wTxqiPjp3qAujjfQxJGA2nhEeJGBKqn94iL" # Magic Sparks
        elif template_NFT=="735049":
            image = "https://atomichub-ipfs.com/ipfs/Qmcz6kZUvQgprGXZDE9mr5r26dwZjuwRwGuQc31qFmXLZu" # Wood
        elif template_NFT=="735051":
            image = "https://atomichub-ipfs.com/ipfs/QmNZdaPKa86mEUuByPaHFfUrAh2QSxsYan3yRBV4ij8bhz" # Iron
        elif template_NFT=="770369":
            image = "https://atomichub-ipfs.com/ipfs/QmPjJEUNxkA6AMziiz3Ej3PGofEhnkbV9vAsLTVb9nnoGs"  # Bronze
        elif template_NFT=="735052":
            image = "https://atomichub-ipfs.com/ipfs/QmZMEfXfDqFmLw9WpyYKeTAiJTfpFGHabUGuDVgbVMdbJy" # Silver
        elif template_NFT=="735058":
            image = "https://atomichub-ipfs.com/ipfs/QmVVAZcJTMyumd9xBL6D3TERLFmjNVB7ohn32Pq9dCxpjX" # Gold
        elif template_NFT=="735054":
            image = "https://atomichub-ipfs.com/ipfs/Qma45WyKtxUtfW78H3zQvPymgsh8KsgPB3nPWfsmZVNYhK" # Ruby
        elif template_NFT=="735055":
            image = "https://atomichub-ipfs.com/ipfs/QmTFDkPo3oH6vBQwtpVLKWpn1WivQZC51pzNmqzbWbZziu" # Sapphire
        elif template_NFT=="735056":
            image = "https://atomichub-ipfs.com/ipfs/QmQB23Ym1ygzkHsrzPQKAVjn5KT2CYmGxzqtTkZ4cACA1f" # Emerald
        elif template_NFT=="735057":
            image = "https://atomichub-ipfs.com/ipfs/QmUET1zZpzfekheEKbZEraM6F1Vhv4xUoWsNCCaZzv6vcz" # Amethyst
        elif template_NFT=="759948":
            image = "https://atomichub-ipfs.com/ipfs/QmRqSPpL1kGtekv1T2FxBDKyhj5ejAAz2KQggxt2bY8e4v" # Ruby Dust
        elif template_NFT=="759949":
            image = "https://atomichub-ipfs.com/ipfs/QmRUS4sFj2F4jCCqTpegcdxKvp1JhH11vphxyJnov3v47q" # Sapphire Dust
        elif template_NFT=="759950":
            image = "https://atomichub-ipfs.com/ipfs/QmZzBtjonxRbQVqeiJ8eHpPd45WKsjJY9MHz6Ky1us3118" # Emerald Dust
        elif template_NFT=="759951":
            image = "https://atomichub-ipfs.com/ipfs/QmPYYPZvpc1Q7mA1nSXiKKy6e9mCTBjeVMH5erPjav2SBn" # Amethyst Dust
        elif template_NFT=="740817":
            image = "https://atomichub-ipfs.com/ipfs/QmPJJNMZpXUnTVCTvQXgqgSq15PFXQUkzQs6w3PPZedfTX" # Magic Hat
        elif template_NFT=="735050":
            image = "https://atomichub-ipfs.com/ipfs/QmdCkAAnpzAVZeRtsRytY8VfQPfknmd1WxCzR3y4o43N4V" # Leather
        elif template_NFT=="735324":
            image = "https://atomichub-ipfs.com/ipfs/QmWiXe7in9QbhUaprtGeVwDcgZPxm8p8a2UjxkkohfnweQ"  # Needle and Thread
        elif template_NFT=="773938":
            image = "https://atomichub-ipfs.com/ipfs/QmNqaDoQL4qHfNo9P7HbruuHfAxdWJkTzXegMXRp9dKnKA"  # Water Elemental Stone
        elif template_NFT=="773939":
            image = "https://atomichub-ipfs.com/ipfs/QmdWYuyXuN34KTu7SFxsEC5ndYUz9cmJAoUvs1TCXo1iJs"  # Wind Elemental Stone
        elif template_NFT=="773940":
            image = "https://atomichub-ipfs.com/ipfs/QmPNU2GcDQNpCk3ruiB9ZkNZb2ZKHxQ2VQpZsqvfjCxGfE"  # Earth Elemental Stone
        elif template_NFT=="773941":
            image = "https://atomichub-ipfs.com/ipfs/QmWfYBFTNBqxPKh7Lmyf1B5Kcb2jkjHyRAGZ3YzKoV4J57"  # Fire Elemental Stone
        elif (int(template_NFT)>=780676 and int(template_NFT)<=780717):
            image = "https://atomichub-ipfs.com/ipfs/QmRBQEPWSivDWk9AnY2GwahwNb2LaAN7JSeUwi7nM7g5qo"  # Eldoria Map fragment
        elif template_NFT=="782745":
            image = "https://atomichub-ipfs.com/ipfs/QmV75tY7K6YixWPA3A8EiQvyXy8vZ5YiVJun4fHEt7nufv"  # Sun Celestial Stone
        elif template_NFT=="782852":
            image = "https://atomichub-ipfs.com/ipfs/QmaRB3g3qKHvrXxfXgHA4sfWoMdAa5FQeyzoxL32hhxj4L"  # Moon Celestial Stone
        elif template_NFT=="784270":
            image = "https://atomichub-ipfs.com/ipfs/QmWFEmGixMtrGVotdhWCCB5L1abaKCc8o2Ev5vZYCC6fYv"  # Venus Celestial Stone
        elif template_NFT=="784441":
            image = "https://atomichub-ipfs.com/ipfs/QmXfjCkjG8Mx8KeViCGfgbQ8xpjyUKjHHd1G2b2Yy1SzL1"  # Mars Celestial Stone
        elif template_NFT=="787287":
            image = "https://atomichub-ipfs.com/ipfs/QmZHtLKFfv6dSTPSnr84pTKtpjwNroPZ3KkDHsVcpK4btR"  # Jupiter Celestial Stone
        elif template_NFT=="787866":
            image = "https://atomichub-ipfs.com/ipfs/QmS4ntYCDvPKrvtVsNn5sDF1ZACNinCbyCz7bMirEnzAmP"  # Saturn Celestial Stone
        elif template_NFT=="808594":
            image = "https://atomichub-ipfs.com/ipfs/QmSwnnzzyaoMqiGeVhBkYhJzcPMpdBnVJdbxq8cNnnzAbc"  # Magic Dark Sparks
        elif template_NFT=="825108":
            image = "https://atomichub-ipfs.com/ipfs/QmVsRhjfSNxrxq2BX25gfHXbATbjA124Naa3z1uAVesm39"  # Golden coin
        elif template_NFT=="832310":
            image = "https://atomichub-ipfs.com/ipfs/QmcXJGeAvu16ojCWtqeJ4FoX9U8m2SHvsqwtYu9xvngRKJ"  # Notes
        elif template_NFT=="857632":
            image = "https://atomichub-ipfs.com/ipfs/QmVJGzHvFJexRtuaCj9SjGbk5vm9TdedLC4A36Anux5SUR"  # Gravitite
        else:
            image = ""

        # Sketch Art Collection
        private_key = constants.PRIVATE_KEY_ESABG
        collection = "brsketchart1"
        collection_wallet = "brsketchart1"
        schema_NFT = "wizardsworld"
        nft2send = []
        nft2send.append((schema_NFT, str(template_NFT)))

        # Create object
        assetsender = AssetSender(collection, collection_wallet, private_key)

        # Send mission reward with given asset template to the given wallet
        print("Mission : ", level, "  Template mission reward: ", template_NFT, "  to the wallet: ", recipient)
        mint_transaction = assetsender.mint_assets(schema_NFT, template_NFT, recipient, 1)
        # Para verificar se o NFT está disponível da brsketchart1 wallet e enviar diretamente de wallet sem fazer mint de um novo NFT
        # descomentar a linha abaixo e comentar a posterior.
        # mint_transaction = assetsender.send_or_mint_assets(nft2send, recipient)
        print("Transaction ID: https://waxblock.io/transaction/"+str(mint_transaction[0][1]))

        # Send Adventure prizes with given asset template to the given wallet
        if level==10 or level==20 or level==40:
            template_NFT = "735053" # Spell sheet
            image = "https://atomichub-ipfs.com/ipfs/QmQ8z72KdNmcrZDZyZVUds3wzBf2k6eKPCGnxNqdkkAZHR" # Spell sheet
            print("Aventura : ", level, " Template adventure prize: ", template_NFT, "  To the wallet: ", recipient)
            assetsender.mint_assets(schema_NFT, template_NFT, recipient, 1)

        elif level==30:
            template_NFT = "747935" # Ventus
            image = "https://atomichub-ipfs.com/ipfs/QmVLnVMQFyxb497J7GUbHC9XmSEZkFtzLnZcgmFpm8WVqS" # Ventus
            print("Aventura : ", level, " Template adventure prize: ", template_NFT, "  To the wallet: ", recipient)
            assetsender.mint_assets(schema_NFT, template_NFT, recipient, 1)

        elif level==50:
            template_NFT = "749449" # Terra
            image = "https://atomichub-ipfs.com/ipfs/QmUrfmxLGVh73eYkS8z3tpTFTzgyvhiV9eN1BfBwKUBAJg" # Terra
            print("Aventura : ", level, " Template adventure prize: ", template_NFT, "  To the wallet: ", recipient)
            assetsender.mint_assets(schema_NFT, template_NFT, recipient, 1)


        registro = image + "\nTransaction ID: \nhttps://waxblock.io/transaction/"+str(mint_transaction[0][1])

        return registro

    except Exception as e:
        print(f"Error: {e}")

# Envia o reward diário quando não houver novas missões.
def claim_daily_reward(name):
    user_name = str(name).lower()

    status = "Hi, "+user_name+"! "
    #conecta com o banco de dados MySQL
    onnection = mysql.connector.connect(
        host="host",
        user="user",
        password=constants.DBACCESS,
        database="wizardworld"
    )



    cursor = connection.cursor()

    # Localiza o registro do usuário
    sql = "SELECT * FROM battlefield WHERE username='"+user_name+"'"
    cursor.execute(sql)
    results = cursor.fetchall()

    if len(results)>0:
        row = results[0]
        db_id, db_username, db_wallet, db_adventure, db_mission, db_level, db_round, db_magic, db_enemymp, db_bluepotions, db_redpotions, db_yellowpotions, db_purplepotions, db_invisible, db_updated, db_nextmission, db_password, db_skart, db_acum_skart, db_last_reward = row

        if db_nextmission>datetime.now():
            next_mission_time = db_nextmission - datetime.now()
            return "Hello "+ user_name+"! Your wizard need some rest. 😉\nThere are <b>"+str(round(next_mission_time.seconds/3600,2))+" hours</b> remaining until next mission."

        # Check the number of available adventures
        if db_adventure>aventuras_disponiveis:

            print("********************* \n Player has finished all available adventures \nSending rewards to :",db_username)

            # Envia o SKART reward para a conta do jogador no jogo
            db_last_reward = datetime.now()
            player_reward = round(float(getRewardPlayer(db_username, db_wallet)),4)
            db_skart = round((float(db_skart)+float(player_reward)),4)
            db_acum_skart = round((float(db_acum_skart) + float(player_reward)),4)

            db_updated="n"
            my_blue_potions=db_bluepotions
            my_red_potions=db_redpotions
            my_yellow_potions=db_yellowpotions
            my_purple_potions=db_purplepotions
            db_nextmission = datetime.now()+timebetweenmissions-timedelta(hours=db_purplepotions)

            # Max usable potions = 10
            if my_blue_potions>10:
                my_blue_potions=10

            if my_red_potions>10:
                my_red_potions=10

            if my_yellow_potions>10:
                my_yellow_potions=10

            if my_purple_potions>12:
                my_purple_potions=12


            status = status + "\nCongratulations! You just claimed your SKART reward."
            status = status + "\n🎨 SKART received = "+str(round(player_reward,4))+"\n🎨 SKART balance = "+str(round(db_skart,4))+"   \n🎨 SKART earned so far = "+ str(round(db_acum_skart,4))

            sql = "UPDATE battlefield SET username = %s, wallet = %s, adventure = %s, mission = %s, level = %s, round = %s, magic = %s, enemymp = %s, bluepotions = %s, redpotions = %s, yellowpotions = %s, purplepotions = %s, invisible=%s, updated = %s, nextmission = %s, password = %s, skart = %s, acum_skart = %s, last_reward = %s WHERE id = %s"
            data = (db_username, db_wallet, db_adventure, db_mission, db_level, db_round, db_magic, db_enemymp, my_blue_potions, my_red_potions, my_yellow_potions, my_purple_potions, db_invisible, db_updated, db_nextmission, db_password, db_skart, db_acum_skart, db_last_reward, db_id)

            cursor.execute(sql, data)
            connection.commit()
            recordsaffected = cursor.rowcount
        else:

            status = status + "You can use this command and continue to /claim your reward when you have completed all the missions. \nKeep playing with the /spell or /pass commands."

    else:
        status = "Player "+ user_name + " not found!"

    # Fecha conexão com banco de dados
    cursor.close()
    connection.close()

    return status


# Jogo de Senha
def senha(name, text):
    text = text.lower()
    user_name = str(name).lower()
    list_tentativa=[]
    for numero in text:
        if (int(numero)>9) or (int(numero)<1):
            result = "<b>Error: The password has 5 digits (numbers 1 to 9)</b>. \nUse the <b>/pass <i>99999</i> </b>command (replace <i>99999</i> with your password attempt)."
            return result
        list_tentativa.append(numero)

    if (len(set(list_tentativa)))!= (len(list_tentativa)):
        return "<b>Error: The password does not contain repeated numbers. \nIt has 5 digits (numbers 1 to 9)</b>. \nUse the <b>/pass <i>99999</i> </b>command (replace <i>99999</i> with your password attempt)."

    #conecta com o banco de dados MySQL
    connection = mysql.connector.connect(
        host="host",
        user="user",
        password=constants.DBACCESS,
        database="wizardworld"
    )


    cursor = connection.cursor()

    # Localiza o registro do usuário
    sql = "SELECT * FROM battlefield WHERE username='"+user_name+"'"
    cursor.execute(sql)
    results = cursor.fetchall()
    cursor.close()
    connection.close()

    if len(results)>0:
        row = results[0]
        db_id, db_username, db_wallet, db_adventure, db_mission, db_level, db_round, db_magic, db_enemymp, db_bluepotions, db_redpotions, db_yellowpotions, db_purplepotions, db_invisible, db_updated, db_nextmission, db_password, db_skart, db_acum_skart, db_last_reward = row

        # Check the number of available adventures
        if db_adventure>aventuras_disponiveis:
            return "gameover"
            # return "⚔️ TO BE CONTINUED... ⚔️' because there are not more levels.

        password=str(db_password)

        pass1 = password[0]
        pass2 = password[1]
        pass3 = password[2]
        pass4 = password[3]
        pass5 = password[4]

        numbers = {
            1: "1️⃣",
            2: "2️⃣",
            3: "3️⃣",
            4: "4️⃣",
            5: "5️⃣",
            6: "6️⃣",
            7: "7️⃣",
            8: "8️⃣",
            9: "9️⃣"
        }

        bigdigit1 = numbers.get(int(pass1))
        bigdigit2 = numbers.get(int(pass2))
        bigdigit3 = numbers.get(int(pass3))
        bigdigit4 = numbers.get(int(pass4))
        bigdigit5 = numbers.get(int(pass5))
        password_big = bigdigit1+bigdigit2+bigdigit3+bigdigit4+bigdigit5

        tent1 = text[0]
        tent2 = text[1]
        tent3 = text[2]
        tent4 = text[3]
        tent5 = text[4]

        bigtent1 = numbers.get(int(tent1))
        bigtent2 = numbers.get(int(tent2))
        bigtent3 = numbers.get(int(tent3))
        bigtent4 = numbers.get(int(tent4))
        bigtent5 = numbers.get(int(tent5))
        tentativa_big = bigtent1+bigtent2+bigtent3+bigtent4+bigtent5

        resultado=[]

        if tent1==pass1:
            resultado.append("🟢")
        elif tent1==pass2:
            resultado.append("🟡")
        elif tent1==pass3:
            resultado.append("🟡")
        elif tent1==pass4:
            resultado.append("🟡")
        elif tent1==pass5:
            resultado.append("🟡")
        else:
            resultado.append("🔴")

        if tent2==pass1:
            resultado.append("🟡")
        elif tent2==pass2:
            resultado.append("🟢")
        elif tent2==pass3:
            resultado.append("🟡")
        elif tent2==pass4:
            resultado.append("🟡")
        elif tent2==pass5:
            resultado.append("🟡")
        else:
            resultado.append("🔴")

        if tent3==pass1:
            resultado.append("🟡")
        elif tent3==pass2:
            resultado.append("🟡")
        elif tent3==pass3:
            resultado.append("🟢")
        elif tent3==pass4:
            resultado.append("🟡")
        elif tent3==pass5:
            resultado.append("🟡")
        else:
            resultado.append("🔴")

        if tent4==pass1:
            resultado.append("🟡")
        elif tent4==pass2:
            resultado.append("🟡")
        elif tent4==pass3:
            resultado.append("🟡")
        elif tent4==pass4:
            resultado.append("🟢")
        elif tent4==pass5:
            resultado.append("🟡")
        else:
            resultado.append("🔴")

        if tent5==pass1:
            resultado.append("🟡")
        elif tent5==pass2:
            resultado.append("🟡")
        elif tent5==pass3:
            resultado.append("🟡")
        elif tent5==pass4:
            resultado.append("🟡")
        elif tent5==pass5:
            resultado.append("🟢")
        else:
            resultado.append("🔴")


        if password==text:
            result = "<b>Congratulations, "+name+"!</b> 🥳\nYou've guessed the password!\n"+ "🟢🟢🟢🟢🟢\n "+password_big
            #conecta com o banco de dados MySQL
            connection = mysql.connector.connect(
                host="host",
                user="user",
                password=constants.DBACCESS,
                database="wizardworld"
            )
            cursor = connection.cursor()
            # Localiza o registro do usuário
            sql = "SELECT * FROM battlefield WHERE username='"+user_name+"'"
            cursor.execute(sql)
            results = cursor.fetchall()

            if len(results)>0:
                row = results[0]
                db_id, db_username, db_wallet, db_adventure, db_mission, db_level, db_round, db_magic, db_enemymp, db_bluepotions, db_redpotions, db_yellowpotions, db_purplepotions, db_invisible, db_updated, db_nextmission, db_password, db_skart, db_acum_skart, db_last_reward = row


                if (db_level/db_adventure)==10:
                    db_adventure=db_adventure+1
                    result = result + "\nYou have finished this adventure! \nThis victory took you to the next level! \nBut beware! Your next adventure might not be so easy!\n"
                else:
                    result = result + "\nYou've entered the secret chamber! \nThis victory took you to the next level! \nBut beware! Your next enemy is also stronger!\n"


                print("********************* \n Sending rewards to :",db_username)
                # Envia o prêmio correspondente ao nível
                imagem_NFT = send_NFT(db_wallet, db_level)

                # Envia o SKART reward para a conta do jogador no jogo
                db_last_reward = datetime.now()
                player_reward = float(getRewardPlayer(db_username, db_wallet))
                db_skart = float(db_skart)+float(player_reward)
                db_acum_skart = float(db_acum_skart) + float(player_reward)

                level=db_level+1
                db_level=level
                db_mission=db_mission+1
                db_enemymp=1000 + (db_level*100)
                db_round=1
                db_invisible=0
                db_updated="n"

                if db_purplepotions>12:
                    db_purplepotions=12

                db_nextmission = datetime.now()+timebetweenmissions-timedelta(hours=db_purplepotions)
                db_password = create_password()

                result = result + "Your enemy dropped an item that was sent to your wallet. It will be useful in your next missions. Use it wisely."
                result = result + "\nTo see your next mission use the /mission command.\n"
                result = result + "🧙🏼‍ Your MP = "+str(db_magic)+"      🧟 Enemy MP = "+ str(db_enemymp)
                result = result + "\n🎨 SKART this mission = "+str(round(player_reward,4))+"\n🎨 SKART balance = "+str(round(db_skart,4))+"   \n🎨 SKART earned so far = "+ str(round(db_acum_skart,4))
                result = result + "\n⭐️ Next Level = "+str(db_level)
                result = result + "\n"+imagem_NFT

                sql = "UPDATE battlefield SET username = %s, wallet = %s, adventure = %s, mission = %s, level = %s, round = %s, magic = %s, enemymp = %s, bluepotions = %s,  redpotions = %s, yellowpotions = %s, purplepotions = %s, invisible = %s, updated = %s, nextmission = %s, password = %s, skart = %s, acum_skart = %s, last_reward = %s WHERE id = %s"
                data = (db_username, db_wallet, db_adventure, db_mission, db_level, db_round, db_magic, db_enemymp, db_bluepotions, db_redpotions, db_yellowpotions, db_purplepotions, db_invisible, db_updated, db_nextmission, db_password, db_skart, db_acum_skart, db_last_reward, db_id)
                cursor.execute(sql, data)
                connection.commit()
                recordsaffected = cursor.rowcount

            else:
                print("Error: Player not found!")
            cursor.close()
            connection.close()

        else:
            result = "<b>Password incorrect!</b>\n"+resultado[0]+resultado[1]+resultado[2]+resultado[3]+resultado[4]+"\n"+tentativa_big
            result = result + "\n\n🟢Right number in the right position"
            result = result + "\n🟡Right number in the wrong position"
            result = result + "\n🔴Number is not part of the password"

    else:
        result ="Hi "+ user_name+"! Please, register your wax wallet with <b>/wax <i>wallet.wam</i></b> command (replace <i>wallet.wam</i> with your wax wallet)."

    return result

# Gera uma nova senha para o jogo Senha
def create_password():

    digitos = [1,2,3,4,5,6,7,8,9]
    random.shuffle(digitos)

    new_password = str(digitos[0])+str(digitos[1])+str(digitos[2])+str(digitos[3])+str(digitos[4])
    return new_password


# Lista os NFT disponiveis para compra no grupo do Telegram
def list_NFT(name):
    #user_wallet = str(wallet[5:20]).lower()
    user_name = str(name).lower()
    #conecta com o banco de dados MySQL
    connection = mysql.connector.connect(
        host="host",
        user="user",
        password=constants.DBACCESS,
        database="wizardworld"
    )

    cursor = connection.cursor()

    sql = "SELECT * FROM templates WHERE (`schema` = 'wizardsworld') AND (available = 'Y' OR available = 'P') ORDER BY template_id DESC"
    cursor.execute(sql)
    results = cursor.fetchall()

    list_templates = []
    lista="<b>ID            Name                    Price (SkArt)  </b>\n"
    lista=lista+"-------------------------------------------\n"

    for template in results:
      db_id, db_schema, db_template_id, db_name, db_issued_supply, db_max_supply, db_price, db_available, db_img = template
      lista=lista+"<code>"+db_template_id+"</code>   "+db_name+"    <i>"+str(round(db_price,2))+"</i>  \n"
      list_templates.append(db_template_id)

    # Fecha conexão com banco de dados
    cursor.close()
    connection.close()

    # Embaralha a lista de números
    random.shuffle(list_templates)
    #print(list_templates[1])
    return lista

# Compra um NFT para o membro do grupo
def buy_NFT(name, text):
    user_name = str(name).lower()
    #template_NFT = str(text[7:14])
    if text=="/buy" or text=="/buy@wizardsworldsbot":
        return "Hi "+ user_name+"! Please, inform a valid template ID."
    else:
        command, template_NFT = text.split()

    if len(template_NFT)<6:
        return "Hi "+ user_name+"! Please, inform a valid template ID."

    #conecta com o banco de dados MySQL
    connection = mysql.connector.connect(
        host="host",
        user="user",
        password=constants.DBACCESS,
        database="wizardworld"
    )
    cursor = connection.cursor()
    sql = "SELECT * FROM templates WHERE (`schema` = 'wizardsworld') AND (available = 'Y' OR available = 'P') ORDER BY template_id DESC"
    cursor.execute(sql)
    results = cursor.fetchall()
    if len(results)>0:
        template = results[0]
        db_id, db_schema, db_template_id, db_name, db_issued_supply, db_max_supply, db_price, db_available, db_img = template
        schema_NFT = db_schema
        template_Price = float(db_price)
    else:
        cursor.close()
        connection.close()
        return "Hi "+ user_name+"! Please, inform a valid template ID."

    # Fecha conexão com banco de dados
    cursor.close()
    connection.close()


    # Sketch Art Collection
    private_key = constants.PRIVATE_KEY_ESABG
    collection = "brsketchart1"
    collection_wallet = "brsketchart1"
    #schema_NFT = "promo.stuff"
    #template_NFT = "679189"



    passholdersonly = "N"

    # Create object
    assetsender = AssetSender(collection, collection_wallet, private_key)

    #conecta com o banco de dados MySQL
    connection = mysql.connector.connect(
        host="host",
        user="user",
        password=constants.DBACCESS,
        database="wizardworld"
    )

    cursor = connection.cursor()

    sql = "SELECT * FROM battlefield WHERE username='"+user_name+"'"
    cursor.execute(sql)
    results = cursor.fetchall()

    if len(results)>0:
        # Localiza o registro do usuário

        row = results[0]

        db_id, db_username, db_wallet, db_adventure, db_mission, db_level, db_round, db_magic, db_enemymp, db_bluepotions, db_redpotions, db_yellowpotions, db_purplepotions, db_invisible, db_updated, db_nextmission, db_password, db_skart, db_acum_skart, db_last_reward = row

        if db_skart<template_Price:
            registro = "Hi "+ db_username+"! You don't have enough balance."
        else:
            print("********************")
            print(db_username+" just bought an NFT. Template ID : "+template_NFT+". Sending...")
            db_skart = float(db_skart) - template_Price
            image_asset = atom.get_template("brsketchart1",template_NFT).image
            nft2send = []
            nft2send.append(("wizardsworld", str(template_NFT)))
            send_transaction = assetsender.send_or_mint_assets(nft2send, db_wallet)

            # send_transaction = assetsender.mint_assets(schema_NFT, template_NFT, db_wallet, 1)

            # assetsender.mint_assets(schema_NFT, template_NFT, db_wallet, 1)

            sql = "UPDATE battlefield SET username = %s, wallet = %s, adventure = %s, mission = %s, level = %s, round = %s, magic = %s, enemymp = %s, bluepotions = %s, redpotions = %s, yellowpotions = %s, purplepotions = %s, invisible=%s, updated = %s, nextmission = %s, password = %s, skart = %s, acum_skart = %s, last_reward = %s WHERE id = %s"
            data = (db_username, db_wallet, db_adventure, db_mission, db_level, db_round, db_magic, db_enemymp, db_bluepotions, db_redpotions, db_yellowpotions, db_purplepotions, db_invisible, db_updated, db_nextmission, db_password, db_skart, db_acum_skart, db_last_reward, db_id)

            cursor.execute(sql, data)
            connection.commit()
            recordsaffected = cursor.rowcount

            registro = "Hi "+db_username+"! I just sent your NFT (Template ID: "+template_NFT+") to "+db_wallet+" wallet. \n"
            registro = registro + image_asset + "\nTransaction ID: \nhttps://waxblock.io/transaction/"+str(send_transaction[0][1])
            print("Transaction ID: https://waxblock.io/transaction/"+str(send_transaction[0][1]))
            print("**** Database updated ****")

    else:
        registro = "Hi "+ user_name+"! Please, whitelist your wax wallet with <b>/wax <i>wallet.wam</i></b> command."

    cursor.close()
    connection.close()

    return registro


# Faz o saque do saldo de tokens da conta no Telegram para a Wax wallet
def withdrawn_tokens(name, text):
    user_name = str(name).lower()
    if text=="/withdraw" or text=="/withdraw@wizardsworldsbot":
        return "Hi "+user_name+"\n<i>Please enter the amount you wish to withdraw.</i> \nYou can check your SKArt balance from the chat with the <b>/mystats</b> command."
    else:
        command, token_quantity = text.split()

    registro = "Hi "+user_name

    value_token_quantity = float(token_quantity)
    token_quantity = f'{value_token_quantity:10.8f}'

    #conecta com o banco de dados MySQL
    connection = mysql.connector.connect(
        host="host",
        user="user",
        password=constants.DBACCESS,
        database="wizardworld"
    )

    cursor = connection.cursor()

    sql = "SELECT * FROM battlefield WHERE username='"+user_name+"'"
    cursor.execute(sql)
    results = cursor.fetchall()

    if len(results)>0:
        # Localiza o registro do usuário

        row = results[0]

        db_id, db_username, db_wallet, db_adventure, db_mission, db_level, db_round, db_magic, db_enemymp, db_bluepotions, db_redpotions, db_yellowpotions, db_purplepotions, db_invisible, db_updated, db_nextmission, db_password, db_skart, db_acum_skart, db_last_reward = row

        tokens = str(round(db_skart,4))
        recipient = db_wallet

        if value_token_quantity<2:
            # Fecha conexão com banco de dados
            cursor.close()
            connection.close()
            return registro+"!\nThe minimum withdrawal amount is <b>2 SKArt</b>."

        if db_skart<value_token_quantity:
            # Fecha conexão com banco de dados
            cursor.close()
            connection.close()
            return registro+"!\nYour balance of SKArt tokens is insufficient.\nYou can check your SKArt balance from the chat with the <b>/mystats</b> command."
        else:
            db_skart = float(db_skart) - value_token_quantity

            sql = "UPDATE battlefield SET username = %s, wallet = %s, adventure = %s, mission = %s, level = %s, round = %s, magic = %s, enemymp = %s, bluepotions = %s, redpotions = %s, yellowpotions = %s, purplepotions = %s, invisible=%s, updated = %s, nextmission = %s, password = %s, skart = %s, acum_skart = %s, last_reward = %s WHERE id = %s"
            data = (db_username, db_wallet, db_adventure, db_mission, db_level, db_round, db_magic, db_enemymp, db_bluepotions, db_redpotions, db_yellowpotions, db_purplepotions, db_invisible, db_updated, db_nextmission, db_password, db_skart, db_acum_skart, db_last_reward, db_id)

            cursor.execute(sql, data)
            connection.commit()
            recordsaffected = cursor.rowcount

            parameters = "sktip "+token_quantity+" "+recipient
            registro = tokens_to_wallet(user_name, parameters)

    else:
        registro = "Hi "+ user_name+"! Please, whitelist your wax wallet with <b>/wax wallet.wam </b> command."

    # Fecha conexão com banco de dados
    cursor.close()
    connection.close()

    return registro

# Enviar tokens para a wax wallet do usuário
def tokens_to_wallet(name, text):
    #recipient = str(wallet[7:20]).lower()
    user_name = str(name).lower()
    command, token_quantity, recipient = text.split()

    value_token_quantity = float(token_quantity)
    token_quantity = f'{value_token_quantity:10.8f}'

    data = [
        # In this case the account me.wam is transferring to account 'receiver'
        pyntelope.Data(name="from", value=pyntelope.types.Name("brsketchart1")),
        pyntelope.Data(name="to", value=pyntelope.types.Name(recipient)),
        pyntelope.Data(
            name="quantity", # Selects the 'quantity' field in this action, must be a valid field in the action
            value=pyntelope.types.Asset(token_quantity+" SKART"), # Asset type must be specified as 'quantity' requires the amount and currency type, which Asset includes
        ),
        pyntelope.Data(
            name="memo", # Selects the 'memo' field in this action, just an extra message with the transfer
            value=pyntelope.types.String("SKArt withdrawal"), # String type is used for memo
        ),
    ]

    auth = pyntelope.Authorization(actor="brsketchart1", permission="active")

    action = pyntelope.Action(
        account="brsketchart1",
        name="transfer",
        data=data,
        authorization=[auth],
    )

    raw_transaction = pyntelope.Transaction(actions=[action])

    net = pyntelope.WaxMainnet()
    linked_transaction = raw_transaction.link(net=net)

    key = constants.PRIVATE_KEY_BRSKETCHART1
    signed_transaction = linked_transaction.sign(key=key)

    resp = signed_transaction.send()

    id_transaction = "https://waxblock.io/transaction/"+resp["transaction_id"]

    return "💰Congratulations "+user_name+"! \n<b>"+token_quantity+" SKArt</b> tokens were sent to the <b>"+recipient+ "</b> wallet.\nTransaction ID:\n"+id_transaction


### WIZARDS WORLD NFT FARM ###

# USO DO ADMINISTRADOR - Verifica o reward reward para um determinado jogador
def payoff(name, username):

    command, user_name = username.split()
    user_name = str(user_name).lower()
    print("*********************")
    print(user_name)
    user_data = getData(user_name)
    user_wallet=user_data[2]
    user_reward = getRewardPlayer(user_name, user_wallet)
    magicpower = inventory(user_name, user_wallet)

    print("Magic Power = ",magicpower)

    print("*********************")

    return "Valor do reward a ser pago... "+str(user_reward)


# Calcula o valor do weekly reward do jogador
def getRewardPlayer(name, wallet):
    user_name = str(name).lower()
    elapsed_time=timedelta(hours=0)
    # Verifica quais itens o jogador possui.
    #url = f"https://atomic.hivebp.io/atomicassets/v1/assets?collection_name=brsketchart1&schema_name=wizardsworld&owner={wallet}&page=1&limit=500&order=desc&sort=asset_id"
    url = f"https://wax.eosusa.io/atomicassets/v1/assets?collection_name=brsketchart1&schema_name=wizardsworld&owner={wallet}&page=1&limit=500&order=desc&sort=asset_id"

    # Send a GET request to the API endpoint
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        data = response.json()

    # Extract template_id and assets from the parsed data
    assets = data['data']
    total_assets=0
    player_reward=float(0)
    time_reduction = 0
    hora_split=[]

    #templates = data['data']['templates']
    for asset in assets:
        asset_id = str(asset['asset_id'])
        collection = asset['collection']['collection_name']
        schema_name = asset['schema']['schema_name']
        template = asset['template']['template_id']
        total_assets = total_assets + 1
        if template == "746407":
            time_reduction= time_reduction + 1

        #print("Asset ID:", asset_id)
        #print("Schema:", schema_name)
        #print("Template:", template, "Reward: ", getRewardTemplate(template))
        player_reward = player_reward + float(getRewardTemplate(template))

    if time_reduction>12:
        time_reduction=12

    print("Player reward 24h = ", round(player_reward,4))

    player_reward = player_reward/24
    print("Player reward/hour = ", round(player_reward,4))

    user_data = getData(user_name)

    #Time in hours since the last reward
    elapsed_time = datetime.now()-user_data[19]
    print("Days since last mission: ",elapsed_time.days)
    if elapsed_time.days == 0:
        hora_split = str(elapsed_time).split(":")

    elif elapsed_time.days>=1:
        hora_split=[24]
    else:
        dia_split = str(elapsed_time).split(",")
        hora_split = str(dia_split[1]).split(":")

    print("Time since the last reward: ", elapsed_time)
    print("Valid hours = ", hora_split[0])

    if int(hora_split[0])>=24:
        player_reward = float((player_reward*24))
    else:
        player_reward = float(player_reward*(int(hora_split[0])))

    #player_reward = player_reward*(24-time_reduction)
    player_reward = round(player_reward,4)

    print("Total assets: ", total_assets)
    print("Purple potions: ", time_reduction)
    print("This mission reward: ", player_reward," SKART")
    print("*********************")

    return player_reward

# Daily Rewards per template
def getRewardTemplate(template):
    cod_template = template
    reward=float(0.0)

    if template=='649929':
        reward=float(0.024)
    elif template=='649930':
        reward=float(0.048)
    elif template=='660835':
        reward=float(0.096)
    elif template=='660839':
        reward=float(0.096)
    elif template=='685511':
        reward=float(0.216)
    elif template=='750119':
        reward=float(0.456)
    elif template=='761405':
        reward=float(0.888)
    elif template=='777207':
        reward=float(1.776)
    elif template=='649934':
        reward=float(0.024)
    elif template=='649936':
        reward=float(0.048)
    elif template=='660777':
        reward=float(0.096)
    elif template=='745208':
        reward=float(0.216)
    elif template=='749104':
        reward=float(0.456)
    elif template=='761406':
        reward=float(0.888)
    elif template=='665364':
        reward=float(0.012)
    elif template=='665365':
        reward=float(0.012)
    elif template=='665366':
        reward=float(0.012)
    elif template=='746407':
        reward=float(0.048)
    elif template=='735049':
        reward=float(0.0024)
    elif template=='735050':
        reward=float(0.0024)
    elif template=='735051':
        reward=float(0.0024)
    elif template=='735320':
        reward=float(0.0024)
    elif template=='735321':
        reward=float(0.0024)
    elif template=='735322':
        reward=float(0.0024)
    elif template=='735324':
        reward=float(0.0024)
    elif template=='772191':
        reward=float(0.0024)
    elif template=='773938':
        reward=float(0.0024)
    elif template=='773939':
        reward=float(0.0024)
    elif template=='773940':
        reward=float(0.0024)
    elif template=='773941':
        reward=float(0.0024)
    elif template=='759948':
        reward=float(0.0024)
    elif template=='649938':
        reward=float(0.024)
    elif template=='649939':
        reward=float(0.048)
    elif template=='649942':
        reward=float(0.096)
    elif template=='649943':
        reward=float(0.216)
    elif template=='749105':
        reward=float(0.456)
    elif template=='749109':
        reward=float(0.888)
    elif template=='749114':
        reward=float(1.776)
    elif template=='665825':
        reward=float(0.0048)
    elif template=='735053':
        reward=float(0.0096)
    elif template=='735059':
        reward=float(0.048)
    elif template=='735319':
        reward=float(0.0264)
    elif template=='739075':
        reward=float(0.0264)
    elif template=='739133':
        reward=float(0.0168)
    elif template=='740816':
        reward=float(0.0096)
    elif template=='740817':
        reward=float(0.0048)
    elif template=='740819':
        reward=float(0.0072)
    elif template=='740828':
        reward=float(0.0192)
    elif template=='740831':
        reward=float(0.024)
    elif template=='746673':
        reward=float(0.024)
    elif template=='746800':
        reward=float(0.024)
    elif template=='747935':
        reward=float(0.024)
    elif template=='749449':
        reward=float(0.024)
    elif template=='756870':
        reward=float(0.012)
    elif template=='757559':
        reward=float(0.024)
    elif template=='757561':
        reward=float(0.024)
    elif template=='758422':
        reward=float(0.0096)
    elif template=='759773':
        reward=float(0.024)
    elif template=='759774':
        reward=float(0.024)
    elif template=='761325':
        reward=float(0.012)
    elif template=='770360':
        reward=float(0.0192)
    elif template=='771157':
        reward=float(0.0288)
    elif template=='772152':
        reward=float(0.024)
    elif template=='772153':
        reward=float(0.0240)
    elif template=='759949':
        reward=float(0.0024)
    elif template=='759950':
        reward=float(0.0024)
    elif template=='759951':
        reward=float(0.0024)
    elif template=='770369':
        reward=float(0.0024)
    elif template=='735052':
        reward=float(0.0048)
    elif template=='735054':
        reward=float(0.0048)
    elif template=='735055':
        reward=float(0.0048)
    elif template=='735056':
        reward=float(0.0048)
    elif template=='735057':
        reward=float(0.0048)
    elif template=='774406':
        reward=float(0.0480)
    elif template=='735058':
        reward=float(0.0072)
    elif template=='781527':
        reward=float(1.7760)
    elif template=="780723":
        reward=float(0.1200)
    elif template=="781792":
        reward=float(0.0480)
    elif template=="782745":
        reward=float(0.0024)
    elif template=="782852":
        reward=float(0.0024)
    elif template=="784270":
        reward=float(0.0024)
    elif template=="784441":
        reward=float(0.0024)
    elif template=="787287":
        reward=float(0.0024)
    elif template=="787866":
        reward=float(0.0024)
    elif template=="784817":
        reward=float(0.024)
    elif template=="784818":
        reward=float(0.024)
    elif template=="789738":
        reward=float(0.024)
    elif template=="789741":
        reward=float(0.024)
    elif template=="790793":
        reward=float(0.024)
    elif template=="791435":
        reward=float(0.024)
    elif template=="791436":
        reward=float(0.024)
    elif template=="791437":
        reward=float(0.024)
    elif template=="791438":
        reward=float(0.024)
    elif template=="794717":
        reward=float(0.024)
    elif template=="808594":
        reward=float(0.0024)
    elif template=="808595":
        reward=float(0.024)
    elif template=="812184":
        reward=float(0.024)
    elif template=="825108":
        reward=float(0.0024)
    elif template=="825274":
        reward=float(0.024)
    elif template=="826027":
        reward=float(0.024)
    elif template=="832310":
        reward=float(0.0024)
    elif template=="838537":
        reward=float(0.024)
    elif template=="857632":
        reward=float(0.0024)
    elif template=="857633":
        reward=float(0.024)
    elif template=="868056":
        reward=float(0.024)

    else:
        reward=float(0.0)

    return reward


# Recupera dados do usuário
def getData(name):
    data=[]

    #conecta com o banco de dados MySQL
    connection = mysql.connector.connect(
        host="host",
        user="user",
        password=constants.DBACCESS,
        database="wizardworld"
    )

    cursor = connection.cursor()
    # Localiza o registro do usuário
    sql = "SELECT * FROM battlefield WHERE username='"+name+"'"
    cursor.execute(sql)
    results = cursor.fetchall()

    if len(results)>0:

        row = results[0]
        db_id, db_username, db_wallet, db_adventure, db_mission, db_level, db_round, db_magic, db_enemymp, db_bluepotions, db_redpotions, db_yellowpotions, db_purplepotions, db_invisible, db_updated, db_nextmission, db_password, db_skart, db_acum_skart, db_last_reward = row


        data.append(db_id)
        data.append(db_username)
        data.append(db_wallet)
        data.append(db_adventure)
        data.append(db_mission)
        data.append(db_level)
        data.append(db_round)
        data.append(db_magic)
        data.append(db_enemymp)
        data.append(db_bluepotions)
        data.append(db_redpotions)
        data.append(db_yellowpotions)
        data.append(db_purplepotions)
        data.append(db_invisible)
        data.append(db_updated)
        data.append(db_nextmission)
        data.append(db_password)
        data.append(float(db_skart))
        data.append(float(db_acum_skart))
        data.append(db_last_reward)

    else:
        user_wallet = wallet
        user_id=0
        user_skart=float(0)
        user_last_reward=datetime.now()
        user_next_mission=datetime.now()+timebetweenmissions
        user_acum_skart=float(0)
        user_password=create_password()

        data.append(0)
        data.append(user_name)
        data.append(user_wallet)
        data.append(user_adventure)
        data.append(user_mission)
        data.append(user_level)
        data.append(user_round)
        data.append(user_magic)
        data.append(user_enemymp)
        data.append(user_bluepotions)
        data.append(user_repotions)
        data.append(user_yellowpotions)
        data.append(user_purplepotions)
        data.append(user_invisible)
        data.append(user_updated)
        data.append(user_next_mission)
        data.append(user_password)
        data.append(user_skart)
        data.append(user_acum_skart)
        data.append(user_last_reward)

    # Fecha conexão com banco de dados
    cursor.close()
    connection.close()

    #print(len(data))
    #for dado in data:
    #    print(dado)

    return data
