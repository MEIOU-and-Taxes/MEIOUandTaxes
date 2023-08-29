# This generates the code for expedition related files

# Python 3.6 or later
from pathlib import Path
import os
import sys
import codecs
import pprint
import re

expedition_duration = 242  # normal 242 (arbitrary but want within same year yet not too close to end), change to 3 for testing

menu_event_number = 3  # Called from disasters/pulse_system If this number changes must also change there
expedition_arrival_start_number = 100
expedition_landing_start_number = 200
expedition_success_start_number = 300
expedition_total_failure_start_number = 400
expedition_map_failure_start_number = 500
expedition_trade_failure_start_number = 600
expedition_no_attack_failure_start_number = 700
expedition_decision_events_start_number = 800


class Expedition:
    def __init__(self, name, localized_name, ai_preference, target_type, associated_TN):
        self.name = name
        self.localized_name = localized_name
        self.ai_preference = ai_preference
        self.target_type = target_type
        self.associated_TN = associated_TN
        self.node_tech_reqs = []
        self.target_provinces = []

    def set_node_tech_reqs(self, node_tech_reqs):  # should be list of tuple pairs of node name and tech level
        assert len(self.node_tech_reqs) == 0, "Should only done once, setting to an empty list."
        self.node_tech_reqs = node_tech_reqs


# Balancing notes: 13 for your own area, 15 for directly next to, 16 for if have coast to go along, 17 if need north/south accuracy
expeditions_list = []  # Expeditions must have appropriately named province groups in in map/provincegroup.txt
# the British Isles
expeditions_list.append(Expedition('british_isles', 'the British Isles', 0, 'Jumping Node', [81]))
expeditions_list[-1].set_node_tech_reqs(
    [('Iberia', 25), ('Strait of Gibraltar', 25), ('Alboran Sea', 25), ('Gulf of Lion', 25), ('Bay of Biscay', 23), ('France', 23), ('North Sea', 23), ('Channel', 23), ('Norwegian Sea', 23), ('Western Baltic', 23), ('Berber Coast', 25), ('Maghreb', 25), ('Tyrrenean Sea', 25), ('Rhineland', 23), ('Upper Danube', 23), ('Lower Nile', 25), ('Po Valley', 25), ('Adriatic Sea', 25), ('Levantine Sea', 25), ('Aegean Sea', 25),
     ('Dniester', 25), ('Lower Danube', 25), ('Middle Danube', 25), ('Elbe', 23), ('Eastern Baltic', 25), ('Vistula', 25), ('Black Sea', 25), ('Western Siberia', 25), ('Dnipro', 25), ('Volga', 25), ('Great Steppe', 25), ('Caspian Sea', 25), ('Zalesye', 25), ('Caucasus', 25), ('Anatolia', 25), ('Sahara', 25), ('Senegambia', 27), ('Upper Niger', 27), ('Guinea Coast', 28), ('Volta', 28), ('Lower Niger', 28), ('Lake Tchad', 28), ('Kongo', 28),
     ('South Africa', 30), ('African Great Lakes', 30), ('Monomotapa', 30), ('Somalia', 30), ('Zanj', 30), ('Red Sea', 32), ('Abyssinian Highlands', 32), ('Upper Nile', 32), ('Jazira', 32), ('Arabian Peninsula', 32), ('Arabian Gulf', 32), ('Iran', 32), ('Khorasan', 32), ('Mawarannahr', 32), ('Tarim Basin', 32),
     ('Punjab', 32), ('Sindh', 32), ('Gurjaratra', 32), ('Konkan', 32), ('Northern Deccan', 32), ('Southern Deccan', 32), ('Tamilakam', 32), ('Kalinga', 32), ('Gondwana', 32), ('Malwa', 32), ('Rajasthan', 32), ('Doab', 32), ('Bihar', 32), ('Assam', 32), ('Bengal', 32), ('Himalayas', 32), ('Tibetan Plateau', 32), ('Guangxi', 32), ('Yunnan', 32), ('Lower Ayeyarwady', 33), ('Upper Ayeyarwady', 33), ('Malacca Strait', 33), ('Mekong', 33), ('Chao Phraya', 33), ('Sunda Strait', 33),
     ('Champa Sea', 33), ('Moluccas', 33), ('Australia', 33), ('Liangguang', 33), ('Szechwan', 33), ('Huazhong', 33), ('Jiangxi', 33), ('Jiangnan', 33), ('Fujian', 33), ('Huabei', 33), ('Xibei', 33), ('Zhongyuan', 33), ('Huai He', 33), ('Eastern Siberia', 33), ('East Sea', 33), ('Nippon', 33),
     ('Yellow Sea', 33), ('Amur', 33), ('Chala', 32), ('Southern Andes', 32), ('Central Andes', 32), ('Southern Cone', 31), ('Guiana', 30), ('Northern Andes', 30), ('Amazonia', 32), ('Cerrado', 32), ('Isthmus of Darien', 31), ('Caribbean', 30), ('Valley of Mexico', 31), ('Western Valley', 31), ('Gulf of Mexico', 31), ('Gulf of Tehuantepec', 31), ('Rio Grande', 31), ('Mississippi', 31), ('Western Cordillera', 31), ('Plains', 31), ('Eastern Seaboard', 29), ('Great Lakes', 29),
     ('American West Coast', 33), ('Pacific', 43)])
# Northern Europe
expeditions_list.append(Expedition('northern_europe', 'Northern Europe', 0, 'Jumping Node', [85]))
expeditions_list[-1].set_node_tech_reqs(
    [('Iberia', 25), ('Strait of Gibraltar', 25), ('Alboran Sea', 25), ('Gulf of Lion', 25), ('Bay of Biscay', 23), ('France', 23), ('North Sea', 23), ('Channel', 23), ('Norwegian Sea', 23), ('Western Baltic', 23), ('Berber Coast', 25), ('Maghreb', 25), ('Tyrrenean Sea', 25), ('Rhineland', 23), ('Upper Danube', 23), ('Lower Nile', 25), ('Po Valley', 25), ('Adriatic Sea', 25), ('Levantine Sea', 25), ('Aegean Sea', 25),
     ('Dniester', 25), ('Lower Danube', 25), ('Middle Danube', 25), ('Elbe', 23), ('Eastern Baltic', 23), ('Vistula', 25), ('Black Sea', 25), ('Western Siberia', 25), ('Dnipro', 25), ('Volga', 25), ('Great Steppe', 25), ('Caspian Sea', 25), ('Zalesye', 25), ('Caucasus', 25), ('Anatolia', 25), ('Sahara', 25), ('Senegambia', 27), ('Upper Niger', 27), ('Guinea Coast', 28), ('Volta', 28), ('Lower Niger', 28), ('Lake Tchad', 28), ('Kongo', 28),
     ('South Africa', 30), ('African Great Lakes', 30), ('Monomotapa', 30), ('Somalia', 30), ('Zanj', 30), ('Red Sea', 32), ('Abyssinian Highlands', 32), ('Upper Nile', 32), ('Jazira', 32), ('Arabian Peninsula', 32), ('Arabian Gulf', 32), ('Iran', 32), ('Khorasan', 32), ('Mawarannahr', 32), ('Tarim Basin', 32),
     ('Punjab', 32), ('Sindh', 32), ('Gurjaratra', 32), ('Konkan', 32), ('Northern Deccan', 32), ('Southern Deccan', 32), ('Tamilakam', 32), ('Kalinga', 32), ('Gondwana', 32), ('Malwa', 32), ('Rajasthan', 32), ('Doab', 32), ('Bihar', 32), ('Assam', 32), ('Bengal', 32), ('Himalayas', 32), ('Tibetan Plateau', 32), ('Guangxi', 32), ('Yunnan', 32), ('Lower Ayeyarwady', 33), ('Upper Ayeyarwady', 33), ('Malacca Strait', 33), ('Mekong', 33), ('Chao Phraya', 33), ('Sunda Strait', 33),
     ('Champa Sea', 33), ('Moluccas', 33), ('Australia', 33), ('Liangguang', 33), ('Szechwan', 33), ('Huazhong', 33), ('Jiangxi', 33), ('Jiangnan', 33), ('Fujian', 33), ('Huabei', 33), ('Xibei', 33), ('Zhongyuan', 33), ('Huai He', 33), ('Eastern Siberia', 33), ('East Sea', 33), ('Nippon', 33),
     ('Yellow Sea', 33), ('Amur', 33), ('Chala', 32), ('Southern Andes', 32), ('Central Andes', 32), ('Southern Cone', 31), ('Guiana', 30), ('Northern Andes', 30), ('Amazonia', 32), ('Cerrado', 32), ('Isthmus of Darien', 31), ('Caribbean', 30), ('Valley of Mexico', 31), ('Western Valley', 31), ('Gulf of Mexico', 31), ('Gulf of Tehuantepec', 31), ('Rio Grande', 31), ('Mississippi', 31), ('Western Cordillera', 31), ('Plains', 31), ('Eastern Seaboard', 29), ('Great Lakes', 29),
     ('American West Coast', 33), ('Pacific', 43)])
# France
expeditions_list.append(Expedition('france', 'France', 0, 'Jumping Node', [81]))
expeditions_list[-1].set_node_tech_reqs(
    [('Iberia', 23), ('Strait of Gibraltar', 25), ('Alboran Sea', 25), ('Gulf of Lion', 25), ('Bay of Biscay', 23), ('France', 23), ('North Sea', 23), ('Channel', 23), ('Norwegian Sea', 23), ('Western Baltic', 23), ('Berber Coast', 25), ('Maghreb', 25), ('Tyrrenean Sea', 25), ('Rhineland', 23), ('Upper Danube', 23), ('Lower Nile', 25), ('Po Valley', 25), ('Adriatic Sea', 25), ('Levantine Sea', 25), ('Aegean Sea', 25),
     ('Dniester', 25), ('Lower Danube', 25), ('Middle Danube', 25), ('Elbe', 23), ('Eastern Baltic', 25), ('Vistula', 25), ('Black Sea', 25), ('Western Siberia', 25), ('Dnipro', 25), ('Volga', 25), ('Great Steppe', 25), ('Caspian Sea', 25), ('Zalesye', 25), ('Caucasus', 25), ('Anatolia', 25), ('Sahara', 25), ('Senegambia', 27), ('Upper Niger', 27), ('Guinea Coast', 28), ('Volta', 28), ('Lower Niger', 28), ('Lake Tchad', 28), ('Kongo', 28),
     ('South Africa', 30), ('African Great Lakes', 30), ('Monomotapa', 30), ('Somalia', 30), ('Zanj', 30), ('Red Sea', 32), ('Abyssinian Highlands', 32), ('Upper Nile', 32), ('Jazira', 32), ('Arabian Peninsula', 32), ('Arabian Gulf', 32), ('Iran', 32), ('Khorasan', 32), ('Mawarannahr', 32), ('Tarim Basin', 32),
     ('Punjab', 32), ('Sindh', 32), ('Gurjaratra', 32), ('Konkan', 32), ('Northern Deccan', 32), ('Southern Deccan', 32), ('Tamilakam', 32), ('Kalinga', 32), ('Gondwana', 32), ('Malwa', 32), ('Rajasthan', 32), ('Doab', 32), ('Bihar', 32), ('Assam', 32), ('Bengal', 32), ('Himalayas', 32), ('Tibetan Plateau', 32), ('Guangxi', 32), ('Yunnan', 32), ('Lower Ayeyarwady', 33), ('Upper Ayeyarwady', 33), ('Malacca Strait', 33), ('Mekong', 33), ('Chao Phraya', 33), ('Sunda Strait', 33),
     ('Champa Sea', 33), ('Moluccas', 33), ('Australia', 33), ('Liangguang', 33), ('Szechwan', 33), ('Huazhong', 33), ('Jiangxi', 33), ('Jiangnan', 33), ('Fujian', 33), ('Huabei', 33), ('Xibei', 33), ('Zhongyuan', 33), ('Huai He', 33), ('Eastern Siberia', 33), ('East Sea', 33), ('Nippon', 33),
     ('Yellow Sea', 33), ('Amur', 33), ('Chala', 32), ('Southern Andes', 32), ('Central Andes', 32), ('Southern Cone', 31), ('Guiana', 30), ('Northern Andes', 30), ('Amazonia', 32), ('Cerrado', 32), ('Isthmus of Darien', 31), ('Caribbean', 30), ('Valley of Mexico', 31), ('Western Valley', 31), ('Gulf of Mexico', 31), ('Gulf of Tehuantepec', 31), ('Rio Grande', 31), ('Mississippi', 31), ('Western Cordillera', 31), ('Plains', 31), ('Eastern Seaboard', 29), ('Great Lakes', 29),
     ('American West Coast', 33), ('Pacific', 43)])
# Iberia
expeditions_list.append(Expedition('iberia', 'Iberia', 0, 'Jumping Node', [70, 74]))
expeditions_list[-1].set_node_tech_reqs(
    [('Iberia', 23), ('Strait of Gibraltar', 23), ('Alboran Sea', 25), ('Gulf of Lion', 25), ('Bay of Biscay', 25), ('France', 25), ('North Sea', 25), ('Channel', 25), ('Norwegian Sea', 25), ('Western Baltic', 25), ('Berber Coast', 25), ('Maghreb', 25), ('Tyrrenean Sea', 25), ('Rhineland', 25), ('Upper Danube', 25), ('Lower Nile', 25), ('Po Valley', 25), ('Adriatic Sea', 25), ('Levantine Sea', 25), ('Aegean Sea', 25),
     ('Dniester', 25), ('Lower Danube', 25), ('Middle Danube', 25), ('Elbe', 25), ('Eastern Baltic', 25), ('Vistula', 25), ('Black Sea', 25), ('Western Siberia', 25), ('Dnipro', 25), ('Volga', 25), ('Great Steppe', 25), ('Caspian Sea', 25), ('Zalesye', 25), ('Caucasus', 25), ('Anatolia', 25), ('Sahara', 25), ('Senegambia', 26), ('Upper Niger', 26),
     ('Guinea Coast', 27), ('Volta', 27), ('Lower Niger', 27), ('Lake Tchad', 27), ('Kongo', 28), ('South Africa', 30), ('African Great Lakes', 30), ('Monomotapa', 30), ('Somalia', 30), ('Zanj', 30), ('Red Sea', 32), ('Abyssinian Highlands', 32), ('Upper Nile', 32), ('Jazira', 32), ('Arabian Peninsula', 32), ('Arabian Gulf', 32), ('Iran', 32), ('Khorasan', 32), ('Mawarannahr', 32), ('Tarim Basin', 32),
     ('Punjab', 32), ('Sindh', 32), ('Gurjaratra', 32), ('Konkan', 32), ('Northern Deccan', 32), ('Southern Deccan', 32), ('Tamilakam', 32), ('Kalinga', 32), ('Gondwana', 32), ('Malwa', 32), ('Rajasthan', 32), ('Doab', 32), ('Bihar', 32), ('Assam', 32), ('Bengal', 32), ('Himalayas', 32), ('Tibetan Plateau', 32), ('Guangxi', 32), ('Yunnan', 32), ('Lower Ayeyarwady', 33), ('Upper Ayeyarwady', 33), ('Malacca Strait', 33), ('Mekong', 33), ('Chao Phraya', 33), ('Sunda Strait', 33),
     ('Champa Sea', 33), ('Moluccas', 33), ('Australia', 33), ('Liangguang', 33), ('Szechwan', 33), ('Huazhong', 33), ('Jiangxi', 33), ('Jiangnan', 33), ('Fujian', 33), ('Huabei', 33), ('Xibei', 33), ('Zhongyuan', 33), ('Huai He', 33), ('Eastern Siberia', 33), ('East Sea', 33), ('Nippon', 33),
     ('Yellow Sea', 33), ('Amur', 33), ('Chala', 32), ('Southern Andes', 32), ('Central Andes', 32), ('Southern Cone', 31), ('Guiana', 30), ('Northern Andes', 30), ('Amazonia', 32), ('Cerrado', 32), ('Isthmus of Darien', 31), ('Caribbean', 29), ('Valley of Mexico', 31), ('Western Valley', 31), ('Gulf of Mexico', 31), ('Gulf of Tehuantepec', 31), ('Rio Grande', 31), ('Mississippi', 31), ('Western Cordillera', 31), ('Plains', 31), ('Eastern Seaboard', 29), ('Great Lakes', 29),
     ('American West Coast', 33), ('Pacific', 43)])
# the Iberian Islands
expeditions_list.append(Expedition('iberian_islands', 'the Iberian Islands', 200, 'Jumping Node', [70, 74]))
expeditions_list[-1].set_node_tech_reqs(
    [('Iberia', 23), ('Strait of Gibraltar', 23), ('Alboran Sea', 25), ('Gulf of Lion', 25), ('Bay of Biscay', 25), ('France', 25), ('North Sea', 25), ('Channel', 25), ('Norwegian Sea', 25), ('Western Baltic', 25), ('Berber Coast', 25), ('Maghreb', 25), ('Tyrrenean Sea', 25), ('Rhineland', 25), ('Upper Danube', 25), ('Lower Nile', 25), ('Po Valley', 25), ('Adriatic Sea', 25), ('Levantine Sea', 25), ('Aegean Sea', 25),
     ('Dniester', 25), ('Lower Danube', 25), ('Middle Danube', 25), ('Elbe', 25), ('Eastern Baltic', 25), ('Vistula', 25), ('Black Sea', 25), ('Western Siberia', 25), ('Dnipro', 25), ('Volga', 25), ('Great Steppe', 25), ('Caspian Sea', 25), ('Zalesye', 25), ('Caucasus', 25), ('Anatolia', 25), ('Sahara', 25), ('Senegambia', 26), ('Upper Niger', 26),
     ('Guinea Coast', 27), ('Volta', 27), ('Lower Niger', 27), ('Lake Tchad', 27), ('Kongo', 28), ('South Africa', 30), ('African Great Lakes', 30), ('Monomotapa', 30), ('Somalia', 30), ('Zanj', 30), ('Red Sea', 32), ('Abyssinian Highlands', 32), ('Upper Nile', 32), ('Jazira', 32), ('Arabian Peninsula', 32), ('Arabian Gulf', 32), ('Iran', 32), ('Khorasan', 32), ('Mawarannahr', 32), ('Tarim Basin', 32),
     ('Punjab', 32), ('Sindh', 32), ('Gurjaratra', 32), ('Konkan', 32), ('Northern Deccan', 32), ('Southern Deccan', 32), ('Tamilakam', 32), ('Kalinga', 32), ('Gondwana', 32), ('Malwa', 32), ('Rajasthan', 32), ('Doab', 32), ('Bihar', 32), ('Assam', 32), ('Bengal', 32), ('Himalayas', 32), ('Tibetan Plateau', 32), ('Guangxi', 32), ('Yunnan', 32), ('Lower Ayeyarwady', 32), ('Upper Ayeyarwady', 32), ('Malacca Strait', 32), ('Mekong', 32), ('Chao Phraya', 32), ('Sunda Strait', 32),
     ('Champa Sea', 32), ('Moluccas', 32), ('Australia', 33), ('Liangguang', 33), ('Szechwan', 33), ('Huazhong', 33), ('Jiangxi', 33), ('Jiangnan', 33), ('Fujian', 33), ('Huabei', 33), ('Xibei', 33), ('Zhongyuan', 33), ('Huai He', 33), ('Eastern Siberia', 33), ('East Sea', 33), ('Nippon', 33),
     ('Yellow Sea', 33), ('Amur', 33), ('Chala', 32), ('Southern Andes', 32), ('Central Andes', 32), ('Southern Cone', 31), ('Guiana', 30), ('Northern Andes', 30), ('Amazonia', 30), ('Cerrado', 30), ('Isthmus of Darien', 31), ('Caribbean', 29), ('Valley of Mexico', 31), ('Western Valley', 31), ('Gulf of Mexico', 31), ('Gulf of Tehuantepec', 31), ('Rio Grande', 31), ('Mississippi', 31), ('Western Cordillera', 31), ('Plains', 31), ('Eastern Seaboard', 29), ('Great Lakes', 29),
     ('American West Coast', 33), ('Pacific', 43)])
# Northwest Africa
expeditions_list.append(Expedition('northwest_africa', 'Northwest Africa', 100, 'Jumping Node', [70]))
expeditions_list[-1].set_node_tech_reqs(
    [('Iberia', 23), ('Strait of Gibraltar', 23), ('Alboran Sea', 25), ('Gulf of Lion', 25), ('Bay of Biscay', 25), ('France', 25), ('North Sea', 25), ('Channel', 25), ('Norwegian Sea', 25), ('Western Baltic', 25), ('Berber Coast', 25), ('Maghreb', 25), ('Tyrrenean Sea', 25), ('Rhineland', 25), ('Upper Danube', 25), ('Lower Nile', 25), ('Po Valley', 25), ('Adriatic Sea', 25), ('Levantine Sea', 25), ('Aegean Sea', 25),
     ('Dniester', 25), ('Lower Danube', 25), ('Middle Danube', 25), ('Elbe', 25), ('Eastern Baltic', 25), ('Vistula', 25), ('Black Sea', 25), ('Western Siberia', 25), ('Dnipro', 25), ('Volga', 25), ('Great Steppe', 25), ('Caspian Sea', 25), ('Zalesye', 25), ('Caucasus', 25), ('Anatolia', 25), ('Sahara', 25), ('Senegambia', 26), ('Upper Niger', 26), ('Guinea Coast', 27), ('Volta', 27), ('Lower Niger', 27), ('Lake Tchad', 27), ('Kongo', 28),
     ('South Africa', 30), ('African Great Lakes', 30), ('Monomotapa', 30), ('Somalia', 30), ('Zanj', 30), ('Red Sea', 32), ('Abyssinian Highlands', 32), ('Upper Nile', 32), ('Jazira', 32), ('Arabian Peninsula', 32), ('Arabian Gulf', 32), ('Iran', 32), ('Khorasan', 32), ('Mawarannahr', 32), ('Tarim Basin', 32),
     ('Punjab', 32), ('Sindh', 32), ('Gurjaratra', 32), ('Konkan', 32), ('Northern Deccan', 32), ('Southern Deccan', 32), ('Tamilakam', 32), ('Kalinga', 32), ('Gondwana', 32), ('Malwa', 32), ('Rajasthan', 32), ('Doab', 32), ('Bihar', 32), ('Assam', 32), ('Bengal', 32), ('Himalayas', 32), ('Tibetan Plateau', 32), ('Guangxi', 32), ('Yunnan', 32), ('Lower Ayeyarwady', 32), ('Upper Ayeyarwady', 32), ('Malacca Strait', 32), ('Mekong', 32), ('Chao Phraya', 32), ('Sunda Strait', 32),
     ('Champa Sea', 32), ('Moluccas', 32), ('Australia', 33), ('Liangguang', 33), ('Szechwan', 33), ('Huazhong', 33), ('Jiangxi', 33), ('Jiangnan', 33), ('Fujian', 33), ('Huabei', 33), ('Xibei', 33), ('Zhongyuan', 33), ('Huai He', 33), ('Eastern Siberia', 33), ('East Sea', 33), ('Nippon', 33),
     ('Yellow Sea', 33), ('Amur', 33), ('Chala', 32), ('Southern Andes', 32), ('Central Andes', 32), ('Southern Cone', 31), ('Guiana', 30), ('Northern Andes', 30), ('Amazonia', 32), ('Cerrado', 32), ('Isthmus of Darien', 31), ('Caribbean', 29), ('Valley of Mexico', 31), ('Western Valley', 31), ('Gulf of Mexico', 31), ('Gulf of Tehuantepec', 31), ('Rio Grande', 31), ('Mississippi', 31), ('Western Cordillera', 31), ('Plains', 31), ('Eastern Seaboard', 29), ('Great Lakes', 29),
     ('American West Coast', 33), ('Pacific', 43)])
# West Africa
expeditions_list.append(Expedition('west_africa', 'West Africa', 800, 'Jumping Node', [51]))
expeditions_list[-1].set_node_tech_reqs(
    [('Iberia', 26), ('Strait of Gibraltar', 26), ('Sahara', 26), ('Alboran Sea', 27), ('Gulf of Lion', 27), ('Bay of Biscay', 27), ('France', 27), ('North Sea', 27), ('Channel', 27), ('Norwegian Sea', 27), ('Western Baltic', 27), ('Berber Coast', 27), ('Maghreb', 27), ('Tyrrenean Sea', 27), ('Rhineland', 27), ('Upper Danube', 27), ('Lower Nile', 27), ('Po Valley', 27), ('Adriatic Sea', 27), ('Levantine Sea', 27),
     ('Aegean Sea', 27), ('Dniester', 27), ('Lower Danube', 27), ('Middle Danube', 27), ('Elbe', 27), ('Eastern Baltic', 27), ('Vistula', 27), ('Black Sea', 27), ('Western Siberia', 27), ('Dnipro', 27), ('Volga', 27), ('Great Steppe', 27), ('Caspian Sea', 27), ('Zalesye', 27), ('Caucasus', 27), ('Anatolia', 27), ('Senegambia', 23), ('Upper Niger', 23), ('Guinea Coast', 23), ('Volta', 23), ('Lower Niger', 23), ('Lake Tchad', 23), ('Kongo', 25),
     ('South Africa', 27), ('African Great Lakes', 28), ('Monomotapa', 28), ('Somalia', 28), ('Zanj', 28), ('Red Sea', 30), ('Abyssinian Highlands', 30), ('Upper Nile', 30), ('Jazira', 30), ('Arabian Peninsula', 30), ('Arabian Gulf', 30), ('Iran', 30), ('Khorasan', 30), ('Mawarannahr', 30), ('Tarim Basin', 30),
     ('Punjab', 30), ('Sindh', 30), ('Gurjaratra', 30), ('Konkan', 30), ('Northern Deccan', 30), ('Southern Deccan', 30), ('Tamilakam', 30), ('Kalinga', 30), ('Gondwana', 30), ('Malwa', 30), ('Rajasthan', 30), ('Doab', 30), ('Bihar', 32), ('Assam', 32), ('Bengal', 30), ('Himalayas', 30), ('Tibetan Plateau', 30), ('Guangxi', 30), ('Yunnan', 30), ('Lower Ayeyarwady', 31), ('Upper Ayeyarwady', 31), ('Malacca Strait', 31), ('Mekong', 31), ('Chao Phraya', 31), ('Sunda Strait', 31),
     ('Champa Sea', 31), ('Moluccas', 31), ('Australia', 32), ('Liangguang', 32), ('Szechwan', 32), ('Huazhong', 32), ('Jiangxi', 32), ('Jiangnan', 32), ('Fujian', 32), ('Huabei', 32), ('Xibei', 32), ('Zhongyuan', 32), ('Huai He', 32), ('Eastern Siberia', 32), ('East Sea', 32), ('Nippon', 32),
     ('Yellow Sea', 32), ('Amur', 32), ('Chala', 31), ('Southern Andes', 31), ('Central Andes', 31), ('Southern Cone', 30), ('Guiana', 27), ('Northern Andes', 27), ('Amazonia', 31), ('Cerrado', 31), ('Isthmus of Darien', 31), ('Caribbean', 29), ('Valley of Mexico', 31), ('Western Valley', 31), ('Gulf of Mexico', 31), ('Gulf of Tehuantepec', 31), ('Rio Grande', 31), ('Mississippi', 31), ('Western Cordillera', 31), ('Plains', 31), ('Eastern Seaboard', 31), ('Great Lakes', 31),
     ('American West Coast', 32), ('Pacific', 43)])
# the Gulf of Guinea
expeditions_list.append(Expedition('gulf_of_guinea', 'the Gulf of Guinea', 800, 'Jumping Node', [48]))
expeditions_list[-1].set_node_tech_reqs(
    [('Iberia', 27), ('Strait of Gibraltar', 27), ('Sahara', 26), ('Alboran Sea', 28), ('Gulf of Lion', 28), ('Bay of Biscay', 28), ('France', 28), ('North Sea', 28), ('Channel', 28), ('Norwegian Sea', 28), ('Western Baltic', 28), ('Berber Coast', 28), ('Maghreb', 28), ('Tyrrenean Sea', 28), ('Rhineland', 28), ('Upper Danube', 28), ('Lower Nile', 28), ('Po Valley', 28), ('Adriatic Sea', 28), ('Levantine Sea', 28),
     ('Aegean Sea', 28), ('Dniester', 28), ('Lower Danube', 28), ('Middle Danube', 28), ('Elbe', 28), ('Eastern Baltic', 28), ('Vistula', 28), ('Black Sea', 28), ('Western Siberia', 28), ('Dnipro', 28), ('Volga', 28), ('Great Steppe', 28), ('Caspian Sea', 28), ('Zalesye', 28), ('Caucasus', 28), ('Anatolia', 28), ('Senegambia', 23), ('Upper Niger', 23), ('Guinea Coast', 23), ('Volta', 23), ('Lower Niger', 23), ('Lake Tchad', 23), ('Kongo', 23),
     ('South Africa', 27), ('African Great Lakes', 27), ('Monomotapa', 27), ('Somalia', 27), ('Zanj', 27), ('Red Sea', 30), ('Abyssinian Highlands', 30), ('Upper Nile', 30), ('Jazira', 31), ('Arabian Peninsula', 31), ('Arabian Gulf', 31), ('Iran', 31), ('Khorasan', 31), ('Mawarannahr', 31), ('Tarim Basin', 31),
     ('Punjab', 31), ('Sindh', 31), ('Gurjaratra', 31), ('Konkan', 31), ('Northern Deccan', 31), ('Southern Deccan', 31), ('Tamilakam', 31), ('Kalinga', 31), ('Gondwana', 31), ('Malwa', 31), ('Rajasthan', 31), ('Doab', 31), ('Bihar', 31), ('Assam', 31), ('Bengal', 31), ('Himalayas', 31), ('Tibetan Plateau', 31), ('Guangxi', 31), ('Yunnan', 31), ('Lower Ayeyarwady', 31), ('Upper Ayeyarwady', 31), ('Malacca Strait', 31), ('Mekong', 31), ('Chao Phraya', 31), ('Sunda Strait', 31),
     ('Champa Sea', 31), ('Moluccas', 31), ('Australia', 32), ('Liangguang', 32), ('Szechwan', 32), ('Huazhong', 32), ('Jiangxi', 32), ('Jiangnan', 32), ('Fujian', 32), ('Huabei', 32), ('Xibei', 32), ('Zhongyuan', 32), ('Huai He', 32), ('Eastern Siberia', 32), ('East Sea', 32), ('Nippon', 32),
     ('Yellow Sea', 32), ('Amur', 32), ('Chala', 31), ('Southern Andes', 31), ('Central Andes', 31), ('Southern Cone', 30), ('Guiana', 27), ('Northern Andes', 27), ('Amazonia', 31), ('Cerrado', 31), ('Isthmus of Darien', 31), ('Caribbean', 29), ('Valley of Mexico', 31), ('Western Valley', 31), ('Gulf of Mexico', 31), ('Gulf of Tehuantepec', 31), ('Rio Grande', 31), ('Mississippi', 31), ('Western Cordillera', 31), ('Plains', 31), ('Eastern Seaboard', 31), ('Great Lakes', 31),
     ('American West Coast', 32), ('Pacific', 43)])

