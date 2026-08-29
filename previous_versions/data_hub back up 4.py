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
    return base_dmg + total_mod
    
#dictionary of effects that happen during each step of the game
p_misc_effects = {}
op_misc_effects = {}
#modifiers, passive stacks, etc.
p_values = {}
op_values = {}
#dictionary of all cards in player's character's deck
p_card_effect_dict = {}
p_hand = []
p_deck = []
op_card_effect_dict = {}
op_hand = []
op_deck = []

#other game variables
drawn_card = None
round_num = 0

p_chosen_card = None
op_chosen_card = None
p_win_bool, op_win_bool = None, None
