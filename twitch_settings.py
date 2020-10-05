#
import  urllib3
import urllib.parse
#
import json
# import requests as reqs
# #
urllib3.disable_warnings()
http = urllib3.PoolManager()
#
# # OAuth = 'r04uhg9ph5zcmbx1pxzuqazkd5g9om'


CLIENT_ID = 'c9u77qx1wc1p87ft08pxanzc4bcunl'
CLIENT_SECRET ='n5dkwuqd1i974uafcoh9s30bukyph6'
r = http.request('POST',f'https://id.twitch.tv/oauth2/token?client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}&grant_type=client_credentials')
# print(r.data)
OAuth = json.loads(r.data.decode('utf-8'))['access_token']
print(OAuth)
# r2 = http.request('POST',f'https://api.twitch.tv/helix/search/channels?query=dartchiolivi',headers=({
#  'client-id':f'{CLIENT_ID}',
# "Authorization": f"Bearer {OAuth}"
# }))
# print(r2.data)

headers = ({
    'client-id':CLIENT_ID,
"Authorization": "Bearer " + OAuth
})


import requests
r2 = requests.get(f'https://api.twitch.tv/helix/search/channels?query=dartchiolivi', headers=headers)

print(r2)

response_dict = json.loads(r2.text)
channelDetais = response_dict['data'][0]
id = channelDetais['id']
r3 =  requests.get(f'https://api.twitch.tv/helix/users/follows?to_id={id}', headers=headers)
response_dict2 = json.loads(r3.text)
print(response_dict2)






# # url = f"""https://id.twitch.tv/oauth2/revoke?client_id={CLIENT_ID}&token={OAuth}"""
# # print(url)
# url = "https://api.twitch.tv/helix/search/channels?query=raggaxe"

# url = f'https://id.twitch.tv/oauth2/token?client_id=<{CLIENT_ID}&client_secret={CLIENT_SECRET}&grant_type=client_credentials'
# url = 'https://id.twitch.tv/helix'
# headers = ({
#
#     'client-id':CLIENT_ID,
# # "Authorization": "OAuth " + OAuth
# })
#
# # # channel_id = http.request('GET', url,headers=)
# r = http.request(
#      'POST',
#     url,
#     headers= headers
#  )

# print(r.data)
# # Make the HTTP request.
# response = reqs.get(url, headers=headers)
#
#
#
# response_dict = json.loads(response.text)
# print(response_dict)



# def refreashToken():
#     newToken = 'r04uhg9ph5zcmbx1pxzuqazkd5g9oc'
#     url = f'https://id.twitch.tv/oauth2/token--data-urlencode?grant_type=refresh_token&refresh_token={newToken} &client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}'
#     r = http.request(
#          'POST', url
#      )
#     # newDict = json.loads(r.text)
#     # print(newDict)
#     print(r)
# refreashToken()
 # r = requests.post(f"""https://id.twitch.tv/oauth2/token
# #     #     ?client_id={client_id}
# #     #     &client_secret={client_secret}
# #     #     &grant_type=client_credentials
# #     #     """)
# #     #
# print(json.load(r.data))
# print(json.loads(r.data.decode('utf-8'))['headers'])
 # json.loads(r.data.decode('utf-8'))['headers']

# channel_id.add_header("Client-ID", CLIENT_ID)
# channel_id.add_header("Authorization", "OAuth " + f"{OAuth}")
#
# response = urllib.request.urlopen(channel_id)
# tmpJSON = json.loads(response.read())
#
# print( str(tmpJSON['_id']))


# def make_request(URL):
#     CLIENT_ID = 'y5dnz65ei1o4whoukrg0nnmowqzsc0'
#     header ={'client-id':CLIENT_ID}
#     req = urllib.request.Request(URL, headers=header)
#     recv = urllib.request.urlopen(req)
#     return  json.load(recv.read().decode('utf-8'))
# def main():
#     pass
#
# def get_current_online_streams():
#     streamer = ['raggaxe']
#     URL = 'https://id.twitch.tv/helix/streams/metadata?user_login='
#     resp = []
#     online_streams = []
#     for name in streamer:
#         resp.append(make_request(URL + name))
#
#     print(resp)
#
# if __name__ == '__main__':
#     get_current_online_streams()
#
#
#
# #
# #
# # import requests, json,sys
# #

import  urllib.request
import  urllib.parse
import json




import urllib.request

# CLIENT_ID = 'y5dnz65ei1o4whoukrg0nnmowqzsc0'



#
#
# def main():
#     pass
#
# def get_current_online_streams():
#     streams = ['raggaxe','dartchiolivi']
#     # BASE_URL = 'https://api.twitch.tv/helix/users?login='
#     url = f'https://id.twitch.tv/oauth2/token?client_id=<{CLIENT_ID}&client_secret={CLIENT_SECRET}&grant_type=client_credentials'
#
#     resps = []
#     online_streams = []
#
#     for name in streams:
#         resps.append(make_request(BASE_URL + name))
#     print(resps)
#     # make_request(BASE_URL)
#
#
#
# def make_request(URL):
#     CLIENT_ID = 'c9u77qx1wc1p87ft08pxanzc4bcunl'
#     # CLIENT_SECRET ='n5dkwuqd1i974uafcoh9s30bukyph6'
#     # OAuth = 'ofrz51jpfb0bm7fq0d26jl2o2nysx2'
#     # HEADERS = ({'client-id': CLIENT_ID,
#     #            "Authorization": "OAuth " + OAuth
#     #            })
#     # INDENT = 2
#
#     req = http.request('get',URL)
#     print(req.status)
#     # recv = urllib.request.urlopen((req))
#     # return json.loads(recv.read().decode('utf-8'))
#
# # def get_responde(query):
# #     url =BASE_URL + query
# #     response = requests.get(url,headers=HEADERS)
# #     return response
#
# def print_response(response):
#     response_json = response.json()
#     # print_response = json.dumps(response_json,indent=INDENT)
#     print(response_json)
#
# def get_user_streams_query(user_login):
#     return f'streams?user_login={user_login}'
#
# def get_user_query(user_login):
#     return f'streams?login={user_login}'
# def get_user_videos(use_id):
#     return f'streams?login={use_id}&first=50'
#
#
#     # client_id = {'client_id': 'y5dnz65ei1o4whoukrg0nnmowqzsc0'}
#     # client_secret = {'client_secret': 'pxqIyySFxDZA1HbT4EdiXPIAKYWYy8BK/y75UTCeFUM='}
#     #
#     # r = requests.post(f"""https://id.twitch.tv/oauth2/token
#     #     ?client_id={client_id}
#     #     &client_secret={client_secret}
#     #     &grant_type=client_credentials
#     #     """)
#     #
#     # print(r)
#
# if __name__ == '__main__':
#     get_current_online_streams()
#
#
#
#
#
#