# Central Africa
expeditions_list.append(Expedition('central_africa', 'Central Africa', 800, 'Jumping Node', [47]))
expeditions_list[-1].set_node_tech_reqs(
    [('Iberia', 28), ('Strait of Gibraltar', 28), ('Sahara', 27), ('Alboran Sea', 29), ('Gulf of Lion', 29), ('Bay of Biscay', 29), ('France', 29),
    ('North Sea', 29), ('Channel', 29), ('Norwegian Sea', 29), ('Western Baltic', 29), ('Berber Coast', 29), ('Maghreb', 29), ('Tyrrenean Sea', 29), ('Rhineland', 29), ('Upper Danube', 29), ('Lower Nile', 29), ('Po Valley', 29), ('Adriatic Sea', 29), ('Levantine Sea', 29), ('Aegean Sea', 29), ('Dniester', 29), ('Lower Danube', 29), ('Middle Danube', 29), ('Elbe', 29), ('Eastern Baltic', 29),
    ('Vistula', 29), ('Black Sea', 29), ('Western Siberia', 29), ('Dnipro', 29), ('Volga', 29), ('Great Steppe', 29), ('Caspian Sea', 29), ('Zalesye', 29), ('Caucasus', 29), ('Anatolia', 29), ('Senegambia', 25), ('Upper Niger', 23), ('Guinea Coast', 23), ('Volta', 23), ('Lower Niger', 23), ('Lake Tchad', 23), ('Kongo', 23), ('South Africa', 25), ('African Great Lakes', 27), ('Monomotapa', 27),
    ('Somalia', 27), ('Zanj', 27), ('Red Sea', 29), ('Abyssinian Highlands', 29), ('Upper Nile', 29), ('Jazira', 30), ('Arabian Peninsula', 30), ('Arabian Gulf', 30), ('Iran', 30), ('Khorasan', 30), ('Mawarannahr', 30), ('Tarim Basin', 30),
    ('Punjab', 30), ('Sindh', 30), ('Gurjaratra', 30), ('Konkan', 30), ('Northern Deccan', 30), ('Southern Deccan', 30), ('Tamilakam', 30), ('Kalinga', 30), ('Gondwana', 30), ('Malwa', 30), ('Rajasthan', 30), ('Doab', 30), ('Bihar', 30), ('Assam', 30), ('Bengal', 30), ('Himalayas', 30), ('Tibetan Plateau', 30), ('Guangxi', 30), ('Yunnan', 30), ('Lower Ayeyarwady', 30), ('Upper Ayeyarwady', 30), ('Malacca Strait', 30),
    ('Mekong', 30), ('Chao Phraya', 30), ('Sunda Strait', 30),
    ('Champa Sea', 30), ('Moluccas', 30), ('Australia', 31), ('Liangguang', 31), ('Szechwan', 31), ('Huazhong', 31), ('Jiangxi', 31), ('Jiangnan', 31), ('Fujian', 31), ('Huabei', 31), ('Xibei', 31), ('Zhongyuan', 31), ('Huai He', 31), ('Eastern Siberia', 31), ('East Sea', 31), ('Nippon', 31),
    ('Yellow Sea', 31), ('Amur', 31), ('Chala', 31), ('Southern Andes', 31), ('Central Andes', 31), ('Southern Cone', 30), ('Guiana', 28), ('Northern Andes', 28), ('Amazonia', 31), ('Cerrado', 31), ('Isthmus of Darien', 31), ('Caribbean', 29), ('Valley of Mexico', 31), ('Western Valley', 31), ('Gulf of Mexico', 31), ('Gulf of Tehuantepec', 31), ('Rio Grande', 31), ('Mississippi', 31), ('Western Cordillera', 31), ('Plains', 31), ('Eastern Seaboard', 31), ('Great Lakes', 31),
    ('American West Coast', 32), ('Pacific', 43)])
# South Africa
expeditions_list.append(Expedition('south_africa', 'South Africa', 1200, 'Colonial Node', [44]))
expeditions_list[-1].set_node_tech_reqs(
    [('Iberia', 30), ('Strait of Gibraltar', 30), ('Sahara', 28), ('Alboran Sea', 30), ('Gulf of Lion', 30), ('Bay of Biscay', 30), ('France', 30), ('North Sea', 30), ('Channel', 30), ('Norwegian Sea', 30), ('Western Baltic', 30), ('Berber Coast', 30), ('Maghreb', 30), ('Tyrrenean Sea', 30), ('Rhineland', 30), ('Upper Danube', 30), ('Lower Nile', 30), ('Po Valley', 30), ('Adriatic Sea', 30), ('Levantine Sea', 30),
     ('Aegean Sea', 30), ('Dniester', 30), ('Lower Danube', 30), ('Middle Danube', 30), ('Elbe', 30), ('Eastern Baltic', 30),
     ('Vistula', 30), ('Black Sea', 30), ('Western Siberia', 30), ('Dnipro', 30), ('Volga', 30), ('Great Steppe', 30), ('Caspian Sea', 30), ('Zalesye', 30), ('Caucasus', 30), ('Anatolia', 30), ('Senegambia', 27), ('Upper Niger', 27), ('Guinea Coast', 27), ('Volta', 27), ('Lower Niger', 27), ('Lake Tchad', 27), ('Kongo', 25), ('South Africa', 23), ('African Great Lakes', 25), ('Monomotapa', 25), ('Somalia', 25), ('Zanj', 25), ('Red Sea', 26),
     ('Abyssinian Highlands', 26), ('Upper Nile', 26), ('Jazira', 27), ('Arabian Peninsula', 27), ('Arabian Gulf', 27), ('Iran', 27), ('Khorasan', 27), ('Mawarannahr', 27), ('Tarim Basin', 27),
     ('Punjab', 27), ('Sindh', 28), ('Gurjaratra', 28), ('Konkan', 28), ('Northern Deccan', 28), ('Southern Deccan', 28), ('Tamilakam', 28), ('Kalinga', 28), ('Gondwana', 28), ('Malwa', 28), ('Rajasthan', 28), ('Doab', 28), ('Bihar', 28), ('Assam', 28), ('Bengal', 28), ('Himalayas', 28), ('Tibetan Plateau', 28), ('Guangxi', 28), ('Yunnan', 28), ('Lower Ayeyarwady', 30), ('Upper Ayeyarwady', 30), ('Malacca Strait', 30), ('Mekong', 30), ('Chao Phraya', 30), ('Sunda Strait', 30),
     ('Champa Sea', 30), ('Moluccas', 30), ('Australia', 31), ('Liangguang', 30), ('Szechwan', 30), ('Huazhong', 30), ('Jiangxi', 30), ('Jiangnan', 30), ('Fujian', 30), ('Huabei', 30), ('Xibei', 30), ('Zhongyuan', 31), ('Huai He', 31), ('Eastern Siberia', 31), ('East Sea', 31), ('Nippon', 31),
     ('Yellow Sea', 31), ('Amur', 31), ('Chala', 31), ('Southern Andes', 31), ('Central Andes', 31), ('Southern Cone', 30), ('Guiana', 29), ('Northern Andes', 29), ('Amazonia', 31), ('Cerrado', 31), ('Isthmus of Darien', 31), ('Caribbean', 30), ('Valley of Mexico', 31), ('Western Valley', 31), ('Gulf of Mexico', 31), ('Gulf of Tehuantepec', 31), ('Rio Grande', 31), ('Mississippi', 31), ('Western Cordillera', 31), ('Plains', 31), ('Eastern Seaboard', 31), ('Great Lakes', 31),
     ('American West Coast', 32), ('Pacific', 43)])
# East Africa
expeditions_list.append(Expedition('east_africa', 'East Africa', 800, 'Jumping Node', [43]))
expeditions_list[-1].set_node_tech_reqs(
    [('Iberia', 30), ('Strait of Gibraltar', 30), ('Sahara', 30), ('Alboran Sea', 30), ('Gulf of Lion', 30), ('Bay of Biscay', 30), ('France', 30), ('North Sea', 30), ('Channel', 30), ('Norwegian Sea', 30), ('Western Baltic', 30), ('Berber Coast', 30), ('Maghreb', 30), ('Tyrrenean Sea', 30), ('Rhineland', 30), ('Upper Danube', 30), ('Lower Nile', 28), ('Po Valley', 30), ('Adriatic Sea', 30), ('Levantine Sea', 30),
     ('Aegean Sea', 30), ('Dniester', 30), ('Lower Danube', 30), ('Middle Danube', 30), ('Elbe', 30), ('Eastern Baltic', 30),
     ('Vistula', 30), ('Black Sea', 30), ('Western Siberia', 30), ('Dnipro', 30), ('Volga', 30), ('Great Steppe', 30), ('Caspian Sea', 30), ('Zalesye', 30), ('Caucasus', 30), ('Anatolia', 30), ('Senegambia', 28), ('Upper Niger', 28), ('Guinea Coast', 27), ('Volta', 28), ('Lower Niger', 28), ('Lake Tchad', 28), ('Kongo', 27), ('South Africa', 25), ('African Great Lakes', 23), ('Monomotapa', 23), ('Somalia', 23), ('Zanj', 23), ('Red Sea', 23),
     ('Abyssinian Highlands', 23), ('Upper Nile', 23), ('Jazira', 25), ('Arabian Peninsula', 25), ('Arabian Gulf', 25), ('Iran', 26), ('Khorasan', 26), ('Mawarannahr', 26), ('Tarim Basin', 26),
     ('Punjab', 26), ('Sindh', 27), ('Gurjaratra', 27), ('Konkan', 27), ('Northern Deccan', 27), ('Southern Deccan', 27), ('Tamilakam', 27), ('Kalinga', 27), ('Gondwana', 27), ('Malwa', 27), ('Rajasthan', 27), ('Doab', 27), ('Bihar', 27), ('Assam', 27), ('Bengal', 27), ('Himalayas', 27), ('Tibetan Plateau', 27), ('Guangxi', 27), ('Yunnan', 27), ('Lower Ayeyarwady', 29), ('Upper Ayeyarwady', 29), ('Malacca Strait', 29), ('Mekong', 30), ('Chao Phraya', 30), ('Sunda Strait', 30),
     ('Champa Sea', 30), ('Moluccas', 30), ('Australia', 31), ('Liangguang', 30), ('Szechwan', 30), ('Huazhong', 30), ('Jiangxi', 30), ('Jiangnan', 30), ('Fujian', 30), ('Huabei', 30), ('Xibei', 30), ('Zhongyuan', 31), ('Huai He', 31), ('Eastern Siberia', 31), ('East Sea', 31), ('Nippon', 31),
     ('Yellow Sea', 31), ('Amur', 31), ('Chala', 32), ('Southern Andes', 32), ('Central Andes', 32), ('Southern Cone', 31), ('Guiana', 30), ('Northern Andes', 30), ('Amazonia', 32), ('Cerrado', 32), ('Isthmus of Darien', 32), ('Caribbean', 31), ('Valley of Mexico', 32), ('Western Valley', 32), ('Gulf of Mexico', 32), ('Gulf of Tehuantepec', 32), ('Rio Grande', 32), ('Mississippi', 32), ('Western Cordillera', 32), ('Plains', 32), ('Eastern Seaboard', 32), ('Great Lakes', 32),
     ('American West Coast', 33), ('Pacific', 43)])
# the Indian Ocean
expeditions_list.append(Expedition('indian_ocean', 'the Indian Ocean', 800, 'Jumping Node', [43]))
expeditions_list[-1].set_node_tech_reqs(
    [('Iberia', 30), ('Strait of Gibraltar', 30), ('Sahara', 30), ('Alboran Sea', 30), ('Gulf of Lion', 30), ('Bay of Biscay', 30), ('France', 30), ('North Sea', 30), ('Channel', 30), ('Norwegian Sea', 30), ('Western Baltic', 30), ('Berber Coast', 30), ('Maghreb', 30), ('Tyrrenean Sea', 30), ('Rhineland', 30), ('Upper Danube', 30), ('Lower Nile', 28), ('Po Valley', 30), ('Adriatic Sea', 30), ('Levantine Sea', 30),
     ('Aegean Sea', 30), ('Dniester', 30), ('Lower Danube', 30), ('Middle Danube', 30), ('Elbe', 30), ('Eastern Baltic', 30),
     ('Vistula', 30), ('Black Sea', 30), ('Western Siberia', 30), ('Dnipro', 30), ('Volga', 30), ('Great Steppe', 30), ('Caspian Sea', 30), ('Zalesye', 30), ('Caucasus', 30), ('Anatolia', 30), ('Senegambia', 28), ('Upper Niger', 28), ('Guinea Coast', 27), ('Volta', 28), ('Lower Niger', 28), ('Lake Tchad', 28), ('Kongo', 27), ('South Africa', 25), ('African Great Lakes', 23), ('Monomotapa', 23), ('Somalia', 23), ('Zanj', 23), ('Red Sea', 25),
     ('Abyssinian Highlands', 25), ('Upper Nile', 25), ('Jazira', 27), ('Arabian Peninsula', 27), ('Arabian Gulf', 27), ('Iran', 27), ('Khorasan', 27), ('Mawarannahr', 27), ('Tarim Basin', 27),
     ('Punjab', 27), ('Sindh', 27), ('Gurjaratra', 27), ('Konkan', 27), ('Northern Deccan', 27), ('Southern Deccan', 27), ('Tamilakam', 27), ('Kalinga', 27), ('Gondwana', 27), ('Malwa', 27), ('Rajasthan', 27), ('Doab', 27), ('Bihar', 27), ('Assam', 27), ('Bengal', 27), ('Himalayas', 27), ('Tibetan Plateau', 27), ('Guangxi', 27), ('Yunnan', 27), ('Lower Ayeyarwady', 29), ('Upper Ayeyarwady', 29), ('Malacca Strait', 29), ('Mekong', 30), ('Chao Phraya', 30), ('Sunda Strait', 30),
     ('Champa Sea', 30), ('Moluccas', 30), ('Australia', 31), ('Liangguang', 30), ('Szechwan', 30), ('Huazhong', 30), ('Jiangxi', 30), ('Jiangnan', 30), ('Fujian', 30), ('Huabei', 30), ('Xibei', 30), ('Zhongyuan', 31), ('Huai He', 31), ('Eastern Siberia', 31), ('East Sea', 31), ('Nippon', 31),
     ('Yellow Sea', 31), ('Amur', 31), ('Chala', 32), ('Southern Andes', 32), ('Central Andes', 32), ('Southern Cone', 31), ('Guiana', 30), ('Northern Andes', 30), ('Amazonia', 32), ('Cerrado', 32), ('Isthmus of Darien', 32), ('Caribbean', 31), ('Valley of Mexico', 32), ('Western Valley', 32), ('Gulf of Mexico', 32), ('Gulf of Tehuantepec', 32), ('Rio Grande', 32), ('Mississippi', 32), ('Western Cordillera', 32), ('Plains', 32), ('Eastern Seaboard', 32), ('Great Lakes', 32),
     ('American West Coast', 33), ('Pacific', 43)])
# Arabian Gulf
expeditions_list.append(Expedition('arabia', 'Arabia', 400, 'Jumping Node', [41, 40]))
expeditions_list[-1].set_node_tech_reqs(
    [('Iberia', 30), ('Strait of Gibraltar', 30), ('Sahara', 30), ('Alboran Sea', 30), ('Gulf of Lion', 30), ('Bay of Biscay', 30), ('France', 30), ('North Sea', 30), ('Channel', 30), ('Norwegian Sea', 30), ('Western Baltic', 30), ('Berber Coast', 30), ('Maghreb', 30), ('Tyrrenean Sea', 30), ('Rhineland', 30), ('Upper Danube', 30), ('Lower Nile', 26), ('Po Valley', 30), ('Adriatic Sea', 30), ('Levantine Sea', 30),
     ('Aegean Sea', 30), ('Dniester', 30), ('Lower Danube', 30), ('Middle Danube', 30), ('Elbe', 30), ('Eastern Baltic', 30),
     ('Vistula', 30), ('Black Sea', 30), ('Western Siberia', 30), ('Dnipro', 30), ('Volga', 30), ('Great Steppe', 30), ('Caspian Sea', 30), ('Zalesye', 30), ('Caucasus', 30), ('Anatolia', 30), ('Senegambia', 30), ('Upper Niger', 30), ('Guinea Coast', 30), ('Volta', 30), ('Lower Niger', 30), ('Lake Tchad', 30), ('Kongo', 30), ('South Africa', 27), ('African Great Lakes', 26), ('Monomotapa', 26), ('Somalia', 25), ('Zanj', 25), ('Red Sea', 23),
     ('Abyssinian Highlands', 23), ('Upper Nile', 23), ('Jazira', 23), ('Arabian Peninsula', 23), ('Arabian Gulf', 23), ('Iran', 23), ('Khorasan', 23), ('Mawarannahr', 23), ('Tarim Basin', 23),
     ('Punjab', 23), ('Sindh', 25), ('Gurjaratra', 25), ('Konkan', 25), ('Northern Deccan', 25), ('Southern Deccan', 25), ('Tamilakam', 25), ('Kalinga', 25), ('Gondwana', 25), ('Malwa', 25), ('Rajasthan', 25), ('Doab', 25), ('Bihar', 25), ('Assam', 25), ('Bengal', 25), ('Himalayas', 25), ('Tibetan Plateau', 25), ('Guangxi', 25), ('Yunnan', 25), ('Lower Ayeyarwady', 27), ('Upper Ayeyarwady', 27), ('Malacca Strait', 27), ('Mekong', 27), ('Chao Phraya', 27), ('Sunda Strait', 27),
     ('Champa Sea', 27), ('Moluccas', 27), ('Australia', 29), ('Liangguang', 29), ('Szechwan', 29), ('Huazhong', 29), ('Jiangxi', 29), ('Jiangnan', 29), ('Fujian', 29), ('Huabei', 29), ('Xibei', 29), ('Zhongyuan', 30), ('Huai He', 30), ('Eastern Siberia', 30), ('East Sea', 30), ('Nippon', 30),
     ('Yellow Sea', 30), ('Amur', 30), ('Chala', 32), ('Southern Andes', 32), ('Central Andes', 32), ('Southern Cone', 31), ('Guiana', 30), ('Northern Andes', 30), ('Amazonia', 32), ('Cerrado', 32), ('Isthmus of Darien', 32), ('Caribbean', 31), ('Valley of Mexico', 32), ('Western Valley', 32), ('Gulf of Mexico', 32), ('Gulf of Tehuantepec', 32), ('Rio Grande', 32), ('Mississippi', 32), ('Western Cordillera', 32), ('Plains', 32), ('Eastern Seaboard', 32), ('Great Lakes', 32),
     ('American West Coast', 33), ('Pacific', 43)])
# Western India
expeditions_list.append(Expedition('western_india', 'Western India', 1200, 'Jumping Node', [36, 37]))
expeditions_list[-1].set_node_tech_reqs(
    [('Iberia', 30), ('Strait of Gibraltar', 30), ('Sahara', 30), ('Alboran Sea', 30), ('Gulf of Lion', 30), ('Bay of Biscay', 30), ('France', 30), ('North Sea', 30), ('Channel', 30), ('Norwegian Sea', 30), ('Western Baltic', 30), ('Berber Coast', 30), ('Maghreb', 30), ('Tyrrenean Sea', 30), ('Rhineland', 30), ('Upper Danube', 30), ('Lower Nile', 28), ('Po Valley', 30), ('Adriatic Sea', 30), ('Levantine Sea', 30),
     ('Aegean Sea', 30), ('Dniester', 30), ('Lower Danube', 30), ('Middle Danube', 30), ('Elbe', 30), ('Eastern Baltic', 30),
     ('Vistula', 30), ('Black Sea', 30), ('Western Siberia', 30), ('Dnipro', 30), ('Volga', 30), ('Great Steppe', 30), ('Caspian Sea', 30), ('Zalesye', 30), ('Caucasus', 30), ('Anatolia', 30), ('Senegambia', 30), ('Upper Niger', 30), ('Guinea Coast', 30), ('Volta', 30), ('Lower Niger', 30), ('Lake Tchad', 30), ('Kongo', 30), ('South Africa', 28), ('African Great Lakes', 27), ('Monomotapa', 27), ('Somalia', 27), ('Zanj', 27), ('Red Sea', 25),
     ('Abyssinian Highlands', 25), ('Upper Nile', 25), ('Jazira', 23), ('Arabian Peninsula', 23), ('Arabian Gulf', 23), ('Iran', 25), ('Khorasan', 25), ('Mawarannahr', 23), ('Tarim Basin', 23),
     ('Punjab', 23), ('Sindh', 23), ('Gurjaratra', 23), ('Konkan', 23), ('Northern Deccan', 23), ('Southern Deccan', 23), ('Tamilakam', 23), ('Kalinga', 25), ('Gondwana', 25), ('Malwa', 23), ('Rajasthan', 23), ('Doab', 23), ('Bihar', 23), ('Assam', 23), ('Bengal', 25), ('Himalayas', 25), ('Tibetan Plateau', 25), ('Guangxi', 25), ('Yunnan', 25), ('Lower Ayeyarwady', 27), ('Upper Ayeyarwady', 27), ('Malacca Strait', 27), ('Mekong', 27), ('Chao Phraya', 27), ('Sunda Strait', 27),
     ('Champa Sea', 27), ('Moluccas', 27), ('Australia', 28), ('Liangguang', 28), ('Szechwan', 28), ('Huazhong', 28), ('Jiangxi', 28), ('Jiangnan', 28), ('Fujian', 28), ('Huabei', 28), ('Xibei', 28), ('Zhongyuan', 29), ('Huai He', 29), ('Eastern Siberia', 29), ('East Sea', 29), ('Nippon', 29),
     ('Yellow Sea', 29), ('Amur', 29), ('Chala', 33), ('Southern Andes', 33), ('Central Andes', 33), ('Southern Cone', 32), ('Guiana', 31), ('Northern Andes', 31), ('Amazonia', 33), ('Cerrado', 33), ('Isthmus of Darien', 33), ('Caribbean', 32), ('Valley of Mexico', 33), ('Western Valley', 33), ('Gulf of Mexico', 33), ('Gulf of Tehuantepec', 33), ('Rio Grande', 33), ('Mississippi', 33), ('Western Cordillera', 33), ('Plains', 33), ('Eastern Seaboard', 33), ('Great Lakes', 33),
     ('American West Coast', 33), ('Pacific', 43)])
# Southern India
expeditions_list.append(Expedition('southern_india', 'Southern India', 1200, 'Jumping Node', [35, 36]))
expeditions_list[-1].set_node_tech_reqs(
    [('Iberia', 30), ('Strait of Gibraltar', 30), ('Sahara', 30), ('Alboran Sea', 30), ('Gulf of Lion', 30), ('Bay of Biscay', 30), ('France', 30), ('North Sea', 30), ('Channel', 30), ('Norwegian Sea', 30), ('Western Baltic', 30), ('Berber Coast', 30), ('Maghreb', 30), ('Tyrrenean Sea', 30), ('Rhineland', 30), ('Upper Danube', 30), ('Lower Nile', 28), ('Po Valley', 30), ('Adriatic Sea', 30), ('Levantine Sea', 30),
     ('Aegean Sea', 30), ('Dniester', 30), ('Lower Danube', 30), ('Middle Danube', 30), ('Elbe', 30), ('Eastern Baltic', 30),
     ('Vistula', 30), ('Black Sea', 30), ('Western Siberia', 30), ('Dnipro', 30), ('Volga', 30), ('Great Steppe', 30), ('Caspian Sea', 30), ('Zalesye', 30), ('Caucasus', 30), ('Anatolia', 30), ('Senegambia', 30), ('Upper Niger', 30), ('Guinea Coast', 30), ('Volta', 30), ('Lower Niger', 30), ('Lake Tchad', 30), ('Kongo', 30), ('South Africa', 28), ('African Great Lakes', 27), ('Monomotapa', 27), ('Somalia', 27), ('Zanj', 27), ('Red Sea', 25),
     ('Abyssinian Highlands', 25), ('Upper Nile', 25), ('Jazira', 25), ('Arabian Peninsula', 25), ('Arabian Gulf', 25), ('Iran', 25), ('Khorasan', 25), ('Mawarannahr', 25), ('Tarim Basin', 25),
     ('Punjab', 25), ('Sindh', 23), ('Gurjaratra', 23), ('Konkan', 23), ('Northern Deccan', 23), ('Southern Deccan', 23), ('Tamilakam', 23), ('Kalinga', 23), ('Gondwana', 23), ('Malwa', 23), ('Rajasthan', 23), ('Doab', 23), ('Bihar', 23), ('Assam', 23), ('Bengal', 25), ('Himalayas', 25), ('Tibetan Plateau', 25), ('Guangxi', 25), ('Yunnan', 25), ('Lower Ayeyarwady', 25), ('Upper Ayeyarwady', 25), ('Malacca Strait', 26), ('Mekong', 26), ('Chao Phraya', 26), ('Sunda Strait', 26),
     ('Champa Sea', 26), ('Moluccas', 26), ('Australia', 28), ('Liangguang', 28), ('Szechwan', 28), ('Huazhong', 28), ('Jiangxi', 28), ('Jiangnan', 28), ('Fujian', 28), ('Huabei', 28), ('Xibei', 28), ('Zhongyuan', 29), ('Huai He', 29), ('Eastern Siberia', 29), ('East Sea', 29), ('Nippon', 29),
     ('Yellow Sea', 29), ('Amur', 29), ('Chala', 33), ('Southern Andes', 33), ('Central Andes', 33), ('Southern Cone', 32), ('Guiana', 31), ('Northern Andes', 31), ('Amazonia', 33), ('Cerrado', 33), ('Isthmus of Darien', 33), ('Caribbean', 32), ('Valley of Mexico', 33), ('Western Valley', 33), ('Gulf of Mexico', 33), ('Gulf of Tehuantepec', 33), ('Rio Grande', 33), ('Mississippi', 33), ('Western Cordillera', 33), ('Plains', 33), ('Eastern Seaboard', 33), ('Great Lakes', 33),
     ('American West Coast', 33), ('Pacific', 43)])
# Eastern India
expeditions_list.append(Expedition('eastern_india', 'Eastern India', 1200, 'Jumping Node', [34, 35]))
expeditions_list[-1].set_node_tech_reqs(
    [('Iberia', 30), ('Strait of Gibraltar', 30), ('Sahara', 30), ('Alboran Sea', 30), ('Gulf of Lion', 30), ('Bay of Biscay', 30), ('France', 30), ('North Sea', 30), ('Channel', 30), ('Norwegian Sea', 30), ('Western Baltic', 30), ('Berber Coast', 30), ('Maghreb', 30), ('Tyrrenean Sea', 30), ('Rhineland', 30), ('Upper Danube', 30), ('Lower Nile', 28), ('Po Valley', 30), ('Adriatic Sea', 30), ('Levantine Sea', 30),
     ('Aegean Sea', 30), ('Dniester', 30), ('Lower Danube', 30), ('Middle Danube', 30), ('Elbe', 30), ('Eastern Baltic', 30),
     ('Vistula', 30), ('Black Sea', 30), ('Western Siberia', 30), ('Dnipro', 30), ('Volga', 30), ('Great Steppe', 30), ('Caspian Sea', 30), ('Zalesye', 30), ('Caucasus', 30), ('Anatolia', 30), ('Senegambia', 30), ('Upper Niger', 30), ('Guinea Coast', 30), ('Volta', 30), ('Lower Niger', 30), ('Lake Tchad', 30), ('Kongo', 30), ('South Africa', 28), ('African Great Lakes', 27), ('Monomotapa', 27), ('Somalia', 27), ('Zanj', 27), ('Red Sea', 26),
     ('Abyssinian Highlands', 26), ('Upper Nile', 26), ('Jazira', 25), ('Arabian Peninsula', 25), ('Arabian Gulf', 25), ('Iran', 25), ('Khorasan', 25), ('Mawarannahr', 25), ('Tarim Basin', 25),
     ('Punjab', 25), ('Sindh', 25), ('Gurjaratra', 25), ('Konkan', 25), ('Northern Deccan', 25), ('Southern Deccan', 25), ('Tamilakam', 23), ('Kalinga', 23), ('Gondwana', 23), ('Malwa', 23), ('Rajasthan', 23), ('Doab', 23), ('Bihar', 23), ('Assam', 23), ('Bengal', 23), ('Himalayas', 23), ('Tibetan Plateau', 23), ('Guangxi', 23), ('Yunnan', 23), ('Lower Ayeyarwady', 25), ('Upper Ayeyarwady', 25), ('Malacca Strait', 26), ('Mekong', 26), ('Chao Phraya', 26), ('Sunda Strait', 26),
     ('Champa Sea', 26), ('Moluccas', 26), ('Australia', 27), ('Liangguang', 26), ('Szechwan', 26), ('Huazhong', 27), ('Jiangxi', 27), ('Jiangnan', 27), ('Fujian', 27), ('Huabei', 27), ('Xibei', 27), ('Zhongyuan', 27), ('Huai He', 27), ('Eastern Siberia', 28), ('East Sea', 28), ('Nippon', 28),
     ('Yellow Sea', 28), ('Amur', 28), ('Chala', 33), ('Southern Andes', 33), ('Central Andes', 33), ('Southern Cone', 32), ('Guiana', 31), ('Northern Andes', 31), ('Amazonia', 33), ('Cerrado', 33), ('Isthmus of Darien', 33), ('Caribbean', 32), ('Valley of Mexico', 33), ('Western Valley', 33), ('Gulf of Mexico', 33), ('Gulf of Tehuantepec', 33), ('Rio Grande', 33), ('Mississippi', 33), ('Western Cordillera', 33), ('Plains', 33), ('Eastern Seaboard', 33), ('Great Lakes', 33),
     ('American West Coast', 33), ('Pacific', 43)])
# Malacca
expeditions_list.append(Expedition('malacca', 'Malacca', 800, 'Regular', [24]))
expeditions_list[-1].set_node_tech_reqs(
    [('Iberia', 31), ('Strait of Gibraltar', 31), ('Sahara', 31), ('Alboran Sea', 31), ('Gulf of Lion', 31), ('Bay of Biscay', 31), ('France', 31), ('North Sea', 31), ('Channel', 31), ('Norwegian Sea', 31), ('Western Baltic', 31), ('Berber Coast', 31), ('Maghreb', 31), ('Tyrrenean Sea', 31), ('Rhineland', 31), ('Upper Danube', 31), ('Lower Nile', 29), ('Po Valley', 31), ('Adriatic Sea', 31), ('Levantine Sea', 31),
     ('Aegean Sea', 31), ('Dniester', 31), ('Lower Danube', 31), ('Middle Danube', 31), ('Elbe', 31), ('Eastern Baltic', 31),
     ('Vistula', 31), ('Black Sea', 31), ('Western Siberia', 31), ('Dnipro', 31), ('Volga', 31), ('Great Steppe', 31), ('Caspian Sea', 31), ('Zalesye', 31), ('Caucasus', 31), ('Anatolia', 31), ('Senegambia', 31), ('Upper Niger', 31), ('Guinea Coast', 31), ('Volta', 31), ('Lower Niger', 31), ('Lake Tchad', 31), ('Kongo', 31), ('South Africa', 30), ('African Great Lakes', 30), ('Monomotapa', 30), ('Somalia', 30), ('Zanj', 30), ('Red Sea', 27),
     ('Abyssinian Highlands', 27), ('Upper Nile', 27), ('Jazira', 27), ('Arabian Peninsula', 27), ('Arabian Gulf', 27), ('Iran', 27), ('Khorasan', 27), ('Mawarannahr', 27), ('Tarim Basin', 27),
     ('Punjab', 27), ('Sindh', 27), ('Gurjaratra', 27), ('Konkan', 27), ('Northern Deccan', 27), ('Southern Deccan', 27), ('Tamilakam', 26), ('Kalinga', 25), ('Gondwana', 25), ('Malwa', 25), ('Rajasthan', 25), ('Doab', 25), ('Bihar', 25), ('Assam', 25), ('Bengal', 25), ('Himalayas', 25), ('Tibetan Plateau', 25), ('Guangxi', 25), ('Yunnan', 25), ('Lower Ayeyarwady', 23), ('Upper Ayeyarwady', 23), ('Malacca Strait', 23), ('Mekong', 25), ('Chao Phraya', 25), ('Sunda Strait', 23),
     ('Champa Sea', 25), ('Moluccas', 25), ('Australia', 27), ('Liangguang', 25), ('Szechwan', 25), ('Huazhong', 25), ('Jiangxi', 25), ('Jiangnan', 26), ('Fujian', 26), ('Huabei', 26), ('Xibei', 26), ('Eastern Siberia', 27), ('Zhongyuan', 26), ('Huai He', 26), ('East Sea', 27), ('Nippon', 27),
     ('Yellow Sea', 27), ('Amur', 27), ('Chala', 33), ('Southern Andes', 33), ('Central Andes', 33), ('Southern Cone', 32), ('Guiana', 31), ('Northern Andes', 31), ('Amazonia', 33), ('Cerrado', 33), ('Isthmus of Darien', 33), ('Caribbean', 32), ('Valley of Mexico', 33), ('Western Valley', 33), ('Gulf of Mexico', 33), ('Gulf of Tehuantepec', 33), ('Rio Grande', 33), ('Mississippi', 33), ('Western Cordillera', 33), ('Plains', 33), ('Eastern Seaboard', 33), ('Great Lakes', 33),
     ('American West Coast', 33), ('Pacific', 43)])
