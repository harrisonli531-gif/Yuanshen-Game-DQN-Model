from collections import namedtuple
import data_hub as hub
import random


### GENERIC VARIABLES ###
char_name = "Navia"
hand = []
target_values = {} #keeps track of which target character to target for effects

def get_deck_info():
    '''returns values related to passive'''
    return f" (Rosula Ammunition Shell: {rosula_ammunition})"

### CHAR VALUES AND CHAR SPECIFIC VARIABLES ###
char_values = {"hp": 25, 
               "dmg_mod": [[+0, 1000]], "pow_mod":[[+0, 1000]], "queued_mods" : [], 
               "queued_dmg" : None, 
               "player": None, "chosen_card": None, "is_ai" : False}

rosula_ammunition = 0 

ult_damage = 0

damage = 0 #crystalshot damage

finnese_bool = None #True if she creates shield and False is she discards

discarded_card = None
### CARD AND PASSIVE FUNCTIONS ###

# Passives and Outside Combat #

def gain_ammunition():
    '''Gains ammunition stacks at start of turn'''
    global rosula_ammunition
    rosula_ammunition += 1
   
 

def crystalshot_consume_shells():
    '''Consumes shells and boosts power of Navia's crystalshot volley'''
    global rosula_ammunition
    if char_values["chosen_card"].card_id == crystalshot.card_id:
        char_values["pow_mod"].append([2 * rosula_ammunition, 0])
        rosula_ammunition = 0

def finnese_shield():
    '''iF shield is created, create it before resolution phase'''
    global finnese_bool
    if target_values["chosen_card"].is_dmg_bool and hub.win_bools[char_values["player"]] and char_values["chosen_card"].card_id == flexible_finnese.card_id:
        finnese_bool = True
        target_values["dmg_mod"].append([-4, 0])

# Cards #
def crystalshot():
    global damage
    #get both player's power
    target_pow = target_values["chosen_card"].power + hub.get_mod_values(target_values, "pow_mod")
    navia_pow = char_values["chosen_card"].power + hub.get_mod_values(char_values, "pow_mod")
    #determine how much you won by
    excess_pow = navia_pow - target_pow
    if excess_pow == 1:
        damage = 1
    elif excess_pow == 2:
        damage = 2
    elif excess_pow == 3:
        damage = 3
    elif excess_pow == 4:
        damage = 6
    elif excess_pow == 5:
        damage = 9
    elif excess_pow >= 6:
        damage = 11
    
    total_dmg = hub.calc_dmg(damage, char_values["dmg_mod"]) 
    char_values["queued_dmg"] =  total_dmg


def blunt_refusal():
    total_dmg = hub.calc_dmg(blunt_refusal.dmg, char_values["dmg_mod"]) 
    char_values["queued_dmg"] =  total_dmg

def courteous_distance():
    target_values["queued_mods"].append(("pow", -2, 1))
    global rosula_ammunition
    rosula_ammunition += 1

def flexible_finnese(): #THIS ISN"T WORKING PROPERLY WHEN COMBINED WITH OTHER DMG MOD EFFECTS LIKE CORTEOUS DISTNACE OR MAYBE IT IS?
    global finnese_bool
    if not target_values["chosen_card"].is_dmg_bool:
        finnese_bool = False
        target_values["queued_mods"].append(("dmg", -3, 1))

def thorns(): 
        global discarded_card
        if target_values["player"] == "p1":
            if len(hub.p1_hand) > 0:
                discarded_card = hub.p1_hand.pop(random.randrange(0, len(hub.p1_hand))).display_name

        else:
            if len(hub.p2_hand) > 0:
                discarded_card = hub.p2_hand.pop(random.randrange(0, len(hub.p2_hand))).display_name
        
    

