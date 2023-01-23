import discord
import requests
from operator import itemgetter

#configure discord
intents = discord.Intents.all()
client = discord.Client(command_prefix='!', intents=intents)
 

#set headers for json
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

#set the URL for the API
api_url = "https://nykloo.com/api/PlayerStats/Stats/"

#static list of members for now. Need to externalise.
members = ["74858C942F89E7CD","2C46189ECA58F6E9","D737372B153287B6","35D271462D9D51C9","DAB84E33EF1FB7A3","353294D952B83FE5","9C407141D884E344","AD04C0C21AACF21B","515FE93B4DD376F0","CC97CACB108F523C","C093C64B548B3359"]

#function to get the api data and do some quick maths
def getDatafrom_API(members):
    d=[]
    # loop the members list and get API reponse for each
    for member in members:
        #form the URL and Querystring and get API response
        response = requests.get(api_url + member)
        #try the API and test the response
        if response.status_code == 200:
            #parse the resu
            data = response.json()
            #loop the dictionary to find the data we want and save the data to a variable
            for statistic in data['playerStatistics']:
                if statistic['statisticName'] == 'SeasonKills':
                    season_kills = statistic['value']
                elif statistic['statisticName'] == 'SeasonGamesPlayed':
                    season_games_played = statistic['value']
                elif statistic['statisticName'] == 'SeasonDamage':
                    season_damage = statistic['value']
                elif statistic['statisticName'] == 'SeasonWins':
                    season_wins = statistic['value']
            #append the data to a dictionary
            d.append(
                {"playerName": data['accountInfo']['titleInfo']['displayName'],
                #"playerAvatar": data['accountInfo']['titleInfo']['avatarUrl'],
                "seasonGamesPlayed": season_games_played,
                #"seasonKills" : season_kills,
                #"seasonDamage": season_damage,
                #"seasonWins" : season_wins,
                "seasonAVGKills" : season_kills / season_games_played,
                "seasonAVGDamage" : season_damage /season_games_played,
                "seasonAVGWins" : (season_wins / season_games_played)*100
                }
            )

        else:
            #catch the response errors
            print('API CALL FAILED: ' + api_url + member)
    return d

#connect to discord server
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
 
#get and send messges to the discord server
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    #the command to fire off the function
    if message.content.startswith('/getstats'):
        #send some messages to the user, let them know whats going down
        await message.channel.send("Loading the data...\nPlease wait...")
        await message.channel.send("This might take a while\nStats are a big messed up, im working on it.")
        #do the api call
        m = getDatafrom_API(members)
        #sort the returned data
        m = sorted(m, key=itemgetter('seasonAVGWins'), reverse=True)
        await message.channel.send("SEASON STATS IN ORDER OF HIGHEST WIN RATIO")
        #build and send the messsage, looping though the members list
        for x in m:
            msg= ""
           # msg += x['playerName'].ljust(30, ' ') + ",  {:.0f}".format(x['seasonGamesPlayed']) +"       , {:.2f}".format(x['seasonAVGKills']) +"       , {:.2f}".format(x['seasonAVGDamage']) +"       , {:.2f}".format(x['seasonAVGWins']) +"%\n"
            msg +="--------------------------------------------------------\n"
            msg += "Player: " +x['playerName'] +"\nGames Played This Season:  {:.0f}".format(x['seasonGamesPlayed'])+"\n"
            msg += "Season Average Kills Per Game: {:.0f}".format(x['seasonAVGKills']) +"\nSeason Average Damage Per Game: {:.0f}".format(x['seasonAVGDamage'])+"\n"
            msg += "Season Win Ratio: {:.2f}".format(x['seasonAVGWins']) +"%\n\n"
            await message.channel.send(msg)


        
#need to set up as application key 
client.run('')


