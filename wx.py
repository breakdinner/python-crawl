from wxpy import *

bot = Bot()

myFriends = bot.friends()

sexDict = {'male': 0, 'female': 1}

for friend in myFriends:
    if friend.sex == 1:
        sexDict['male'] += 1
    elif friend.sex == 0:
        sexDict['female'] += 1

print(sexDict);