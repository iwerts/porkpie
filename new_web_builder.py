import json, pprint, os

output = pprint.PrettyPrinter(indent=4)

quick_build_cards = json.load(open('C:\\Users\\s278729\\Desktop\\X-Wing\\WebBuilder\\xwsquickbuilds.json', encoding='utf-8'))
manifest = json.load(open('C:\\Users\\s278729\\Desktop\\X-Wing\\WebBuilder\\xwing-data2-master\\data\\manifest.json', encoding='utf-8'))

astromechs = json.load(open('C:\\Users\\s278729\\Desktop\\X-Wing\\WebBuilder\\xwing-data2-master\\data\\upgrades\\astromech.json', encoding='utf-8'))
cannons = json.load(open('C:\\Users\\s278729\\Desktop\\X-Wing\\WebBuilder\\xwing-data2-master\\data\\upgrades\\cannon.json', encoding='utf-8'))
configurations = json.load(open('C:\\Users\\s278729\\Desktop\\X-Wing\\WebBuilder\\xwing-data2-master\\data\\upgrades\\configuration.json', encoding='utf-8'))
crews = json.load(open('C:\\Users\\s278729\\Desktop\\X-Wing\\WebBuilder\\xwing-data2-master\\data\\upgrades\\crew.json', encoding='utf-8'))
devices = json.load(open('C:\\Users\\s278729\\Desktop\\X-Wing\\WebBuilder\\xwing-data2-master\\data\\upgrades\\device.json', encoding='utf-8'))
force_powers = json.load(open('C:\\Users\\s278729\\Desktop\\X-Wing\\WebBuilder\\xwing-data2-master\\data\\upgrades\\force-power.json', encoding='utf-8'))
gunners = json.load(open('C:\\Users\\s278729\\Desktop\\X-Wing\\WebBuilder\\xwing-data2-master\\data\\upgrades\\gunner.json', encoding='utf-8'))
illicits = json.load(open('C:\\Users\\s278729\\Desktop\\X-Wing\\WebBuilder\\xwing-data2-master\\data\\upgrades\\illicit.json', encoding='utf-8'))
missiles = json.load(open('C:\\Users\\s278729\\Desktop\\X-Wing\\WebBuilder\\xwing-data2-master\\data\\upgrades\\missile.json', encoding='utf-8'))
modifications = json.load(open('C:\\Users\\s278729\\Desktop\\X-Wing\\WebBuilder\\xwing-data2-master\\data\\upgrades\\modification.json', encoding='utf-8'))
sensors = json.load(open('C:\\Users\\s278729\\Desktop\\X-Wing\\WebBuilder\\xwing-data2-master\\data\\upgrades\\sensor.json', encoding='utf-8'))
tactical_relays = json.load(open('C:\\Users\\s278729\\Desktop\\X-Wing\\WebBuilder\\xwing-data2-master\\data\\upgrades\\tactical-relay.json', encoding='utf-8'))
talents = json.load(open('C:\\Users\\s278729\\Desktop\\X-Wing\\WebBuilder\\xwing-data2-master\\data\\upgrades\\talent.json', encoding='utf-8'))
techs = json.load(open('C:\\Users\\s278729\\Desktop\\X-Wing\\WebBuilder\\xwing-data2-master\\data\\upgrades\\tech.json', encoding='utf-8'))
titles = json.load(open('C:\\Users\\s278729\\Desktop\\X-Wing\\WebBuilder\\xwing-data2-master\\data\\upgrades\\title.json', encoding='utf-8'))
torpedoes = json.load(open('C:\\Users\\s278729\\Desktop\\X-Wing\\WebBuilder\\xwing-data2-master\\data\\upgrades\\torpedo.json', encoding='utf-8'))
turrets = json.load(open('C:\\Users\\s278729\\Desktop\\X-Wing\\WebBuilder\\xwing-data2-master\\data\\upgrades\\turret.json', encoding='utf-8'))

html_template = '''<html>

<head>
        <link rel="stylesheet" href="xwing-miniatures-font-master/dist/xwing-miniatures.css">
        <link rel="stylesheet" href="style.css">
</head>

<body>
    {cards}
</body>

</html>'''

card_template = '''
<div class="bleed">
    <div class="faction_background {faction}"></div>
    <div class="ship_symbol_background"></div>
        
<div class="card">
    <div class="title_section">
                        <div class="section">
                            <div class="faction_symbol">
                                <i class="xwing-miniatures-font xwing-miniatures-font-{faction_font_code} {faction}" ></i>
                            </div>
                        </div>
                        
                        <div class="section">
                            <div class="ship_name">
                            {ship_name}
                           <br>
                            <span class="set_expansion">{expansion}</span>
                            </div>
                        </div>
                        
                        <div class="section">
                            <div class="ship_symbol">
                                <i class="xwing-miniatures-ship xwing-miniatures-ship-{ship_font_code}"></i>
                            </div>
                        </div>
                </div>
    <div class="main">
        {builds}
    </div>
</div>
'''

build_template = '''
<div class="build">
    <img class="threat_bar" src="/threat-bars/{threat_value}.png"/>
    {pilots}
</div>
'''

pilot_template = '''
    <span class="pilot_name">{pilot_name}</span>
    {upgrades}
'''

upgrade_template = '''
<div class="upgrade">
<span class="upgrade_symbol">{upgrade_symbol}</span>
{upgrade_name}
</div>
'''

upgrade_symbol_template = '''
    <i class="xwing-miniatures-font xwing-miniatures-font-{upgrade_symbol}"></i>                            
    '''
upgrade_name_template = '''
    <span class="upgrade_name">
        {upgrade_name}
    </span>
'''

