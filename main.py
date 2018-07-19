import requests
import json

'''
Allows the user to get a list of all the apps listed for a category.
Count is the number of pages on dappradar which need to be scanned.
Category is the ... well ... category. (e.g. 'games', 'gambling', etc.)
'''
def GetList(count, category):
    i = 0
    while (i < count + 1):
        url = "https://dappradar.com/api/dapps/list/{}".format(i)
        headers = {
        'referer': "https://dappradar.com/category/{}".format(category)
        }
        response = requests.request("GET", url, headers=headers)
        data = response.json()
        with open('Lists/{}/{}.json'.format(category,i),'w') as file:
            file.write(json.dumps(data, indent=4))
        i += 1

#GetList(6, 'games')
#GetList(2, 'gambling')

'''
Get IDs from the JSON files Collected
'''
def GetIDs():
    

'''
Get individual chart for a dapp
'''
def GetChart(id):
    response = requests.get('https://dappradar.com/api/dapp/{}/graph'.format(id))
    data = response.json()