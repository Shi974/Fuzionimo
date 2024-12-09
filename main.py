import os, random, datetime, json, re, save
import discord
#import pycord
import requests
from discord import Color

#https://www.freecodecamp.org/news/create-a-discord-bot-with-python/
#https://discordpy.readthedocs.io/en/stable/index.html
#https://realpython.com/how-to-make-a-discord-bot-python/#interacting-with-discord-apis
#https://replit.com/@InvisibleOne/Bot-for-Tutorial?v=1#main.py

intents = discord.Intents.default()
intents.message_content = True


# --> bot commands settings
from discord.ext import commands
bot = commands.Bot(
  command_prefix = "$",  
  case_insensitive = True,  
  intents = intents 
)
# bot commands settings <--


#Connexion bot
@bot.event
async def on_ready():
  print(f'Connecté en tant que {bot.user}')


# BOT COMMANDS
# $random
@bot.command(name = "random", help = "Renvoie une citation de Kaamelot")
async def get_Kaamelot_quote(ctx):
  try:
    response = requests.get("https://kaamelott.chaudie.re/api/random")
    json_data = json.loads(response.text)
    #print(json_data)
    quote = f"{json_data['citation']['citation']} - **{json_data['citation']['infos']['personnage']}** (*{json_data['citation']['infos']['saison']} - {json_data['citation']['infos']['episode']}*)"
    await ctx.send(quote)
  except Exception as e :
    print(e)
    
    
# $hello
@bot.command(name = 'hello', help = 'Renvoie des salutations')
async def hello(ctx):
  await ctx.channel.send(f":robot: Bip bip bip, boop boop ! Salut {ctx.author.mention} !")

  
# $oeuf
@bot.command(name = 'oeuf', help = "Permet d'obtenir un oeuf")
@commands.cooldown(1, 300, commands.BucketType.user)
async def oeuf(ctx):
  with open('animals.json') as f:
    animal_list = json.load(f)
  weights = [animal["rarity"] for animal in animal_list]
  animal = random.choices(animal_list, weights, k = 3)
  animal = dict(animal[0])
  animal_name = animal["name"]
  animal_reg = re.sub("^.*\/([^/]*).*.png", r'\1', animal["img"])
  animal_img = 'img/' + animal_reg + '-128.png'
  if animal["gender"] == "M":
    animal_gender = "un"
  else:
    animal_gender = "une"
  animal_type = animal["type"]
  match animal_type:
    case "reptile":
      animal_type_color = Color.dark_gold()
    case "mammifère":
      animal_type_color = Color.green()
    case "poisson":
      animal_type_color = Color.blue()
    case "oiseau":
      animal_type_color = Color.purple()
    case "crustacé":
      animal_type_color = Color.dark_blue()
    case "gastéropode":
      animal_type_color = Color.light_gray()
    case _:
      animal_type_color = Color.teal()
  animal_rar = animal["rarity"]
  match animal_rar:
    case 0.1:
      animal_rarity = "rare"
    case 0.05:
      animal_rarity = "super rare"
    case 0.5:
      animal_rarity = "commun"
    case 0.35:
      animal_rarity = "peu commun"
    case _:
      animal_rarity = "bug"
  try :
    await ctx.send(":egg: Ton oeuf a éclos ! Tu reçois " + animal_gender + " " + animal_name + " ! ")
    # EMBED
    file = discord.File(animal_img, filename = f"{animal_reg}-128.png")
    embed = discord.Embed(title = animal_name, color = animal_type_color, description = animal_type + ' ' + animal_rarity).set_image(url = f"attachment://{animal_reg}-128.png")
    await ctx.send(file = file, embed = embed)
  except Exception as e :
    print(e)

    
# $pièces
@bot.command(name = 'pièces', help = "Cherche des pièces")
@commands.cooldown(1, 600, commands.BucketType.user)
async def pieces(ctx):
  if save.checkExist(ctx.author.id):
    pass
  else:
    user = save.createUser(ctx.author.id, ctx.guild.id)
  try:
    user = save.read(ctx.author.id)
    coins = random.randrange(1, 31)
    user['coins'] += coins
    u_coins = user['coins']
    updatedData = {
      'userid' : user['userid'],
      'guildid' : user['guildid'],
      'coins' : u_coins,
    }
    save.updateUser(updatedData)
    place_coin = ["sous le canapé", "sous l'oreiller", "dans ta chaussure droite", "dans le frigo", "dans la veste de ton père"]
    random_place_coin = random.choice(place_coin)
    await ctx.send(f"Tu trouves {coins} :coin: {random_place_coin} ! :moneybag: Total en banque : {u_coins} :coin: ")
  except Exception as e:
    print(e)