# Southeast Asia
expeditions_list.append(Expedition('southeast_asia', 'Southeast Asia', 600, 'Regular', [25, 20, 19]))
expeditions_list[-1].set_node_tech_reqs(
    [('Iberia', 31), ('Strait of Gibraltar', 31), ('Sahara', 31), ('Alboran Sea', 31), ('Gulf of Lion', 31), ('Bay of Biscay', 31), ('France', 31), ('North Sea', 31), ('Channel', 31), ('Norwegian Sea', 31), ('Western Baltic', 31), ('Berber Coast', 31), ('Maghreb', 31), ('Tyrrenean Sea', 31), ('Rhineland', 31), ('Upper Danube', 31), ('Lower Nile', 29), ('Po Valley', 31), ('Adriatic Sea', 31), ('Levantine Sea', 31),
     ('Aegean Sea', 31), ('Dniester', 31), ('Lower Danube', 31), ('Middle Danube', 31), ('Elbe', 31), ('Eastern Baltic', 31),
     ('Vistula', 31), ('Black Sea', 31), ('Western Siberia', 31), ('Dnipro', 31), ('Volga', 31), ('Great Steppe', 31), ('Caspian Sea', 31), ('Zalesye', 31), ('Caucasus', 31), ('Anatolia', 31), ('Senegambia', 31), ('Upper Niger', 31), ('Guinea Coast', 31), ('Volta', 31), ('Lower Niger', 31), ('Lake Tchad', 31), ('Kongo', 31), ('South Africa', 30), ('African Great Lakes', 30), ('Monomotapa', 30), ('Somalia', 30), ('Zanj', 30), ('Red Sea', 27),
     ('Abyssinian Highlands', 27), ('Upper Nile', 27), ('Jazira', 27), ('Arabian Peninsula', 27), ('Arabian Gulf', 27), ('Iran', 27), ('Khorasan', 27), ('Mawarannahr', 27), ('Tarim Basin', 27),
     ('Punjab', 27), ('Sindh', 27), ('Gurjaratra', 27), ('Konkan', 27), ('Northern Deccan', 27), ('Southern Deccan', 27), ('Tamilakam', 26), ('Kalinga', 25), ('Gondwana', 25), ('Malwa', 25), ('Rajasthan', 25), ('Doab', 25), ('Bihar', 25), ('Assam', 25), ('Bengal', 25), ('Himalayas', 25), ('Tibetan Plateau', 25), ('Guangxi', 25), ('Yunnan', 25), ('Lower Ayeyarwady', 23), ('Upper Ayeyarwady', 23), ('Malacca Strait', 23), ('Mekong', 23), ('Chao Phraya', 23), ('Sunda Strait', 25),
     ('Champa Sea', 25), ('Moluccas', 25), ('Australia', 27), ('Liangguang', 25), ('Szechwan', 25), ('Huazhong', 25), ('Jiangxi', 25), ('Jiangnan', 26), ('Fujian', 26), ('Huabei', 26), ('Xibei', 26), ('Eastern Siberia', 27), ('Zhongyuan', 26), ('Huai He', 26), ('East Sea', 27), ('Nippon', 27),
     ('Yellow Sea', 27), ('Amur', 27), ('Chala', 33), ('Southern Andes', 33), ('Central Andes', 33), ('Southern Cone', 32), ('Guiana', 31), ('Northern Andes', 31), ('Amazonia', 33), ('Cerrado', 33), ('Isthmus of Darien', 33), ('Caribbean', 32), ('Valley of Mexico', 33), ('Western Valley', 33), ('Gulf of Mexico', 33), ('Gulf of Tehuantepec', 33), ('Rio Grande', 33), ('Mississippi', 33), ('Western Cordillera', 33), ('Plains', 33), ('Eastern Seaboard', 33), ('Great Lakes', 33),
     ('American West Coast', 33), ('Pacific', 43)])
# Indonesia
expeditions_list.append(Expedition('indonesia', 'Indonesia', 1200, 'Regular', [23]))
expeditions_list[-1].set_node_tech_reqs(
    [('Iberia', 31), ('Strait of Gibraltar', 31), ('Sahara', 31), ('Alboran Sea', 31), ('Gulf of Lion', 31), ('Bay of Biscay', 31), ('France', 31), ('North Sea', 31), ('Channel', 31), ('Norwegian Sea', 31), ('Western Baltic', 31), ('Berber Coast', 31), ('Maghreb', 31), ('Tyrrenean Sea', 31), ('Rhineland', 31), ('Upper Danube', 31), ('Lower Nile', 29), ('Po Valley', 31), ('Adriatic Sea', 31), ('Levantine Sea', 31),
     ('Aegean Sea', 31), ('Dniester', 31), ('Lower Danube', 31), ('Middle Danube', 31), ('Elbe', 31), ('Eastern Baltic', 31),
     ('Vistula', 31), ('Black Sea', 31), ('Western Siberia', 31), ('Dnipro', 31), ('Volga', 31), ('Great Steppe', 31), ('Caspian Sea', 31), ('Zalesye', 31), ('Caucasus', 31), ('Anatolia', 31), ('Senegambia', 31), ('Upper Niger', 31), ('Guinea Coast', 31), ('Volta', 31), ('Lower Niger', 31), ('Lake Tchad', 31), ('Kongo', 31), ('South Africa', 30), ('African Great Lakes', 30), ('Monomotapa', 30), ('Somalia', 30), ('Zanj', 30), ('Red Sea', 27),
     ('Abyssinian Highlands', 27), ('Upper Nile', 27), ('Jazira', 27), ('Arabian Peninsula', 27), ('Arabian Gulf', 27), ('Iran', 27), ('Khorasan', 27), ('Mawarannahr', 27), ('Tarim Basin', 27),
     ('Punjab', 27), ('Sindh', 27), ('Gurjaratra', 27), ('Konkan', 27), ('Northern Deccan', 27), ('Southern Deccan', 27), ('Tamilakam', 26), ('Kalinga', 26), ('Gondwana', 26), ('Malwa', 26), ('Rajasthan', 26), ('Doab', 26), ('Bihar', 26), ('Assam', 26), ('Bengal', 26), ('Himalayas', 26), ('Tibetan Plateau', 26), ('Guangxi', 26), ('Yunnan', 26), ('Lower Ayeyarwady', 25), ('Upper Ayeyarwady', 25), ('Malacca Strait', 23), ('Mekong', 25), ('Chao Phraya', 25), ('Sunda Strait', 23),
     ('Champa Sea', 25), ('Moluccas', 25), ('Australia', 27), ('Liangguang', 25), ('Szechwan', 25), ('Huazhong', 25), ('Jiangxi', 25), ('Jiangnan', 26), ('Fujian', 26), ('Huabei', 26), ('Xibei', 26), ('Eastern Siberia', 27), ('Zhongyuan', 26), ('Huai He', 26), ('East Sea', 27), ('Nippon', 27),
     ('Yellow Sea', 27), ('Amur', 27), ('Chala', 33), ('Southern Andes', 33), ('Central Andes', 33), ('Southern Cone', 32), ('Guiana', 31), ('Northern Andes', 31), ('Amazonia', 33), ('Cerrado', 33), ('Isthmus of Darien', 33), ('Caribbean', 32), ('Valley of Mexico', 33), ('Western Valley', 33), ('Gulf of Mexico', 33), ('Gulf of Tehuantepec', 33), ('Rio Grande', 33), ('Mississippi', 33), ('Western Cordillera', 33), ('Plains', 33), ('Eastern Seaboard', 33), ('Great Lakes', 33),
     ('American West Coast', 33), ('Pacific', 43)])
# the Philippines
expeditions_list.append(Expedition('philippines', 'the Philippines', 800, 'Regular', [20]))
expeditions_list[-1].set_node_tech_reqs(
    [('Iberia', 31), ('Strait of Gibraltar', 31), ('Sahara', 31), ('Alboran Sea', 31), ('Gulf of Lion', 31), ('Bay of Biscay', 31), ('France', 31), ('North Sea', 31), ('Channel', 31), ('Norwegian Sea', 31), ('Western Baltic', 31), ('Berber Coast', 31), ('Maghreb', 31), ('Tyrrenean Sea', 31), ('Rhineland', 31), ('Upper Danube', 31), ('Lower Nile', 29), ('Po Valley', 31), ('Adriatic Sea', 31), ('Levantine Sea', 31),
     ('Aegean Sea', 31), ('Dniester', 31), ('Lower Danube', 31), ('Middle Danube', 31), ('Elbe', 31), ('Eastern Baltic', 31),
     ('Vistula', 31), ('Black Sea', 31), ('Western Siberia', 31), ('Dnipro', 31), ('Volga', 31), ('Great Steppe', 31), ('Caspian Sea', 31), ('Zalesye', 31), ('Caucasus', 31), ('Anatolia', 31), ('Senegambia', 31), ('Upper Niger', 31), ('Guinea Coast', 31), ('Volta', 31), ('Lower Niger', 31), ('Lake Tchad', 31), ('Kongo', 31), ('South Africa', 30), ('African Great Lakes', 30), ('Monomotapa', 30), ('Somalia', 30), ('Zanj', 30), ('Red Sea', 27),
     ('Abyssinian Highlands', 27), ('Upper Nile', 27), ('Jazira', 27), ('Arabian Peninsula', 27), ('Arabian Gulf', 27), ('Iran', 27), ('Khorasan', 27), ('Mawarannahr', 27), ('Tarim Basin', 27),
     ('Punjab', 27), ('Sindh', 27), ('Gurjaratra', 27), ('Konkan', 27), ('Northern Deccan', 27), ('Southern Deccan', 27), ('Tamilakam', 26), ('Kalinga', 26), ('Gondwana', 26), ('Malwa', 26), ('Rajasthan', 26), ('Doab', 26), ('Bihar', 26), ('Assam', 26), ('Bengal', 26), ('Himalayas', 26), ('Tibetan Plateau', 26), ('Guangxi', 26), ('Yunnan', 26), ('Lower Ayeyarwady', 25), ('Upper Ayeyarwady', 25), ('Malacca Strait', 25), ('Mekong', 25), ('Chao Phraya', 25), ('Sunda Strait', 25),
     ('Champa Sea', 23), ('Moluccas', 23), ('Australia', 27), ('Liangguang', 25), ('Szechwan', 25), ('Huazhong', 25), ('Jiangxi', 25), ('Jiangnan', 26), ('Fujian', 26), ('Huabei', 26), ('Xibei', 26), ('Eastern Siberia', 27), ('Zhongyuan', 26), ('Huai He', 26), ('East Sea', 27), ('Nippon', 27),
     ('Yellow Sea', 27), ('Amur', 27), ('Chala', 33), ('Southern Andes', 33), ('Central Andes', 33), ('Southern Cone', 32), ('Guiana', 31), ('Northern Andes', 31), ('Amazonia', 33), ('Cerrado', 33), ('Isthmus of Darien', 33), ('Caribbean', 32), ('Valley of Mexico', 33), ('Western Valley', 33), ('Gulf of Mexico', 33), ('Gulf of Tehuantepec', 33), ('Rio Grande', 33), ('Mississippi', 33), ('Western Cordillera', 33), ('Plains', 33), ('Eastern Seaboard', 33), ('Great Lakes', 33),
     ('American West Coast', 33), ('Pacific', 43)])
# Papua New Guinea
expeditions_list.append(Expedition('papua', 'Papua New Guinea', 100, 'Regular', [2]))
expeditions_list[-1].set_node_tech_reqs(
    [('Iberia', 49), ('Strait of Gibraltar', 49), ('Sahara', 49), ('Alboran Sea', 49), ('Gulf of Lion', 49), ('Bay of Biscay', 49), ('France', 49), ('North Sea', 49), ('Channel', 49), ('Norwegian Sea', 49), ('Western Baltic', 49), ('Berber Coast', 49), ('Maghreb', 49), ('Tyrrenean Sea', 49), ('Rhineland', 49), ('Upper Danube', 49), ('Lower Nile', 49), ('Po Valley', 49), ('Adriatic Sea', 49), ('Levantine Sea', 49),
     ('Aegean Sea', 49), ('Dniester', 49), ('Lower Danube', 49), ('Middle Danube', 49), ('Elbe', 49), ('Eastern Baltic', 49),
     ('Vistula', 49), ('Black Sea', 49), ('Western Siberia', 49), ('Dnipro', 49), ('Volga', 49), ('Great Steppe', 49), ('Caspian Sea', 49), ('Zalesye', 49), ('Caucasus', 49), ('Anatolia', 49), ('Senegambia', 49), ('Upper Niger', 49), ('Guinea Coast', 49), ('Volta', 49), ('Lower Niger', 49), ('Lake Tchad', 49), ('Kongo', 49), ('South Africa', 49), ('African Great Lakes', 49), ('Monomotapa', 49), ('Somalia', 49), ('Zanj', 49), ('Red Sea', 49),
     ('Abyssinian Highlands', 49), ('Upper Nile', 49), ('Jazira', 49), ('Arabian Peninsula', 49), ('Arabian Gulf', 49), ('Iran', 49), ('Khorasan', 49), ('Mawarannahr', 49), ('Tarim Basin', 49),
     ('Punjab', 49), ('Sindh', 49), ('Gurjaratra', 49), ('Konkan', 49), ('Northern Deccan', 49), ('Southern Deccan', 49), ('Tamilakam', 49), ('Kalinga', 49), ('Gondwana', 49), ('Malwa', 49), ('Rajasthan', 49), ('Doab', 49), ('Bihar', 49), ('Assam', 49), ('Bengal', 49), ('Himalayas', 49), ('Tibetan Plateau', 49), ('Guangxi', 49), ('Yunnan', 49), ('Lower Ayeyarwady', 49), ('Upper Ayeyarwady', 49), ('Malacca Strait', 49), ('Mekong', 49), ('Chao Phraya', 49), ('Sunda Strait', 49),
     ('Champa Sea', 49), ('Moluccas', 49), ('Australia', 49), ('Liangguang', 49), ('Szechwan', 49), ('Huazhong', 49), ('Jiangxi', 49), ('Jiangnan', 49), ('Fujian', 49), ('Huabei', 49), ('Xibei', 49), ('Eastern Siberia', 49), ('Zhongyuan', 49), ('Huai He', 49), ('East Sea', 49), ('Nippon', 49),
     ('Yellow Sea', 49), ('Amur', 49), ('Chala', 49), ('Southern Andes', 49), ('Central Andes', 49), ('Southern Cone', 49), ('Guiana', 49), ('Northern Andes', 49), ('Amazonia', 49), ('Cerrado', 49), ('Isthmus of Darien', 49), ('Caribbean', 49), ('Valley of Mexico', 49), ('Western Valley', 49), ('Gulf of Mexico', 49), ('Gulf of Tehuantepec', 49), ('Rio Grande', 49), ('Mississippi', 49), ('Western Cordillera', 49), ('Plains', 49), ('Eastern Seaboard', 49), ('Great Lakes', 49),
     ('American West Coast', 49), ('Pacific', 49)])
# Australia
expeditions_list.append(Expedition('australia', 'Australia', 100, 'Colonial Node', [2]))
expeditions_list[-1].set_node_tech_reqs(
    [('Iberia', 48), ('Strait of Gibraltar', 48), ('Sahara', 48), ('Alboran Sea', 48), ('Gulf of Lion', 48), ('Bay of Biscay', 48), ('France', 48), ('North Sea', 48), ('Channel', 48), ('Norwegian Sea', 48), ('Western Baltic', 48), ('Berber Coast', 48), ('Maghreb', 48), ('Tyrrenean Sea', 48), ('Rhineland', 48), ('Upper Danube', 48), ('Lower Nile', 48), ('Po Valley', 48), ('Adriatic Sea', 48), ('Levantine Sea', 48),
     ('Aegean Sea', 48), ('Dniester', 48), ('Lower Danube', 48), ('Middle Danube', 48), ('Elbe', 48), ('Eastern Baltic', 48),
     ('Vistula', 48), ('Black Sea', 48), ('Western Siberia', 48), ('Dnipro', 48), ('Volga', 48), ('Great Steppe', 48), ('Caspian Sea', 48), ('Zalesye', 48), ('Caucasus', 48), ('Anatolia', 48), ('Senegambia', 48), ('Upper Niger', 48), ('Guinea Coast', 48), ('Volta', 48), ('Lower Niger', 48), ('Lake Tchad', 48), ('Kongo', 48), ('South Africa', 48), ('African Great Lakes', 48), ('Monomotapa', 48), ('Somalia', 48), ('Zanj', 48), ('Red Sea', 48),
     ('Abyssinian Highlands', 48), ('Upper Nile', 48), ('Jazira', 48), ('Arabian Peninsula', 48), ('Arabian Gulf', 48), ('Iran', 48), ('Khorasan', 48), ('Mawarannahr', 48), ('Tarim Basin', 48),
     ('Punjab', 48), ('Sindh', 48), ('Gurjaratra', 48), ('Konkan', 48), ('Northern Deccan', 48), ('Southern Deccan', 48), ('Tamilakam', 48), ('Kalinga', 48), ('Gondwana', 48), ('Malwa', 48), ('Rajasthan', 48), ('Doab', 48), ('Bihar', 48), ('Assam', 48), ('Bengal', 48), ('Himalayas', 48), ('Tibetan Plateau', 48), ('Guangxi', 48), ('Yunnan', 48), ('Lower Ayeyarwady', 48), ('Upper Ayeyarwady', 48), ('Malacca Strait', 48), ('Mekong', 48), ('Chao Phraya', 48), ('Sunda Strait', 48),
     ('Champa Sea', 48), ('Moluccas', 48), ('Australia', 25), ('Liangguang', 48), ('Szechwan', 48), ('Huazhong', 48), ('Jiangxi', 48), ('Jiangnan', 48), ('Fujian', 48), ('Huabei', 48), ('Xibei', 48), ('Eastern Siberia', 48), ('Zhongyuan', 48), ('Huai He', 48), ('East Sea', 48), ('Nippon', 48),
     ('Yellow Sea', 48), ('Amur', 48), ('Chala', 48), ('Southern Andes', 48), ('Central Andes', 48), ('Southern Cone', 48), ('Guiana', 48), ('Northern Andes', 48), ('Amazonia', 48), ('Cerrado', 48), ('Isthmus of Darien', 48), ('Caribbean', 48), ('Valley of Mexico', 48), ('Western Valley', 48), ('Gulf of Mexico', 48), ('Gulf of Tehuantepec', 48), ('Rio Grande', 48), ('Mississippi', 48), ('Western Cordillera', 48), ('Plains', 48), ('Eastern Seaboard', 48), ('Great Lakes', 48),
     ('American West Coast', 48), ('Pacific', 43)])
# the Pacific Islands
expeditions_list.append(Expedition('pacific_islands', 'the Pacific Islands', 400, 'Jumping Node', [1]))
expeditions_list[-1].set_node_tech_reqs(
    [('Iberia', 43), ('Strait of Gibraltar', 43), ('Sahara', 43), ('Alboran Sea', 43), ('Gulf of Lion', 43), ('Bay of Biscay', 43), ('France', 43), ('North Sea', 43), ('Channel', 43), ('Norwegian Sea', 43), ('Western Baltic', 43), ('Berber Coast', 43), ('Maghreb', 43), ('Tyrrenean Sea', 43), ('Rhineland', 43), ('Upper Danube', 43), ('Lower Nile', 43), ('Po Valley', 43), ('Adriatic Sea', 43), ('Levantine Sea', 43),
     ('Aegean Sea', 43), ('Dniester', 43), ('Lower Danube', 43), ('Middle Danube', 43), ('Elbe', 43), ('Eastern Baltic', 43),
     ('Vistula', 43), ('Black Sea', 43), ('Western Siberia', 43), ('Dnipro', 43), ('Volga', 43), ('Great Steppe', 43), ('Caspian Sea', 43), ('Zalesye', 43), ('Caucasus', 43), ('Anatolia', 43), ('Senegambia', 43), ('Upper Niger', 43), ('Guinea Coast', 43), ('Volta', 43), ('Lower Niger', 43), ('Lake Tchad', 43), ('Kongo', 43), ('South Africa', 43), ('African Great Lakes', 43), ('Monomotapa', 43), ('Somalia', 43), ('Zanj', 43), ('Red Sea', 43),
     ('Abyssinian Highlands', 43), ('Upper Nile', 43), ('Jazira', 43), ('Arabian Peninsula', 43), ('Arabian Gulf', 43), ('Iran', 43), ('Khorasan', 43), ('Mawarannahr', 43), ('Tarim Basin', 43),
     ('Punjab', 43), ('Sindh', 43), ('Gurjaratra', 43), ('Konkan', 43), ('Northern Deccan', 43), ('Southern Deccan', 43), ('Tamilakam', 43), ('Kalinga', 43), ('Gondwana', 43), ('Malwa', 43), ('Rajasthan', 43), ('Doab', 43), ('Bihar', 43), ('Assam', 43), ('Bengal', 43), ('Himalayas', 43), ('Tibetan Plateau', 43), ('Guangxi', 43), ('Yunnan', 43), ('Lower Ayeyarwady', 43), ('Upper Ayeyarwady', 43), ('Malacca Strait', 43), ('Mekong', 43), ('Chao Phraya', 43), ('Sunda Strait', 43),
     ('Champa Sea', 43), ('Moluccas', 43), ('Australia', 43), ('Liangguang', 43), ('Szechwan', 43), ('Huazhong', 43), ('Jiangxi', 43), ('Jiangnan', 43), ('Fujian', 43), ('Huabei', 43), ('Xibei', 43), ('Eastern Siberia', 43), ('Zhongyuan', 43), ('Huai He', 43), ('East Sea', 43), ('Nippon', 43),
     ('Yellow Sea', 43), ('Amur', 43), ('Chala', 43), ('Southern Andes', 43), ('Central Andes', 43), ('Southern Cone', 43), ('Guiana', 43), ('Northern Andes', 43), ('Amazonia', 43), ('Cerrado', 43), ('Isthmus of Darien', 43), ('Caribbean', 43), ('Valley of Mexico', 43), ('Western Valley', 43), ('Gulf of Mexico', 43), ('Gulf of Tehuantepec', 43), ('Rio Grande', 43), ('Mississippi', 43), ('Western Cordillera', 43), ('Plains', 43), ('Eastern Seaboard', 43), ('Great Lakes', 43),
     ('American West Coast', 43), ('Pacific', 43)])
# Southern China
expeditions_list.append(Expedition('southern_china', 'Southern China', 800, 'Chinese Mainland', [3, 18]))
expeditions_list[-1].set_node_tech_reqs(
    [('Iberia', 32), ('Strait of Gibraltar', 32), ('Sahara', 32), ('Alboran Sea', 32), ('Gulf of Lion', 32), ('Bay of Biscay', 32), ('France', 32), ('North Sea', 32), ('Channel', 32), ('Norwegian Sea', 32), ('Western Baltic', 32), ('Berber Coast', 32), ('Maghreb', 32), ('Tyrrenean Sea', 32), ('Rhineland', 32), ('Upper Danube', 32), ('Lower Nile', 30), ('Po Valley', 32), ('Adriatic Sea', 32), ('Levantine Sea', 32),
     ('Aegean Sea', 32), ('Dniester', 32), ('Lower Danube', 32), ('Middle Danube', 32), ('Elbe', 32), ('Eastern Baltic', 32),
     ('Vistula', 32), ('Black Sea', 32), ('Western Siberia', 32), ('Dnipro', 32), ('Volga', 32), ('Great Steppe', 32), ('Caspian Sea', 32), ('Zalesye', 32), ('Caucasus', 32), ('Anatolia', 32), ('Senegambia', 32), ('Upper Niger', 32), ('Guinea Coast', 32), ('Volta', 32), ('Lower Niger', 32), ('Lake Tchad', 32), ('Kongo', 32), ('South Africa', 31), ('African Great Lakes', 31), ('Monomotapa', 31), ('Somalia', 31), ('Zanj', 31), ('Red Sea', 29),
     ('Abyssinian Highlands', 29), ('Upper Nile', 29), ('Jazira', 29), ('Arabian Peninsula', 29), ('Arabian Gulf', 29), ('Iran', 29), ('Khorasan', 29), ('Mawarannahr', 29), ('Tarim Basin', 29),
     ('Punjab', 28), ('Sindh', 28), ('Gurjaratra', 28), ('Konkan', 28), ('Northern Deccan', 28), ('Southern Deccan', 28), ('Tamilakam', 28), ('Kalinga', 28), ('Gondwana', 28), ('Malwa', 28), ('Rajasthan', 28), ('Doab', 28), ('Bihar', 28), ('Assam', 28), ('Bengal', 28), ('Himalayas', 28), ('Tibetan Plateau', 28), ('Guangxi', 28), ('Yunnan', 28), ('Lower Ayeyarwady', 26), ('Upper Ayeyarwady', 26), ('Malacca Strait', 26), ('Mekong', 26), ('Chao Phraya', 26), ('Sunda Strait', 26),
     ('Champa Sea', 25), ('Moluccas', 25), ('Australia', 27), ('Liangguang', 23), ('Szechwan', 23), ('Huazhong', 23), ('Jiangxi', 23), ('Jiangnan', 23), ('Fujian', 23), ('Huabei', 23), ('Xibei', 25), ('Zhongyuan', 25), ('Huai He', 25), ('Eastern Siberia', 25), ('East Sea', 25), ('Nippon', 25),
     ('Yellow Sea', 26), ('Amur', 26), ('Chala', 33), ('Southern Andes', 33), ('Central Andes', 33), ('Southern Cone', 33), ('Guiana', 32), ('Northern Andes', 32), ('Amazonia', 33), ('Cerrado', 33), ('Isthmus of Darien', 33), ('Caribbean', 33), ('Valley of Mexico', 33), ('Western Valley', 33), ('Gulf of Mexico', 33), ('Gulf of Tehuantepec', 33), ('Rio Grande', 33), ('Mississippi', 33), ('Western Cordillera', 33), ('Plains', 33), ('Eastern Seaboard', 33), ('Great Lakes', 33),
     ('American West Coast', 33), ('Pacific', 43)])
# Northern China
expeditions_list.append(Expedition('northern_china', 'Northern China', 800, 'Chinese Mainland', [3, 6, 4, 12]))
expeditions_list[-1].set_node_tech_reqs(
    [('Iberia', 32), ('Strait of Gibraltar', 32), ('Sahara', 32), ('Alboran Sea', 32), ('Gulf of Lion', 32), ('Bay of Biscay', 32), ('France', 32), ('North Sea', 32), ('Channel', 32), ('Norwegian Sea', 32), ('Western Baltic', 32), ('Berber Coast', 32), ('Maghreb', 32), ('Tyrrenean Sea', 32), ('Rhineland', 32), ('Upper Danube', 32), ('Lower Nile', 30), ('Po Valley', 32), ('Adriatic Sea', 32), ('Levantine Sea', 32),
     ('Aegean Sea', 32), ('Dniester', 32), ('Lower Danube', 32), ('Middle Danube', 32), ('Elbe', 32), ('Eastern Baltic', 32),
     ('Vistula', 32), ('Black Sea', 32), ('Western Siberia', 32), ('Dnipro', 32), ('Volga', 32), ('Great Steppe', 32), ('Caspian Sea', 32), ('Zalesye', 32), ('Caucasus', 32), ('Anatolia', 32), ('Senegambia', 32), ('Upper Niger', 32), ('Guinea Coast', 32), ('Volta', 32), ('Lower Niger', 32), ('Lake Tchad', 32), ('Kongo', 32), ('South Africa', 31), ('African Great Lakes', 31), ('Monomotapa', 31), ('Somalia', 31), ('Zanj', 31), ('Red Sea', 29),
     ('Abyssinian Highlands', 29), ('Upper Nile', 29), ('Jazira', 29), ('Arabian Peninsula', 29), ('Arabian Gulf', 29), ('Iran', 29), ('Khorasan', 29), ('Mawarannahr', 29), ('Tarim Basin', 29),
     ('Punjab', 28), ('Sindh', 28), ('Gurjaratra', 28), ('Konkan', 28), ('Northern Deccan', 28), ('Southern Deccan', 28), ('Tamilakam', 28), ('Kalinga', 27), ('Gondwana', 27), ('Malwa', 27), ('Rajasthan', 27), ('Doab', 27), ('Bihar', 27), ('Assam', 27), ('Bengal', 27), ('Himalayas', 27), ('Tibetan Plateau', 27), ('Guangxi', 27), ('Yunnan', 27), ('Lower Ayeyarwady', 26), ('Upper Ayeyarwady', 26), ('Malacca Strait', 26), ('Mekong', 26), ('Chao Phraya', 26), ('Sunda Strait', 26),
     ('Champa Sea', 25), ('Moluccas', 25), ('Australia', 27), ('Liangguang', 25), ('Szechwan', 25), ('Huazhong', 23), ('Jiangxi', 23), ('Jiangnan', 23), ('Fujian', 23), ('Huabei', 23), ('Xibei', 23), ('Zhongyuan', 25), ('Huai He', 25), ('Eastern Siberia', 23), ('East Sea', 25), ('Nippon', 25),
     ('Yellow Sea', 26), ('Amur', 26), ('Chala', 33), ('Southern Andes', 33), ('Central Andes', 33), ('Southern Cone', 33), ('Guiana', 32), ('Northern Andes', 32), ('Amazonia', 33), ('Cerrado', 33), ('Isthmus of Darien', 33), ('Caribbean', 33), ('Valley of Mexico', 33), ('Western Valley', 33), ('Gulf of Mexico', 33), ('Gulf of Tehuantepec', 33), ('Rio Grande', 33), ('Mississippi', 33), ('Western Cordillera', 33), ('Plains', 33), ('Eastern Seaboard', 33), ('Great Lakes', 33),
     ('American West Coast', 33), ('Pacific', 43)])
# Korea
expeditions_list.append(Expedition('korea', 'Korea', 400, 'Chinese Mainland', [4]))
expeditions_list[-1].set_node_tech_reqs(
    [('Iberia', 32), ('Strait of Gibraltar', 32), ('Sahara', 32), ('Alboran Sea', 32), ('Gulf of Lion', 32), ('Bay of Biscay', 32), ('France', 32), ('North Sea', 32), ('Channel', 32), ('Norwegian Sea', 32), ('Western Baltic', 32), ('Berber Coast', 32), ('Maghreb', 32), ('Tyrrenean Sea', 32), ('Rhineland', 32), ('Upper Danube', 32), ('Lower Nile', 30), ('Po Valley', 32), ('Adriatic Sea', 32), ('Levantine Sea', 32),
     ('Aegean Sea', 32), ('Dniester', 32), ('Lower Danube', 32), ('Middle Danube', 32), ('Elbe', 32), ('Eastern Baltic', 32),
     ('Vistula', 32), ('Black Sea', 32), ('Western Siberia', 32), ('Dnipro', 32), ('Volga', 32), ('Great Steppe', 32), ('Caspian Sea', 32), ('Zalesye', 32), ('Caucasus', 32), ('Anatolia', 32), ('Senegambia', 32), ('Upper Niger', 32), ('Guinea Coast', 32), ('Volta', 32), ('Lower Niger', 32), ('Lake Tchad', 32), ('Kongo', 32), ('South Africa', 31), ('African Great Lakes', 31), ('Monomotapa', 31), ('Somalia', 31), ('Zanj', 31), ('Red Sea', 30),
     ('Abyssinian Highlands', 30), ('Upper Nile', 30), ('Jazira', 30), ('Arabian Peninsula', 30), ('Arabian Gulf', 30), ('Iran', 30), ('Khorasan', 30), ('Mawarannahr', 30), ('Tarim Basin', 30),
     ('Punjab', 29), ('Sindh', 29), ('Gurjaratra', 29), ('Konkan', 29), ('Northern Deccan', 29), ('Southern Deccan', 29), ('Tamilakam', 29), ('Kalinga', 29), ('Gondwana', 29), ('Malwa', 29), ('Rajasthan', 29), ('Doab', 29), ('Bihar', 29), ('Assam', 29), ('Bengal', 29), ('Himalayas', 29), ('Tibetan Plateau', 29), ('Guangxi', 29), ('Yunnan', 29), ('Lower Ayeyarwady', 26), ('Upper Ayeyarwady', 26), ('Malacca Strait', 26), ('Mekong', 26), ('Chao Phraya', 26), ('Sunda Strait', 26),
     ('Champa Sea', 25), ('Moluccas', 25), ('Australia', 27), ('Liangguang', 25), ('Szechwan', 25), ('Huazhong', 25), ('Jiangxi', 25), ('Jiangnan', 25), ('Fujian', 25), ('Huabei', 25), ('Xibei', 25), ('Zhongyuan', 23), ('Huai He', 23), ('Eastern Siberia', 25), ('East Sea', 25), ('Nippon', 25),
     ('Yellow Sea', 25), ('Amur', 25), ('Chala', 33), ('Southern Andes', 33), ('Central Andes', 33), ('Southern Cone', 33), ('Guiana', 32), ('Northern Andes', 32), ('Amazonia', 33), ('Cerrado', 33), ('Isthmus of Darien', 33), ('Caribbean', 33), ('Valley of Mexico', 33), ('Western Valley', 33), ('Gulf of Mexico', 33), ('Gulf of Tehuantepec', 33), ('Rio Grande', 33), ('Mississippi', 33), ('Western Cordillera', 33), ('Plains', 33), ('Eastern Seaboard', 33), ('Great Lakes', 33),
     ('American West Coast', 33), ('Pacific', 43)])
