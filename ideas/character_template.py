from collections import namedtuple
import data_hub as hub
import random


### GENERIC VARIABLES ###
char_name = ""
hand = []
target_values = {} #keeps track of which target character to target for effects

def get_deck_info():
    '''returns values related to passive'''
   

### CHAR VALUES AND CHAR SPECIFIC VARIABLES ###
char_values = {"hp": 25, "dmg_mod": [[+0, 1000]], "pow_mod":[[+0, 1000]], "queued_mods" : [], "player": None, "chosen_card": None, "is_ai" : False}


### CARD AND PASSIVE FUNCTIONS ###

# Passives and Outside Combat #



# Cards #



    
### TRIGGERS ###
#stores functions that trigger outside of the damage step
misc_effects = {}

### CARD EFFECT DICT ###
card_effect_dict = {}


### CARD TUPLES ###
card = namedtuple('card', ['display_name', 'card_id', 'speed', 'power', 'dmg', 'is_dmg_bool'])

#Thousand Slash Cascade
card_template = card("card_template", "card_template", "S", 0, 0, True)





#Resolution text
def resolution_text(card_id, base_dmg, win_bool):
    '''Returns either the dmg dealt and false for unique_bool or the unique resolution text and true'''
    #check if the resolution text needs to be unique

    if win_bool:
        if card_id == card_template.card_id:
            return True, ""
        
    #generic text
        return False, str(hub.calc_dmg(base_dmg, char_values["dmg_mod"]))
        #return just the damage if the resolution text is doing to be generic
    else:
        return False, "placeholder"
 

### DECK ###
deck_list = [(card_template, 8) ]
deck = [card for card, count in deck_list for _ in range(count)]

#BUGS