# $daily
@bot.command(name = 'daily', help = "Récupère tes pièces quotidiennes")
@commands.cooldown(1, 43200, commands.BucketType.user)
async def daily(ctx):
  if save.checkExist(ctx.author.id):
    pass
  else:
    user = save.createUser(ctx.author.id)
  try:
    user = save.read(ctx.author.id)
    coins = 30
    user['coins'] += coins
    u_coins = user['coins']
    updatedData = {
      'userid' : user['userid'],
      'guildid' : user['guildid'],
      'coins' : u_coins,
    }
    save.updateUser(updatedData)
    await ctx.send(f":moneybag: :clock2: Récupération des revenus passifs ... Tu reçois {coins} :coin: !  Total en banque : {u_coins} :coin: ")
  except Exception as e:
    print(e)

    
# --> DEBUT SLOTS
#TODO (discord bot game reaction trigger embed?)    
# $slots x
@bot.command(name = 'slots', help = "Tente ta chance aux slots, nécessite un montant : `$slots x`")
async def start(ctx, amount: int):
  try:
    user = save.read(ctx.author.id)
    u_coins = user['coins']
    if amount > u_coins:
      await ctx.send(f"{ctx.author.mention} Essaye pas de m'arnaquer ! Tu ne peux pas miser autant ! Tu n'as que {u_coins} :coin: ")
    else:
      embed = discord.Embed(title = 'Slot Machine', description = format_board_as_str(), color = Color.gold())
      embed.add_field(name = "Comment jouer :", value = "Utilise 1️⃣ 2️⃣ 3️⃣ pour parier sur les :regional_indicator_x: premières lignes et multiplier ta mise. \n  \n Appuie sur ❌ pour quitter.", inline = False)
      embed.add_field(name = 'Mise', value = f"{amount} :coin:", inline = False)
      msg = await ctx.send(embed = embed)
      await msg.add_reaction("1️⃣")
      await msg.add_reaction("2️⃣")
      await msg.add_reaction("3️⃣")
      await msg.add_reaction("❌")
  except Exception as e:
    print(e)

symbol_count = {
  "🍀": 4,
  "⭐": 5,
  "🍉": 7,
  "🍋": 8
}

symbol_value = {
  "🍀": 20,
  "⭐": 15,
  "🍉": 10,
  "🍋": 8
}

def format_board_as_str():
  board = [
    ['》 ', '⭐', '🍋', '🍉', ' 《'],
    ['》 ', '🍀', '⭐', '🍋', ' 《'],
    ['》 ', '🍉', '🍋', '🍉', ' 《']
  ]
  board_as_str = ''
  for row in range(3):
    for col in range(5):
      board_as_str += (board[row][col]) + " "
      if col == 5 - 1:
        board_as_str += "\n "
  return board_as_str