# Japan
expeditions_list.append(Expedition('japan', 'Japan', 400, 'Jumping Node', [7]))
expeditions_list[-1].set_node_tech_reqs(
    [('Iberia', 32), ('Strait of Gibraltar', 32), ('Sahara', 32), ('Alboran Sea', 32), ('Gulf of Lion', 32), ('Bay of Biscay', 32), ('France', 32), ('North Sea', 32), ('Channel', 32), ('Norwegian Sea', 32), ('Western Baltic', 32), ('Berber Coast', 32), ('Maghreb', 32), ('Tyrrenean Sea', 32), ('Rhineland', 32), ('Upper Danube', 32), ('Lower Nile', 30), ('Po Valley', 32), ('Adriatic Sea', 32), ('Levantine Sea', 32),
     ('Aegean Sea', 32), ('Dniester', 32), ('Lower Danube', 32), ('Middle Danube', 32), ('Elbe', 32), ('Eastern Baltic', 32),
     ('Vistula', 32), ('Black Sea', 32), ('Western Siberia', 32), ('Dnipro', 32), ('Volga', 32), ('Great Steppe', 32), ('Caspian Sea', 32), ('Zalesye', 32), ('Caucasus', 32), ('Anatolia', 32), ('Senegambia', 32), ('Upper Niger', 32), ('Guinea Coast', 32), ('Volta', 32), ('Lower Niger', 32), ('Lake Tchad', 32), ('Kongo', 32), ('South Africa', 31), ('African Great Lakes', 31), ('Monomotapa', 31), ('Somalia', 31), ('Zanj', 31), ('Red Sea', 30),
     ('Abyssinian Highlands', 30), ('Upper Nile', 30), ('Jazira', 30), ('Arabian Peninsula', 30), ('Arabian Gulf', 30), ('Iran', 30), ('Khorasan', 30), ('Mawarannahr', 30), ('Tarim Basin', 30),
     ('Punjab', 29), ('Sindh', 29), ('Gurjaratra', 29), ('Konkan', 29), ('Northern Deccan', 29), ('Southern Deccan', 29), ('Tamilakam', 29), ('Kalinga', 29), ('Gondwana', 29), ('Malwa', 29), ('Rajasthan', 29), ('Doab', 29), ('Bihar', 29), ('Assam', 29), ('Bengal', 29), ('Himalayas', 29), ('Tibetan Plateau', 29), ('Guangxi', 29), ('Yunnan', 29), ('Lower Ayeyarwady', 26), ('Upper Ayeyarwady', 26), ('Malacca Strait', 26), ('Mekong', 26), ('Chao Phraya', 26), ('Sunda Strait', 26),
     ('Champa Sea', 25), ('Moluccas', 25), ('Australia', 27), ('Liangguang', 25), ('Szechwan', 25), ('Huazhong', 25), ('Jiangxi', 25), ('Jiangnan', 25), ('Fujian', 25), ('Huabei', 25), ('Xibei', 25), ('Zhongyuan', 25), ('Huai He', 25), ('Eastern Siberia', 25), ('East Sea', 23), ('Nippon', 23),
     ('Yellow Sea', 25), ('Amur', 25), ('Chala', 33), ('Southern Andes', 33), ('Central Andes', 33), ('Southern Cone', 33), ('Guiana', 32), ('Northern Andes', 32), ('Amazonia', 33), ('Cerrado', 33), ('Isthmus of Darien', 33), ('Caribbean', 33), ('Valley of Mexico', 33), ('Western Valley', 33), ('Gulf of Mexico', 33), ('Gulf of Tehuantepec', 33), ('Rio Grande', 33), ('Mississippi', 33), ('Western Cordillera', 33), ('Plains', 33), ('Eastern Seaboard', 33), ('Great Lakes', 33),
     ('American West Coast', 33), ('Pacific', 43)])

# Cuba
expeditions_list.append(Expedition('cuba', 'Cuba', 800, 'Colonial Node', [68]))
expeditions_list[-1].set_node_tech_reqs(
    [('Iberia', 29), ('Strait of Gibraltar', 29), ('Sahara', 29), ('Alboran Sea', 29), ('Gulf of Lion', 29), ('Bay of Biscay', 29), ('France', 29), ('North Sea', 29), ('Channel', 29), ('Norwegian Sea', 29), ('Western Baltic', 29), ('Berber Coast', 30), ('Maghreb', 30), ('Tyrrenean Sea', 30), ('Rhineland', 30), ('Upper Danube', 30), ('Lower Nile', 30), ('Po Valley', 30), ('Adriatic Sea', 30), ('Levantine Sea', 30),
     ('Aegean Sea', 30), ('Dniester', 30), ('Lower Danube', 30), ('Middle Danube', 30), ('Elbe', 30), ('Eastern Baltic', 30),
     ('Vistula', 30), ('Black Sea', 30), ('Western Siberia', 30), ('Dnipro', 30), ('Volga', 32), ('Great Steppe', 32), ('Caspian Sea', 32), ('Zalesye', 30), ('Caucasus', 30), ('Anatolia', 30), ('Senegambia', 29), ('Upper Niger', 29), ('Guinea Coast', 29), ('Volta', 29), ('Lower Niger', 29), ('Lake Tchad', 29), ('Kongo', 29), ('South Africa', 30), ('African Great Lakes', 30), ('Monomotapa', 30), ('Somalia', 30), ('Zanj', 30), ('Red Sea', 31),
     ('Abyssinian Highlands', 31), ('Upper Nile', 31), ('Jazira', 32), ('Arabian Peninsula', 32), ('Arabian Gulf', 32), ('Iran', 32), ('Khorasan', 32), ('Mawarannahr', 32), ('Tarim Basin', 32),
     ('Punjab', 32), ('Sindh', 32), ('Gurjaratra', 32), ('Konkan', 32), ('Northern Deccan', 32), ('Southern Deccan', 32), ('Tamilakam', 32), ('Kalinga', 32), ('Gondwana', 32), ('Malwa', 32), ('Rajasthan', 32), ('Doab', 32), ('Bihar', 32), ('Assam', 32), ('Bengal', 32), ('Himalayas', 32), ('Tibetan Plateau', 32), ('Guangxi', 32), ('Yunnan', 32), ('Lower Ayeyarwady', 32), ('Upper Ayeyarwady', 32), ('Malacca Strait', 32), ('Mekong', 32), ('Chao Phraya', 32), ('Sunda Strait', 32),
     ('Champa Sea', 32), ('Moluccas', 32), ('Australia', 32), ('Liangguang', 32), ('Szechwan', 32), ('Huazhong', 32), ('Jiangxi', 32), ('Jiangnan', 32), ('Fujian', 32), ('Huabei', 32), ('Xibei', 32), ('Zhongyuan', 32), ('Huai He', 32), ('Eastern Siberia', 32), ('East Sea', 32), ('Nippon', 32),
     ('Yellow Sea', 32), ('Amur', 32), ('Chala', 29), ('Southern Andes', 29), ('Central Andes', 29), ('Southern Cone', 27), ('Guiana', 26), ('Northern Andes', 26), ('Amazonia', 29), ('Cerrado', 29), ('Isthmus of Darien', 25), ('Caribbean', 23), ('Valley of Mexico', 25), ('Western Valley', 25), ('Gulf of Mexico', 25), ('Gulf of Tehuantepec', 25), ('Rio Grande', 25), ('Mississippi', 25), ('Western Cordillera', 25), ('Plains', 25), ('Eastern Seaboard', 25), ('Great Lakes', 27),
     ('American West Coast', 30), ('Pacific', 43)])
# Hispaniola
expeditions_list.append(Expedition('hispaniola', 'Hispaniola', 800, 'Colonial Node', [68]))
expeditions_list[-1].set_node_tech_reqs(
    [('Iberia', 29), ('Strait of Gibraltar', 29), ('Sahara', 29), ('Alboran Sea', 29), ('Gulf of Lion', 29), ('Bay of Biscay', 29), ('France', 29), ('North Sea', 29), ('Channel', 29), ('Norwegian Sea', 29), ('Western Baltic', 29), ('Berber Coast', 30), ('Maghreb', 30), ('Tyrrenean Sea', 30), ('Rhineland', 30), ('Upper Danube', 30), ('Lower Nile', 30), ('Po Valley', 30), ('Adriatic Sea', 30), ('Levantine Sea', 30),
     ('Aegean Sea', 30), ('Dniester', 30), ('Lower Danube', 30), ('Middle Danube', 30), ('Elbe', 30), ('Eastern Baltic', 30),
     ('Vistula', 30), ('Black Sea', 30), ('Western Siberia', 30), ('Dnipro', 30), ('Volga', 30), ('Great Steppe', 30), ('Caspian Sea', 30), ('Zalesye', 30), ('Caucasus', 30), ('Anatolia', 30), ('Senegambia', 29), ('Upper Niger', 29), ('Guinea Coast', 29), ('Volta', 29), ('Lower Niger', 29), ('Lake Tchad', 29), ('Kongo', 29), ('South Africa', 30), ('African Great Lakes', 30), ('Monomotapa', 30), ('Somalia', 30), ('Zanj', 30), ('Red Sea', 31),
     ('Abyssinian Highlands', 31), ('Upper Nile', 31), ('Jazira', 32), ('Arabian Peninsula', 32), ('Arabian Gulf', 32), ('Iran', 32), ('Khorasan', 32), ('Mawarannahr', 32), ('Tarim Basin', 32),
     ('Punjab', 32), ('Sindh', 32), ('Gurjaratra', 32), ('Konkan', 32), ('Northern Deccan', 32), ('Southern Deccan', 32), ('Tamilakam', 32), ('Kalinga', 32), ('Gondwana', 32), ('Malwa', 32), ('Rajasthan', 32), ('Doab', 32), ('Bihar', 32), ('Assam', 32), ('Bengal', 32), ('Himalayas', 32), ('Tibetan Plateau', 32), ('Guangxi', 32), ('Yunnan', 32), ('Lower Ayeyarwady', 32), ('Upper Ayeyarwady', 32), ('Malacca Strait', 32), ('Mekong', 32), ('Chao Phraya', 32), ('Sunda Strait', 32),
     ('Champa Sea', 32), ('Moluccas', 32), ('Australia', 32), ('Liangguang', 32), ('Szechwan', 32), ('Huazhong', 32), ('Jiangxi', 32), ('Jiangnan', 32), ('Fujian', 32), ('Huabei', 32), ('Xibei', 32), ('Zhongyuan', 32), ('Huai He', 32), ('Eastern Siberia', 32), ('East Sea', 32), ('Nippon', 32),
     ('Yellow Sea', 32), ('Amur', 32), ('Chala', 29), ('Southern Andes', 29), ('Central Andes', 29), ('Southern Cone', 27), ('Guiana', 26), ('Northern Andes', 26), ('Amazonia', 29), ('Cerrado', 29), ('Isthmus of Darien', 25), ('Caribbean', 23), ('Valley of Mexico', 25), ('Western Valley', 25), ('Gulf of Mexico', 25), ('Gulf of Tehuantepec', 25), ('Rio Grande', 25), ('Mississippi', 25), ('Western Cordillera', 25), ('Plains', 25), ('Eastern Seaboard', 25), ('Great Lakes', 27),
     ('American West Coast', 30), ('Pacific', 43)])
# Caribbean
expeditions_list.append(Expedition('caribbean', 'Caribbean', 800, 'Jumping Node', [68]))
expeditions_list[-1].set_node_tech_reqs(
    [('Iberia', 29), ('Strait of Gibraltar', 29), ('Sahara', 29), ('Alboran Sea', 29), ('Gulf of Lion', 29), ('Bay of Biscay', 29), ('France', 29), ('North Sea', 29), ('Channel', 29), ('Norwegian Sea', 29), ('Western Baltic', 29), ('Berber Coast', 30), ('Maghreb', 30), ('Tyrrenean Sea', 30), ('Rhineland', 30), ('Upper Danube', 30), ('Lower Nile', 30), ('Po Valley', 30), ('Adriatic Sea', 30), ('Levantine Sea', 30),
     ('Aegean Sea', 30), ('Dniester', 30), ('Lower Danube', 30), ('Middle Danube', 30), ('Elbe', 30), ('Eastern Baltic', 30),
     ('Vistula', 30), ('Black Sea', 30), ('Western Siberia', 30), ('Dnipro', 30), ('Volga', 30), ('Great Steppe', 30), ('Caspian Sea', 30), ('Zalesye', 30), ('Caucasus', 30), ('Anatolia', 30), ('Senegambia', 29), ('Upper Niger', 29), ('Guinea Coast', 29), ('Volta', 29), ('Lower Niger', 29), ('Lake Tchad', 29), ('Kongo', 29), ('South Africa', 30), ('African Great Lakes', 30), ('Monomotapa', 30), ('Somalia', 30), ('Zanj', 30), ('Red Sea', 31),
     ('Abyssinian Highlands', 31), ('Upper Nile', 31), ('Jazira', 32), ('Arabian Peninsula', 32), ('Arabian Gulf', 32), ('Iran', 32), ('Khorasan', 32), ('Mawarannahr', 32), ('Tarim Basin', 32),
     ('Punjab', 32), ('Sindh', 32), ('Gurjaratra', 32), ('Konkan', 32), ('Northern Deccan', 32), ('Southern Deccan', 32), ('Tamilakam', 32), ('Kalinga', 32), ('Gondwana', 32), ('Malwa', 32), ('Rajasthan', 32), ('Doab', 32), ('Bihar', 32), ('Assam', 32), ('Bengal', 32), ('Himalayas', 32), ('Tibetan Plateau', 32), ('Guangxi', 32), ('Yunnan', 32), ('Lower Ayeyarwady', 32), ('Upper Ayeyarwady', 32), ('Malacca Strait', 32), ('Mekong', 32), ('Chao Phraya', 32), ('Sunda Strait', 32),
     ('Champa Sea', 32), ('Moluccas', 32), ('Australia', 32), ('Liangguang', 32), ('Szechwan', 32), ('Huazhong', 32), ('Jiangxi', 32), ('Jiangnan', 32), ('Fujian', 32), ('Huabei', 32), ('Xibei', 32), ('Zhongyuan', 32), ('Huai He', 32), ('Eastern Siberia', 32), ('East Sea', 32), ('Nippon', 32),
     ('Yellow Sea', 32), ('Amur', 32), ('Chala', 29), ('Southern Andes', 29), ('Central Andes', 29), ('Southern Cone', 27), ('Guiana', 26), ('Northern Andes', 26), ('Amazonia', 28), ('Cerrado', 28), ('Isthmus of Darien', 25), ('Caribbean', 23), ('Valley of Mexico', 25), ('Western Valley', 25), ('Gulf of Mexico', 25), ('Gulf of Tehuantepec', 25), ('Rio Grande', 25), ('Mississippi', 25), ('Western Cordillera', 25), ('Plains', 25), ('Eastern Seaboard', 25), ('Great Lakes', 27),
     ('American West Coast', 30), ('Pacific', 43)])
# Atlantic Colombia
expeditions_list.append(Expedition('atlantic_colombia', 'Atlantic Colombia', 300, 'Colonial Node', [46]))
expeditions_list[-1].set_node_tech_reqs(
    [('Iberia', 30), ('Strait of Gibraltar', 30), ('Sahara', 30), ('Alboran Sea', 30), ('Gulf of Lion', 30), ('Bay of Biscay', 30), ('France', 30), ('North Sea', 30), ('Channel', 30), ('Norwegian Sea', 30), ('Western Baltic', 30), ('Berber Coast', 30), ('Maghreb', 30), ('Tyrrenean Sea', 30), ('Rhineland', 30), ('Upper Danube', 30), ('Lower Nile', 30), ('Po Valley', 30), ('Adriatic Sea', 30), ('Levantine Sea', 30),
     ('Aegean Sea', 30), ('Dniester', 30), ('Lower Danube', 30), ('Middle Danube', 30), ('Elbe', 30), ('Eastern Baltic', 30),
     ('Vistula', 30), ('Black Sea', 30), ('Western Siberia', 30), ('Dnipro', 30), ('Volga', 30), ('Great Steppe', 30), ('Caspian Sea', 30), ('Zalesye', 30), ('Caucasus', 30), ('Anatolia', 30), ('Senegambia', 30), ('Upper Niger', 30), ('Guinea Coast', 30), ('Volta', 30), ('Lower Niger', 30), ('Lake Tchad', 30), ('Kongo', 30), ('South Africa', 31), ('African Great Lakes', 31), ('Monomotapa', 31), ('Somalia', 31), ('Zanj', 31), ('Red Sea', 33),
     ('Abyssinian Highlands', 33), ('Upper Nile', 33), ('Jazira', 33), ('Arabian Peninsula', 33), ('Arabian Gulf', 33), ('Iran', 33), ('Khorasan', 33), ('Mawarannahr', 33), ('Tarim Basin', 33),
     ('Punjab', 33), ('Sindh', 33), ('Gurjaratra', 33), ('Konkan', 33), ('Northern Deccan', 33), ('Southern Deccan', 33), ('Tamilakam', 33), ('Kalinga', 33), ('Gondwana', 33), ('Malwa', 33), ('Rajasthan', 33), ('Doab', 33), ('Bihar', 33), ('Assam', 33), ('Bengal', 33), ('Himalayas', 33), ('Tibetan Plateau', 33), ('Guangxi', 33), ('Yunnan', 33), ('Lower Ayeyarwady', 33), ('Upper Ayeyarwady', 33), ('Malacca Strait', 33), ('Mekong', 33), ('Chao Phraya', 33), ('Sunda Strait', 33),
     ('Champa Sea', 33), ('Moluccas', 33), ('Australia', 33), ('Liangguang', 33), ('Szechwan', 33), ('Huazhong', 33), ('Jiangxi', 33), ('Jiangnan', 33), ('Fujian', 33), ('Huabei', 33), ('Xibei', 33), ('Zhongyuan', 33), ('Huai He', 33), ('Eastern Siberia', 33), ('East Sea', 33), ('Nippon', 33),
     ('Yellow Sea', 33), ('Amur', 33), ('Chala', 29), ('Southern Andes', 29), ('Central Andes', 29), ('Southern Cone', 26), ('Guiana', 25), ('Northern Andes', 25), ('Amazonia', 29), ('Cerrado', 29), ('Isthmus of Darien', 23), ('Caribbean', 25), ('Valley of Mexico', 26), ('Western Valley', 26), ('Gulf of Mexico', 26), ('Gulf of Tehuantepec', 26), ('Rio Grande', 26), ('Mississippi', 26), ('Western Cordillera', 26), ('Plains', 26), ('Eastern Seaboard', 26), ('Great Lakes', 27),
     ('American West Coast', 30), ('Pacific', 43)])
# Guyana
expeditions_list.append(Expedition('guyana', 'Guyana', 200, 'Colonial Node', [46]))
expeditions_list[-1].set_node_tech_reqs(
    [('Iberia', 30), ('Strait of Gibraltar', 30), ('Sahara', 30), ('Alboran Sea', 30), ('Gulf of Lion', 30), ('Bay of Biscay', 30), ('France', 30), ('North Sea', 30), ('Channel', 30), ('Norwegian Sea', 30), ('Western Baltic', 30), ('Berber Coast', 30), ('Maghreb', 30), ('Tyrrenean Sea', 30), ('Rhineland', 30), ('Upper Danube', 30), ('Lower Nile', 30), ('Po Valley', 30), ('Adriatic Sea', 30), ('Levantine Sea', 30),
     ('Aegean Sea', 30), ('Dniester', 30), ('Lower Danube', 30), ('Middle Danube', 30), ('Elbe', 30), ('Eastern Baltic', 30),
     ('Vistula', 30), ('Black Sea', 30), ('Western Siberia', 30), ('Dnipro', 30), ('Volga', 30), ('Great Steppe', 30), ('Caspian Sea', 30), ('Zalesye', 30), ('Caucasus', 30), ('Anatolia', 30), ('Senegambia', 30), ('Upper Niger', 30), ('Guinea Coast', 30), ('Volta', 30), ('Lower Niger', 30), ('Lake Tchad', 30), ('Kongo', 30), ('South Africa', 31), ('African Great Lakes', 31), ('Monomotapa', 31), ('Somalia', 31), ('Zanj', 31), ('Red Sea', 33),
     ('Abyssinian Highlands', 33), ('Upper Nile', 33), ('Jazira', 33), ('Arabian Peninsula', 33), ('Arabian Gulf', 33), ('Iran', 33), ('Khorasan', 33), ('Mawarannahr', 33), ('Tarim Basin', 33),
     ('Punjab', 33), ('Sindh', 33), ('Gurjaratra', 33), ('Konkan', 33), ('Northern Deccan', 33), ('Southern Deccan', 33), ('Tamilakam', 33), ('Kalinga', 33), ('Gondwana', 33), ('Malwa', 33), ('Rajasthan', 33), ('Doab', 33), ('Bihar', 33), ('Assam', 33), ('Bengal', 33), ('Himalayas', 33), ('Tibetan Plateau', 33), ('Guangxi', 33), ('Yunnan', 33), ('Lower Ayeyarwady', 33), ('Upper Ayeyarwady', 33), ('Malacca Strait', 33), ('Mekong', 33), ('Chao Phraya', 33), ('Sunda Strait', 33),
     ('Champa Sea', 33), ('Moluccas', 33), ('Australia', 33), ('Liangguang', 33), ('Szechwan', 33), ('Huazhong', 33), ('Jiangxi', 33), ('Jiangnan', 33), ('Fujian', 33), ('Huabei', 33), ('Xibei', 33), ('Zhongyuan', 33), ('Huai He', 33), ('Eastern Siberia', 33), ('East Sea', 33), ('Nippon', 33),
     ('Yellow Sea', 33), ('Amur', 33), ('Chala', 29), ('Southern Andes', 29), ('Central Andes', 29), ('Southern Cone', 26), ('Guiana', 25), ('Northern Andes', 25), ('Amazonia', 29), ('Cerrado', 29), ('Isthmus of Darien', 23), ('Caribbean', 25), ('Valley of Mexico', 26), ('Western Valley', 26), ('Gulf of Mexico', 26), ('Gulf of Tehuantepec', 26), ('Rio Grande', 26), ('Mississippi', 26), ('Western Cordillera', 26), ('Plains', 26), ('Eastern Seaboard', 26), ('Great Lakes', 27),
     ('American West Coast', 30), ('Pacific', 43)])
# Atlantic Mexico
expeditions_list.append(Expedition('atlantic_mexico', 'Atlantic Mexico', 1600, 'Colonial Node', [45, 9]))
expeditions_list[-1].set_node_tech_reqs(
    [('Iberia', 31), ('Strait of Gibraltar', 31), ('Sahara', 31), ('Alboran Sea', 31), ('Gulf of Lion', 31), ('Bay of Biscay', 31), ('France', 31), ('North Sea', 31), ('Channel', 31), ('Norwegian Sea', 31), ('Western Baltic', 31), ('Berber Coast', 31), ('Maghreb', 31), ('Tyrrenean Sea', 31), ('Rhineland', 31), ('Upper Danube', 31), ('Lower Nile', 31), ('Po Valley', 31), ('Adriatic Sea', 31), ('Levantine Sea', 31),
     ('Aegean Sea', 31), ('Dniester', 31), ('Lower Danube', 31), ('Middle Danube', 31), ('Elbe', 31), ('Eastern Baltic', 31),
     ('Vistula', 31), ('Black Sea', 31), ('Western Siberia', 31), ('Dnipro', 31), ('Volga', 31), ('Great Steppe', 31), ('Caspian Sea', 31), ('Zalesye', 31), ('Caucasus', 31), ('Anatolia', 31), ('Senegambia', 31), ('Upper Niger', 31), ('Guinea Coast', 31), ('Volta', 31), ('Lower Niger', 31), ('Lake Tchad', 31), ('Kongo', 31), ('South Africa', 31), ('African Great Lakes', 31), ('Monomotapa', 31), ('Somalia', 31), ('Zanj', 31), ('Red Sea', 33),
     ('Abyssinian Highlands', 33), ('Upper Nile', 33), ('Jazira', 33), ('Arabian Peninsula', 33), ('Arabian Gulf', 33), ('Iran', 33), ('Khorasan', 33), ('Mawarannahr', 33), ('Tarim Basin', 33),
     ('Punjab', 33), ('Sindh', 33), ('Gurjaratra', 33), ('Konkan', 33), ('Northern Deccan', 33), ('Southern Deccan', 33), ('Tamilakam', 33), ('Kalinga', 33), ('Gondwana', 33), ('Malwa', 33), ('Rajasthan', 33), ('Doab', 33), ('Bihar', 33), ('Assam', 33), ('Bengal', 33), ('Himalayas', 33), ('Tibetan Plateau', 33), ('Guangxi', 33), ('Yunnan', 33), ('Lower Ayeyarwady', 33), ('Upper Ayeyarwady', 33), ('Malacca Strait', 33), ('Mekong', 33), ('Chao Phraya', 33), ('Sunda Strait', 33),
     ('Champa Sea', 33), ('Moluccas', 33), ('Australia', 33), ('Liangguang', 33), ('Szechwan', 33), ('Huazhong', 33), ('Jiangxi', 33), ('Jiangnan', 33), ('Fujian', 33), ('Huabei', 33), ('Xibei', 33), ('Zhongyuan', 33), ('Huai He', 33), ('Eastern Siberia', 33), ('East Sea', 33), ('Nippon', 33),
     ('Yellow Sea', 33), ('Amur', 33), ('Chala', 29), ('Southern Andes', 29), ('Central Andes', 29), ('Southern Cone', 27), ('Guiana', 26), ('Northern Andes', 26), ('Amazonia', 29), ('Cerrado', 29), ('Isthmus of Darien', 23), ('Caribbean', 25), ('Valley of Mexico', 23), ('Western Valley', 23), ('Gulf of Mexico', 23), ('Gulf of Tehuantepec', 23), ('Rio Grande', 23), ('Mississippi', 25), ('Western Cordillera', 25), ('Plains', 25), ('Eastern Seaboard', 26), ('Great Lakes', 27),
     ('American West Coast', 30), ('Pacific', 43)])
# Northern Brazil
expeditions_list.append(Expedition('north_brazil', 'Northern Brazil', 600, 'Colonial Node', [46]))
expeditions_list[-1].set_node_tech_reqs(
    [('Iberia', 30), ('Strait of Gibraltar', 30), ('Sahara', 30), ('Alboran Sea', 30), ('Gulf of Lion', 30), ('Bay of Biscay', 30), ('France', 30), ('North Sea', 30), ('Channel', 30), ('Norwegian Sea', 30), ('Western Baltic', 30), ('Berber Coast', 30), ('Maghreb', 30), ('Tyrrenean Sea', 30), ('Rhineland', 30), ('Upper Danube', 30), ('Lower Nile', 30), ('Po Valley', 30), ('Adriatic Sea', 30), ('Levantine Sea', 30),
     ('Aegean Sea', 30), ('Dniester', 30), ('Lower Danube', 30), ('Middle Danube', 30), ('Elbe', 30), ('Eastern Baltic', 30),
     ('Vistula', 30), ('Black Sea', 30), ('Western Siberia', 30), ('Dnipro', 30), ('Volga', 30), ('Great Steppe', 30), ('Caspian Sea', 30), ('Zalesye', 30), ('Caucasus', 30), ('Anatolia', 30), ('Senegambia', 27), ('Upper Niger', 27), ('Guinea Coast', 27), ('Volta', 27), ('Lower Niger', 27), ('Lake Tchad', 27), ('Kongo', 28), ('South Africa', 29), ('African Great Lakes', 30), ('Monomotapa', 30), ('Somalia', 30), ('Zanj', 30), ('Red Sea', 30),
     ('Abyssinian Highlands', 30), ('Upper Nile', 30), ('Jazira', 31), ('Arabian Peninsula', 31), ('Arabian Gulf', 31), ('Iran', 31), ('Khorasan', 31), ('Mawarannahr', 31), ('Tarim Basin', 31),
     ('Punjab', 31), ('Sindh', 31), ('Gurjaratra', 31), ('Konkan', 31), ('Northern Deccan', 31), ('Southern Deccan', 31), ('Tamilakam', 31), ('Kalinga', 31), ('Gondwana', 31), ('Malwa', 31), ('Rajasthan', 31), ('Doab', 31), ('Bihar', 31), ('Assam', 31), ('Bengal', 31), ('Himalayas', 31), ('Tibetan Plateau', 31), ('Guangxi', 31), ('Yunnan', 31), ('Lower Ayeyarwady', 31), ('Upper Ayeyarwady', 31), ('Malacca Strait', 31), ('Mekong', 31), ('Chao Phraya', 31), ('Sunda Strait', 31),
     ('Champa Sea', 31), ('Moluccas', 31), ('Australia', 32), ('Liangguang', 32), ('Szechwan', 32), ('Huazhong', 32), ('Jiangxi', 32), ('Jiangnan', 32), ('Fujian', 32), ('Huabei', 32), ('Xibei', 32), ('Zhongyuan', 32), ('Huai He', 32), ('Eastern Siberia', 32), ('East Sea', 32), ('Nippon', 32),
     ('Yellow Sea', 32), ('Amur', 32), ('Chala', 27), ('Southern Andes', 27), ('Central Andes', 27), ('Southern Cone', 23), ('Guiana', 23), ('Northern Andes', 23), ('Amazonia', 27), ('Cerrado', 27), ('Isthmus of Darien', 26), ('Caribbean', 25), ('Valley of Mexico', 26), ('Western Valley', 26), ('Gulf of Mexico', 26), ('Gulf of Tehuantepec', 26), ('Rio Grande', 26), ('Mississippi', 26), ('Western Cordillera', 26), ('Plains', 26), ('Eastern Seaboard', 26), ('Great Lakes', 27),
     ('American West Coast', 29), ('Pacific', 43)])
# Southern Brazil
expeditions_list.append(Expedition('south_brazil', 'Southern Brazil', 600, 'Colonial Node', [17]))
expeditions_list[-1].set_node_tech_reqs(
    [('Iberia', 30), ('Strait of Gibraltar', 30), ('Sahara', 30), ('Alboran Sea', 30), ('Gulf of Lion', 30), ('Bay of Biscay', 30), ('France', 30), ('North Sea', 30), ('Channel', 30), ('Norwegian Sea', 30), ('Western Baltic', 30), ('Berber Coast', 30), ('Maghreb', 30), ('Tyrrenean Sea', 30), ('Rhineland', 30), ('Upper Danube', 30), ('Lower Nile', 30), ('Po Valley', 30), ('Adriatic Sea', 30), ('Levantine Sea', 30),
     ('Aegean Sea', 30), ('Dniester', 30), ('Lower Danube', 30), ('Middle Danube', 30), ('Elbe', 30), ('Eastern Baltic', 30),
     ('Vistula', 30), ('Black Sea', 30), ('Western Siberia', 30), ('Dnipro', 30), ('Volga', 30), ('Great Steppe', 30), ('Caspian Sea', 30), ('Zalesye', 30), ('Caucasus', 30), ('Anatolia', 30), ('Senegambia', 27), ('Upper Niger', 27), ('Guinea Coast', 27), ('Volta', 27), ('Lower Niger', 27), ('Lake Tchad', 27), ('Kongo', 28), ('South Africa', 29), ('African Great Lakes', 30), ('Monomotapa', 30), ('Somalia', 30), ('Zanj', 30), ('Red Sea', 30),
     ('Abyssinian Highlands', 30), ('Upper Nile', 30), ('Jazira', 31), ('Arabian Peninsula', 31), ('Arabian Gulf', 31), ('Iran', 31), ('Khorasan', 31), ('Mawarannahr', 31), ('Tarim Basin', 31),
     ('Punjab', 31), ('Sindh', 31), ('Gurjaratra', 31), ('Konkan', 31), ('Northern Deccan', 31), ('Southern Deccan', 31), ('Tamilakam', 31), ('Kalinga', 31), ('Gondwana', 31), ('Malwa', 31), ('Rajasthan', 31), ('Doab', 31), ('Bihar', 31), ('Assam', 31), ('Bengal', 31), ('Himalayas', 31), ('Tibetan Plateau', 31), ('Guangxi', 31), ('Yunnan', 31), ('Lower Ayeyarwady', 31), ('Upper Ayeyarwady', 31), ('Malacca Strait', 31), ('Mekong', 31), ('Chao Phraya', 31), ('Sunda Strait', 31),
     ('Champa Sea', 31), ('Moluccas', 31), ('Australia', 32), ('Liangguang', 32), ('Szechwan', 32), ('Huazhong', 32), ('Jiangxi', 32), ('Jiangnan', 32), ('Fujian', 32), ('Huabei', 32), ('Xibei', 32), ('Zhongyuan', 32), ('Huai He', 32), ('Eastern Siberia', 32), ('East Sea', 32), ('Nippon', 32),
     ('Yellow Sea', 32), ('Amur', 32), ('Chala', 27), ('Southern Andes', 27), ('Central Andes', 27), ('Southern Cone', 23), ('Guiana', 23), ('Northern Andes', 23), ('Amazonia', 27), ('Cerrado', 27), ('Isthmus of Darien', 26), ('Caribbean', 25), ('Valley of Mexico', 26), ('Western Valley', 26), ('Gulf of Mexico', 26), ('Gulf of Tehuantepec', 26), ('Rio Grande', 26), ('Mississippi', 26), ('Western Cordillera', 26), ('Plains', 26), ('Eastern Seaboard', 26), ('Great Lakes', 27),
     ('American West Coast', 29), ('Pacific', 43)])
