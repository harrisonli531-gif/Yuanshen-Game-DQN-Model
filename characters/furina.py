from collections import namedtuple
import data_hub as hub
import random


### GENERIC VARIABLES ###
char_name = "Furina"
hand = []
target_values = {} #keeps track of which target character to target for effects

def get_deck_info():
    '''returns values related to pass'''
    return f" (Fanfare: {fanfare_stacks})"

### CHAR VALUES AND CHAR SPECIFIC VARIABLES ###
char_values = {"hp": 25, 
               "dmg_mod": [[+0, 1000]], "pow_mod":[[+0, 1000]], "queued_mods" : [], 
               "queued_dmg" : None, 
               "player": None, "chosen_card": None, "is_ai" : False}

fanfare_stacks = 0

endless_waltz_stacks = 0


#Encore
recovered_card = None
possible_encores = []

### CARD AND PASSIVE FUNCTIONS ###

# Passives and Outside Combat #
def grant_passive_mod():
    '''triggers start of round, grant furina bonus power for that round based on number of fanfare stacks'''
    if fanfare_stacks == 1:
        char_values["pow_mod"].append([+1, 0])
    elif fanfare_stacks == 2:
        char_values["pow_mod"].append([+2, 0])
    elif fanfare_stacks == 3:
        char_values["pow_mod"].append([+3, 0])
    elif fanfare_stacks >= 4:
        char_values["pow_mod"].append([+4, 0])


def gain_fanfare():
    '''This is literally just a modified copy and paste of the determine_winner() function omg this is so janky ;-;'''
    global fanfare_stacks
    speed_rankings = ["S", "M", "F"]
    target_speed = speed_rankings.index(target_values["chosen_card"].speed)
    target_pow = target_values["chosen_card"].power + hub.get_mod_values(target_values, "pow_mod")
    furina_speed = speed_rankings.index(char_values["chosen_card"].speed)
    furina_pow = char_values["chosen_card"].power + hub.get_mod_values(char_values, "pow_mod")
    if furina_pow > target_pow and furina_speed > target_speed:
        fanfare_stacks += 1
        return True
    return False

def fanfare_text():
    '''Creates different display text when gaining fanfare'''
    text_choice = ["The crowd whoops!", "The crowd cheers!", "The crowd looks upon Furina with awe!"]
    return random.choice(text_choice)
   
def soliloquy_trigger():
    #input(char_values["player"], win_bool)
    win_bool = None
    win_bool = hub.win_bools[char_values["player"]]
    
    if win_bool == False:
        num = random.randint(1, 4)
        if num == 1:
            char_values["hp"] += 2
            return "[Passive] Soliloquy that Remains Unheard: Furina regains 2 hp!"
    return None
    

def pre_end_functions():
    '''Calls both post resolution functions'''
    fanfare_bool = gain_fanfare()
    if fanfare_bool:
        return f"[Passive] Let the People Rejoice: {fanfare_text()} Furina gains 1 fanfare stack!"
    return soliloquy_trigger()

def spotlight_lose():
    '''Spotlight's on Me's lose effect'''
    if  hub.win_bools[char_values["player"]] == False and char_values["chosen_card"].card_id == spotlight.card_id:
        char_values["hp"] += 1
  

    

# Cards #
def endless_waltz():
    possible_encores.append(endless_waltz)
    global endless_waltz_stacks
    char_values["dmg_mod"].append([endless_waltz_stacks, 0])
    total_dmg = hub.calc_dmg(endless_waltz.dmg, char_values["dmg_mod"]) 
    char_values["queued_dmg"] =  total_dmg
    endless_waltz_stacks += 1

def solicitation():
    bonus_dmg = 0
    possible_encores.append(solicitation)
    if fanfare_stacks == 1:
        bonus_dmg = 2
    elif fanfare_stacks == 2:
        bonus_dmg = 3
    elif fanfare_stacks >= 3:
        bonus_dmg = 4
    else:
        bonus_dmg = 0
    char_values["dmg_mod"].append([bonus_dmg, 0])
    total_dmg = hub.calc_dmg(solicitation.dmg + bonus_dmg, char_values["dmg_mod"]) 
    char_values["queued_dmg"] =  total_dmg

def spotlight():
    possible_encores.append(spotlight)
    total_dmg = hub.calc_dmg(spotlight.dmg, char_values["dmg_mod"]) 
    char_values["queued_dmg"] =  total_dmg

def encore():
    global recovered_card
    if len(possible_encores) == 0:
        possible_encores.append(encore)
    recovered_card = random.choice(possible_encores)
    hand.append(recovered_card)
    possible_encores.remove(recovered_card)

def curtain_call():
    total_dmg = hub.calc_dmg(spotlight.dmg, char_values["dmg_mod"]) 
    char_values["queued_dmg"] =  total_dmg

   


    
### TRIGGERS ###
#stores functions that trigger outside of the damage step
misc_effects = {"pre_action_1" : grant_passive_mod,
                "pre_end_1" : pre_end_functions,
                "pre_resolve_cards_1" : spotlight_lose}

### CARD EFFECT DICT ###
card_effect_dict = {"endless_waltz" : endless_waltz,
                    "solicitation" : solicitation,
                    "spotlight" : spotlight,
                    "encore": encore,
                    "curtain_call": curtain_call}


### CARD TUPLES ###
card = namedtuple('card', ['display_name', 'card_id', 'speed', 'power', 'dmg', 'is_dmg_bool'])

#Thousand Slash Cascade
endless_waltz = card("Endless Waltz", "endless_waltz", "M", 7, 1, True)

solicitation = card("The Star's Solicitation", "solicitation", "M", 4, 2, True)

spotlight = card("Spotlight's on Me", "spotlight", "F", 6, 1, True)

encore = card("Encore", "encore", "S", 4, 0, False)

curtain_call = card("[Ultimate] Curtain Call", "curtain_call", "S", 4, 8, True)



#Resolution text
def resolution_text(card_id, base_dmg, win_bool):
    '''Returns either the dmg dealt and false for unique_bool or the unique resolution text and true'''
    #check if the resolution text needs to be unique

    if win_bool:
        #I know these techinqually aren't unique resolution texts but I'm too lazy to ifnd a better to way to do this
        #so alas, spaghetti code :(
        if card_id == endless_waltz.card_id:
            return False, str(char_values["queued_dmg"])
        if card_id == solicitation.card_id:
            return False, str(char_values["queued_dmg"])
        if card_id == encore.card_id:
            return True, f"\"You want to see another \'{recovered_card.display_name}\'? Well of course you do!\""
        if card_id == curtain_call.card_id:
            return True, f"\"The grand finale approaches!\" Furina deals {char_values["queued_dmg"]} damage!"
    #generic text
        return False, str(char_values["queued_dmg"])
        #return just the damage if the resolution text is doing to be generic
    else:
        if card_id == spotlight.card_id:
            return True, "Furina seizes the spotlight and regains 1 hp!"
        return False, "placeholder"
 

### DECK ###
deck_list = [(endless_waltz, 7), (solicitation, 7), (encore, 6), (spotlight, 8),(curtain_call, 2)]
deck = [card for card, count in deck_list for i in range(count)]