# REACTION LISTENER
# TODO : Restrict the reaction to the user that used the $slots command or lock the message or message only visible by user?
#https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjdz43x6v79AhVBhlwKHct8DpkQFnoECBAQAw&url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DlnfrRfiq2is&usg=AOvVaw3u04kk3ehgC2pf9CnijRA3
#https://www.google.com/search?q=discord.py+lock+message+so+users+can%27t+react&client=firefox-b-d&sxsrf=APwXEdduB60F5Q7AWHWDrI5WTId-rfdP7g%3A1680013732769&ei=pPkiZOG-LoXQgQawkK3wBg&ved=0ahUKEwjhoInu6v79AhUFaMAKHTBIC24Q4dUDCA4&uact=5&oq=discord.py+lock+message+so+users+can%27t+react&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIKCAAQRxDWBBCwAzIKCAAQRxDWBBCwAzIKCAAQRxDWBBCwAzIKCAAQRxDWBBCwAzIKCAAQRxDWBBCwAzIKCAAQRxDWBBCwAzIKCAAQRxDWBBCwAzIKCAAQRxDWBBCwA0oECEEYAFCIEViVHmDJH2gCcAF4AYAB4gOIAdsakgEHMi0yLjQuM5gBAKABAcgBCMABAQ&sclient=gws-wiz-serp
#https://stackoverflow.com/questions/61871846/discord-py-avoid-getting-more-than-one-reaction-by-a-same-user-to-a-message-se
# Rajouter condition pour déclencher function : id user doit matcher id user qui $slots?
# https://stackoverflow.com/questions/75040654/discord-py-specific-user-can-react-to-message
# https://guide.pycord.dev/interactions/ui-components/buttons
@bot.event
async def on_reaction_add(reaction, user):
  try:
    if user != bot.user:
      msg = reaction.message
      if str(reaction.emoji) == "❌":
        embed = discord.Embed(title = 'Slot Machine', description = format_board_as_str(), color = Color.gold())
        embed.add_field(name = "Poule mouillée", value = f"Alors comme ça on a peur de perdre ses pièces ? Du balai {user.name} !", inline = False)
        await msg.edit(embed = embed)
        await msg.clear_reactions()
        return null
        
      embeds = reaction.message.embeds
      for embed in embeds:
        fields = embed.fields
        for field in fields:
          name = field.name
          value = field.value
          if name == 'Mise':
            mise = value.replace(' :coin:', '')
            mise = (int(mise))
      if str(reaction.emoji) == "1️⃣":
        #print('User pressed 1️⃣')
        lines = 1
      elif str(reaction.emoji) == "2️⃣":
        #print('User pressed 2️⃣')
        lines = 2
      elif str(reaction.emoji) == "3️⃣":
        #print('User pressed 3️⃣')
        lines = 3
      await msg.clear_reactions()
      spin_res = spin(lines, mise, msg)
      coin_l_g, slots, res_string = spin_res
      print(spin_res)
      #print(user)
      #print(user.id)
      # USER DATA
      user_id = user.id
      user_data = save.read(user_id)
      #print(user_id)
      #print(type(user_id))
      user_data['coins'] += coin_l_g
      u_coins = user_data['coins']
      updatedData = {
        'userid' : user_data['userid'],
        'guildid' : user_data['guildid'],
        'coins' : u_coins,
      }
      save.updateUser(updatedData)
      if coin_l_g > 0:
        slot_color = Color.green()
        mise_totale = mise * lines
        return_string = f"Mise : {mise_totale} :coin: \n\n :partying_face: {res_string} \n Tu reçois {coin_l_g} :coin: \n \n Total : {user_data['coins']} :coin:"
      else:
        slot_color = Color.red()
        return_string = f"{res_string} \n Tu perds {-coin_l_g} :coin: \n \n Total : {user_data['coins']} :coin:"
      # EMBED
      embed = discord.Embed(title = 'Slot Machine', description = print_slots(slots), color = slot_color)
      embed.add_field(name = "Résultat", value = return_string, inline = False)
      await msg.edit(embed = embed)      
  except Exception as e:
    print(e)

def spin(lines, mise, msg):
  try:
    total_bet = mise * lines
    columns = get_slot_machine_spin(3, 3, symbol_count)
    ######
    # DEBOGAGE
    #columns = [['🍋', '🍋', '⭐'],['🍋', '🍋', '⭐'],['🍋', '🍋', '🍀']]
    ######
    winnings, winning_lines = check_winnings(columns, lines, mise, symbol_value)
    gain = winnings - total_bet
    if winnings > 0:
      res = f"🎉 Bravo !"
    else:
      res = f"Tu n'as rien gagné. 😭"
    if winnings > 0:
      if len(winning_lines) > 2:
        res = f"🎉 Bravo ! Tu as gagné sur les lignes : {winning_lines}"
      else:
        res = f"🎉 Bravo ! Tu as gagné sur la ligne : {winning_lines}"
    return (gain, columns, res)
  except Exception as e:
    print(e)

def get_slot_machine_spin(rows, cols, symbols):
  try:
    all_symbols = []
    for symbol, symbol_count in symbols.items():
      for _ in range(symbol_count):
        all_symbols.append(symbol)
    columns = []
    for _ in range(cols):
      column = []
      current_symbols = all_symbols[:]
      for _ in range(rows):
        value = random.choice(current_symbols)
        current_symbols.remove(value)
        column.append(value)
      columns.append(column)
    return columns
  except Exception as e:
    print(e)