# the Gulf of Mexico
expeditions_list.append(Expedition('gulf_of_mexico', 'the Gulf of Mexico', 200, 'Colonial Node', [65, 66]))
expeditions_list[-1].set_node_tech_reqs(
    [('Iberia', 35), ('Strait of Gibraltar', 35), ('Sahara', 35), ('Alboran Sea', 35), ('Gulf of Lion', 35), ('Bay of Biscay', 35), ('France', 35), ('North Sea', 35), ('Channel', 35), ('Norwegian Sea', 35), ('Western Baltic', 35), ('Berber Coast', 35), ('Maghreb', 35), ('Tyrrenean Sea', 35), ('Rhineland', 35), ('Upper Danube', 35), ('Lower Nile', 35), ('Po Valley', 35), ('Adriatic Sea', 35), ('Levantine Sea', 35),
     ('Aegean Sea', 35), ('Dniester', 35), ('Lower Danube', 35), ('Middle Danube', 35), ('Elbe', 35), ('Eastern Baltic', 35),
     ('Vistula', 35), ('Black Sea', 35), ('Western Siberia', 35), ('Dnipro', 35), ('Volga', 35), ('Great Steppe', 35), ('Caspian Sea', 35), ('Zalesye', 35), ('Caucasus', 35), ('Anatolia', 35), ('Senegambia', 35), ('Upper Niger', 35), ('Guinea Coast', 35), ('Volta', 35), ('Lower Niger', 35), ('Lake Tchad', 35), ('Kongo', 35), ('South Africa', 35), ('African Great Lakes', 35), ('Monomotapa', 35), ('Somalia', 35), ('Zanj', 35), ('Red Sea', 35),
     ('Abyssinian Highlands', 35), ('Upper Nile', 35), ('Jazira', 35), ('Arabian Peninsula', 35), ('Arabian Gulf', 35), ('Iran', 35), ('Khorasan', 35), ('Mawarannahr', 35), ('Tarim Basin', 35),
     ('Punjab', 35), ('Sindh', 35), ('Gurjaratra', 35), ('Konkan', 35), ('Northern Deccan', 35), ('Southern Deccan', 35), ('Tamilakam', 35), ('Kalinga', 35), ('Gondwana', 35), ('Malwa', 35), ('Rajasthan', 35), ('Doab', 35), ('Bihar', 35), ('Assam', 35), ('Bengal', 35), ('Himalayas', 35), ('Tibetan Plateau', 35), ('Guangxi', 35), ('Yunnan', 35), ('Lower Ayeyarwady', 35), ('Upper Ayeyarwady', 35), ('Malacca Strait', 35), ('Mekong', 35), ('Chao Phraya', 35), ('Sunda Strait', 35),
     ('Champa Sea', 35), ('Moluccas', 35), ('Australia', 35), ('Liangguang', 35), ('Szechwan', 35), ('Huazhong', 35), ('Jiangxi', 35), ('Jiangnan', 35), ('Fujian', 35), ('Huabei', 35), ('Xibei', 35), ('Zhongyuan', 35), ('Huai He', 35), ('Eastern Siberia', 35), ('East Sea', 35), ('Nippon', 35),
     ('Yellow Sea', 35), ('Amur', 35), ('Chala', 29), ('Southern Andes', 29), ('Central Andes', 29), ('Southern Cone', 27), ('Guiana', 26), ('Northern Andes', 26), ('Amazonia', 29), ('Cerrado', 29), ('Isthmus of Darien', 25), ('Caribbean', 25), ('Valley of Mexico', 25), ('Western Valley', 25), ('Gulf of Mexico', 25), ('Gulf of Tehuantepec', 25), ('Rio Grande', 23), ('Mississippi', 23), ('Western Cordillera', 23), ('Plains', 23), ('Eastern Seaboard', 25), ('Great Lakes', 27),
     ('American West Coast', 30), ('Pacific', 43)])
# Southeastern America
expeditions_list.append(Expedition('southeastern_america', 'Southeastern America', 400, 'Colonial Node', [69, 66]))
expeditions_list[-1].set_node_tech_reqs(
    [('Iberia', 33), ('Strait of Gibraltar', 33), ('Sahara', 33), ('Alboran Sea', 33), ('Gulf of Lion', 33), ('Bay of Biscay', 33), ('France', 33), ('North Sea', 33), ('Channel', 33), ('Norwegian Sea', 33), ('Western Baltic', 33), ('Berber Coast', 33), ('Maghreb', 33), ('Tyrrenean Sea', 33), ('Rhineland', 33), ('Upper Danube', 33), ('Lower Nile', 33), ('Po Valley', 33), ('Adriatic Sea', 33), ('Levantine Sea', 33),
     ('Aegean Sea', 33), ('Dniester', 33), ('Lower Danube', 33), ('Middle Danube', 33), ('Elbe', 33), ('Eastern Baltic', 33),
     ('Vistula', 33), ('Black Sea', 33), ('Western Siberia', 33), ('Dnipro', 33), ('Volga', 33), ('Great Steppe', 33), ('Caspian Sea', 33), ('Zalesye', 33), ('Caucasus', 33), ('Anatolia', 33), ('Senegambia', 33), ('Upper Niger', 33), ('Guinea Coast', 33), ('Volta', 33), ('Lower Niger', 33), ('Lake Tchad', 33), ('Kongo', 33), ('South Africa', 33), ('African Great Lakes', 33), ('Monomotapa', 33), ('Somalia', 33), ('Zanj', 33), ('Red Sea', 33),
     ('Abyssinian Highlands', 33), ('Upper Nile', 33), ('Jazira', 33), ('Arabian Peninsula', 33), ('Arabian Gulf', 33), ('Iran', 33), ('Khorasan', 33), ('Mawarannahr', 33), ('Tarim Basin', 33),
     ('Punjab', 33), ('Sindh', 33), ('Gurjaratra', 33), ('Konkan', 33), ('Northern Deccan', 33), ('Southern Deccan', 33), ('Tamilakam', 33), ('Kalinga', 33), ('Gondwana', 33), ('Malwa', 33), ('Rajasthan', 33), ('Doab', 33), ('Bihar', 33), ('Assam', 33), ('Bengal', 33), ('Himalayas', 33), ('Tibetan Plateau', 33), ('Guangxi', 33), ('Yunnan', 33), ('Lower Ayeyarwady', 33), ('Upper Ayeyarwady', 33), ('Malacca Strait', 33), ('Mekong', 33), ('Chao Phraya', 33), ('Sunda Strait', 33),
     ('Champa Sea', 33), ('Moluccas', 33), ('Australia', 33), ('Liangguang', 33), ('Szechwan', 33), ('Huazhong', 33), ('Jiangxi', 33), ('Jiangnan', 33), ('Fujian', 33), ('Huabei', 33), ('Xibei', 33), ('Zhongyuan', 33), ('Huai He', 33), ('Eastern Siberia', 33), ('East Sea', 33), ('Nippon', 33),
     ('Yellow Sea', 33), ('Amur', 33), ('Chala', 29), ('Southern Andes', 29), ('Central Andes', 29), ('Southern Cone', 27), ('Guiana', 26), ('Northern Andes', 26), ('Amazonia', 29), ('Cerrado', 29), ('Isthmus of Darien', 26), ('Caribbean', 25), ('Valley of Mexico', 25), ('Western Valley', 25), ('Gulf of Mexico', 25), ('Gulf of Tehuantepec', 25), ('Rio Grande', 25), ('Mississippi', 23), ('Western Cordillera', 23), ('Plains', 23), ('Eastern Seaboard', 23), ('Great Lakes', 25),
     ('American West Coast', 30), ('Pacific', 43)])
# Eastern America
expeditions_list.append(Expedition('eastern_america', 'Eastern America', 400, 'Colonial Node', [69]))
expeditions_list[-1].set_node_tech_reqs(
    [('Iberia', 35), ('Strait of Gibraltar', 35), ('Sahara', 35), ('Alboran Sea', 35), ('Gulf of Lion', 35), ('Bay of Biscay', 35), ('France', 35), ('North Sea', 35), ('Channel', 35), ('Norwegian Sea', 35), ('Western Baltic', 35), ('Berber Coast', 35), ('Maghreb', 35), ('Tyrrenean Sea', 35), ('Rhineland', 35), ('Upper Danube', 35), ('Lower Nile', 35), ('Po Valley', 35), ('Adriatic Sea', 35), ('Levantine Sea', 35),
     ('Aegean Sea', 35), ('Dniester', 35), ('Lower Danube', 35), ('Middle Danube', 35), ('Elbe', 35), ('Eastern Baltic', 35),
     ('Vistula', 35), ('Black Sea', 35), ('Western Siberia', 35), ('Dnipro', 35), ('Volga', 35), ('Great Steppe', 35), ('Caspian Sea', 35), ('Zalesye', 35), ('Caucasus', 35), ('Anatolia', 35), ('Senegambia', 35), ('Upper Niger', 35), ('Guinea Coast', 35), ('Volta', 35), ('Lower Niger', 35), ('Lake Tchad', 35), ('Kongo', 35), ('South Africa', 35), ('African Great Lakes', 35), ('Monomotapa', 35), ('Somalia', 35), ('Zanj', 35), ('Red Sea', 35),
     ('Abyssinian Highlands', 35), ('Upper Nile', 35), ('Jazira', 35), ('Arabian Peninsula', 35), ('Arabian Gulf', 35), ('Iran', 35), ('Khorasan', 35), ('Mawarannahr', 35), ('Tarim Basin', 35),
     ('Punjab', 35), ('Sindh', 35), ('Gurjaratra', 35), ('Konkan', 35), ('Northern Deccan', 35), ('Southern Deccan', 35), ('Tamilakam', 35), ('Kalinga', 35), ('Gondwana', 35), ('Malwa', 35), ('Rajasthan', 35), ('Doab', 35), ('Bihar', 35), ('Assam', 35), ('Bengal', 35), ('Himalayas', 35), ('Tibetan Plateau', 35), ('Guangxi', 35), ('Yunnan', 35), ('Lower Ayeyarwady', 35), ('Upper Ayeyarwady', 35), ('Malacca Strait', 35), ('Mekong', 35), ('Chao Phraya', 35), ('Sunda Strait', 35),
     ('Champa Sea', 35), ('Moluccas', 35), ('Australia', 35), ('Liangguang', 35), ('Szechwan', 35), ('Huazhong', 35), ('Jiangxi', 35), ('Jiangnan', 35), ('Fujian', 35), ('Huabei', 35), ('Xibei', 35), ('Zhongyuan', 35), ('Huai He', 35), ('Eastern Siberia', 35), ('East Sea', 35), ('Nippon', 35),
     ('Yellow Sea', 35), ('Amur', 35), ('Chala', 30), ('Southern Andes', 30), ('Central Andes', 30), ('Southern Cone', 29), ('Guiana', 29), ('Northern Andes', 29), ('Amazonia', 30), ('Cerrado', 30), ('Isthmus of Darien', 26), ('Caribbean', 26), ('Valley of Mexico', 26), ('Western Valley', 26), ('Gulf of Mexico', 26), ('Gulf of Tehuantepec', 26), ('Rio Grande', 26), ('Mississippi', 26), ('Western Cordillera', 26), ('Plains', 26), ('Eastern Seaboard', 23), ('Great Lakes', 25),
     ('American West Coast', 31), ('Pacific', 43)])
# Canada
expeditions_list.append(Expedition('canada', 'Canada', 200, 'Colonial Node', [67]))
expeditions_list[-1].set_node_tech_reqs(
    [('Iberia', 35), ('Strait of Gibraltar', 35), ('Sahara', 35), ('Alboran Sea', 35), ('Gulf of Lion', 35), ('Bay of Biscay', 35), ('France', 35), ('North Sea', 35), ('Channel', 35), ('Norwegian Sea', 35), ('Western Baltic', 35), ('Berber Coast', 35), ('Maghreb', 35), ('Tyrrenean Sea', 35), ('Rhineland', 35), ('Upper Danube', 35), ('Lower Nile', 35), ('Po Valley', 35), ('Adriatic Sea', 35), ('Levantine Sea', 35),
     ('Aegean Sea', 35), ('Dniester', 35), ('Lower Danube', 35), ('Middle Danube', 35), ('Elbe', 35), ('Eastern Baltic', 35),
     ('Vistula', 35), ('Black Sea', 35), ('Western Siberia', 35), ('Dnipro', 35), ('Volga', 35), ('Great Steppe', 35), ('Caspian Sea', 35), ('Zalesye', 35), ('Caucasus', 35), ('Anatolia', 35), ('Senegambia', 35), ('Upper Niger', 35), ('Guinea Coast', 35), ('Volta', 35), ('Lower Niger', 35), ('Lake Tchad', 35), ('Kongo', 35), ('South Africa', 35), ('African Great Lakes', 35), ('Monomotapa', 35), ('Somalia', 35), ('Zanj', 35), ('Red Sea', 35),
     ('Abyssinian Highlands', 35), ('Upper Nile', 35), ('Jazira', 35), ('Arabian Peninsula', 35), ('Arabian Gulf', 35), ('Iran', 35), ('Khorasan', 35), ('Mawarannahr', 35), ('Tarim Basin', 35),
     ('Punjab', 35), ('Sindh', 35), ('Gurjaratra', 35), ('Konkan', 35), ('Northern Deccan', 35), ('Southern Deccan', 35), ('Tamilakam', 35), ('Kalinga', 35), ('Gondwana', 35), ('Malwa', 35), ('Rajasthan', 35), ('Doab', 35), ('Bihar', 35), ('Assam', 35), ('Bengal', 35), ('Himalayas', 35), ('Tibetan Plateau', 35), ('Guangxi', 35), ('Yunnan', 35), ('Lower Ayeyarwady', 35), ('Upper Ayeyarwady', 35), ('Malacca Strait', 35), ('Mekong', 35), ('Chao Phraya', 35), ('Sunda Strait', 35),
     ('Champa Sea', 35), ('Moluccas', 35), ('Australia', 35), ('Liangguang', 35), ('Szechwan', 35), ('Huazhong', 35), ('Jiangxi', 35), ('Jiangnan', 35), ('Fujian', 35), ('Huabei', 35), ('Xibei', 35), ('Zhongyuan', 35), ('Huai He', 35), ('Eastern Siberia', 35), ('East Sea', 35), ('Nippon', 35),
     ('Yellow Sea', 35), ('Amur', 35), ('Chala', 35), ('Southern Andes', 35), ('Central Andes', 35), ('Southern Cone', 35), ('Guiana', 35), ('Northern Andes', 35), ('Amazonia', 35), ('Cerrado', 35), ('Isthmus of Darien', 35), ('Caribbean', 35), ('Valley of Mexico', 35), ('Western Valley', 35), ('Gulf of Mexico', 35), ('Gulf of Tehuantepec', 35), ('Rio Grande', 35), ('Mississippi', 35), ('Western Cordillera', 35), ('Plains', 35), ('Eastern Seaboard', 25), ('Great Lakes', 23),
     ('American West Coast', 35), ('Pacific', 43)])
# the North Atlantic
expeditions_list.append(Expedition('north_atlantic', 'the North Atlantic', 50, 'Jumping Node', [85]))
expeditions_list[-1].set_node_tech_reqs(
    [('Iberia', 40), ('Strait of Gibraltar', 40), ('Sahara', 40), ('Alboran Sea', 40), ('Gulf of Lion', 40), ('Bay of Biscay', 40), ('France', 40), ('North Sea', 40), ('Channel', 40), ('Norwegian Sea', 40), ('Western Baltic', 40), ('Berber Coast', 40), ('Maghreb', 40), ('Tyrrenean Sea', 40), ('Rhineland', 40), ('Upper Danube', 40), ('Lower Nile', 40), ('Po Valley', 40), ('Adriatic Sea', 40), ('Levantine Sea', 40),
     ('Aegean Sea', 40), ('Dniester', 40), ('Lower Danube', 40), ('Middle Danube', 40), ('Elbe', 40), ('Eastern Baltic', 40),
     ('Vistula', 40), ('Black Sea', 40), ('Western Siberia', 40), ('Dnipro', 40), ('Volga', 40), ('Great Steppe', 40), ('Caspian Sea', 40), ('Zalesye', 40), ('Caucasus', 40), ('Anatolia', 40), ('Senegambia', 40), ('Upper Niger', 40), ('Guinea Coast', 40), ('Volta', 40), ('Lower Niger', 40), ('Lake Tchad', 40), ('Kongo', 40), ('South Africa', 40), ('African Great Lakes', 40), ('Monomotapa', 40), ('Somalia', 40), ('Zanj', 40), ('Red Sea', 40),
     ('Abyssinian Highlands', 40), ('Upper Nile', 40), ('Jazira', 40), ('Arabian Peninsula', 40), ('Arabian Gulf', 40), ('Iran', 40), ('Khorasan', 40), ('Mawarannahr', 40), ('Tarim Basin', 40),
     ('Punjab', 40), ('Sindh', 40), ('Gurjaratra', 40), ('Konkan', 40), ('Northern Deccan', 40), ('Southern Deccan', 40), ('Tamilakam', 40), ('Kalinga', 40), ('Gondwana', 40), ('Malwa', 40), ('Rajasthan', 40), ('Doab', 40), ('Bihar', 40), ('Assam', 40), ('Bengal', 40), ('Himalayas', 40), ('Tibetan Plateau', 40), ('Guangxi', 40), ('Yunnan', 40), ('Lower Ayeyarwady', 40), ('Upper Ayeyarwady', 40), ('Malacca Strait', 40), ('Mekong', 40), ('Chao Phraya', 40), ('Sunda Strait', 40),
     ('Champa Sea', 40), ('Moluccas', 40), ('Australia', 40), ('Liangguang', 40), ('Szechwan', 40), ('Huazhong', 40), ('Jiangxi', 40), ('Jiangnan', 40), ('Fujian', 40), ('Huabei', 40), ('Xibei', 40), ('Zhongyuan', 40), ('Huai He', 40), ('Eastern Siberia', 40), ('East Sea', 40), ('Nippon', 40),
     ('Yellow Sea', 40), ('Amur', 40), ('Chala', 40), ('Southern Andes', 40), ('Central Andes', 40), ('Southern Cone', 40), ('Guiana', 40), ('Northern Andes', 40), ('Amazonia', 40), ('Cerrado', 40), ('Isthmus of Darien', 40), ('Caribbean', 40), ('Valley of Mexico', 40), ('Western Valley', 40), ('Gulf of Mexico', 40), ('Gulf of Tehuantepec', 40), ('Rio Grande', 40), ('Mississippi', 40), ('Western Cordillera', 40), ('Plains', 40), ('Eastern Seaboard', 40), ('Great Lakes', 40),
     ('American West Coast', 40), ('Pacific', 43)])
# Hudson Bay
expeditions_list.append(Expedition('hudson_bay', 'Hudson Bay', 100, 'Colonial Node', [67]))
expeditions_list[-1].set_node_tech_reqs(
    [('Iberia', 45), ('Strait of Gibraltar', 45), ('Sahara', 45), ('Alboran Sea', 45), ('Gulf of Lion', 45), ('Bay of Biscay', 45), ('France', 45), ('North Sea', 45), ('Channel', 45), ('Norwegian Sea', 45), ('Western Baltic', 45), ('Berber Coast', 45), ('Maghreb', 45), ('Tyrrenean Sea', 45), ('Rhineland', 45), ('Upper Danube', 45), ('Lower Nile', 45), ('Po Valley', 45), ('Adriatic Sea', 45), ('Levantine Sea', 45),
     ('Aegean Sea', 45), ('Dniester', 45), ('Lower Danube', 45), ('Middle Danube', 45), ('Elbe', 45), ('Eastern Baltic', 45),
     ('Vistula', 45), ('Black Sea', 45), ('Western Siberia', 45), ('Dnipro', 45), ('Volga', 45), ('Great Steppe', 45), ('Caspian Sea', 45), ('Zalesye', 45), ('Caucasus', 45), ('Anatolia', 45), ('Senegambia', 45), ('Upper Niger', 45), ('Guinea Coast', 45), ('Volta', 45), ('Lower Niger', 45), ('Lake Tchad', 45), ('Kongo', 45), ('South Africa', 45), ('African Great Lakes', 45), ('Monomotapa', 45), ('Somalia', 45), ('Zanj', 45), ('Red Sea', 45),
     ('Abyssinian Highlands', 45), ('Upper Nile', 45), ('Jazira', 45), ('Arabian Peninsula', 45), ('Arabian Gulf', 45), ('Iran', 45), ('Khorasan', 45), ('Mawarannahr', 45), ('Tarim Basin', 45),
     ('Punjab', 45), ('Sindh', 45), ('Gurjaratra', 45), ('Konkan', 45), ('Northern Deccan', 45), ('Southern Deccan', 45), ('Tamilakam', 45), ('Kalinga', 45), ('Gondwana', 45), ('Malwa', 45), ('Rajasthan', 45), ('Doab', 45), ('Bihar', 45), ('Assam', 45), ('Bengal', 45), ('Himalayas', 45), ('Tibetan Plateau', 45), ('Guangxi', 45), ('Yunnan', 45), ('Lower Ayeyarwady', 45), ('Upper Ayeyarwady', 45), ('Malacca Strait', 45), ('Mekong', 45), ('Chao Phraya', 45), ('Sunda Strait', 45),
     ('Champa Sea', 45), ('Moluccas', 45), ('Australia', 45), ('Liangguang', 45), ('Szechwan', 45), ('Huazhong', 45), ('Jiangxi', 45), ('Jiangnan', 45), ('Fujian', 45), ('Huabei', 45), ('Xibei', 45), ('Zhongyuan', 45), ('Huai He', 45), ('Eastern Siberia', 45), ('East Sea', 45), ('Nippon', 45),
     ('Yellow Sea', 45), ('Amur', 45), ('Chala', 45), ('Southern Andes', 45), ('Central Andes', 45), ('Southern Cone', 45), ('Guiana', 45), ('Northern Andes', 45), ('Amazonia', 45), ('Cerrado', 45), ('Isthmus of Darien', 45), ('Caribbean', 45), ('Valley of Mexico', 45), ('Western Valley', 45), ('Gulf of Mexico', 45), ('Gulf of Tehuantepec', 45), ('Rio Grande', 45), ('Mississippi', 45), ('Western Cordillera', 45), ('Plains', 45), ('Eastern Seaboard', 45), ('Great Lakes', 23),
     ('American West Coast', 45), ('Pacific', 45)])
# Southern Cone
expeditions_list.append(Expedition('la_plata', 'Southern Cone', 100, 'Colonial Node', [17]))
expeditions_list[-1].set_node_tech_reqs(
    [('Iberia', 33), ('Strait of Gibraltar', 33), ('Sahara', 33), ('Alboran Sea', 33), ('Gulf of Lion', 33), ('Bay of Biscay', 33), ('France', 33), ('North Sea', 33), ('Channel', 33), ('Norwegian Sea', 33), ('Western Baltic', 33), ('Berber Coast', 33), ('Maghreb', 33), ('Tyrrenean Sea', 33), ('Rhineland', 33), ('Upper Danube', 33), ('Lower Nile', 33), ('Po Valley', 33), ('Adriatic Sea', 33), ('Levantine Sea', 33),
     ('Aegean Sea', 33), ('Dniester', 33), ('Lower Danube', 33), ('Middle Danube', 33), ('Elbe', 33), ('Eastern Baltic', 33),
     ('Vistula', 33), ('Black Sea', 33), ('Western Siberia', 33), ('Dnipro', 33), ('Volga', 33), ('Great Steppe', 33), ('Caspian Sea', 33), ('Zalesye', 33), ('Caucasus', 33), ('Anatolia', 33), ('Senegambia', 30), ('Upper Niger', 30), ('Guinea Coast', 30), ('Volta', 30), ('Lower Niger', 30), ('Lake Tchad', 30), ('Kongo', 31), ('South Africa', 33), ('African Great Lakes', 33), ('Monomotapa', 33), ('Somalia', 33), ('Zanj', 33), ('Red Sea', 33),
     ('Abyssinian Highlands', 33), ('Upper Nile', 33), ('Jazira', 33), ('Arabian Peninsula', 33), ('Arabian Gulf', 33), ('Iran', 33), ('Khorasan', 33), ('Mawarannahr', 33), ('Tarim Basin', 33),
     ('Punjab', 33), ('Sindh', 33), ('Gurjaratra', 33), ('Konkan', 33), ('Northern Deccan', 33), ('Southern Deccan', 33), ('Tamilakam', 33), ('Kalinga', 33), ('Gondwana', 33), ('Malwa', 33), ('Rajasthan', 33), ('Doab', 33), ('Bihar', 33), ('Assam', 33), ('Bengal', 33), ('Himalayas', 33), ('Tibetan Plateau', 33), ('Guangxi', 33), ('Yunnan', 33), ('Lower Ayeyarwady', 33), ('Upper Ayeyarwady', 33), ('Malacca Strait', 33), ('Mekong', 33), ('Chao Phraya', 33), ('Sunda Strait', 33),
     ('Champa Sea', 33), ('Moluccas', 33), ('Australia', 33), ('Liangguang', 33), ('Szechwan', 33), ('Huazhong', 33), ('Jiangxi', 33), ('Jiangnan', 33), ('Fujian', 33), ('Huabei', 33), ('Xibei', 33), ('Zhongyuan', 33), ('Huai He', 33), ('Eastern Siberia', 33), ('East Sea', 33), ('Nippon', 33),
     ('Yellow Sea', 33), ('Amur', 33), ('Chala', 26), ('Southern Andes', 26), ('Central Andes', 26), ('Southern Cone', 23), ('Guiana', 25), ('Northern Andes', 25), ('Amazonia', 26), ('Cerrado', 26), ('Isthmus of Darien', 27), ('Caribbean', 27), ('Valley of Mexico', 27), ('Western Valley', 27), ('Gulf of Mexico', 27), ('Gulf of Tehuantepec', 27), ('Rio Grande', 27), ('Mississippi', 27), ('Western Cordillera', 27), ('Plains', 27), ('Eastern Seaboard', 27), ('Great Lakes', 29),
     ('American West Coast', 29), ('Pacific', 43)])
# California
expeditions_list.append(Expedition('california', 'California', 100, 'Colonial Node', [8]))
expeditions_list[-1].set_node_tech_reqs(
    [('Iberia', 40), ('Strait of Gibraltar', 40), ('Sahara', 40), ('Alboran Sea', 40), ('Gulf of Lion', 40), ('Bay of Biscay', 40), ('France', 40), ('North Sea', 40), ('Channel', 40), ('Norwegian Sea', 40), ('Western Baltic', 40), ('Berber Coast', 40), ('Maghreb', 40), ('Tyrrenean Sea', 40), ('Rhineland', 40), ('Upper Danube', 40), ('Lower Nile', 40), ('Po Valley', 40), ('Adriatic Sea', 40), ('Levantine Sea', 40),
     ('Aegean Sea', 40), ('Dniester', 40), ('Lower Danube', 40), ('Middle Danube', 40), ('Elbe', 40), ('Eastern Baltic', 40),
     ('Vistula', 40), ('Black Sea', 40), ('Western Siberia', 40), ('Dnipro', 40), ('Volga', 40), ('Great Steppe', 40), ('Caspian Sea', 40), ('Zalesye', 40), ('Caucasus', 40), ('Anatolia', 40), ('Senegambia', 40), ('Upper Niger', 40), ('Guinea Coast', 40), ('Volta', 40), ('Lower Niger', 40), ('Lake Tchad', 40), ('Kongo', 40), ('South Africa', 40), ('African Great Lakes', 40), ('Monomotapa', 40), ('Somalia', 40), ('Zanj', 40), ('Red Sea', 35),
     ('Abyssinian Highlands', 35), ('Upper Nile', 35), ('Jazira', 35), ('Arabian Peninsula', 35), ('Arabian Gulf', 35), ('Iran', 35), ('Khorasan', 35), ('Mawarannahr', 35), ('Tarim Basin', 35),
     ('Punjab', 35), ('Sindh', 35), ('Gurjaratra', 35), ('Konkan', 35), ('Northern Deccan', 35), ('Southern Deccan', 35), ('Tamilakam', 35), ('Kalinga', 35), ('Gondwana', 35), ('Malwa', 35), ('Rajasthan', 35), ('Doab', 35), ('Bihar', 35), ('Assam', 35), ('Bengal', 35), ('Himalayas', 35), ('Tibetan Plateau', 35), ('Guangxi', 35), ('Yunnan', 35), ('Lower Ayeyarwady', 33), ('Upper Ayeyarwady', 33), ('Malacca Strait', 33), ('Mekong', 33), ('Chao Phraya', 33), ('Sunda Strait', 33),
     ('Champa Sea', 33), ('Moluccas', 33), ('Australia', 33), ('Liangguang', 31), ('Szechwan', 31), ('Huazhong', 31), ('Jiangxi', 31), ('Jiangnan', 31), ('Fujian', 31), ('Huabei', 31), ('Xibei', 31), ('Zhongyuan', 30), ('Huai He', 30), ('Eastern Siberia', 30), ('East Sea', 30), ('Nippon', 30),
     ('Yellow Sea', 30), ('Amur', 30), ('Chala', 27), ('Southern Andes', 27), ('Central Andes', 27), ('Southern Cone', 29), ('Guiana', 29), ('Northern Andes', 29), ('Amazonia', 27), ('Cerrado', 27), ('Isthmus of Darien', 26), ('Caribbean', 29), ('Valley of Mexico', 25), ('Western Valley', 25), ('Gulf of Mexico', 25), ('Gulf of Tehuantepec', 25), ('Rio Grande', 25), ('Mississippi', 29), ('Western Cordillera', 29), ('Plains', 29), ('Eastern Seaboard', 29), ('Great Lakes', 30),
     ('American West Coast', 23), ('Pacific', 43)])
# Alaska
expeditions_list.append(Expedition('alaska', 'Alaska', 100, 'Colonial Node', [8]))
expeditions_list[-1].set_node_tech_reqs(
    [('Iberia', 47), ('Strait of Gibraltar', 47), ('Sahara', 47), ('Alboran Sea', 47), ('Gulf of Lion', 47), ('Bay of Biscay', 47), ('France', 47), ('North Sea', 47), ('Channel', 47), ('Norwegian Sea', 47), ('Western Baltic', 47), ('Berber Coast', 47), ('Maghreb', 47), ('Tyrrenean Sea', 47), ('Rhineland', 47), ('Upper Danube', 47), ('Lower Nile', 47), ('Po Valley', 47), ('Adriatic Sea', 47), ('Levantine Sea', 47),
     ('Aegean Sea', 47), ('Dniester', 47), ('Lower Danube', 47), ('Middle Danube', 47), ('Elbe', 47), ('Eastern Baltic', 47),
     ('Vistula', 47), ('Black Sea', 47), ('Western Siberia', 47), ('Dnipro', 47), ('Volga', 47), ('Great Steppe', 47), ('Caspian Sea', 47), ('Zalesye', 47), ('Caucasus', 47), ('Anatolia', 47), ('Senegambia', 47), ('Upper Niger', 47), ('Guinea Coast', 47), ('Volta', 47), ('Lower Niger', 47), ('Lake Tchad', 47), ('Kongo', 47), ('South Africa', 47), ('African Great Lakes', 47), ('Monomotapa', 47), ('Somalia', 47), ('Zanj', 47), ('Red Sea', 47),
     ('Abyssinian Highlands', 47), ('Upper Nile', 47), ('Jazira', 47), ('Arabian Peninsula', 47), ('Arabian Gulf', 47), ('Iran', 47), ('Khorasan', 47), ('Mawarannahr', 47), ('Tarim Basin', 47),
     ('Punjab', 47), ('Sindh', 47), ('Gurjaratra', 47), ('Konkan', 47), ('Northern Deccan', 47), ('Southern Deccan', 47), ('Tamilakam', 47), ('Kalinga', 47), ('Gondwana', 47), ('Malwa', 47), ('Rajasthan', 47), ('Doab', 47), ('Bihar', 47), ('Assam', 47), ('Bengal', 47), ('Himalayas', 47), ('Tibetan Plateau', 47), ('Guangxi', 47), ('Yunnan', 47), ('Lower Ayeyarwady', 47), ('Upper Ayeyarwady', 47), ('Malacca Strait', 47), ('Mekong', 47), ('Chao Phraya', 47), ('Sunda Strait', 47),
     ('Champa Sea', 47), ('Moluccas', 47), ('Australia', 47), ('Liangguang', 47), ('Szechwan', 47), ('Huazhong', 47), ('Jiangxi', 47), ('Jiangnan', 47), ('Fujian', 47), ('Huabei', 47), ('Xibei', 47), ('Zhongyuan', 47), ('Huai He', 47), ('Eastern Siberia', 40), ('East Sea', 40), ('Nippon', 40),
     ('Yellow Sea', 40), ('Amur', 40), ('Chala', 40), ('Southern Andes', 40), ('Central Andes', 40), ('Southern Cone', 40), ('Guiana', 40), ('Northern Andes', 40), ('Amazonia', 40), ('Cerrado', 40), ('Isthmus of Darien', 40), ('Caribbean', 40), ('Valley of Mexico', 40), ('Western Valley', 40), ('Gulf of Mexico', 40), ('Gulf of Tehuantepec', 40), ('Rio Grande', 40), ('Mississippi', 40), ('Western Cordillera', 40), ('Plains', 40), ('Eastern Seaboard', 40), ('Great Lakes', 35),
     ('American West Coast', 23), ('Pacific', 43)])
