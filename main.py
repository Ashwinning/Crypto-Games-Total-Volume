import requests
import json
import os

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
def GetIDs(folder):
    ids = []
    files = os.listdir('Lists/{}/'.format(folder))
    for file in files:
        with open('Lists/{}/'.format(folder)+file, 'r') as f:
            data = json.loads(f.read())
            for object in data['data']['list']:
                ids.append(object['id'])
    return ids
'''
Get individual chart for a dapp
'''
def GetChart(id):
    response = requests.get('https://dappradar.com/api/dapp/{}/graph'.format(id))
    data = response.json()
    return data


def SaveAllChartsAsJSON():
    games = GetIDs('games')
    #print 'GAMES'
    #print games
    gambling = GetIDs('gambling')
    for id in games:
        chart = GetChart(id)
        with open('Charts/{}/{}.json'.format('games',id),'w') as file:
            file.write(json.dumps(chart, indent=4))
    for id in gambling:
        chart = GetChart(id)
        with open('Charts/{}/{}.json'.format('gambling',id),'w') as file:
            file.write(json.dumps(chart, indent=4))

#SaveAllChartsAsJSON()

def TotalVolume(folder):
    totalVolume = 0
    files = os.listdir('Charts/{}/'.format(folder))
    for file in files:
        with open('Charts/{}/'.format(folder)+file, 'r') as f:
            data = json.loads(f.read())
            for object in data['data']:
                totalVolume += object['volume']
    return totalVolume

#print(TotalVolume('gambling'))


dataPoints = {}

def TotalVolumeOverTimeToCSV(folder):
    files = os.listdir('Charts/{}/'.format(folder))
    for file in files:
        with open('Charts/{}/'.format(folder)+file, 'r') as f:
            data = json.loads(f.read())
            for dataPoint in data['data']:
                if dataPoint['date'] in dataPoints.keys():
                    dataPoints[dataPoint['date']]['dau'] += dataPoint['dau']
                    dataPoints[dataPoint['date']]['volume'] += dataPoint['volume']
                else:
                    dataPoints[dataPoint['date']] = {'dau':dataPoint['dau'],'volume':dataPoint['volume']}

TotalVolumeOverTimeToCSV('combined')

with open('volume.csv','w') as f:
    for date in dataPoints.keys():
        f.write('date' + ',' + 'dau' + ',' + 'volume' + '\n')
        f.write(str(date) + ',' + str(dataPoints[date]['dau']) + ',' + str(dataPoints[date]['volume']) + '\n')
