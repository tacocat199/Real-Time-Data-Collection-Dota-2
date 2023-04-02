
class Realtime_Dota2_Parser():
    import pandas as pd
    import csv\

    f_buildings = {} # Dictionary containing information about buildings
    
       
    # Parser of dota 2 in realtime takes as input a json request and have as output a csv file call in_game_data.csv
    def __init__(self, real_data):
        # In these variables will be saved all the values and keys pairs given by json file to create a dictionary
        self.real_data = real_data
        self.provider = []
        self.provider_values = [] 
        self.maps = []
        self.maps_values = []
        self.player= []
        self.player_values = []
        self.hero = []
        self.hero_values = []
        self.buildings = []
        self.buildings_values = []
        self.abilities = []
        self.abilities_values = []
        self.items = []
        self.items_values = []
        self.columns = []
        self.values = []
        self.dict= []
        self.dictionary= []
        self.d_buildings = []
                
    # Getting all the values and keys
        try:
            for p in self.real_data['provider']:
                self.provider.append('provider.{}'.format(p))
                self.provider_values.append(real_data['provider'][p])
        except:
            pass

        try:
            for m in self.real_data['map']:
                self.maps.append('map.{}'.format(m))
                self.maps_values.append(real_data['map'][m])
        except:
            pass
        
        try:
            for r in self.real_data['player']:
                if r== "kill_list":
                    pass
                else:
                    self.player.append('player.{}'.format(r))
                    self.player_values.append(real_data['player'][r])
        except:
            pass
        
        try:
            for v in self.real_data['hero']:
                self.hero.append('hero.{}'.format(v))
                self.hero_values.append(real_data['hero'][v])
        except:
            pass

        try:
            if self.f_buildings == {}:
                for j in self.real_data['buildings']:
                    for k in self.real_data['buildings'][j]:
                        for h in self.real_data['buildings'][j][k]:
                            self.f_buildings['buildings.{}.{}.{}'.format(j,k,h)] = self.real_data['buildings'][j][k][h]
            else:
                for j in self.real_data['buildings']:
                    for k in self.real_data['buildings'][j]:
                        for h in real_data['buildings'][j][k]:
                            self.buildings.append('buildings.{}.{}.{}'.format(j,k,h))
                            self.buildings_values.append(real_data['buildings'][j][k][h])
                    
                    
        except:
            pass

        try:
            for a in self.real_data['abilities']:
                for b in self.real_data['abilities'][a]:
                    self.abilities.append('abilities.{}.{}'.format(a,b))
                    self.abilities_values.append(real_data['abilities'][a][b])
        except:
            pass
        
        
        try:
            for c in self.real_data['items']:
                for d in self.real_data['items'][c]:
                    self.items.append('items.{}.{}'.format(c,d))
                    self.items_values.append(real_data['items'][c][d])
        except:
            pass
        
        
                
        # Saving list of values and columns names for each arrived request in dict(not buldings)
        self.columns = self.provider + self.maps + self.player + self.hero + self.abilities 
        self.values = self.provider_values + self.maps_values + self.player_values + self.hero_values + self.abilities_values 
        self.dict = dict(zip(self.columns, self.values))
        # Saving list of values and columns names for buildings in d_buildings
        self.d_buildings = dict(zip(self.buildings, self.buildings_values))
        # Updating information about buildings in each post request
        for i in self.f_buildings.keys():
            if i in self.d_buildings.keys():
                self.f_buildings[i] = self.d_buildings[i]
            else:
                self.f_buildings[i] = 'Destroyed'
        # Creating the final dictionary with the information in dict and f_buildings
        self.dictionary = {**self.dict,**self.f_buildings}
        
        try: # Create and clean the csv file 
            if os.path.isfile('./in_game_data.csv'):
                pass
            else:
                with open("in_game_data.csv", 'w'):
                    pass
                
            if self.dictionary["map.game_state"] == 'DOTA_GAMERULES_STATE_GAME_IN_PROGRESS'or self.dictionary["map.game_state"] == 'DOTA_GAMERULES_STATE_POST_GAME':
                # Open a csv file in read mode
                with open("in_game_data.csv", 'r+') as csvfile:
                    csv_dict = [row for row in csv.DictReader(csvfile)]
                
                    if len(csv_dict) == 0: # checking if the file is empty
                        with open('in_game_data.csv', 'w') as csvfile: # if it the case, writing the header and the fist row
                            writer = csv.DictWriter(csvfile, fieldnames=self.dictionary.keys())
                            writer.writeheader()
                            writer.writerow(self.dictionary)
                    else:
                        with open('in_game_data.csv', 'a') as csvfile: # of not empty just write next row
                            writer = csv.DictWriter(csvfile, fieldnames=self.dictionary.keys())
                            writer.writerow(self.dictionary)

            else:
                pass
        
        except:
            pass