def check_winnings(columns, lines, mise, values):
  try:
    winnings = 0
    winning_lines = ''
    #winning_lines = []
    for line in range(lines):
      symbol = columns[0][line]
      for column in columns:
        symbol_to_check = column[line]
        if symbol != symbol_to_check:
          break
      else:
        winnings += values[symbol] * mise
        index = line + 1
        winning_lines += f"{index} "
    #print(winning_lines)
    #print(len(winning_lines))
    return winnings, winning_lines
  except Exception as e:
    print(e)

def print_slots(slots):
  board_as_str = ''
  for row in range(len(slots[0])):
    for i, column in enumerate(slots):
      if i != len(slots) - 1:
        board_as_str += column[row] + " | "
      else:
        board_as_str += column[row] + "\n "
  return(board_as_str)
  #TODO : rajouter les chevrons à chaque ligne?
# --> FIN SLOTS
  
 
# $profil
@bot.command(name = 'profil', help = "Visualise ton profil")
async def profil(ctx):
  try:
    user = save.read(ctx.author.id)
    pfp = ctx.author.avatar
    # EMBED
    embed = discord.Embed(title=f":identification_card:  {ctx.author.name}", color = Color.random(), description=f":coin: `{str(user['coins'])}`").set_thumbnail(url=(pfp))
    await ctx.send(embed=embed)
  except Exception as e:
    print(e)


# $leaderboard serveur
@bot.command(name = 'leaderboard', help = "Visualise le Top 5 du serveur")
async def leaderboard(ctx):
  try:
    guildid = ctx.guild.id
    topFive = save.leaderboard_guild(guildid)
    embed = discord.Embed(title = "Leaderboard", description = f"Top 5 des utilisateurs les plus riches de {ctx.guild.name} :moneybag: ", color = Color.gold())
    for user in topFive:
      discordData = await ctx.message.guild.query_members(user_ids = [user['userid']])
      embed.add_field(name = f"{str(topFive.index(user)+1)}. {discordData[0].name}", value = f"Pièces : `{str(user['coins'])}`")
    await ctx.send(embed=embed)
  except Exception as e:
    print(e)


# $leaderboard global
@bot.command(name = 'leaderboard_gb', help = "Visualise le Top 5 global")
async def leaderboard_global(ctx):
  try:
    topFive = save.leaderboard_global()
    embed = discord.Embed(title = "Leaderboard global", description = "Top 5 des utilisateurs les plus riches :moneybag: ", color = Color.gold())
    for user in topFive:
      fetch_user = await bot.fetch_user(user['userid'])
      guild = bot.get_guild(user['guildid'])
      embed.add_field(name = f"{str(topFive.index(user)+1)}. {fetch_user.name} ({guild.name})", value = f"Pièces : `{str(user['coins'])}`")
    await ctx.send(embed = embed)
  except Exception as e:
    print(e)
    
    
# DEBOGAGE ---> CRUD USER EN DB
@bot.command(name = 'create', help = "DEBOGAGE CREATE USER")
async def create(ctx):
	save.createUser(ctx.author.id)

@bot.command(name = 'read', help = "DEBOGAGE READ USER")
async def read(ctx):
	save.read(ctx.author.id)

@bot.command(name = 'remove', help = "DEBOGAGE DELETE USER")
async def remove(ctx):
	save.remove(ctx.author.id)
  
@bot.command(name = 'list', help = "DEBOGAGE LIST USERS")
async def list(ctx):
  save.list()

@bot.command(name = 'CHECK', help = "DEBOGAGE CHECK IF USER EXISTS")
async def check(ctx):
  save.checkExist(ctx.author.id)
# FIN DEBOGAGE ---> CRUD USER EN DB

    
# ERROR MESSAGE
@bot.event
async def on_command_error(ctx, error):
  #COOLDOWN
  if isinstance(error, commands.CommandOnCooldown):
    remaining_time = str(datetime.timedelta(seconds=int(error.retry_after)))
    embed = discord.Embed(title = ":clock1: Relax !!", description = f'{ctx.author.mention}, tu pourras utiliser à nouveau cette commande dans ' + str(remaining_time), color = Color.red())
    await ctx.send(embed = embed)

#TODO : utiliser des pièces pour acheter un oeuf, sauvegarder les animaux des users, récap des commandes, faire une commande slots pour essayer de gagner des pièces, commande pour voir les cooldowns, étoffer le profil

#https://replit.com/talk/learn/Discord-bot-in-Python/141711#currency-system
    
# ACTIVER LE BOT
bot.run(os.environ['token'])
