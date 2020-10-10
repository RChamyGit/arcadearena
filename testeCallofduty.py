import asyncio

import callofduty
from callofduty import Mode, Platform, Title


async def main(user, plataforma):

    client = await callofduty.Login("arcadearenaofc@gmail.com", "ArcadeArena2020")
    print(user)

    if plataforma == "BattleNet":
         results = await client.SearchPlayers(Platform.BattleNet, user, limit=3)
    if plataforma == "PlayStation":
         results = await client.SearchPlayers(Platform.PlayStation, user, limit=3)
    if plataforma == "Xbox":
        results = await client.SearchPlayers(Platform.Xbox, user, limit=3)
    if plataforma == "Activision":
        results = await client.SearchPlayers(Platform.Activision, user, limit=3)

    try:
        searchPlayer = results[0]
        profile = await searchPlayer.profile(Title.ModernWarfare, Mode.Warzone)
        level = profile["level"]
        wins = profile['lifetime']['mode']['br']['properties']["wins"]
        kd = profile['lifetime']['mode']['br']['properties']["kdRatio"]
        kills = profile['lifetime']['mode']['br']['properties']["kills"]
        topFive = profile['lifetime']['mode']['br']['properties']["topFive"]
        deaths = profile['lifetime']['mode']['br']['properties']["deaths"]

    #print(f"\n{searchPlayer.username} ({searchPlayer.platform.name})")
    #print(f"Level: {level}, K/D Ratio: {round(kd, 3)}, Wins: {wins} , Kills:{kills}, TopFive:{topFive}, Deaths:{deaths}")

        myDict = {'username': f'{searchPlayer.username}',
                  'plataform': f'{searchPlayer.platform.name}',
                  'level': f'{int(level)}',
                  'K/D Ratio': f'{round(kd, 2)}',
                  'Wins': f'{int(wins)}',
                  'Kills': f'{int(kills)}',
                  'TopFive': f'{int(topFive)}',
                  'Deaths': f'{int(deaths)}'}

        return myDict
    except Exception as e:
        #print(f' ERROR:       {str(e)}')
        return str('False')
def getuser(user, plataforma):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    data = asyncio.get_event_loop().run_until_complete(main(user, plataforma))
    return data