def main():
    cards = ''
    for card_index, card in enumerate(quick_build_cards):
        cards = cards + get_card(card)
    strToFile(html_template.format(**locals()), 'dummywebsite.html')
def strToFile(text, filename):
    output = open(filename, "w")
    output.write(text)
    output.close()

def get_card(card):

    faction = card['faction']
    faction_font_code = convertFaction(faction)

    ship_name = get_ship_by_id(-1)
    expansion = card['expansion']
    ship_font_code = card['ship']

    builds = ''
    for build_index, build in enumerate(card['builds']):
        builds = builds + get_build(build)
    
    return card_template.format(**locals())



def convertFaction(faction):
    switcher = {
        'first-order':'firstorder',
        'galactic-empire':'empire',
        'scum-and-villainy':'scum',
        'resistance':'rebel',
        'rebel-alliance':'rebel'
    }
    return switcher.get(faction, '')

def get_build(build):
    ret = ''
    threat_value = build['threat']
    pilots = ''

    if 'pilots' in build:

        if duplicate_ships(build['pilots']):
            pilots = pilots + str(get_duplicated_pilots(build['pilots'][0], len(build['pilots'])))
        else:
            for pilot in build['pilots']:
                pilots = pilots + get_pilot(pilot)
    return build_template.format(**locals())

def duplicate_ships(pilots):
    if len(pilots) > 1:
        previous_pilot_name = ''
        for pilot_index, pilot in enumerate(pilots):
            if previous_pilot_name == '' or previous_pilot_name == pilot:
                previous_pilot_name = pilot
                continue
            else:
                return False
        return True
    else:
        return False

def get_duplicated_pilots(pilot, number_of_pilots):
    pilot_name = ''
    upgrades = ''

    if 'id' in pilot:
        pilot_name = get_pilot_name(pilot['id']) + ' x' + str(number_of_pilots)
    if 'upgrades' in pilot:
        for upgrade_type in pilot['upgrades']:
            
            for upgrade_id in pilot['upgrades'][upgrade_type]:
                upgrades = upgrades + str(get_filled_upgrade_template(upgrade_type,upgrade_id))
    return pilot_template.format(**locals())

def get_pilot_by_xws(pilot_xws):
 for directory, subdirectories, files in os.walk('C:\\Users\\s278729\\Desktop\\X-Wing\\WebBuilder\\xwing-data2-master\\data\\pilots'):
        for file in files:
            pilots = json.load(open(directory + '\\' + file))
            if 'pilots' in pilots:
                for pilot in pilots['pilots']:
                    if pilot['xws'] == pilot_xws:
                        return pilot

def get_upgrade_by_xws(upgrade_xws):
     for directory, subdirectories, files in os.walk('C:\\Users\\s278729\\Desktop\\X-Wing\\WebBuilder\\xwing-data2-master\\data\\upgrades'):
        for file in files:
            upgrades = json.load(open(directory + '\\' + file))
            for upgrade in upgrades:
                if upgrade['xws'] == upgrade_xws:
                    return upgrade

def get_ship_by_id(ship_id):
    return -1

def get_pilot(pilot):
    pilot_name = ''
    upgrades = ''

    if 'id' in pilot:
        pilot_name = get_pilot_name(pilot['id'])
    if 'upgrades' in pilot:
        for upgrade_type in pilot['upgrades']:
            for upgrade_id in pilot['upgrades'][upgrade_type]:
                upgrades = upgrades + str(get_filled_upgrade_template(upgrade_type,upgrade_id))
    return pilot_template.format(**locals())

def get_pilot_name(pilot_id):
    
    pilot = get_pilot_by_xws(pilot_id)
    pilot_name = ''

    if pilot['limited'] > 0:
        pilot_name = ' • '

    pilot_name = pilot_name + pilot['name']

    return pilot_name

def get_upgrade_name(upgrade):
    upgrade_name = ''

    if upgrade['limited'] > 0:
        upgrade_name = ' • '

    upgrade_name = upgrade_name + upgrade['name']

    return upgrade_name_template.format(**locals())


def get_upgrade_symbol(upgrade):
    ret = ''
    for slot in upgrade['sides'][0]['slots']:
        ret_symbol = get_upgrade_category_xwing_font(str(slot).lower().replace(' ', '-'))
        upgrade_symbol = ret_symbol
        ret = ret + upgrade_symbol_template.format(**locals())

    return ret

def get_filled_upgrade_template(upgrade_category, upgrade_id):
    upgrade_symbol = ''
    upgrade_name = ''

    upgrade = get_upgrade_by_xws(upgrade_id)
    
    upgrade_symbol = get_upgrade_symbol(upgrade)

    upgrade_name = get_upgrade_name(upgrade)

    return upgrade_template.format(**locals())

def get_upgrade(upgrade_category, upgrade_id):
    for upgrade in upgrade_category:
        if 'xws' in upgrade:
            if upgrade['xws'] == upgrade_id:
                return upgrade

def get_upgrade_category_xwing_font(upgrade_category):
    switcher = {
        'astromech':"astromech",
        'cannon':"cannon",
        'configuration':"config",
        'crew':"crew",
        'device':"device",
        'force-power': "forcepower",
        'gunner':"gunner",
        'illicit':"illicit",
        'missile':"missile",
        'modification' : "modification",
        'sensor':"sensor",
        'tactical-relay': "tacticalrelay",
        'talent':"talent",
        'tech':"tech",
        'title':"title",
        'torpedo':"torpedo",
        'turret':"turret"
    }
    return switcher.get(str(upgrade_category), 'COULDNT FIND ' + str(upgrade_category))

main()