def singing_salvo():
    global ult_damage
    global rosula_ammunition
    if rosula_ammunition == 0:
        ult_damage = 0
    elif rosula_ammunition == 1:
        ult_damage = 1
    elif rosula_ammunition == 2:
        ult_damage = 3
    elif rosula_ammunition == 3:
        ult_damage = 6
    elif rosula_ammunition == 4:
        ult_damage = 10
    elif rosula_ammunition >= 5:
        ult_damage = 14
    total_dmg = hub.calc_dmg(ult_damage, char_values["dmg_mod"]) 
    char_values["queued_dmg"] =  total_dmg
    rosula_ammunition = 0

   


    
### TRIGGERS ###
#stores functions that trigger outside of the damage step
misc_effects = {"pre_action_1" : gain_ammunition,
                "pre_determine_winner_1" : crystalshot_consume_shells,
                "pre_resolve_cards_1": finnese_shield}

### CARD EFFECT DICT ###
card_effect_dict = {"crystalshot" : crystalshot,
                    "blunt_refusal" : blunt_refusal,
                    "courteous_distance" : courteous_distance,
                    "flexible_finnese": flexible_finnese,
                    "thorns": thorns,
                    "singing_salvo" : singing_salvo}


### CARD TUPLES ###
card = namedtuple('card', ['display_name', 'card_id', 'speed', 'power', 'dmg', 'is_dmg_bool'])

#Thousand Slash Cascade
crystalshot = card("Crystalshot Volley", "crystalshot", "S", 2, 0, True)

blunt_refusal = card("Blunt Refusal", "blunt_refusal", "M", 5, 2, True)

courteous_distance = card("Rules for Keeping a Courteous Distance", "courteous_distance", "S", 7, 0, False)

flexible_finnese = card("A Lady's Flexible Finnese", "flexible_finnese", "F", 1, 0, False)

thorns = card("Yellow Rose's Thorns", "thorns", "M", 7, 0, False)

singing_salvo = card("[Ultimate] The Spina's Singing Salvo", "singing_salvo", "S", 5, 0, True)



#Resolution text
def resolution_text(card_id, base_dmg, win_bool):
    '''Returns either the dmg dealt and false for unique_bool or the unique resolution text and true'''
    #check if the resolution text needs to be unique

    if win_bool:
        #I know these techinqually aren't unique resolution texts but I'm too lazy to ifnd a better to way to do this
        #so alas, spaghetti code :(
        if card_id == crystalshot.card_id:
            return False, str(char_values["queued_dmg"])
        if card_id == courteous_distance.card_id:
            return True, f"Navia gains another Rosula ammunition shell and uses evasive maneuvers to reduce her opponent's next attack by -2 power!"
        if card_id == flexible_finnese.card_id:
            if finnese_bool:
                return True, "A shield erupts from Navia's umbrella, blocking her opponent's attack!"
            else:
                #return True, f"Navia launches a disruptive counter attacking, discarding {discarded_card} from her opponent's hand!"
                return True, f"Navia preemptively counterattacks, reducing her opponent's damage next turn by -3!"
        if card_id == thorns.card_id:
            return True, f"Disarming, geo-manifested rose thorns root Navia's opponent in place! They lost a '{discarded_card}'!"
        if card_id == singing_salvo.card_id:
            return True, f"\"From the Spina with Love!\" Navia's supporting fire deals {char_values["queued_dmg"]} damage!"
        
    #generic text
        return False, str(char_values["queued_dmg"])
        #return just the damage if the resolution text is doing to be generic
    else:
        return False, "placeholder"
 

### DECK ###
deck_list = [(crystalshot, 8), (blunt_refusal, 6),(courteous_distance, 5), (flexible_finnese, 5),(thorns, 4), (singing_salvo, 2) ]
deck = [card for card, count in deck_list for _ in range(count)]

#BUGS
#whys her ult deal 14 damage with 6 shells consumed against ayato cascade *2
#her shotgun blast needs to snap shot their pow rather than doign the calculations based on when the card resolves since some cards can change the powers