# Pacific Mexico
expeditions_list.append(Expedition('pacific_mexico', 'Pacific Mexico', 800, 'Colonial Node', [9, 65]))
expeditions_list[-1].set_node_tech_reqs(
    [('Iberia', 33), ('Strait of Gibraltar', 33), ('Sahara', 33), ('Alboran Sea', 33), ('Gulf of Lion', 33), ('Bay of Biscay', 33), ('France', 33), ('North Sea', 33), ('Channel', 33), ('Norwegian Sea', 33), ('Western Baltic', 33), ('Berber Coast', 33), ('Maghreb', 33), ('Tyrrenean Sea', 33), ('Rhineland', 33), ('Upper Danube', 33), ('Lower Nile', 33), ('Po Valley', 33), ('Adriatic Sea', 33), ('Levantine Sea', 33),
     ('Aegean Sea', 33), ('Dniester', 33), ('Lower Danube', 33), ('Middle Danube', 33), ('Elbe', 33), ('Eastern Baltic', 33), ('Vistula', 33), ('Black Sea', 33), ('Western Siberia', 33), ('Dnipro', 33), ('Volga', 33), ('Great Steppe', 33), ('Caspian Sea', 33), ('Zalesye', 33), ('Caucasus', 33), ('Anatolia', 33), ('Senegambia', 33), ('Upper Niger', 33), ('Guinea Coast', 33), ('Volta', 33), ('Lower Niger', 33), ('Lake Tchad', 33), ('Kongo', 33),
     ('South Africa', 33), ('African Great Lakes', 33), ('Monomotapa', 33), ('Somalia', 33), ('Zanj', 33), ('Red Sea', 33), ('Abyssinian Highlands', 33), ('Upper Nile', 33), ('Jazira', 33), ('Arabian Peninsula', 33), ('Arabian Gulf', 33), ('Iran', 33), ('Khorasan', 33), ('Mawarannahr', 33), ('Tarim Basin', 33),
     ('Punjab', 33), ('Sindh', 33), ('Gurjaratra', 33), ('Konkan', 33), ('Northern Deccan', 33), ('Southern Deccan', 33), ('Tamilakam', 33), ('Kalinga', 33), ('Gondwana', 33), ('Malwa', 33), ('Rajasthan', 33), ('Doab', 33), ('Bihar', 33), ('Assam', 33), ('Bengal', 33), ('Himalayas', 33), ('Tibetan Plateau', 33), ('Guangxi', 33), ('Yunnan', 33), ('Lower Ayeyarwady', 33), ('Upper Ayeyarwady', 33), ('Malacca Strait', 33), ('Mekong', 33), ('Chao Phraya', 33), ('Sunda Strait', 33),
     ('Champa Sea', 33), ('Moluccas', 33), ('Australia', 33), ('Liangguang', 32), ('Szechwan', 32), ('Huazhong', 32), ('Jiangxi', 32), ('Jiangnan', 32), ('Fujian', 32), ('Huabei', 32), ('Xibei', 32), ('Zhongyuan', 31), ('Huai He', 31), ('Eastern Siberia', 31), ('East Sea', 31), ('Nippon', 31),
     ('Yellow Sea', 31), ('Amur', 31), ('Chala', 26), ('Southern Andes', 26), ('Central Andes', 26), ('Southern Cone', 27), ('Guiana', 27), ('Northern Andes', 27), ('Amazonia', 26), ('Cerrado', 26), ('Isthmus of Darien', 25), ('Caribbean', 29), ('Valley of Mexico', 25), ('Western Valley', 25), ('Gulf of Mexico', 25), ('Gulf of Tehuantepec', 25), ('Rio Grande', 23), ('Mississippi', 29), ('Western Cordillera', 29), ('Plains', 29), ('Eastern Seaboard', 29), ('Great Lakes', 30),
     ('American West Coast', 25), ('Pacific', 43)])
# Pacific Central America
expeditions_list.append(Expedition('pacific_central_america', 'Pacific Central America', 1200, 'Colonial Node', [45]))
expeditions_list[-1].set_node_tech_reqs(
    [('Iberia', 33), ('Strait of Gibraltar', 33), ('Sahara', 33), ('Alboran Sea', 33), ('Gulf of Lion', 33), ('Bay of Biscay', 33), ('France', 33), ('North Sea', 33), ('Channel', 33), ('Norwegian Sea', 33), ('Western Baltic', 33), ('Berber Coast', 33), ('Maghreb', 33), ('Tyrrenean Sea', 33), ('Rhineland', 33), ('Upper Danube', 33), ('Lower Nile', 33), ('Po Valley', 33), ('Adriatic Sea', 33), ('Levantine Sea', 33),
     ('Aegean Sea', 33), ('Dniester', 33), ('Lower Danube', 33), ('Middle Danube', 33), ('Elbe', 33), ('Eastern Baltic', 33),
     ('Vistula', 33), ('Black Sea', 33), ('Western Siberia', 33), ('Dnipro', 33), ('Volga', 33), ('Great Steppe', 33), ('Caspian Sea', 33), ('Zalesye', 33), ('Caucasus', 33), ('Anatolia', 33), ('Senegambia', 33), ('Upper Niger', 33), ('Guinea Coast', 33), ('Volta', 33), ('Lower Niger', 33), ('Lake Tchad', 33), ('Kongo', 33), ('South Africa', 33), ('African Great Lakes', 33), ('Monomotapa', 33), ('Somalia', 33), ('Zanj', 33), ('Red Sea', 33),
     ('Abyssinian Highlands', 33), ('Upper Nile', 33), ('Jazira', 33), ('Arabian Peninsula', 33), ('Arabian Gulf', 33), ('Iran', 33), ('Khorasan', 33), ('Mawarannahr', 33), ('Tarim Basin', 33),
     ('Punjab', 33), ('Sindh', 33), ('Gurjaratra', 33), ('Konkan', 33), ('Northern Deccan', 33), ('Southern Deccan', 33), ('Tamilakam', 33), ('Kalinga', 33), ('Gondwana', 33), ('Malwa', 33), ('Rajasthan', 33), ('Doab', 33), ('Bihar', 33), ('Assam', 33), ('Bengal', 33), ('Himalayas', 33), ('Tibetan Plateau', 33), ('Guangxi', 33), ('Yunnan', 33), ('Lower Ayeyarwady', 33), ('Upper Ayeyarwady', 33), ('Malacca Strait', 33), ('Mekong', 33), ('Chao Phraya', 33), ('Sunda Strait', 33),
     ('Champa Sea', 33), ('Moluccas', 33), ('Australia', 33), ('Liangguang', 33), ('Szechwan', 33), ('Huazhong', 33), ('Jiangxi', 33), ('Jiangnan', 33), ('Fujian', 33), ('Huabei', 33), ('Xibei', 33), ('Zhongyuan', 32), ('Huai He', 32), ('Eastern Siberia', 32), ('East Sea', 32), ('Nippon', 32),
     ('Yellow Sea', 32), ('Amur', 32), ('Chala', 25), ('Southern Andes', 25), ('Central Andes', 25), ('Southern Cone', 27), ('Guiana', 27), ('Northern Andes', 27), ('Amazonia', 25), ('Cerrado', 25), ('Isthmus of Darien', 23), ('Caribbean', 29), ('Valley of Mexico', 25), ('Western Valley', 25), ('Gulf of Mexico', 25), ('Gulf of Tehuantepec', 25), ('Rio Grande', 25), ('Mississippi', 29), ('Western Cordillera', 29), ('Plains', 29), ('Eastern Seaboard', 29), ('Great Lakes', 30),
     ('American West Coast', 26), ('Pacific', 43)])
# Peru
expeditions_list.append(Expedition('peru', 'Peru', 2400, 'Colonial Node', [16]))
expeditions_list[-1].set_node_tech_reqs(
    [('Iberia', 33), ('Strait of Gibraltar', 33), ('Sahara', 33), ('Alboran Sea', 33), ('Gulf of Lion', 33), ('Bay of Biscay', 33), ('France', 33), ('North Sea', 33), ('Channel', 33), ('Norwegian Sea', 33), ('Western Baltic', 33), ('Berber Coast', 33), ('Maghreb', 33), ('Tyrrenean Sea', 33), ('Rhineland', 33), ('Upper Danube', 33), ('Lower Nile', 33), ('Po Valley', 33), ('Adriatic Sea', 33), ('Levantine Sea', 33),
     ('Aegean Sea', 33), ('Dniester', 33), ('Lower Danube', 33), ('Middle Danube', 33), ('Elbe', 33), ('Eastern Baltic', 33),
     ('Vistula', 33), ('Black Sea', 33), ('Western Siberia', 33), ('Dnipro', 33), ('Volga', 33), ('Great Steppe', 33), ('Caspian Sea', 33), ('Zalesye', 33), ('Caucasus', 33), ('Anatolia', 33), ('Senegambia', 33), ('Upper Niger', 33), ('Guinea Coast', 33), ('Volta', 33), ('Lower Niger', 33), ('Lake Tchad', 33), ('Kongo', 33), ('South Africa', 33), ('African Great Lakes', 33), ('Monomotapa', 33), ('Somalia', 33), ('Zanj', 33), ('Red Sea', 33),
     ('Abyssinian Highlands', 33), ('Upper Nile', 33), ('Jazira', 33), ('Arabian Peninsula', 33), ('Arabian Gulf', 33), ('Iran', 33), ('Khorasan', 33), ('Mawarannahr', 33), ('Tarim Basin', 33),
     ('Punjab', 33), ('Sindh', 33), ('Gurjaratra', 33), ('Konkan', 33), ('Northern Deccan', 33), ('Southern Deccan', 33), ('Tamilakam', 33), ('Kalinga', 33), ('Gondwana', 33), ('Malwa', 33), ('Rajasthan', 33), ('Doab', 33), ('Bihar', 33), ('Assam', 33), ('Bengal', 33), ('Himalayas', 33), ('Tibetan Plateau', 33), ('Guangxi', 33), ('Yunnan', 33), ('Lower Ayeyarwady', 33), ('Upper Ayeyarwady', 33), ('Malacca Strait', 33), ('Mekong', 33), ('Chao Phraya', 33), ('Sunda Strait', 33),
     ('Champa Sea', 33), ('Moluccas', 33), ('Australia', 33), ('Liangguang', 33), ('Szechwan', 33), ('Huazhong', 33), ('Jiangxi', 33), ('Jiangnan', 33), ('Fujian', 33), ('Huabei', 33), ('Xibei', 33), ('Zhongyuan', 33), ('Huai He', 33), ('Eastern Siberia', 33), ('East Sea', 33), ('Nippon', 33),
     ('Yellow Sea', 33), ('Amur', 33), ('Chala', 23), ('Southern Andes', 23), ('Central Andes', 23), ('Southern Cone', 26), ('Guiana', 27), ('Northern Andes', 27), ('Amazonia', 23), ('Cerrado', 23), ('Isthmus of Darien', 26), ('Caribbean', 29), ('Valley of Mexico', 26), ('Western Valley', 26), ('Gulf of Mexico', 26), ('Gulf of Tehuantepec', 26), ('Rio Grande', 27), ('Mississippi', 29), ('Western Cordillera', 29), ('Plains', 29), ('Eastern Seaboard', 29), ('Great Lakes', 30),
     ('American West Coast', 27), ('Pacific', 43)])
# Chile
expeditions_list.append(Expedition('chile', 'Chile', 400, 'Colonial Node', [16]))
expeditions_list[-1].set_node_tech_reqs(
    [('Iberia', 33), ('Strait of Gibraltar', 33), ('Sahara', 33), ('Alboran Sea', 33), ('Gulf of Lion', 33), ('Bay of Biscay', 33), ('France', 33), ('North Sea', 33), ('Channel', 33), ('Norwegian Sea', 33), ('Western Baltic', 33), ('Berber Coast', 33), ('Maghreb', 33), ('Tyrrenean Sea', 33), ('Rhineland', 33), ('Upper Danube', 33), ('Lower Nile', 33), ('Po Valley', 33), ('Adriatic Sea', 33), ('Levantine Sea', 33),
     ('Aegean Sea', 33), ('Dniester', 33), ('Lower Danube', 33), ('Middle Danube', 33), ('Elbe', 33), ('Eastern Baltic', 33),
     ('Vistula', 33), ('Black Sea', 33), ('Western Siberia', 33), ('Dnipro', 33), ('Volga', 33), ('Great Steppe', 33), ('Caspian Sea', 33), ('Zalesye', 33), ('Caucasus', 33), ('Anatolia', 33), ('Senegambia', 33), ('Upper Niger', 33), ('Guinea Coast',33), ('Volta', 33), ('Lower Niger', 33), ('Lake Tchad', 33), ('Kongo', 33), ('South Africa', 33), ('African Great Lakes', 33), ('Monomotapa', 33), ('Somalia', 33), ('Zanj', 33), ('Red Sea', 33),
     ('Abyssinian Highlands', 33), ('Upper Nile', 33), ('Jazira', 33), ('Arabian Peninsula', 33), ('Arabian Gulf', 33), ('Iran', 33), ('Khorasan', 33), ('Mawarannahr', 33), ('Tarim Basin', 33),
     ('Punjab', 33), ('Sindh', 33), ('Gurjaratra', 33), ('Konkan', 33), ('Northern Deccan', 33), ('Southern Deccan', 33), ('Tamilakam', 33), ('Kalinga', 33), ('Gondwana', 33), ('Malwa', 33), ('Rajasthan', 33), ('Doab', 33), ('Bihar', 33), ('Assam', 33), ('Bengal', 33), ('Himalayas', 33), ('Tibetan Plateau', 33), ('Guangxi', 33), ('Yunnan', 33), ('Lower Ayeyarwady', 33), ('Upper Ayeyarwady', 33), ('Malacca Strait', 33), ('Mekong', 33), ('Chao Phraya', 33), ('Sunda Strait', 33),
     ('Champa Sea', 33), ('Moluccas', 33), ('Australia', 33), ('Liangguang', 33), ('Szechwan', 33), ('Huazhong', 33), ('Jiangxi', 33), ('Jiangnan', 33), ('Fujian', 33), ('Huabei', 33), ('Xibei', 33), ('Zhongyuan', 33), ('Huai He', 33), ('Eastern Siberia', 33), ('East Sea', 33), ('Nippon', 33),
     ('Yellow Sea', 33), ('Amur', 33), ('Chala', 23), ('Southern Andes', 23), ('Central Andes', 23), ('Southern Cone', 26), ('Guiana', 27), ('Northern Andes', 27), ('Amazonia', 23), ('Cerrado', 23), ('Isthmus of Darien', 26), ('Caribbean', 29), ('Valley of Mexico', 26), ('Western Valley', 26), ('Gulf of Mexico', 26), ('Gulf of Tehuantepec', 26), ('Rio Grande', 27), ('Mississippi', 29), ('Western Cordillera', 29), ('Plains', 29), ('Eastern Seaboard', 29), ('Great Lakes', 30),
     ('American West Coast', 27), ('Pacific', 43)])

trade_nodes = {'Pacific': 1, 'Australia': 2, 'Huai He': 3, 'Zhongyuan': 4, 'Jiangnan': 5, 'East Sea': 6, 'Amur': 7, 'Yellow Sea': 8, 'Nippon': 9, 'Jiangxi': 10, 
               'Fujian': 11, 'Eastern Siberia': 12, 'Huabei': 13, 'American West Coast': 14, 'Western Valley': 15, 'Gulf of Tehuantepec': 16, 'Valley of Mexico': 17, 
               'Huazhong': 18, 'Guangxi': 19, 'Szechwan': 20, 'Xibei': 21, 'Amazonia': 22, 'Cerrado': 23, 'Central Andes': 24, 'Southern Andes': 25, 'Chala': 26, 
               'Northern Andes': 27, 'Southern Cone': 28, 'Liangguang': 29, 'Mekong': 30, 'Yunnan': 31, 'Chao Phraya': 32, 'Moluccas': 33, 'Champa Sea': 34, 
               'Tibetan Plateau': 35, 'Himalayas': 36, 'Sunda Strait': 37, 'Malacca Strait': 38, 'Upper Ayeyarwady': 39, 'Lower Ayeyarwady': 40, 'Assam': 41, 
               'Bihar': 42, 'Doab': 43, 'Tarim Basin': 44, 'Punjab': 45, 'Mawarannahr': 46, 'Khorasan': 47, 'Bengal': 48, 'Gondwana': 49, 'Southern Deccan': 50, 
               'Northern Deccan': 51, 'Rajasthan': 52, 'Malwa': 53, 'Kalinga': 54, 'Tamilakam': 55, 'Konkan': 56, 'Gurjaratra': 57, 'Sindh': 58,
               'Abyssinian Highlands': 59, 'Upper Nile': 60, 'Iran': 61, 'Arabian Peninsula': 62, 'Arabian Gulf': 63, 'Red Sea': 64, 'African Great Lakes': 65, 'Monomotapa': 66, 
               'Somalia': 67, 'Zanj': 68, 'South Africa': 69, 'Gulf of Mexico': 70, 'Isthmus of Darien': 71, 'Guiana': 72, 'Kongo': 73, 'Volta': 74, 'Guinea Coast': 75, 
               'Lower Niger': 76, 'Lake Tchad': 77, 'Upper Niger': 78, 'Sahara': 79, 'Senegambia': 80, 'Great Steppe': 81, 'Western Siberia': 82, 'Caspian Sea': 83, 
               'Volga': 84, 'Jazira': 85, 'Maghreb': 86, 'Berber Coast': 87, 'Lower Nile': 88, 'Dnipro': 89, 'Caucasus': 90, 'Anatolia': 91, 'Dniester': 92, 'Black Sea': 93, 
               'Levantine Sea': 94, 'Zalesye': 95, 'Vistula': 96, 'Western Cordillera': 97, 'Plains': 98, 'Rio Grande': 99, 'Mississippi': 100, 'Great Lakes': 101, 'Caribbean': 102, 
               'Eastern Seaboard': 103, 'Strait of Gibraltar': 104, 'Lower Danube': 105, 'Middle Danube': 106, 'Aegean Sea': 107, 'Alboran Sea': 108, 'Iberia': 109, 'Po Valley': 110, 
               'Upper Danube': 111, 'Rhineland': 112, 'Gulf of Lion': 113, 'Bay of Biscay': 114, 'France': 115, 'Eastern Baltic': 116, 'Adriatic Sea': 117, 'Norwegian Sea': 118,
               'Elbe': 119, 'Western Baltic': 120, 'North Sea': 121, 'Tyrrenean Sea': 122, 'Channel': 123 }

# Jiangxi, Volga, Jazira, Lower Danube

can_trigger_MAM_event_15 = ['east_africa', 'indian_ocean', 'arabia', 'indian_ocean', 'western_india', 'southern_india']

# Setup expeditions unlocks dict with keys for each tradenode holding an empty list
expedition_unlocks = {}
for node in trade_nodes:
    expedition_unlocks[node] = []

# Fill expeditions unlocked dict for when you unlock expeditions based on your capital location
for expedition in expeditions_list:
    assert len(set([i[0] for i in expedition.node_tech_reqs])) == len(expedition.node_tech_reqs)  # Assert all trade nodes are unique
    assert len(trade_nodes) == len(expedition.node_tech_reqs), f"{expedition.name} is missing some tech reqs"  # Assert all trade nodes were included
    for (trade_node, tech) in expedition.node_tech_reqs:
        assert trade_node in trade_nodes, f"{trade_node} spelled incorrectly"  # Assert all trade nodes are spelled correctly
        assert tech >= 13
        assert tech < 50
        expedition_unlocks[trade_node].append((expedition.localized_name, int(tech)))
for key in expedition_unlocks:  # Sort the list in each each tradenode by teach level
    expedition_unlocks[key].sort(key=lambda x: x[1])
assert len(trade_nodes) == len(expedition_unlocks), "Expedition unlocks should have 1 key per trade node"

num_total_expeditions = len(expeditions_list)

hash_line = "############################################################################################################\n"

neighboring_colonization_event = """\
# Gives rare colonization of neighboring provinces for countries without colonists
country_event = {
	id = MEC_Expeditions.002
	title = MEC_Expeditions.002.name
	desc = MEC_Expeditions.002.desc
	picture = TRADEGOODS_eventPicture
	
	trigger = {
		total_development = 30
		has_institution = Legalism
		NOT = { has_idea = exploration_ideas_2 } # Doesn't have colonist
		NOT = { has_idea = expansion_ideas_1 }
		OR = {
			AND = {
				is_colonial_nation = yes
				any_owned_province = {
					has_empty_adjacent_province = yes
				}
			}
			any_owned_province = {
				any_empty_neighbor_province = {
					NOT = {
						has_province_flag = ColonyBecomesOwner
						has_province_flag = NoRandomSpread
					}
				}
			}
		}
	}
	
	mean_time_to_happen = {
		years = 100 # 100 years
	}
	
	immediate = {
		hidden_effect = {
			random_owned_province = {
				limit = {
					has_empty_adjacent_province = yes
					OR = {
						ROOT = { is_colonial_nation = yes }
						any_empty_neighbor_province = {
							NOT = {
								has_province_flag = ColonyBecomesOwner
								has_province_flag = NoRandomSpread
							}
						}
					}
				}
				random_empty_neighbor_province = {
					limit = {
						OR = {
							ROOT = { is_colonial_nation = yes }
							NOT = {
								has_province_flag = ColonyBecomesOwner
								has_province_flag = NoRandomSpread
							}
						}
					}
					save_event_target_as = neighbor_province
					discover_country = ROOT
					if = {
						limit = {
							ROOT = { is_colonial_nation = yes }
						}
						change_religion = ROOT # Re-evaluate and probably change after religion rework is complete
						change_culture = ROOT
					}
					add_territorial_core = ROOT 
					cede_province = ROOT
				}
			}
		}
	}
	
	option = {
		name = MEC_Expeditions.002.opt
	}
}
"""

decisions_frame_top = """\
country_decisions = {

	# Decision to highlight all expedition provinces and toggle other expedition decisions
	MEC_Expeditions_Decision = {
		potential = { # Always visible for players
			ai = no
		}
		provinces_to_highlight = { # Highlight provinces for all expeditions
			OR = {
"""

decisions_frame_bottom = """\
			}
		}
		allow = { # Always allow
			custom_trigger_tooltip = {
				tooltip = MEC_Expeditions_Decision_Highlight_All
				always = yes
			}
		}
		effect = { # Toggle showing decisions for all expeditions
			custom_tooltip = MEC_Expeditions_Decision_Effect
			if = {
				limit = {
					has_country_flag = MEC_Expeditions_Show_Decisions
				}
				clr_country_flag = MEC_Expeditions_Show_Decisions
			}
			else = {
				set_country_flag = MEC_Expeditions_Show_Decisions
			}
		}
		ai_will_do = { # AI doesn't need informational decisions
			factor = 0
		}
	}
"""

decision_toggle_expeditions = """\
	MEC_Expeditions_Decision_toggle_expeditions = {
		potential = {
			has_country_flag = MEC_Expeditions_Show_Decisions
			OR = {
				has_idea = exploration_ideas_3
				has_country_modifier = can_colonize_country_modifier
			}
		}
		allow = {
			OR = {
				has_idea = exploration_ideas_3
				has_country_modifier = can_colonize_country_modifier
			}
		}
		effect = {
			if = {
				limit = {
					has_country_flag = MEC_Expeditions_paused
				}
				custom_tooltip = MEC_Expeditions_Decision_toggle_expeditions_restart
				clr_country_flag = MEC_Expeditions_paused
			}
			else = {
				custom_tooltip = MEC_Expeditions_Decision_toggle_expeditions_stop
				set_country_flag = MEC_Expeditions_paused
			}
		}
		ai_will_do = {
			factor = 0
		}
	}
"""

decision_toggle_always_fight = """\
	MEC_Expeditions_Decision_toggle_always_fight = {
		potential = {
			has_country_flag = MEC_Expeditions_Show_Decisions
		}
		allow = {
		    ai = no
		}
		effect = {
			if = {
				limit = {
					has_country_flag = MEC_Expeditions_always_fight
				}
				custom_tooltip = MEC_Expeditions_Decision_toggle_always_fight_no
				clr_country_flag = MEC_Expeditions_always_fight
			}
			else = {
				custom_tooltip = MEC_Expeditions_Decision_toggle_always_fight_yes
				set_country_flag = MEC_Expeditions_always_fight
			}
		}
		ai_will_do = {
			factor = 0
		}
	}
"""

# Has variables: event_num
select_expedition_frame_top = """\
country_event = {{
	id = MEC_Expeditions.{event_num}
	title = MEC_Expeditions.{event_num}.name
	desc = MEC_Expeditions.{event_num}.desc
	picture = TRADEGOODS_eventPicture
	is_triggered_only = yes
	
"""

# Has variables: event_num, expedition_name
select_expedition_option_repeat_frame_top = """\
	option = {{
		name = MEC_Expeditions.{event_num}.{expedition_name}_repeat
		#log = "MEC_Expeditions:[GetYear]:[Root.GetName]:selected expedition to:{expedition_name}:repeated"
		trigger = {{
			MEC_Expeditions_available_{expedition_name}_trigger = yes
			has_country_flag = MEC_Expeditions_sent_{expedition_name}
		}}
		ai_chance = {{
			factor = {ai_base_chance}
"""
# Has variables: event_num, expedition_name
select_expedition_option_regular_frame_top = """\
	option = {{
		name = MEC_Expeditions.{event_num}.{expedition_name}
		#log = "MEC_Expeditions:[GetYear]:[Root.GetName]:selected expedition to:{expedition_name}"
		trigger = {{
			MEC_Expeditions_available_{expedition_name}_trigger = yes
			NOT = {{ has_country_flag = MEC_Expeditions_sent_{expedition_name} }}
		}}
		ai_chance = {{
			factor = {ai_base_chance}
"""
# Has variables: expedition_name
select_expedition_option_frame_bottom_jumping_node = """\
			modifier = {{ # Less likely to send expeditions to places you already have a province
				factor = 0.1
				num_of_provinces_owned_or_owned_by_non_sovereign_subjects_with = {{
					province_group = expedition_provs.{expedition_name}
					OR = {{
						has_province_modifier = trading_post_province
						has_province_flag = TN_Natural
						}}
					value = 1
				}}
			}}
"""
# Has variables: expedition_name
select_expedition_option_frame_bottom_colonial_node = """\
			modifier = {{ # More likely to send expeditions to places you already have a province
				factor = 5
				num_of_provinces_owned_or_owned_by_non_sovereign_subjects_with = {{
					value = 1
					province_group = expedition_provs.{expedition_name}
				}}
			}}
"""
# Has variables: expedition_name
select_expedition_option_frame_bottom_chinese_mainland = """\
			modifier = {{ # Stop AI from sending expeditions to mainlaind China if all of the coast is held by the Emperor. Meant to stop dragging relations to -200. harming trade and causing wars
				factor = 0
				expedition_provs.{expedition_name} = {{
					type = all 
					is_empty = no
					OR = {{
						owner = {{ is_emperor_of_china_meiou = yes }}
						owner = {{ overlord = {{ is_emperor_of_china_meiou = yes }} }}
						owner = {{ overlord = {{ overlord = {{ is_emperor_of_china_meiou = yes }} }} }}
					}}
				}}
			}}
			modifier = {{ # Less likely to send expeditions to places you already have a province
				factor = 0.1
				num_of_provinces_owned_or_owned_by_non_sovereign_subjects_with = {{
					province_group = expedition_provs.{expedition_name}
					OR = {{
						has_province_modifier = trading_post_province
						has_province_flag = TN_Natural
						}}
					value = 1
				}}
			}}
"""
# Has variables: expedition_name, event_num_arrival, event_num_total_failure, event_num_map_failure, event_num_trade_failure, expedition_duration, ai_base_chance, clr_all_sent_flags
select_expedition_option_frame_TN_link_check_top = """\
			modifier = { # Less likely to send expeditions to places you have no trade node connection with
				factor = 0 
				NOT = {is_year = 1650}
"""
select_expedition_option_frame_TN_link_check_inside = """\
				NOT = {{
					num_of_provinces_owned_or_owned_by_non_sovereign_subjects_with = {{
						value = 1
                        OR = {{
                            province_group = tradenode_mult_{TN}
                            province_group = tradenode_{TN}
                        }}
					}}
				}}
"""

select_expedition_option_claim_frame = """\
			modifier = {{ # Stop AI from sending expeditions to colonial regions already populated by another colonisers
				factor = 0.02
				calc_true_if = {{
					all_province = {{
						province_group=expedition_provs.{expedition_name}
						NOT = {{country_or_non_sovereign_subject_holds = ROOT}}
						owner = {{
							OR = {{
								is_colonial_nation = yes
								is_former_colonial_nation = yes
								has_idea = exploration_ideas_1
							}}
						}}
					}}
					amount = 2
				}}
				NOT={{
					num_of_provinces_owned_or_owned_by_non_sovereign_subjects_with = {{
						value = 2
						province_group = expedition_provs.{expedition_name}
					}}
				}}
			}}
"""

# Has variables: expedition_name, event_num_arrival, event_num_total_failure, event_num_map_failure, event_num_trade_failure, expedition_duration, ai_base_chance, clr_all_sent_flags
select_expedition_option_frame_bottom = """\
			modifier = {{ # Far less likely to send expeditions to places you failed a takeover attempt at
				factor = 0.1
				has_country_modifier = MEC_Modifier_Expedition_Failed_{expedition_name}
			}}
			modifier = {{ # Stop AI from loosing expeditions of provinces owned by comparable nations
				factor = 0.05
				expedition_provs.{expedition_name} = {{
					type = all 
					is_empty = no
					owner = {{ check_key = {{ lhs = tech_mil which = ROOT }} }}
				}}
			}}
		}}
		hidden_effect = {{
			add_country_modifier = {{
				name = MEC_Modifier_Expedition_{expedition_name}
				duration = {expedition_duration}
			}}
{clr_all_sent_flags}
			set_country_flag = MEC_Expeditions_sent_{expedition_name}
		}}
		if = {{
			limit = {{
				has_idea = colonialism_ideas_1
			}}
			random_list = {{
				80 = {{
					country_event = {{
						id = MEC_Expeditions.{event_num_arrival}
						days = {expedition_duration} random = 50
					}}
				}}
				10 = {{
					country_event = {{
						id = MEC_Expeditions.{event_num_trade_failure}
						days = {expedition_duration} random = 50
					}}
				}}
				5 = {{
					country_event = {{
						id = MEC_Expeditions.{event_num_map_failure}
						days = {expedition_duration} random = 50
					}}
				}}
				5 = {{
					country_event = {{
						id = MEC_Expeditions.{event_num_total_failure}
						days = {expedition_duration} random = 50
					}}
				}}
			}}
		}}
		else = {{
			random_list = {{
				40 = {{
					country_event = {{
						id = MEC_Expeditions.{event_num_arrival}
						days = {expedition_duration} random = 50
					}}
				}}
				15 = {{
					country_event = {{
						id = MEC_Expeditions.{event_num_trade_failure}
						days = {expedition_duration} random = 50
					}}
				}}
				15 = {{
					country_event = {{
						id = MEC_Expeditions.{event_num_map_failure}
						days = {expedition_duration} random = 50
					}}
				}}
				30 = {{
					country_event = {{
						id = MEC_Expeditions.{event_num_total_failure}
						days = {expedition_duration} random = 50
					}}
				}}
			}}
		}}
		expedition_provs.{expedition_name} = {{
			clr_province_flag = MEC_Expeditions_owned_by_sender_or_subjects
		}}
	}}
"""

