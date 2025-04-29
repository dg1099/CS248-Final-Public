import requests
import datetime

locations = {'Lulu': [96, {'Breakfast': 148, 'Lunch': 149, 'Dinner': 312}], 
         'Bates': [95, {'Breakfast': 145, 'Lunch': 146, 'Dinner': 311}],
         'Stone D': [131, {'Breakfast': 261, 'Lunch': 262, 'Dinner': 263}], 
         'Tower': [97, {'Breakfast': 153, 'Lunch': 154, 'Dinner': 310}]
         }

def wellesleyCall(location, meal, date):
    locID = locations[location][0]
    mealID = locations[location][1][meal]
    baseURL = "https://dish.avifoodsystems.com/api/menu-items/week"
    params = {'date': date,
              'locationID': locID,
              'mealID': mealID}
    
    response = requests.get(baseURL, params=params)
    data = response.json()
    return data

print(datetime.date(2025, 4, 1))
data = wellesleyCall('Bates', 'Breakfast', datetime.date(2025, 4, 1))
print(data)