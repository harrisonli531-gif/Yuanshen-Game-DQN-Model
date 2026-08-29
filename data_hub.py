import os 

def clear():    
    os.system('cls' if os.name == 'nt' else 'clear')

def print_space():
    #prints space and line for formatting
    print()
    print("----------------------------------------------------------")
    print()

def calc_dmg(base_dmg, dmg_mod):
    total_mod = 0
    for mod in dmg_mod:
        total_mod += mod[0]
    if (base_dmg + total_mod) < 0:
        return 0
    return base_dmg + total_mod

def get_mod_values(player, mod_type):
    '''Take in the player and dmg or pow mod and return total bonus'''
    total = 0
    for mod in player[mod_type]:
        total += mod[0]
    return (total)
    
#dictionary of effects that happen during each step of the game
p1_misc_effects = {}
p2_misc_effects = {}
#modifiers, passive stacks, etc.
p1_values = {}
p2_values = {}
#dictionary of all cards in player's character's deck
p1_card_effect_dict = {}
p1_hand = []
p1_deck = []
p2_card_effect_dict = {}
p2_hand = []
p2_deck = []

#other game variables
drawn_card = None

win_bools = {"p1": None , "p2": None} 
other_values = {"round_num" : 0}