# Has variables: event_num, event_num_landing, expedition_name, event_num_total_failure
expedition_arrival_frame = """\
country_event = {{
	id = MEC_Expeditions.{event_num}
	title = MEC_Expeditions.{event_num}.title
	desc = MEC_Expeditions.{event_num}.desc
	picture = TRADEGOODS_eventPicture
	is_triggered_only = yes
	hidden = yes
	
	option = {{
		name = MEC_Expeditions.arrival
		if = {{ # Have to check again in case of change while expedition was in progress
			limit = {{ 
				expedition_provs.{expedition_name} = {{
					MEC_Expeditions_eligible_province_trigger = yes
				}}
			}}
			set_key = {{ # Counter for loop
				lhs = Tmp_7
				value = 20
			}}
			set_key = {{ # High initial value to guarantee first province will be lower
				lhs = Tmp_8
				value = 1000
			}}
			while = {{
				limit = {{ # Exit loop when counter is below 1
					check_key = {{
						lhs = Tmp_7
						value = 1
					}}
				}}
			    if = {{ # if best value is negative (aka empty with feature)
			        limit = {{
			            NOT = {{
                            check_key = {{
                                lhs = Tmp_8
                                value = 0
                            }}
                        }}
			        }}
			        # Multiply best value by 5 and then add (it's negative) to loop counter
			        set_key = {{
			            lhs = Tmp_6
			            which = Tmp_8
			        }}
			        multiply_key = {{ 
			            lhs = Tmp_6
			            value = 5
			        }}
			        change_key = {{ 
			            lhs = Tmp_7
			            which = Tmp_6
			        }}
			    }}
			    else = {{
                    subtract_key = {{ # Reduce loop counter
                        lhs = Tmp_7
                        value = 1
                    }}
				}}
				random_province = {{  # In province group, not owned by sender or their subjects, and doesn't have truce with owner
					limit = {{ 
						province_group = expedition_provs.{expedition_name}
						MEC_Expeditions_eligible_province_trigger = yes
					}}
					MEC_Expeditions_defence_calc_effect = yes # Sets Tmp 0-4, 9
                    set_key = {{ # Copy current best number from country into this scope
                        lhs = Tmp_8
                        which = ROOT
                    }}
                    if = {{ # If the current province number is better target (lower number) then set it as the new target
                        limit = {{ # 8 < 2
                            NOT = {{ 
                                check_key = {{ 
                                    lhs = Tmp_9
                                    which = Tmp_8
                                }}
                            }}
                        }}
                        save_event_target_as = MEC_Expedition_Target_Province
                        set_key = {{ # Overwrite the number in this scope
                            lhs = Tmp_8
                            which = Tmp_9
                        }}
                        ROOT = {{ # Copy the overwrite to the country scope
                            set_key = {{
                                lhs = Tmp_8
                                which = PREV
                            }}
                        }}
					}}
				}}
			}} 
			event_target:MEC_Expedition_Target_Province = {{ # Call the landing event on the province that was found to be best
			    if = {{ # If player has selected to always fight, skip landing event
			        limit = {{
			            is_empty = no
			            owner = {{
			                has_country_flag = MEC_Expeditions_always_fight
			            }}
			        }}
			        export_to_key = {{ # Expedition sender mil tech
                        lhs = MEC_Expeditions_Comparison
                        value = mil_tech
                        who = FROM
                    }}
                    MEC_Expeditions_defence_calc_effect = yes # Sets Tmp 0-4, 9
                    subtract_key = {{
                        lhs = MEC_Expeditions_Comparison
                        which = Tmp_9
                    }}
		            {landing_success}  
			    }}
			    else = {{
                    province_event = {{ # Call landing event
                        id = MEC_Expeditions.{event_num_landing}
                        days = 0
                    }}
				}}
			}}
		}} 
		else = {{
			country_event = {{ # Call failure event
				id = MEC_Expeditions.{event_num_total_failure}
				days = 0
			}}
		}}
		expedition_provs.{expedition_name} = {{
			clr_province_flag = MEC_Expeditions_owned_by_sender_or_subjects
		}}
	}}
}}
"""

# Tmp key values set by this effect 0: Harbour level or current owner mil tech, 1: Feature level or doubled fort level, 2: colony, 3: manpower, 4: prov size, 9: total
province_defence_calculation = """\
MEC_Expeditions_defence_calc_effect = {
    if = { # If uncolonized province
        limit = {
            is_empty = yes
        }
        set_key = {
            lhs = Tmp_0
            value = 0
        }
        set_key = {
            lhs = Tmp_1
            value = 0
        }
        # Set Tmp_0 based on level of harbour
        if = {
            limit = {
                has_province_flag = TN_Harbour_Major
            }
            change_key = {
                lhs = Tmp_0
                value = -5
            }
        }
        if = {
            limit = {
                has_province_flag = TN_Harbour_Important
            }
            change_key = {
                lhs = Tmp_0
                value = -3
            }
        }
        if = {
            limit = {
                has_province_flag = TN_Harbour_Minor
            }
            change_key = {
                lhs = Tmp_0
                value = -1
            }
        }
        # Set Tmp_1 based on level of natural feature
        if = {
            limit = {
                has_province_flag = TN_Natural_Major
            }
            change_key = {
                lhs = Tmp_1
                value = -3
            }
        }
        if = {
            limit = {
                has_province_flag = TN_Natural_Important
            }
            change_key = {
                lhs = Tmp_1
                value = -2
            }
        }
        if = {
            limit = {
                has_province_flag = TN_Natural_Minor
            }
            change_key = {
                lhs = Tmp_1
                value = -1
            }
        }
        # Modify Tmp_1 based on adjacency of friendly province
        if = {
            limit = {
                any_neighbor_province = {
                    country_or_subject_holds = ROOT
                }
            }
            change_key = {
                lhs = Tmp_1
                value = -1
            }
        }
        # Total values from harbours and natural features
        set_key = {
            lhs = Tmp_9
            which = Tmp_0
        }
        change_key = {
            lhs = Tmp_9
            which = Tmp_1
        }
    }
    else = {
        export_to_key = { # Current owner mil tech
            lhs = Tmp_0
            value = mil_tech
            who = owner
        }
        export_to_key = { # Get defender fort level
            lhs = Tmp_1
            value = trigger_value:fort_level
        }
        multiply_key = { # Double fort bonus
            lhs = Tmp_1
            value = 2
        }
        set_key = {
            lhs = Tmp_2
            value = 0
        }
        if = {
            limit = { # Bonus against incomplete colonies
                is_colony = yes
            }
            change_key = {
                lhs = Tmp_2
                value = -5
            }
        }
        # Sum manpower in province
        set_key = {
            lhs = Tmp_3
            value = 0
        }
        change_key = {
            lhs = Tmp_3
            which = Tax_MP
        }
        change_key = {
            lhs = Tmp_3
            which = Tax_NOMP
        }
        change_key = {
            lhs = Tmp_3
            which = Tax_BGMP
        }
        change_key = {
            lhs = Tmp_3
            which = Tax_TRMP
        }
        if = { # If manpower sum > 10 set 5 elif > 7 set 4 elif > 4 set 2 elif > 2 set 1
            limit = {
                check_key = {
                    lhs = Tmp_3
                    value = 10
                }
            }
            set_key = {
                lhs = Tmp_3
                value = 5
            }
        }
        else_if = {
            limit = {
                check_key = {
                    lhs = Tmp_3
                    value = 7
                }
            }
            set_key = {
                lhs = Tmp_3
                value = 4
            }
        }
        else_if = {
            limit = {
                check_key = {
                    lhs = Tmp_3
                    value = 4
                }
            }
            set_key = {
                lhs = Tmp_3
                value = 2
            }
        }
        else_if = {
            limit = {
                check_key = {
                    lhs = Tmp_3
                    value = 2
                }
            }
            set_key = {
                lhs = Tmp_3
                value = 1
            }
        }
        else = {
            set_key = {
                lhs = Tmp_3
                value = 0
            }
        }
        set_key = {
            lhs = Tmp_4
            value = 0
        }
        if = { # If Land Province Size > 700 set 5 elif > 400 set 3 elif >250 set 2 elif > 100 set 1
            limit = {
                check_key = {
                    lhs = Land_Size
                    value = 700
                }
            }
            set_key = {
                lhs = Tmp_4
                value = 5
            }
        }
        else_if = {
            limit = {
                check_key = {
                    lhs = Land_Size
                    value = 400
                }
            }
            set_key = {
                lhs = Tmp_4
                value = 3
            }
        }
        else_if = {
            limit = {
                check_key = {
                    lhs = Land_Size
                    value = 250
                }
            }
            set_key = {
                lhs = Tmp_4
                value = 2
            }
        }
        else_if = {
            limit = {
                check_key = {
                    lhs = Land_Size
                    value = 100
                }
            }
            set_key = {
                lhs = Tmp_4
                value = 1
            }
        }
        # Sum all values into Tmp_9 for total defence value
        set_key = {
            lhs = Tmp_9
            value = 0
        }
        change_key = {
            lhs = Tmp_9
            which = Tmp_0
        }
        change_key = {
            lhs = Tmp_9
            which = Tmp_1
        }
        change_key = {
            lhs = Tmp_9
            which = Tmp_2
        }
        change_key = {
            lhs = Tmp_9
            which = Tmp_3
        }
        change_key = {
            lhs = Tmp_9
            which = Tmp_4
        }
	}
}
"""

# Uses MEC_Expeditions_Comparison to decide whether to call success or failure event
# Has variables: event_num_success, event_num_total_failure, expedition_name, event_num_no_attack_failure
landing_success = """\
if = {{ # Use MEC_Expeditions_Comparison as success chance
    limit = {{
        check_key = {{
            lhs = MEC_Expeditions_Comparison
            value = 10
        }}
    }}
    FROM = {{ # 100%
        country_event = {{ # Success
            id = MEC_Expeditions.{event_num_success}
            days = 0
        }}
    }} 
}}
else_if = {{
    limit = {{
        check_key = {{
            lhs = MEC_Expeditions_Comparison
            value = 9
        }}
    }}
    random_list = {{
        90 = {{
            FROM = {{
                country_event = {{ # Success
                    id = MEC_Expeditions.{event_num_success}
                    days = 0
                }}
            }} 
        }}
        10 = {{
            FROM = {{
                country_event = {{ # Failure
                    id = MEC_Expeditions.{event_num_total_failure}
                    days = 0
                }}
                hidden_effect = {{
                    add_country_modifier = {{
                        name = MEC_Modifier_Expedition_Failed_{expedition_name}
                        duration = 7300 # 20 years
                        hidden = yes
                    }}
                }}
            }}
        }}
    }}
}}
else_if = {{
    limit = {{
        check_key = {{
            lhs = MEC_Expeditions_Comparison
            value = 8
        }}
    }}
    random_list = {{
        80 = {{
            FROM = {{
                country_event = {{ # Success
                    id = MEC_Expeditions.{event_num_success}
                    days = 0
                }}
            }} 
        }}
        20 = {{
            FROM = {{
                country_event = {{ # Failure
                    id = MEC_Expeditions.{event_num_total_failure}
                    days = 0
                }}
                hidden_effect = {{
                    add_country_modifier = {{
                        name = MEC_Modifier_Expedition_Failed_{expedition_name}
                        duration = 3650
                        hidden = yes
                    }}
                }}
            }}
        }}
    }}
}}
else_if = {{
    limit = {{
        check_key = {{
            lhs = MEC_Expeditions_Comparison
            value = 7
        }}
    }}
    random_list = {{
        70 = {{
            FROM = {{
                country_event = {{ # Success
                    id = MEC_Expeditions.{event_num_success}
                    days = 0
                }}
            }} 
        }}
        30 = {{
            FROM = {{
                country_event = {{ # Failure
                    id = MEC_Expeditions.{event_num_total_failure}
                    days = 0
                }}
                hidden_effect = {{
                    add_country_modifier = {{
                        name = MEC_Modifier_Expedition_Failed_{expedition_name}
                        duration = 3650
                        hidden = yes
                    }}
                }}
            }}
        }}
    }}
}}
else_if = {{
    limit = {{
        check_key = {{
            lhs = MEC_Expeditions_Comparison
            value = 6
        }}
    }}
    random_list = {{
        60 = {{
            FROM = {{
                country_event = {{ # Success
                    id = MEC_Expeditions.{event_num_success}
                    days = 0
                }}
            }} 
        }}
        40 = {{
            FROM = {{
                country_event = {{ # Failure
                    id = MEC_Expeditions.{event_num_total_failure}
                    days = 0
                }}
                hidden_effect = {{
                    add_country_modifier = {{
                        name = MEC_Modifier_Expedition_Failed_{expedition_name}
                        duration = 3650
                        hidden = yes
                    }}
                }}
            }}
        }}
    }}
}}
else_if = {{
    limit = {{
        check_key = {{
            lhs = MEC_Expeditions_Comparison
            value = 5
        }}
    }}
    random_list = {{
        50 = {{
            FROM = {{
                country_event = {{ # Success
                    id = MEC_Expeditions.{event_num_success}
                    days = 0
                }}
            }} 
        }}
        50 = {{
            FROM = {{
                country_event = {{ # Failure
                    id = MEC_Expeditions.{event_num_total_failure}
                    days = 0
                }}
                hidden_effect = {{
                    add_country_modifier = {{
                        name = MEC_Modifier_Expedition_Failed_{expedition_name}
                        duration = 3650
                        hidden = yes
                    }}
                }}
            }}
        }}
    }}
}}
else_if = {{
    limit = {{
        check_key = {{
            lhs = MEC_Expeditions_Comparison
            value = 4
        }}
    }}
    random_list = {{
        40 = {{
            FROM = {{
                country_event = {{ # Success
                    id = MEC_Expeditions.{event_num_success}
                    days = 0
                }}
            }} 
        }}
        60 = {{
            FROM = {{
                country_event = {{ # Failure
                    id = MEC_Expeditions.{event_num_total_failure}
                    days = 0
                }}
                hidden_effect = {{
                    add_country_modifier = {{
                        name = MEC_Modifier_Expedition_Failed_{expedition_name}
                        duration = 3650
                        hidden = yes
                    }}
                }}
            }}
        }}
    }}
}}
else_if = {{
    limit = {{
        check_key = {{
            lhs = MEC_Expeditions_Comparison
            value = 3
        }}
    }}
    random_list = {{
        30 = {{
            FROM = {{
                country_event = {{ # Success
                    id = MEC_Expeditions.{event_num_success}
                    days = 0
                }}
            }} 
        }}
        70 = {{
            FROM = {{
                country_event = {{ # Failure
                    id = MEC_Expeditions.{event_num_total_failure}
                    days = 0
                }}
                hidden_effect = {{
                    add_country_modifier = {{
                        name = MEC_Modifier_Expedition_Failed_{expedition_name}
                        duration = 3650
                        hidden = yes
                    }}
                }}
            }}
        }}
    }}
}}
else = {{
    FROM = {{
        country_event = {{ # Failure
            id = MEC_Expeditions.{event_num_no_attack_failure}
            days = 0
        }}
        hidden_effect = {{
            add_country_modifier = {{
                name = MEC_Modifier_Expedition_Failed_{expedition_name}
                duration = 3650
                hidden = yes
            }}
        }}
    }}
}}
"""

# Has variables: event_num, event_num_success, expedition_name
expedition_landing_frame = """\
province_event = {{ # Called on province being colonized
	id = MEC_Expeditions.{event_num}
	title = MEC_Expeditions.{event_num}.title
	desc = MEC_Expeditions.{event_num}.desc
	picture = TRADEGOODS_eventPicture
	is_triggered_only = yes
	
	immediate = {{
		hidden_effect = {{
			if = {{
				limit = {{
					is_empty = no
				}} # Note if make changes here also have to make changes to the similar section in the previous event
				export_to_key = {{ # Expedition sender mil tech
					lhs = MEC_Expeditions_Comparison
					value = mil_tech
					who = FROM
				}}
				MEC_Expeditions_defence_calc_effect = yes # Sets Tmp 0-4, 9
				subtract_key = {{
					lhs = MEC_Expeditions_Comparison
					which = Tmp_9
				}}
				# Cap value between 0-10 for display purpose
                if = {{ # if >= 10 set to 10
                    limit = {{
                        check_key = {{
                            lhs = MEC_Expeditions_Comparison
                            value = 10
                        }}
                    }}
                    set_key = {{
                        lhs = MEC_Expeditions_Comparison
                        value = 10
                    }}
                }}
                else_if = {{ # if < 0 set to 0
                    limit = {{
                        NOT = {{
                            check_key = {{
                                lhs = MEC_Expeditions_Comparison
                                value = 0
                            }}
                        }}
                    }}
                    set_key = {{
                        lhs = MEC_Expeditions_Comparison
                        value = 0
                    }}
                }}
			}}
		}}
	}}

	option = {{
		name = MEC_Expeditions.colony
		trigger = {{
			is_empty = yes
		}}
		FROM = {{
			country_event = {{ 
				id = MEC_Expeditions.{event_num_success}
				days = 0
			}}
		}} 
	}}
	option = {{
		name = MEC_Expeditions.reject_trade_fort
		trigger = {{
			is_empty = no
		}}
		ai_chance = {{ # Higher ai chance when more likely to fight off colonizers
			factor = 1
			modifier = {{
				factor = 2
				check_key = {{
					lhs = MEC_Expeditions_Comparison
					value = 6
				}}
			}}
			modifier = {{
				factor = 4
				check_key = {{
					lhs = MEC_Expeditions_Comparison
					value = 5
				}}
			}}
			modifier = {{
				factor = 6
				check_key = {{
					lhs = MEC_Expeditions_Comparison
					value = 4
				}}
			}}
			modifier = {{
				factor = 10
				check_key = {{
					lhs = MEC_Expeditions_Comparison
					value = 3
				}}
			}}
			modifier = {{
				factor = 16
				check_key = {{
					lhs = MEC_Expeditions_Comparison
					value = 2
				}}
			}}
			modifier = {{
				factor = 20
				check_key = {{
					lhs = MEC_Expeditions_Comparison
					value = 1
				}}
			}}
			modifier = {{
				factor = 100
				NOT = {{
					check_key = {{
						lhs = MEC_Expeditions_Comparison
						value = 1
					}}
				}}
			}}
		}}
		{landing_success}
	}}
	option = {{
		name = MEC_Expeditions.always_reject_trade_fort
		trigger = {{
			is_empty = no
		}}
		ai_chance = {{
		    factor = 0
		}}
		owner = {{
		    set_country_flag = MEC_Expeditions_always_fight
		}}
        {landing_success}
	}}
	option = {{
		name = MEC_Expeditions.accept_trade_fort
		trigger = {{
			is_empty = no
		}}
		ai_chance = {{ # Higher ai chance when less likely to fight off colonizers
			factor = 1
			modifier = {{
				factor = 9
				check_key = {{
					lhs = MEC_Expeditions_Comparison
					value = 9
				}}
			}}
			modifier = {{
				factor = 4
				check_key = {{
					lhs = MEC_Expeditions_Comparison
					value = 8
				}}
			}}
			modifier = {{
				factor = 2
				check_key = {{
					lhs = MEC_Expeditions_Comparison
					value = 7
				}}
			}}
		}}
		owner = {{
			add_treasury = 100
			add_truce_with = FROM
		}}
		FROM = {{
			country_event = {{ 
				id = MEC_Expeditions.{event_num_success}
				days = 0
			}}
		}}
	}}
}}
"""

# Has variables: event_num, expedition_name
expedition_success_frame = """\
country_event = {{
	id = MEC_Expeditions.{event_num}
	title = MEC_Expeditions.{event_num}.title
	desc = MEC_Expeditions.{event_num}.desc
	picture = TRADEGOODS_eventPicture
	is_triggered_only = yes
	
	immediate = {{
		hidden_effect = {{
			expedition_provs.{expedition_name}_vision = {{ # Note this can cause crashes if the prov group has invalid province numbers
				discover_country = ROOT
			}}
			event_target:MEC_Expedition_Target_Province = {{ # FROM is the province, ROOT is the expedition sender
				if = {{ # if it is a colony then they get a claim on the province they're losing
					limit = {{ # Non-colonies will have cores so don't need anything added
						is_colony = yes
					}}
					add_claim = owner
				}}
				add_territorial_core = ROOT 
				
				if = {{ # Change religion and culture if empty province not in trade company or in trade company with no population
					limit = {{
						is_empty = yes
						has_province_flag = ColonyBecomesOwner
					}} 
					change_religion = ROOT # Re-evaluate and probably change after religion rework is complete
					change_culture = ROOT
					ROOT = {{
						capital_scope = {{
							event_target:MEC_Expedition_Target_Province = {{ set_key = {{ lhs = Plague_Resistance1 which = PREV }} }}
							event_target:MEC_Expedition_Target_Province = {{ set_key = {{ lhs = Plague_Resistance2 which = PREV }} }}
							event_target:MEC_Expedition_Target_Province = {{ set_key = {{ lhs = Plague_Resistance4 which = PREV }} }}
						    
						    event_target:MEC_Expedition_Target_Province = {{ divide_key = {{ lhs = Plague_Resistance1 value = 3 }} }}
						    event_target:MEC_Expedition_Target_Province = {{ divide_key = {{ lhs = Plague_Resistance2 value = 3 }} }}
						    event_target:MEC_Expedition_Target_Province = {{ divide_key = {{ lhs = Plague_Resistance4 value = 3 }} }}
						}}
						
                        if = {{
                            limit = {{
                                any_owned_province = {{
                                    check_key = {{ lhs = Plague_SpawnChance4 value = 0.1 }}
                                }}
                            }}                        
                            event_target:MEC_Expedition_Target_Province = {{
                                if = {{
                                    limit = {{
                                        has_province_flag = possible_malaria
                                    }}
                                    America_Malaria_Calculator = yes
                                }}
                                every_neighbor_province = {{
                                    limit = {{
                                        has_province_flag = possible_malaria
                                    }}
                                    America_Malaria_Calculator = yes
                                }}
                            }}
                        }}
                    }}
                }}
                # System for 'waking' up smallpox in America. 
                random_list = {{ 
                    1 = {{
                        event_target:MEC_Expedition_Target_Province = {{
                            if = {{
                                limit = {{
                                    continent = north_america                                                                 
                                }}
                                if = {{
                                    limit = {{
                                        has_global_flag = not_namerica_smallpox
                                        superregion = east_america_superregion
                                    }}
                                    every_neighbor_province = {{
                                        limit = {{
                                            NOT = {{
                                                check_key = {{ lhs = Plague_SpawnChance2 value = 0.1 }}
                                                check_key = {{ lhs = Plague_Resistance2 value = 0.1 }}
                                            }}
                                            owner = {{
                                                OR = {{
                                                    technology_group = andean
                                                    technology_group = mesoamerican
                                                    technology_group = south_american
                                                    technology_group = high_american
                                                }}
                                            }}
                                        }}
                                        #log = "MEC_Expeditions:[GetYear]:North America Smallpox Triggered from Expedition"
                                        province_event = {{ id = Plague_Spawner.221 days = 2555 random = 365 }}
                                    }}
                                }}
                                else_if = {{
                                    limit = {{
                                        has_global_flag = not_camerica_smallpox
                                        superregion = central_america_superregion
                                    }}
                                    every_neighbor_province = {{
                                        limit = {{
                                            NOT = {{
                                                check_key = {{ lhs = Plague_SpawnChance2 value = 0.1 }}
                                                check_key = {{ lhs = Plague_Resistance2 value = 0.1 }}
                                            }}
                                            owner = {{
                                                OR = {{
                                                    technology_group = andean
                                                    technology_group = mesoamerican
                                                    technology_group = south_american
                                                    technology_group = high_american
                                                }}
                                            }}
                                        }}
                                        #log = "MEC_Expeditions:[GetYear]:Central America Smallpox Triggered from Expedition"
                                        province_event = {{ id = Plague_Spawner.222 days = 2555 random = 365 }}
                                    }}
                                }}
                            }}
                            else_if = {{
                                limit = {{
                                    continent = south_america
                                    has_global_flag = not_samerica_smallpox
                                }}
                                every_neighbor_province = {{
                                    limit = {{
                                        NOT = {{
                                            check_key = {{ lhs = Plague_SpawnChance2 value = 0.1 }}
                                            check_key = {{ lhs = Plague_Resistance2 value = 0.1 }}
                                        }}
                                        owner = {{
                                            OR = {{
                                                technology_group = andean
                                                technology_group = mesoamerican
                                                technology_group = south_american
                                                technology_group = high_american
                                            }}
                                        }}
                                    }}
                                    #log = "MEC_Expeditions:[GetYear]:South America Smallpox Triggered from Expedition"
                                    province_event = {{ id = Plague_Spawner.2 days = 2555 random = 365 }}
                                }}
                            }}
                        }}
                    }}                      
                    2 = {{ 
                    }}
                }}                  
				if = {{ # If not empty add negative opinion for owner against expedition sender
					limit = {{
						is_empty = no
					}}
					#log = "MEC_Expeditions:[GetYear]:[Root.GetName]:received negative opinion modifier from::[MEC_Expedition_Target_Province.Owner.GetName]"
					owner = {{
						add_opinion = {{
							who = ROOT
							modifier = MEC_Expeditions_taken_province
						}}
					}}
				}}
				cede_province = ROOT
				if = {{ # if it is a colony then instantly finish it
					limit = {{
						is_colony = yes
					}}
					add_colonysize = 1000
				}}
			}}
		}}
	}}
	
"""
# Has variables: expedition_name
expedition_success_confirmation_MAM_event_15 = """\
	option = {{
		name = MEC_Expeditions.expedition_success
        goto = MEC_Expedition_Target_Province
		#log = "MEC_Expeditions:[GetYear]:[Root.GetName]:successful expedition to:{expedition_name}:[MEC_Expedition_Target_Province.GetName]"
		add_prestige = 3
		hidden_effect = {{ MAM = {{ country_event = {{ id = flavor_mam.15 days = 1 }} }} }}
	}}
}}
"""

# Has variables: expedition_name
expedition_success_confirmation = """\
	option = {{
		name = MEC_Expeditions.expedition_success
		goto = MEC_Expedition_Target_Province
		#log = "MEC_Expeditions:[GetYear]:[Root.GetName]:successful expedition to:{expedition_name}:[MEC_Expedition_Target_Province.GetName]"
		add_prestige = 3
	}}
}}
"""

# Has variables: event_num, expedition_name
expedition_total_failure_frame = """\
country_event = {{
	id = MEC_Expeditions.{event_num}
	title = MEC_Expeditions.{event_num}.title
	desc = MEC_Expeditions.{event_num}.desc
	picture = TRADEGOODS_eventPicture
	is_triggered_only = yes

	option = {{
		name = MEC_Expeditions.total_failure
		#log = "MEC_Expeditions:[GetYear]:[Root.GetName]:expedition totally failed:{expedition_name}"
		ai_chance = {{
			factor = 1
		}}
		add_prestige = -3
	}}
}}
"""

# Has variables: event_num, expedition_name
expedition_map_failure_frame = """\
country_event = {{
	id = MEC_Expeditions.{event_num}
	title = MEC_Expeditions.{event_num}.title
	desc = MEC_Expeditions.{event_num}.desc
	picture = TRADEGOODS_eventPicture
	is_triggered_only = yes

	option = {{
		name = MEC_Expeditions.map_failure
		#log = "MEC_Expeditions:[GetYear]:[Root.GetName]:expedition map failed:{expedition_name}"
		ai_chance = {{
			factor = 1
		}}
		add_prestige = -1
		hidden_effect = {{
			expedition_provs.{expedition_name}_vision = {{ # Note this can cause crashes if the prov group has invalid province numbers
				discover_country = ROOT
			}}
		}}
	}}
}}
"""

# Has variables: event_num, expedition_name
expedition_trade_failure_frame = """\
country_event = {{
	id = MEC_Expeditions.{event_num}
	title = MEC_Expeditions.{event_num}.title
	desc = MEC_Expeditions.{event_num}.desc
	picture = TRADEGOODS_eventPicture
	is_triggered_only = yes

	option = {{
		name = MEC_Expeditions.trade_failure
		#log = "MEC_Expeditions:[GetYear]:[Root.GetName]:expedition trade failed:{expedition_name}"
		ai_chance = {{
			factor = 1
		}}
		add_treasury = 20
		hidden_effect = {{
			expedition_provs.{expedition_name}_vision = {{ # Note this can cause crashes if the prov group has invalid province numbers
				discover_country = ROOT
			}}
		}}
	}}
}}
"""

# Has variables: event_num, expedition_name
expedition_no_attack_failure_frame = """\
country_event = {{
	id = MEC_Expeditions.{event_num}
	title = MEC_Expeditions.{event_num}.title
	desc = MEC_Expeditions.{event_num}.desc
	picture = TRADEGOODS_eventPicture
	is_triggered_only = yes

	option = {{
		name = MEC_Expeditions.no_attack_failure
		#log = "MEC_Expeditions:[GetYear]:[Root.GetName]:expedition no attack failed:{expedition_name}"
		ai_chance = {{
			factor = 1
		}}
		add_prestige = -1
		hidden_effect = {{
			expedition_provs.{expedition_name}_vision = {{ # Note this can cause crashes if the prov group has invalid province numbers
				discover_country = ROOT
			}}
		}}
	}}
}}
"""

# Has variables: event_num, expedition_name, more_info_event_num
expedition_decision_events_frame = """\
country_event = {{
	id = MEC_Expeditions.{event_num}
	title = MEC_Expeditions.{event_num}.title
	desc = MEC_Expeditions.{event_num}.desc
	picture = TRADEGOODS_eventPicture
	is_triggered_only = yes
	
	immediate = {{
		hidden_effect = {{
			expedition_provs.{expedition_name} = {{
				MEC_Expeditions_defence_calc_effect = yes
			}}
		}}
	}}
	
	option = {{
		name = MEC_Expeditions.more_info
		highlight = yes
		set_country_flag = MEC_Expeditions_decision_event_{event_num}
		country_event = {{
			id = MEC_Expeditions.{more_info_event_num}
		}}
		ai_chance = {{
			factor = 0
		}}
	}}
	option = {{
		name = MEC_Expeditions.report
		#log = "MEC_Expeditions:[GetYear]:[Root.GetName]:picked decision event for:{expedition_name}:If that is an AI it is a bug."		
		ai_chance = {{
			factor = 1
		}}
	}}
}}
"""

# Has variables: event_num
expedition_decision_info_event_frame_top = """\
country_event = {{
	id = MEC_Expeditions.{event_num}
	title = MEC_Expeditions.{event_num}.title
	desc = MEC_Expeditions.{event_num}.desc
	picture = TRADEGOODS_eventPicture
	is_triggered_only = yes

	option = {{
		name = MEC_Expeditions.back
		ai_chance = {{
			factor = 1
		}}
"""

expedition_decision_info_event_frame_bottom = """\
	}
	option = {
		name = MEC_Expeditions.close
		ai_chance = {
			factor = 1
		}
"""

python_generated_file_warning = """\
############################################################################################################
###############################       DO NOT MANUALLY EDIT THIS FILE    ####################################
############################################################################################################

############################################################################################################
##################  THIS FILE GENERATED BY PYTHON SCRIPT MEC_Expeditions_Writer.py  ########################
############################################################################################################
"""

# Get the province ids from the province groups
provincegroups = Path('map/provincegroup.txt').read_text(encoding='cp1252')
no_comments_pgs = re.sub('#.*', '', provincegroups)  # Get rid of comments
split_pgs = re.split(r'\n\s*expedition_provs.', no_comments_pgs)[1:]  # Split on the expedition province groups

for pg in split_pgs:
    name = re.findall(r'^(.*?)(?:[\s*=#])', pg)[0]  # Get the expedition name
    pg = re.sub(r'.*\{', '', re.sub(r'}.*', '', pg, flags=re.DOTALL), flags=re.DOTALL)  # Get string between brackets
    ids = re.findall(r'\d+', pg, flags=re.DOTALL)  # Pull out the province ids and put in list

    ids = [int(i) for i in ids]  # Convert strings to ints
    for id in ids:
        assert 0 <= id <= 10000, "Must be valid province id"
    assert len(set(ids)) == len(ids), f"Shouldn't have duplicate ids in {name}"

    for expedition in expeditions_list:
        if name == expedition.name:
            assert len(expedition.target_provinces) == 0, "Should only be added once"
            expedition.target_provinces += ids

# Check expeditions have target provinces
for expedition in expeditions_list:
    assert len(expedition.target_provinces) != 0, "Every expedition should have some target provinces"

# Overwrite the modifier file
with open(Path('common/event_modifiers/MEC-Expeditions_modifiers.txt'), 'w', encoding='cp1252') as modifiers:
    modifiers.write(python_generated_file_warning + '\n')
    for expedition in expeditions_list:
        modifiers.write(f'\nMEC_Modifier_Expedition_{expedition.name} = {{\n}}\n')
        modifiers.write(f'\nMEC_Modifier_Expedition_Failed_{expedition.name} = {{\n}}\n')

# Overwrite the decision file
with open(Path('decisions/MEC-Expeditions_decisions.txt'), 'w', encoding='cp1252') as decisions:
    decisions.write(python_generated_file_warning + '\n')

    # Main decision that highlights all provinces and toggles other decisions
    decisions.write(decisions_frame_top)
    for expedition in expeditions_list:
        decisions.write(f'\t\t\t\tprovince_group = expedition_provs.{expedition.name}\n')
    decisions.write(decisions_frame_bottom)

    decisions.write(decision_toggle_expeditions)
    decisions.write(decision_toggle_always_fight)

    # Decisions for each expedition to highlight their provinces
    for index, expedition in enumerate(expeditions_list):
        decisions.write(f"\tMEC_Expeditions_Decision_{expedition.name} = {{\n\t\tpotential = {{\n\t\t\thas_country_flag = MEC_Expeditions_Show_Decisions\n\t\t}}\n")
        decisions.write(f"\t\tprovinces_to_highlight = {{\n\t\t\tprovince_group = expedition_provs.{expedition.name}\n\t\t}}\n")
        decisions.write("\t\tallow = {\n\t\t\talways = yes\n\t\t}\n")
        decisions.write(f"\t\teffect = {{\n\t\t\tcountry_event = {{\n\t\t\t\tid = MEC_Expeditions.{str(expedition_decision_events_start_number + index).zfill(3)}\n\t\t\t}}\n\t\t}}\n")
        decisions.write("\t\tai_will_do = {\n\t\t\tfactor = 0\n\t\t}\n\t}\n")

    decisions.write('}\n')

