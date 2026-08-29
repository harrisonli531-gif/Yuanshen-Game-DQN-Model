from collections import namedtuple
import data_hub as hub


### GENERIC VARIABLES ###
char_name = "Eula"
hand = []
target_values = {} #keeps track of which target character to target for effects

def get_deck_info():
    '''returns values related to passive'''
    if glacial_illumination not in hand:
        return f" (Glacial Seal: {len(glacial_seal)})"
    return " "
   

### CHAR VALUES AND CHAR SPECIFIC VARIABLES ###
char_values = {"hp": 25, 
               "dmg_mod": [[+0, 1000]], "pow_mod":[[+0, 1000]], "queued_mods" : [], 
               "queued_dmg" : None, 
               "player": None, "chosen_card": None, "is_ai" : False}

glacial_seal = []

op_starting_hp = None

missing_hp_dmg = 0

### CARD AND PASSIVE FUNCTIONS ###

# Passives and Outside Combat #

def get_starting_op_hp():
    global op_starting_hp
    if op_starting_hp == None:
        op_starting_hp = target_values["hp"]

def gain_glacial_stacks():
    '''Check if chosen card this round has already been played, gain stacks if not'''
    if (char_values["chosen_card"] not in glacial_seal) and (glacial_illumination not in hand):
        glacial_seal.append(char_values["chosen_card"])


def check_glacial_stacks():
    '''If four stacks, create Eula's ultimate in hand'''
    if len(glacial_seal) >= 4:
        hand.append(glacial_illumination)
        glacial_seal.clear()
        return "Eula's glacial seal has transformed and she has created a 'Glacial Illumination in hand!"
    return None

def transform_glacial_seal_back():
    if char_values["chosen_card"] == glacial_illumination:
        return "Eula has regained her glacial seal!"
    return " "

def pre_end_passive():
    '''Create ult in hand in needed or return glacial seal'''
    output = check_glacial_stacks()
    if output == None:
        output = transform_glacial_seal_back()
    return output

def roiling_rime_gain_pow():
    '''If card is roiling rime and meet passive stacks, gain power'''
    if char_values["chosen_card"] == roiling_rime and len(glacial_seal) >= 3:
        char_values["pow_mod"].append([4, 0])

def check_ult_played():
    '''If ult played, don't draw card for turn'''
    if char_values["chosen_card"] == glacial_illumination:
        return False
    return True

# Cards #
def ocean_swell_step():
    gain_glacial_stacks()

    total_dmg = hub.calc_dmg(ocean_swell_step.dmg, char_values["dmg_mod"]) 
    char_values["queued_dmg"] = total_dmg

def flutter_of_frost():
    gain_glacial_stacks()
    if len(glacial_seal) > 0:
        char_values["dmg_mod"].append([1, 0])
    total_dmg = hub.calc_dmg(flutter_of_frost.dmg, char_values["dmg_mod"]) 
    char_values["queued_dmg"] = total_dmg

def icetide_tempo():
    gain_glacial_stacks()

    total_dmg = hub.calc_dmg(icetide_tempo.dmg, char_values["dmg_mod"]) 
    char_values["queued_dmg"] = total_dmg
    char_values["queued_mods"].append(("dmg", +1, 1)) #lasts one turn for +2 power total
    char_values["queued_mods"].append(("dmg", +1, 2)) #lasts two turns 


def roiling_rime():
    gain_glacial_stacks()

    global missing_hp_dmg
    missing_hp_dmg = 0
    if target_values["hp"] < op_starting_hp:
        missing_hp_dmg = (op_starting_hp - target_values["hp"]) // 2
        if missing_hp_dmg > 4:
            missing_hp_dmg = 4
    total_dmg = hub.calc_dmg(roiling_rime.dmg + missing_hp_dmg, char_values["dmg_mod"]) 
    char_values["queued_dmg"] = total_dmg
    

def vengeance():
    gain_glacial_stacks()

    total_dmg = hub.calc_dmg(vengeance.dmg, char_values["dmg_mod"]) * 2
    char_values["queued_dmg"] =total_dmg
    target_values["queued_mods"].append(("pow", -2, 1))

