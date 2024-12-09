from replit import db

def createUser(_id, g_id):
  basicData = {
    'userid' : _id,
    'guildid' : g_id,
    'coins' : 0,
  }
  try:
    db[f"{_id}"] = basicData
    print(basicData)
    print(f"Utilisateur {_id} créé")
  except Exception as e :
    print(e)


def updateUser(data):
  _id = data['userid']
  print(_id)
  try:
    db[f"{_id}"] = data
    print(data)
    print(f"Utilisateur {_id} mis à jour")
  except Exception as e :
    print(e)    


def checkExist(_id):
  try:
    data = db[f"{_id}"]
    if len(data) > 0:
      data = dict(data)
      print('Utilisateur existant en DB')
      return data
  except Exception as e:
    print(e)


def read(_id):
  try:
    #print(db[f"{_id}"])
    data = db[f"{_id}"]
    if len(data) > 0:
      data = dict(data)
      return data
  except Exception as e:
    print(e)


def leaderboard_guild(guildid):
  try:
    user_ids = db.keys()
    dataList = []
    for uid in user_ids:
      uid = int(uid)
      userData = {
        'userid' : db[f"{uid}"]['userid'],
        'coins' : db[f"{uid}"]['coins'],
      }
      if db[f"{uid}"]['guildid'] == guildid:
        dataList.append(userData)
    #print("Leaderboard server OK")
    dataList = sorted(dataList, key = lambda i: i['coins'],reverse=True)
    results = dataList[:5]
    return results
  except Exception as e:
    print(e)


def leaderboard_global():
  try:
    user_ids = db.keys()
    dataList = []
    for uid in user_ids:
      uid = int(uid)
      userData = {
        'userid' : db[f"{uid}"]['userid'],
        'guildid' : db[f"{uid}"]['guildid'],
        'coins' : db[f"{uid}"]['coins'],
      }
      dataList.append(userData)
    #print("Leaderboard globale OK")
    dataList = sorted(dataList, key = lambda i: i['coins'],reverse=True)
    results = dataList[:5]
    return results
  except Exception as e:
    print(e)
    

def list():
  data = db.keys()
  print(data)


def remove(_id):
  del db[f"{_id}"]
  print(f"Utilisateur {_id} supprimé")
