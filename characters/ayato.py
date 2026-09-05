from collections import namedtuple
import data_hub as hub
import random


### GENERIC VARIABLES ###
char_name = "Ayato"
hand = []
target_values = {} #keeps track of which target character to target for effects

### CHAR VALUES AND CHAR SPECIFIC VARIABLES ###
char_values = {"hp": 25, 
               "dmg_mod": [[+0, 1000]], "pow_mod":[[+0, 1000]], "queued_mods" : [], 
               "queued_dmg" : None, 
               "player": None, "chosen_card": None, "is_ai" : False}

is_thousand_slash = False #whether or not thousand_slash was committed

### CARD AND PASSIVE FUNCTIONS ###

# Passives and Outside Combat #
def ebb_and_flow():
    '''Lets player commit cards'''
    global is_thousand_slash
    if len(hand) > 0:
        if char_values["is_ai"]:
            committed_card = random.randrange(0, len(hand))
        else:
            hub.print_space()
            print(f"[Passive] Ebb and Flow: Enter the index of the card (1 - {len(hand)}) you would like to commit or 0 for none:")
            committed_card = int(input(""))
        
    if (committed_card != 0):
        if hand[committed_card-1].card_id == thousand_slash.card_id:
            is_thousand_slash = True
        else:
            is_thousand_slash = False
        if hand[committed_card-1].card_id == garden.card_id:
            char_values["pow_mod"].append([2, 0])
        char_values["pow_mod"].append([hand.pop(committed_card-1).power, 0])
        
    else:
        is_thousand_slash = False
    
def passive_card_draw():
    if hub.other_values["round_ num"] != 1:
        drawn_card = random.choice(deck)
        hand.append(drawn_card)
        deck.remove(drawn_card)

# Cards #
def thousand_slash():
    if is_thousand_slash:
        char_values["dmg_mod"].append([2, 0])
    total_dmg = hub.calc_dmg(thousand_slash.dmg, char_values["dmg_mod"])
    char_values["queued_dmg"] =  total_dmg

def morning_blossoms():
    char_values["hp"] += 4

def lucid_rapids():
    char_values["queued_mods"].append(("pow", +4, 1))


def deluge():
    total_dmg = hub.calc_dmg(deluge.dmg, char_values["dmg_mod"])
    char_values["queued_dmg"] =  total_dmg

def garden():
    char_values["queued_mods"].append(("dmg", +1, 100))


    
### TRIGGERS ###
#stores functions that trigger outside of the damage step
misc_effects = {"post_action_1" : ebb_and_flow,
                "pre_action_1":passive_card_draw}

### CARD EFFECT DICT ###
card_effect_dict = {"thousand_slash" : thousand_slash,
                    "morning_blossoms" : morning_blossoms,
                    "garden" : garden,
                    "deluge" : deluge,
                    "lucid_rapids" : lucid_rapids}


### CARD TUPLES ###
card = namedtuple('card', ['display_name', 'card_id', 'speed', 'power', 'dmg', 'is_dmg_bool'])

#Thousand Slash Cascade
thousand_slash = card("Thousand Slash Cascade", "thousand_slash", "F", 1, 2, True)

morning_blossoms = card("As the Dew on Morning Blossoms", "morning_blossoms", "M", 3, 0, False)

#Deluge of Endless Flow[S][5]
deluge = card("Deluge of Endless Flow", "deluge", "S", 2, 6, True)

#Deluge of Endless Flow[S][5]
lucid_rapids = card("Lucid Rapids Circling the Summit", "lucid_rapids", "M", 3, 0, False)

#[Ultimate] Garden of Tranquil Waters[S][5]
garden = card("[Ultimate] Garden of Tranquil Waters", "garden", "S", 5, 0, False)

## MAP CARD ID TO NUMBER #
card_id_to_number = {
    thousand_slash.card_id : 0,
    morning_blossoms.card_id : 1,
    deluge.card_id : 2,
    lucid_rapids.card_id : 3,
    garden.card_id : 4
}

#Resolution text
def resolution_text(card_id, base_dmg, win_bool):
    '''Returns either the dmg dealt and false for unique_bool or the unique resolution text and true'''
    #check if the resolution text needs to be unique
    if win_bool:
        if card_id == morning_blossoms.card_id:
            return True, "Ayato gains 4 life!"
        elif card_id == garden.card_id:
            return True, "\"Be still!\" Ayato gains +1 damage for the rest of the match"
        elif card_id == lucid_rapids.card_id:
            return True, "Taking a moment, Ayato prepares himself, granting +4 power to his next attack"
    #generic text
        return False, str(char_values["queued_dmg"]) 
        #return just the damage if the resolution text is doing to be generic
    else:
        return False, "placeholder"
 

### DECK ###
deck_list = [(thousand_slash, 25), (lucid_rapids, 12),(morning_blossoms, 6), (deluge, 13),(garden, 4)]
deck = [card for card, count in deck_list for _ in range(count)]
