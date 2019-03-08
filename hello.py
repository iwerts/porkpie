import json, pprint

def getUpgrade(xws, upgrades):
    for upgrade in upgrades:
        if upgrade['xws'] == xws:
            return upgrade['name']

def getUpgrades(buildUpgrades, buildUpgradeTypes, buildUpgradeType, upgradeJSON):
    for upgrade in pilot['upgrades'][buildUpgradeType]:
        buildUpgrades.append(getUpgrade(upgrade, upgradeJSON))
        buildUpgradeTypes.append(buildUpgradeType)

output = pprint.PrettyPrinter(indent=4)

cards = json.load(open('./xwsquickbuilds.json', encoding='utf-8'))
manifest = json.load(open('xwing-data2-master/data/manifest.json', encoding='utf-8'))

astromechs = json.load(open('xwing-data2-master/data/upgrades/astromech.json', encoding='utf-8'))
cannons = json.load(open('xwing-data2-master/data/upgrades/cannon.json', encoding='utf-8'))
configurations = json.load(open('xwing-data2-master/data/upgrades/configuration.json', encoding='utf-8'))
crews = json.load(open('xwing-data2-master/data/upgrades/crew.json', encoding='utf-8'))
devices = json.load(open('xwing-data2-master/data/upgrades/device.json', encoding='utf-8'))
forcePowers = json.load(open('xwing-data2-master/data/upgrades/force-power.json', encoding='utf-8'))
gunners = json.load(open('xwing-data2-master/data/upgrades/gunner.json', encoding='utf-8'))
illicit = json.load(open('xwing-data2-master/data/upgrades/illicit.json', encoding='utf-8'))
missiles = json.load(open('xwing-data2-master/data/upgrades/missile.json', encoding='utf-8'))
modifications = json.load(open('xwing-data2-master/data/upgrades/modification.json', encoding='utf-8'))
sensors = json.load(open('xwing-data2-master/data/upgrades/sensor.json', encoding='utf-8'))
tacticalRelays = json.load(open('xwing-data2-master/data/upgrades/tactical-relay.json', encoding='utf-8'))
talents = json.load(open('xwing-data2-master/data/upgrades/talent.json', encoding='utf-8'))
techs = json.load(open('xwing-data2-master/data/upgrades/tech.json', encoding='utf-8'))
titles = json.load(open('xwing-data2-master/data/upgrades/title.json', encoding='utf-8'))
torpedoes = json.load(open('xwing-data2-master/data/upgrades/torpedo.json', encoding='utf-8'))
turrets = json.load(open('xwing-data2-master/data/upgrades/turret.json', encoding='utf-8'))

pilots = manifest['pilots']

legalCards = 0
for card in cards:
    
    hyperspaceLegal = True
        
    strings = []
    
    faction = card['faction']
    ships = card['ship'].split('+')

    shipBar = ''

    for shipIndex, ship in enumerate(ships):
        shipBar = shipBar + json.load(open('./xwing-data2-master/data/pilots/'+faction+'/'+ships[shipIndex].strip()+'.json', encoding='utf-8'))['name']        
        
        if shipIndex < (len(ships)-1):
            shipBar = shipBar + ' + '

    strings.append(shipBar)

    expansion = card['expansion']

    strings.append(expansion)

    builds = card['builds']
    
    for build in builds:
        threat = build['threat']

        threatBar = 0
        threatBarDraw = '| '

        while threatBar < threat:
            threatBarDraw = threatBarDraw + '['+str(threat)+']'

            threatBar = threatBar+1

        while threatBar < 5:
            threatBarDraw = threatBarDraw + '---'
            threatBar = threatBar + 1

        threatBarDraw = threatBarDraw + ' |'
        strings.append(threatBarDraw)
        pilots = build['pilots']

        for pilotIndex, pilot in enumerate(pilots):
            
            name = ''

            shipIndex = pilotIndex
            if len(pilots) != len(ships):
                shipIndex = 0
            master = json.load(open('./xwing-data2-master/data/pilots/'+faction+'/'+ships[shipIndex].strip()+'.json', encoding='utf-8'))        
            
            for masterPilot in master['pilots']:
                if masterPilot['xws'] == pilot['id']:
                    name = masterPilot['name']
                    hyperspaceLegal = masterPilot['hyperspace'] and hyperspaceLegal


            buildUpgrades = []
            buildUpgradeTypes = []
            if 'upgrades' in pilot:
                if 'astromech' in pilot['upgrades']:
                    getUpgrades(buildUpgrades, buildUpgradeTypes, 'astromech', astromechs)
                if 'cannon' in pilot['upgrades']:
                    getUpgrades(buildUpgrades, buildUpgradeTypes, 'cannon', cannons)
                if 'configuration' in pilot['upgrades']:
                    getUpgrades(buildUpgrades, buildUpgradeTypes, 'configuration', configurations)
                if 'crew' in pilot['upgrades']:
                    getUpgrades(buildUpgrades, buildUpgradeTypes, 'crew', crews)
                if 'device' in pilot['upgrades']:
                    getUpgrades(buildUpgrades, buildUpgradeTypes, 'device', devices)
                if 'force-power' in pilot['upgrades']:
                    getUpgrades(buildUpgrades, buildUpgradeTypes, 'force-power', forcePowers)
                if 'gunner' in pilot['upgrades']:
                    getUpgrades(buildUpgrades, buildUpgradeTypes, 'gunner', gunners)
                if 'illicit' in pilot['upgrades']:
                    getUpgrades(buildUpgrades, buildUpgradeTypes, 'illicit', illicit)
                if 'missile' in pilot['upgrades']:
                    getUpgrades(buildUpgrades, buildUpgradeTypes, 'missile', missiles)
                if 'modification' in pilot['upgrades']:
                    getUpgrades(buildUpgrades, buildUpgradeTypes, 'modification', modifications)
                if 'sensor' in pilot['upgrades']:
                    getUpgrades(buildUpgrades, buildUpgradeTypes, 'sensor', sensors)
                if 'tactical-relay' in pilot['upgrades']:
                    getUpgrades(buildUpgrades, buildUpgradeTypes, 'tactical-relay', tacticalRelays)
                if 'talent' in pilot['upgrades']:
                    getUpgrades(buildUpgrades, buildUpgradeTypes, 'talent', talents)
                if 'tech' in pilot['upgrades']:
                    getUpgrades(buildUpgrades, buildUpgradeTypes, 'tech', techs)
                if 'title' in pilot['upgrades']:
                    getUpgrades(buildUpgrades, buildUpgradeTypes, 'title', titles)
                if 'torpedo' in pilot['upgrades']:
                    getUpgrades(buildUpgrades, buildUpgradeTypes, 'torpedo', torpedoes)
                if 'turret' in pilot['upgrades']:
                    getUpgrades(buildUpgrades, buildUpgradeTypes, 'turret', turrets)
            strings.append('+ '+ name)
            for upgrade in buildUpgrades:
               strings.append('|--'+str(upgrade))
            strings.append('')

    if not hyperspaceLegal:
        strings = []
    else:
        strings.append('------------------------')
        legalCards = legalCards+1
    for string in strings:
        output.pprint(string)

output.pprint('Legal Cards: ' + str(legalCards))