# Overwrite the scripted effects file
with open(Path('common/scripted_effects/MEC-Expeditions_effects.txt'), 'w', encoding='cp1252') as effects:
    effects.write(python_generated_file_warning + '\n')

    effects.write(province_defence_calculation + '\n')

# Overwrite the scripted triggers file
with open(Path('common/scripted_triggers/MEC-Expeditions_triggers.txt'), 'w', encoding='cp1252') as triggers:
    triggers.write(python_generated_file_warning + '\n')

    triggers.write("# Provinces are eligible expedition targets if neither you nor your subjects own them, and you don't have a truce or alliance with the owner.\n")
    triggers.write("MEC_Expeditions_eligible_province_trigger = {\n\tAND = {\n")
    triggers.write("\t\tNOT = {\n\t\t\tcountry_or_vassal_holds = ROOT\n\t\t}\n\t\tNOT = {\n\t\t\towner = {\n\t\t\t\tROOT = {\n\t\t\t\t\ttruce_with = PREV\n\t\t\t\t}\n\t\t\t}\n\t\t}\n\t\tNOT = {\n\t\t\towner = {\n\t\t\t\toverlord_of = ROOT\n\t\t\t}\n\t\t}\n")
    triggers.write("\t\tNOT = {\n\t\t\towner = {\n\t\t\t\tOR = {\n\t\t\t\t\talliance_with = ROOT\n\t\t\t\t\toverlord = {\n\t\t\t\t\t\talliance_with = ROOT\n\t\t\t\t\t}\n\t\t\t\t}\n\t\t\t}\n\t\t}\n\t}\n}\n\n")

    for expedition in expeditions_list:
        triggers.write(f"MEC_Expeditions_available_{expedition.name}_trigger = {{ # {expedition.localized_name} Expedition Availability Conditions\n\tAND = {{\n")
        triggers.write(f"\t\texpedition_provs.{expedition.name} = {{\n\t\t\tMEC_Expeditions_eligible_province_trigger = yes\n\t\t}}\n")
        triggers.write(f"\t\tOR = {{ # Dip tech requirements based on capital location in trade node\n")
        current_nodes = [False]
        for (node, tech) in sorted(expedition.node_tech_reqs, key=lambda x: x[1], reverse=True):
            if tech == current_nodes[0]:
                current_nodes.append(node)
            elif current_nodes[0] == False:  # First time through don't print
                current_nodes.clear()
                current_nodes.append(tech)
                current_nodes.append(node)
            else:
                triggers.write(f"\t\t\tAND = {{\n\t\t\t\tdip_tech = {current_nodes[0]}\n\t\t\t\tcapital_scope = {{\n\t\t\t\t\tOR = {{\n")
                for trade_node in current_nodes[1:]:
                    triggers.write(f"\t\t\t\t\t\tprovince_group = tradenode_{trade_nodes[trade_node]} # {trade_node}\n")
                current_nodes.clear()
                current_nodes.append(tech)
                current_nodes.append(node)
                triggers.write(f"\t\t\t\t\t}}\n\t\t\t\t}}\n\t\t\t}}\n")
        triggers.write(f"\t\t\tAND = {{\n\t\t\t\tdip_tech = {current_nodes[0]}\n\t\t\t\tcapital_scope = {{\n\t\t\t\t\tOR = {{\n")
        for trade_node in current_nodes[1:]:
            triggers.write(f"\t\t\t\t\t\tprovince_group = tradenode_{trade_nodes[trade_node]} # {trade_node}\n")
        triggers.write("\t\t\t\t\t}\n\t\t\t\t}\n\t\t\t}\n\t\t}\n\t}\n}\n\n")

# Overwrite the custom localization file
with open(Path('customizable_localization/MEC-Expeditions_customloc.txt'), 'w', encoding='cp1252') as custom_loc:
    custom_loc.write(python_generated_file_warning + '\n\n')
    custom_loc.write('defined_text = {\n\tname = MEC_Expeditions_Decision_tradenode\n\n')

    # Custom trigger for every trade node describing when you unlock expeditions
    for trade_node in expedition_unlocks:
        custom_loc.write(f'\ttext = {{\n\t\tlocalisation_key = MEC_Expeditions_Decision_{str(trade_node).replace(" ", "_")}\n')
        custom_loc.write("\t\ttrigger = {\n")
        custom_loc.write(f'\t\t\tcapital_scope = {{\n\t\t\t\tprovince_group = tradenode_{trade_nodes[trade_node]} # {trade_node}\n\t\t\t}}\n\t\t}}\n\t}}\n')
    custom_loc.write("}\n")

    # Custom loc for info events from decisions
    custom_loc.write('defined_text = {\n\tname = MEC_Expeditions_Decision_Event_Info\n\trandom = no\n\n')  # random = no makes it stop at first valid one
    custom_loc.write('\ttext = {\n\t\tlocalisation_key = MEC_Expeditions_Decision_Event_Info_undiscovered\n\t\ttrigger = {\n\t\t\tNOT = {\n\t\t\t\thas_discovered = FROM\n\t\t\t}\n\t\t}\n\t}\n')
    custom_loc.write('\ttext = {\n\t\tlocalisation_key = MEC_Expeditions_Decision_Event_Info_uncolonized\n\t\ttrigger = {\n\t\t\tis_empty = yes\n\t\t}\n\t}\n')
    custom_loc.write('\ttext = {\n\t\tlocalisation_key = MEC_Expeditions_Decision_Event_Info_colony\n\t\ttrigger = {\n\t\t\tis_colony = yes\n\t\t}\n\t}\n')
    custom_loc.write('\ttext = {\n\t\tlocalisation_key = MEC_Expeditions_Decision_Event_Info_owned\n\t\ttrigger = {\n\t\t\talways = yes\n\t\t}\n\t}\n')
    custom_loc.write("}\n")

# Overwrite the event file
with open(Path('events/MEC-Expeditions.txt'), 'w', encoding='cp1252') as events:
    with open(Path('localisation/MEC-Expeditions_l_english.yml'), 'w', encoding='utf-8-sig') as loc:
        loc.write("l_english:\n\n")
        loc.write(python_generated_file_warning + '\n')

        # Province groups localization
        loc.write(' # Province Group Localizations\n')
        for expedition in expeditions_list:
            loc.write(f' expedition_provs.{expedition.name}: "{expedition.localized_name} Expedition Target"\n')
            loc.write(f' expedition_provs.{expedition.name}_vision: "{expedition.localized_name} Expedition Gives Vision"\n')
        loc.write('\n')

        # Opinion modifier localization
        loc.write(' # Opinion Modifier\n')
        loc.write(' MEC_Expeditions_taken_province: "Took Province by Expedition"\n\n')

        # Write the decision localizations
        # Main decision localization
        loc.write(' # Expedition Decision\n')
        loc.write(' MEC_Expeditions_Decision_title: "Expeditions Unlock Tooltip & Decisions Toggle"\n')
        loc.write(' MEC_Expeditions_Decision_desc: "[Root.MEC_Expeditions_Decision_tradenode]"\n')
        loc.write(' MEC_Expeditions_Decision_Effect: "Toggle showing decisions for every expedition which allow province highlighting of only their provinces and tell when each trade node unlocks that expedition."\n')
        loc.write(' MEC_Expeditions_Decision_Highlight_All: "Click to highlight all provinces that are targeted by any expedition."\n')
        level_locations = {}  # Used for alphabetizing locations per level
        for trade_node in expedition_unlocks:
            loc.write(f' MEC_Expeditions_Decision_{str(trade_node).replace(" ", "_")}: "Based on our capital location in {trade_node} trade node, we will be able to send expeditions to these locations when we reach the corresponding §Ydiplomatic technology§! levels:')
            for (location, level) in expedition_unlocks[trade_node]:
                level_locations.setdefault(level, [])
                level_locations.get(level).append(location)
            for level in sorted(level_locations.keys()):
                loc.write(f'\\n§Y{level}§!: ' + ', '.join(sorted(level_locations.get(level))))
            level_locations.clear()
            loc.write('"\n')
        # Expedition specific decision localizations
        for expedition in expeditions_list:
            loc.write(f' MEC_Expeditions_Decision_{expedition.name}_title: "Expedition to {expedition.localized_name} Info"\n')
            loc.write(f' MEC_Expeditions_Decision_{expedition.name}_desc: "This expedition can be unlocked by countries with capitals in the following trade nodes at the corresponding §Ydiplomatic technology§! levels:')
            current_level = 0
            for (location, level) in expedition.node_tech_reqs:
                level_locations.setdefault(level, [])
                level_locations.get(level).append(location)
            for level in sorted(level_locations.keys()):
                loc.write(f'\\n§Y{level}§!: ' + ', '.join(sorted(level_locations.get(level))))
            level_locations.clear()
            loc.write('"\n')
        loc.write('\n')

        # Pause Expeditions Toggle Decision Localizations
        loc.write(' MEC_Expeditions_Decision_toggle_expeditions_title: "Expedition Events Toggle"\n')
        loc.write(' MEC_Expeditions_Decision_toggle_expeditions_desc: "Enable or disable your country getting the event for sending expeditions."\n')
        loc.write(' MEC_Expeditions_Decision_toggle_expeditions_stop: "Stop getting the event for sending expeditions."\n')
        loc.write(' MEC_Expeditions_Decision_toggle_expeditions_restart: "Restart getting the event for sending expeditions."\n')

        # Always Fight Expeditions Toggle Decision Localizations
        loc.write(' MEC_Expeditions_Decision_toggle_always_fight_title: "Expedition Landing Toggle"\n')
        loc.write(' MEC_Expeditions_Decision_toggle_always_fight_desc: "Set response to expeditions landing in your provinces."\n')
        loc.write(' MEC_Expeditions_Decision_toggle_always_fight_no: "Have a choice in responding to expeditions. Expedition landing event will show."\n')
        loc.write(' MEC_Expeditions_Decision_toggle_always_fight_yes: "Always fight off expeditions. Expedition landing event will be skipped."\n')

        # Write the modifier localizations
        loc.write("\n # Expedition Country Modifiers\n")
        for expedition in expeditions_list:
            loc.write(
                f' MEC_Modifier_Expedition_{expedition.name}: "Ongoing expedition to {expedition.localized_name}"\n')

        events.write("namespace = MEC_Expeditions\n\n")
        events.write(python_generated_file_warning + '\n\n')

        # Write the Neighboring Colonization event
        events.write(neighboring_colonization_event + '\n')
        loc.write('\n # Neighboring Colonization event\n')
        loc.write(' MEC_Expeditions.002.name: "Expansion into [neighbor_province.GetName]"\n')
        loc.write(' MEC_Expeditions.002.desc: "Some of our countrymen have long ventured into the uncolonized borderland of [neighbor_province.GetName]. Recently they made an organized effort to become permanently established there and properly integrate it into our country."\n')
        loc.write(' MEC_Expeditions.002.opt: "We shall now call it one of our provinces."\n')

        # Write the Select Expedition section header
        events.write(hash_line)
        events.write(
            "#####################################      Select Expedition       #########################################\n")
        events.write(hash_line + '\n')

        # Write the select expedition event
        # Loops through every expedition writing an option for it and localization
        events.write(select_expedition_frame_top.format(event_num=str(menu_event_number).zfill(3)))
        loc.write('\n # Select Expedition Menu Event')
        loc.write(
            '\n MEC_Expeditions.{event_num}.name: "Select Expedition"\n'.format(event_num=str(menu_event_number).zfill(3)))
        loc.write(
            f' MEC_Expeditions.{str(menu_event_number).zfill(3)}.desc: "We are able to send expeditions to establish our nation far from our capital. This enables us to expand our colonization and trade efforts. While we can make estimates for our chances of success to uncolonized territory, '
            f'if our expeditions arrive at already owned land their success will depend on if our military technology is superior enough against the locals as well as what defenses they have, how many trained men they have, and the size of the province. We would expect to hear back from our expedition within a year."\n')
        loc.write(f' MEC_Expeditions.{str(menu_event_number).zfill(3)}.dont: "Don\'t send an expedition."\n')

        events.write(
            "\ttrigger = {\n\t\tOR = {\n\t\t\thas_idea = exploration_ideas_3\n\t\t\thas_country_modifier = can_colonize_country_modifier\n\t\t}\n\t\tmax_sailors = 1500\n\t\tNOT = {\n\t\t\thas_country_flag = MEC_Expeditions_paused\n\t\t}\n\t\tnum_of_ports = 1\n\t\tOR = { # Has an expedition available\n")
        for expedition in expeditions_list:
            events.write(f"\t\t\tMEC_Expeditions_available_{expedition.name}_trigger = yes\n")
        events.write("\t\t}\n\t}\n\n")
        events.write('\timmediate = {\n\t\thidden_effect = {\n\t\t\tROOT = {\n\t\t\t\tsubtract_key = { lhs = tech_mil value = 5 }\n\t\t\t}\n\t\t}\n\t}\n\n')
        events.write(f"\toption = {{ # AI should take when no expedition available\n\t\tname = MEC_Expeditions.{str(menu_event_number).zfill(3)}.dont\n\t\tai_chance = {{\n\t\t\tfactor = 0.1\n\t\t}}\n\t}}\n\n")

        clr_all_sent_flags = ''
        for expedition in expeditions_list:
            clr_all_sent_flags += f"\t\t\tclr_country_flag = MEC_Expeditions_sent_{expedition.name}\n"

        for index, expedition in enumerate(expeditions_list):
            events.write(f"\t# Option for repeating sending Expedition to {expedition.localized_name}\n")
            events.write(select_expedition_option_repeat_frame_top.format(event_num=str(menu_event_number).zfill(3), expedition_name=expedition.name, ai_base_chance=expedition.ai_preference))

            if expedition.target_type == 'Jumping Node':
                events.write(select_expedition_option_frame_bottom_jumping_node.format(expedition_name=expedition.name))
            if expedition.target_type == 'Colonial Node':
                events.write(select_expedition_option_frame_bottom_colonial_node.format(expedition_name=expedition.name))
            if expedition.target_type == 'Chinese Mainland':
                events.write(select_expedition_option_frame_bottom_chinese_mainland.format(expedition_name=expedition.name))
            events.write(select_expedition_option_frame_TN_link_check_top)
            for i, node_number in enumerate(expedition.associated_TN):
                events.write(select_expedition_option_frame_TN_link_check_inside.format(TN=node_number))
            events.write("\t\t\t}\n")

            events.write(select_expedition_option_frame_bottom.format(expedition_name=expedition.name,
                                                                      event_num_arrival=str(expedition_arrival_start_number + index).zfill(3), event_num_total_failure=str(expedition_total_failure_start_number + index).zfill(3),
                                                                      event_num_map_failure=str(expedition_map_failure_start_number + index).zfill(3),
                                                                      event_num_trade_failure=str(expedition_trade_failure_start_number + index).zfill(3), expedition_duration=expedition_duration, clr_all_sent_flags=''))  # Repeat 0 AI chance
            loc.write(f' MEC_Expeditions.{str(menu_event_number).zfill(3)}.{expedition.name}_repeat: "Send another expedition to {expedition.localized_name}"\n')

        for index, expedition in enumerate(expeditions_list):
            events.write(f"\t# Option for sending Expedition to {expedition.localized_name}\n")
            events.write(select_expedition_option_regular_frame_top.format(event_num=str(menu_event_number).zfill(3), expedition_name=expedition.name, ai_base_chance=expedition.ai_preference))

            if expedition.target_type == 'Jumping Node':
                events.write(select_expedition_option_frame_bottom_jumping_node.format(expedition_name=expedition.name))
            if expedition.target_type == 'Colonial Node':
                events.write(select_expedition_option_frame_bottom_colonial_node.format(expedition_name=expedition.name))
            if expedition.target_type == 'Chinese Mainland':
                events.write(select_expedition_option_frame_bottom_chinese_mainland.format(expedition_name=expedition.name))
            events.write(select_expedition_option_frame_TN_link_check_top)
            for i, node_number in enumerate(expedition.associated_TN):
                events.write(select_expedition_option_frame_TN_link_check_inside.format(TN=node_number))
            events.write("\t\t\t}\n")
            if expedition.target_type == 'Colonial Node':
                events.write(select_expedition_option_claim_frame.format(expedition_name=expedition.name))
            events.write(select_expedition_option_frame_bottom.format(expedition_name=expedition.name,
                                                                      event_num_arrival=str(expedition_arrival_start_number + index).zfill(3), event_num_total_failure=str(expedition_total_failure_start_number + index).zfill(3),
                                                                      event_num_map_failure=str(expedition_map_failure_start_number + index).zfill(3),
                                                                      event_num_trade_failure=str(expedition_trade_failure_start_number + index).zfill(3), expedition_duration=expedition_duration, ai_base_chance=expedition.ai_preference, clr_all_sent_flags=clr_all_sent_flags))

            loc.write(f' MEC_Expeditions.{str(menu_event_number).zfill(3)}.{expedition.name}: "Send the expedition to {expedition.localized_name}"\n')

        events.write('\tafter = {\n\t\tif = {\n\t\t\tlimit = {\n\t\t\t\tNOT = {\n\t\t\t\t\thas_idea = colonialism_ideas_1\n\t\t\t\t}\n\t\t\t}\n\t\t\tset_country_flag = MEC_Expeditions_skip_year\n\t\t}\n')
        events.write('\t\tROOT = {change_key = { lhs = tech_mil value = 5 }}\n\t}\n}\n')
        # Write the Expedition Arrival section header
        events.write(hash_line)
        events.write(
            "##################################        Expedition Arrival       #########################################\n")
        events.write(hash_line + '\n')

        # Loop through every expedition and write arrival events for each
        loc.write("\n # Expedition Arrivals\n")
        loc.write(' MEC_Expeditions.arrival: "Okay."\n')

        for index, expedition in enumerate(expeditions_list):
            events.write(f"# Arrivals of Expedition to {expedition.localized_name}\n")
            events.write(expedition_arrival_frame.format(event_num=str(expedition_arrival_start_number + index).zfill(3), event_num_landing=str(expedition_landing_start_number + index).zfill(3), expedition_name=expedition.name, event_num_total_failure=str(expedition_total_failure_start_number +
                                                                                                                                                                                                                                                                index).zfill(3),
                                                         landing_success='\t\t\t\t\t'.join(landing_success.format(
                                                             event_num_success=str(
                                                                 expedition_success_start_number + index).zfill(3), event_num_total_failure=str(expedition_total_failure_start_number + index).zfill(3),
                                                             expedition_name=expedition.name, event_num_no_attack_failure=str(expedition_no_attack_failure_start_number + index).zfill(3)).splitlines(True))))
            loc.write(f' MEC_Expeditions.{str(expedition_arrival_start_number + index).zfill(3)}.title: "Expedition from [From.GetName]"\n')
            loc.write(f' MEC_Expeditions.{str(expedition_arrival_start_number + index).zfill(3)}.desc: "This event is supposed to be hidden. If you are seeing it please report this bug."\n')

        # Write the Expedition Landing section header
        events.write(hash_line)
        events.write(
            "##################################        Expedition Landings       #########################################\n")
        events.write(hash_line + '\n')

        # Loop through every expedition and write landing events for each
        loc.write("\n # Expedition Landings\n")
        loc.write(' MEC_Expeditions.accept_trade_fort: "We shall sell them the province."\n')
        loc.write(' MEC_Expeditions.reject_trade_fort: "Try to fight them off! We don\'t accept."\n')
        loc.write(' MEC_Expeditions.always_reject_trade_fort: "Try to fight them off, this time and always! (Can change via decision)"\n')
        loc.write(' MEC_Expeditions.colony: "You shouldn\'t be seeing this option. Please report the bug."\n')

        for index, expedition in enumerate(expeditions_list):
            events.write(f"# Landings of Expedition to {expedition.localized_name}\n")
            events.write(expedition_landing_frame.format(event_num=str(expedition_landing_start_number + index).zfill(3), event_num_success=str(expedition_success_start_number + index).zfill(3), expedition_name=expedition.name, landing_success='\t\t'.join(landing_success.format(
                event_num_success=str(
                    expedition_success_start_number + index).zfill(3), event_num_total_failure=str(expedition_total_failure_start_number + index).zfill(3),
                expedition_name=expedition.name, event_num_no_attack_failure=str(expedition_no_attack_failure_start_number + index).zfill(3)).splitlines(True))))
            loc.write(f' MEC_Expeditions.{str(expedition_landing_start_number + index).zfill(3)}.title: "Expedition from [From.GetName]"\n')
            loc.write(f' MEC_Expeditions.{str(expedition_landing_start_number + index).zfill(3)}.desc: "Foreigners have arrived wanting to setup a trading fort on our our province of [Root.GetName]. This would effectively give them control of the province. They offer to pay for the province, '
                      f'but our diplomatic advisor suspects that if we don\'t accept they will try to take it by force anyway. Our military advisor estimates that if it comes down to a fight they have a [GV_MEC_Expeditions_Comparison] out of 10 chance of losing the province."\n')

        # Write the Expedition Success section header
        events.write(hash_line)
        events.write(
            "##################################        Expedition Success       #########################################\n")
        events.write(hash_line + '\n')

        # Loop through every expedition writing expedition success events for each
        loc.write("\n # Successful Expeditions\n")
        loc.write(' MEC_Expeditions.expedition_success: "Great. We have a new province."\n')
        for index, expedition in enumerate(expeditions_list):
            events.write(f"# Success of Expedition to {expedition.localized_name}\n")
            events.write(expedition_success_frame.format(event_num=str(expedition_success_start_number + index).zfill(3),
                                                         expedition_name=expedition.name))
            if expedition.name in can_trigger_MAM_event_15:
                events.write(expedition_success_confirmation_MAM_event_15.format(expedition_name=expedition.name))
            else:
                events.write(expedition_success_confirmation.format(expedition_name=expedition.name))
            loc.write(
                f' MEC_Expeditions.{str(expedition_success_start_number + index).zfill(3)}.title: "Expedition to {expedition.localized_name} Successful at [MEC_Expedition_Target_Province.GetName]"\n')
            loc.write(
                f' MEC_Expeditions.{str(expedition_success_start_number + index).zfill(3)}.desc: "We have heard back from the expedition to {expedition.localized_name}. They have established a settlement at [MEC_Expedition_Target_Province.GetName]. Since they also control the surrounding area they are '
                f'asking for recognition as a province."\n')

        # Write the Expedition Failure section header
        events.write(hash_line)
        events.write(
            "################################        Expedition Total Failure       #######################################\n")
        events.write(hash_line + '\n')

        # Loop through every expedition writing expedition failure events for each
        loc.write("\n # Expedition Total Failure\n")
        loc.write(' MEC_Expeditions.total_failure: "This reflects poorly on us."\n')
        for index, expedition in enumerate(expeditions_list):
            events.write(f"# Failure of Expedition to {expedition.localized_name}\n")
            events.write(expedition_total_failure_frame.format(event_num=str(expedition_total_failure_start_number + index).zfill(3),
                                                               expedition_name=expedition.name))
            loc.write(
                f' MEC_Expeditions.{str(expedition_total_failure_start_number + index).zfill(3)}.title: "Expedition to {expedition.localized_name} Lost at Sea"\n')
            loc.write(
                f' MEC_Expeditions.{str(expedition_total_failure_start_number + index).zfill(3)}.desc: "A prominent trader has been spreading word that we since we haven\'t heard back from our expedition to {expedition.localized_name} for so long that we can only assume it has failed '
                f'completely."\n')

        # Write the Expedition Failure section header
        events.write(hash_line)
        events.write(
            "################################        Expedition Map Failure       #######################################\n")
        events.write(hash_line + '\n')

        # Loop through every expedition writing expedition failure events for each
        loc.write("\n # Expedition Map Failure\n")
        loc.write(' MEC_Expeditions.map_failure: "That\'s better than nothing."\n')
        for index, expedition in enumerate(expeditions_list):
            events.write(f"# Failure of Expedition to {expedition.localized_name}\n")
            events.write(expedition_map_failure_frame.format(event_num=str(expedition_map_failure_start_number + index).zfill(3),
                                                             expedition_name=expedition.name))
            loc.write(
                f' MEC_Expeditions.{str(expedition_map_failure_start_number + index).zfill(3)}.title: "Expedition to {expedition.localized_name} Only Got Maps"\n')
            loc.write(
                f' MEC_Expeditions.{str(expedition_map_failure_start_number + index).zfill(3)}.desc: "A ship returned from our expedition to {expedition.localized_name}! However, they reported they were unsuccessful in establishing a settlement and barely made it back. Though they did bring '
                f'back maps of the region."\n')

        # Write the Expedition Failure section header
        events.write(hash_line)
        events.write(
            "################################        Expedition Trade Failure       #######################################\n")
        events.write(hash_line + '\n')

        # Loop through every expedition writing expedition failure events for each
        loc.write("\n # Expedition Trade Failure\n")
        loc.write(' MEC_Expeditions.trade_failure: "Well at least they got something."\n')
        for index, expedition in enumerate(expeditions_list):
            events.write(f"# Failure of Expedition to {expedition.localized_name}\n")
            events.write(expedition_trade_failure_frame.format(event_num=str(expedition_trade_failure_start_number + index).zfill(3),
                                                               expedition_name=expedition.name))
            loc.write(
                f' MEC_Expeditions.{str(expedition_trade_failure_start_number + index).zfill(3)}.title: "Expedition to {expedition.localized_name} Got Maps and Goods"\n')
            loc.write(
                f' MEC_Expeditions.{str(expedition_trade_failure_start_number + index).zfill(3)}.desc: "A ship returned from our expedition to {expedition.localized_name}! However, they reported they were unsuccessful in establishing a settlement. Though they did bring back a small amount from '
                f'trading and maps of the region."\n')

        # Write the Expedition Failure section header
        events.write(hash_line)
        events.write(
            "################################        Expedition No Attack Failure       #######################################\n")
        events.write(hash_line + '\n')

        # Loop through every expedition writing expedition failure events for each
        loc.write("\n # Expedition No Attack Failure\n")
        loc.write(' MEC_Expeditions.no_attack_failure: "That is unfortunate."\n')
        for index, expedition in enumerate(expeditions_list):
            events.write(f"# Failure of Expedition to {expedition.localized_name}\n")
            events.write(expedition_no_attack_failure_frame.format(event_num=str(expedition_no_attack_failure_start_number + index).zfill(3),
                                                                   expedition_name=expedition.name))
            loc.write(
                f' MEC_Expeditions.{str(expedition_no_attack_failure_start_number + index).zfill(3)}.title: "Expedition to {expedition.localized_name} Didn\'t Find Opportunity"\n')
            loc.write(
                f' MEC_Expeditions.{str(expedition_no_attack_failure_start_number + index).zfill(3)}.desc: "A ship returned from our expedition to {expedition.localized_name}! However, they reported they were unsuccessful in establishing a settlement. They found people settled in each '
                f'province they checked who seemed too strong for us to be able to grab our own foothold. Though they did bring back maps of the region."\n')

        # Write the Expedition Decision Events section header
        events.write(hash_line)
        events.write(
            "################################        Expedition Decision Events      #######################################\n")
        events.write(hash_line + '\n')

        # Localization for options for these events
        loc.write("\n # Expedition Decision Events\n")
        loc.write(' MEC_Expeditions.more_info: "What does this mean?"\n')
        loc.write(' MEC_Expeditions.report: "Thanks for the report."\n')
        loc.write(' MEC_Expeditions.back: "Back."\n')
        loc.write(' MEC_Expeditions.close: "Close."\n')

        # Loop through every expedition writing expedition decision events for each
        for index, expedition in enumerate(expeditions_list):
            events.write(f"# Info on Expeditions to {expedition.localized_name}\n")
            events.write(expedition_decision_events_frame.format(event_num=str(expedition_decision_events_start_number + index).zfill(3),
                                                                 expedition_name=expedition.name, more_info_event_num=str(expedition_decision_events_start_number + len(expeditions_list)).zfill(3)))
            loc.write(
                f' MEC_Expeditions.{str(expedition_decision_events_start_number + index).zfill(3)}.title: "Info for Expeditions to {expedition.localized_name}"\n')
            loc.write(
                f' MEC_Expeditions.{str(expedition_decision_events_start_number + index).zfill(3)}.desc: "')
            for id in expedition.target_provinces:
                loc.write(f'[{id}.MEC_Expeditions_Decision_Event_Info]\\n')
            loc.write('"\n')
        events.write(expedition_decision_info_event_frame_top.format(event_num=str(expedition_decision_events_start_number + len(expeditions_list)).zfill(3)))
        events.write('\t\ttrigger_switch = {\n\t\t\ton_trigger = has_country_flag\n')
        for index, expedition in enumerate(expeditions_list):
            events.write(f'\t\t\tMEC_Expeditions_decision_event_{str(expedition_decision_events_start_number + index).zfill(3)} = {{\n\t\t\t\tclr_country_flag = MEC_Expeditions_decision_event_'
                         f'{str(expedition_decision_events_start_number + index).zfill(3)}\n\t\t\t\tcountry_event = {{\n\t\t\t\t\tid = MEC_Expeditions.{str(expedition_decision_events_start_number + index).zfill(3)}\n\t\t\t\t}}\n\t\t\t}}\n')
        events.write('\t\t}\n')
        events.write(expedition_decision_info_event_frame_bottom)

        for index, expedition in enumerate(expeditions_list):
            events.write(f'\t\tclr_country_flag = MEC_Expeditions_decision_event_{str(expedition_decision_events_start_number + index).zfill(3)}\n')
        events.write('\t}\n}\n\n')
        loc.write(' MEC_Expeditions_Decision_Event_Info_undiscovered: "Undiscovered province"\n')
        loc.write(' MEC_Expeditions_Decision_Event_Info_uncolonized: "[This.GetName] (Uncolonized) Harbour [GV_Tmp_0] Natural Feature [GV_Tmp_1] Total [GV_Tmp_9]"\n')
        loc.write(' MEC_Expeditions_Decision_Event_Info_colony: "[This.GetName] ([This.Owner.GetName]) Mil Tech [GV_Tmp_0] Def [GV_Tmp_1] Colony [GV_Tmp_2] MP [GV_Tmp_3] Size [GV_Tmp_4] Total [GV_Tmp_9]"\n')
        loc.write(' MEC_Expeditions_Decision_Event_Info_owned: "[This.GetName] ([This.Owner.GetName]) Mil Tech [GV_Tmp_0] Def [GV_Tmp_1] MP [GV_Tmp_3] Size [GV_Tmp_4] Total [GV_Tmp_9]"\n')

        loc.write(f' MEC_Expeditions.{str(expedition_decision_events_start_number + len(expeditions_list)).zfill(3)}.title: "Expeditions Detailed Info"\n')
        loc.write(f' MEC_Expeditions.{str(expedition_decision_events_start_number + len(expeditions_list)).zfill(3)}.desc:')
        loc.write(""""\
When expeditions are sent they have a 40% chance of successful landing at their target area, which can be increased to 80% with the first colonialism idea. Otherwise they \
get one of the failure options which brings back nothing, maps, or maps and some ducats.\\nOnce it is determined an expedition successfully landed there is a calculation for which province it landed at, which randomly loops through a bunch of provinces in the target area to evaluate their \
score and picks the one with the lowest score.\\nUncolonized provinces will be picked before owned provinces, with their scores determined by their rank of habour and natural feature. If all the provinces are owned then the owner of the province with the lowest score will get an event with the \
option \
to \
sell the province or defend it. If they choose to defend it then the chance of the expedition sender taking the province is their military tech level minus the province's defensive score divided by 10.\\nThe province's defensive score is calculated by mil tech, plus defensive bonus which \
consists of 2 + 2 * fort level, \
minus 5 if colony, plus bonus depending on sum of taxed manpower in province by the state and all of the elites, plus bonus based on size of the province.\\nIf the expedition sender has mil tech 20 and the province defensive score is 15, and the owner decides to defend, \
the sender would have 50% chance of taking \
the province after landing. It is not directly 50% after landing because at worse odds owners are more likely to choose to sell the province than try to defend. Thus a 5 point advantage actually gives the sender approximately 64% chance of gaining a province after successfully landing."\n""")

# file = open('wiki.txt', 'w+')
#
# for expedition in expeditions_list:
#     tabletext = """
# ==={}===
# {| class="mildtable sortable" style="width:100%"
# ! style="width:150px" class="unsortable" | Trade Node
# ! style="width:50px" | Tech Requirement
# """.format(expedition.expedition_name)
#     for (trade_node,tech) in expedition.node_tech_reqs:
#         tabletext += """
# |-
#
# |
# {}
# |
# {}
# |
# """.format(trade_node, tech)
#     tabletext += "}\n"
#     file.write(tabletext)
# file.close()