def glacial_illumination():
    total_dmg = hub.calc_dmg(glacial_illumination.dmg, char_values["dmg_mod"]) 
    char_values["queued_dmg"] = total_dmg
   
    
### TRIGGERS ###
#stores functions that trigger outside of the damage step
misc_effects = {"pre_action_1" : get_starting_op_hp,
                "pre_end_1" : pre_end_passive,
                "pre_determine_winner_1" : roiling_rime_gain_pow,
                "draw_phase" : check_ult_played}

### CARD EFFECT DICT ###
card_effect_dict = {"ocean_swell_step" : ocean_swell_step,
                    "flutter_of_frost" : flutter_of_frost,
                    "icetide_tempo": icetide_tempo,
                    "roiling_rime" : roiling_rime,
                    "vengeance" : vengeance,
                    "glacial_illumination" : glacial_illumination}


### CARD TUPLES ###
card = namedtuple('card', ['display_name', 'card_id', 'speed', 'power', 'dmg', 'is_dmg_bool'])

#Thousand Slash Cascade
ocean_swell_step = card("Ocean Swell Step", "ocean_swell_step", "F", 6, 1, True)

flutter_of_frost = card("Flutter of Frost", "flutter_of_frost", "F", 3, 2, True)

icetide_tempo = card("Icetide Tempo", "icetide_tempo", "F", 2, 1, True)

roiling_rime = card("Roiling Rime", "roiling_rime", "S", 3, 2, True)

vengeance = card("Vengeance, Severed with Ice", "vengeance", "M", 6, 1, True)

glacial_illumination = card("[Ultimate] Glacial Illumination", "glacial_illumination", "M", 7, 6, True)


## MAP CARD ID TO NUMBER #
card_id_to_number = {
    "ocean_swell_step": 0,
    "flutter_of_frost": 1,
    "icetide_tempo": 2,
    "roiling_rime": 3,
    "vengeance": 4,
    "glacial_illumination": 5
}

#Resolution text
def resolution_text(card_id, base_dmg, win_bool):
    '''Returns either the dmg dealt and false for unique_bool or the unique resolution text and true'''
    #check if the resolution text needs to be unique

    if win_bool:
        if card_id == icetide_tempo.card_id:
            return True, f"Eula deals {char_values["queued_dmg"]} damage and gains a decaying +2 damage for two rounds!" #-2 to account for dmg bonus
        #yay spaghetti code!!!!
        
        if card_id == roiling_rime.card_id:
            return True, f"\"Frost marks your end!\" Eula deals {char_values["queued_dmg"]} damage"
        
        if card_id == vengeance.card_id:
            return True, f"\"Consider this vengeance fullfilled!\" Eula deals {char_values["queued_dmg"]} damage and given her opponent -2 power for one round!"
        
        if card_id == glacial_illumination.card_id:
            return True, f"\"Your reckoning is upon you!\" Eula deals {char_values["queued_dmg"]} damage"
        
    #generic text
        return False, str(char_values["queued_dmg"])
        #return just the damage if the resolution text is doing to be generic
    else:
        return False, "placeholder"
 

### DECK ###
deck_list = [(ocean_swell_step, 8), (flutter_of_frost, 7) , (icetide_tempo, 7) , (roiling_rime, 4) , (vengeance, 4), (glacial_illumination, 0)]
deck = [card for card, count in deck_list for _ in range(count)]

#BUGS
#alhaitham needs to be able to shut down her bonus damage from her attacks? I guess *shrug*
#why roiling rime pow not being applied
#roiling rime + icetide tempo dmg not correct? Furina had like 20 hp wait OOHHH it was 14 after dmg I think? dealing 6 damage
#against alhaitham icetide tempo > ocean swell step not applied dmg
#not applying roiling rime power bonus against alhaitham
#why did ult display 6 dmg when dealt 7 dmg with icetide tempo
#randomly dealt 3 damage turn 1 I thnk wiht flutter of frost? not checking stacks correct?