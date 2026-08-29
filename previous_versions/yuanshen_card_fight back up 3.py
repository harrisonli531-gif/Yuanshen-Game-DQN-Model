import characters.ayato as ayato
import characters.furina as furina
import random
import os 
from data_hub import *

def clear():    
    os.system('cls' if os.name == 'nt' else 'clear')


def check_input(user_input, valid_inputs):
    '''Takes user input and compares it to possible valid inputs. Loops until user enters something valid.
    user_input is a string while valid_inputs is a tuple'''
    
    user_input = user_input.strip()
    #print(len(user_input))
    while user_input not in valid_inputs or len(user_input) <= 0:
        try:
            user_input = user_input.lower()
            if user_input in valid_inputs:
                return user_input
            else:
                user_input = input(f"Error! Please enter a valid input! {valid_inputs}")
                print_space()
        except:
            user_input = input(f"Error! Please enter a valid input! {valid_inputs}")
            print_space()
    else:
        return user_input

def print_roster():
    '''prints roster of all characters'''
    
    print("Roster:")
    for i in range(len(roster)):
        print(f"{i+1}) {roster[i]}")
    print_space()

'''
function now located in data_hub module
def print_space():
    '#prints space and line for formatting
    print()
    print("----------------------------------------------------------")
    print()
'''
def welcome_screen(answer):
    '''The welcome screen where players are choose between playing '''

def round_start():
    '''sets up the start of the round (print hp, etc)'''

def print_char_info(answer):
    print_space()
    file_name = roster[int(answer)-1].lower() + ".txt"
    with open("C:\\Users\\falco\Documents\\Personal coding stuff\\Yuanshen Game\\character_text\\"+file_name, "r") as character_file:
        char_info = character_file.read()
        char_info = char_info.replace(">", "♦")
        char_info = char_info.replace("-", "◇")
        print(char_info)
    print_space()



#helps assign the right character to the right target value/"target"
char_map = { ayato.char_name : ayato,
                     furina.char_name : furina
}


#roster of characters
roster = [ayato.char_name, furina.char_name]


#loop through all possible choices for start menu
while True:
    #Start screen
    clear()
    print_space()
    print("Welcome!")
    print()
    print("Select an option: 1)Play 2)View Characters")
    print_space()
    user_input = input()
    clear()
    print_space()
    answer = check_input(user_input, ("1", "2"))

    #execute 
    if (answer == "1"):
      
        #answer = 1 means character select

        #get player character
        print_roster()
        print("Please select your character or \"0\" to exit.")
        user_input = input()
        print_space()
        clear()
        #hard code for now accepted inputs
        answer = check_input(user_input, tuple(str(i) for i in range(0, len(roster)+1)))
        if answer == "0":
            continue
        p_char_name = roster[int(answer)-1]
        p_char = char_map[p_char_name]
        #refers to hub variables like hub.p_hand (program can't just use p_char.hand directly)
        p_hand, p_deck, p_card_effect_dict, p_values, p_misc_effects = p_char.hand, p_char.deck, p_char.card_effect_dict, p_char.char_values, p_char.misc_effects
        print_space()
         
       
        #get opponent
        print_roster()
        print("Please select a character for your opponent.")
        user_input = input()
        clear()
        print_space()
        #hard code for now accepted inputs
        answer = check_input(user_input, tuple(str(i) for i in range(1, len(roster)+1)))
        op_char_name = roster[int(answer)-1]
        op_char = char_map[op_char_name]
        op_hand, op_deck, op_card_effect_dict, op_values, op_misc_effects = op_char.hand, op_char.deck, op_char.card_effect_dict, op_char.char_values, op_char.misc_effects
        op_char.char_values["is_ai"] = True
        print_space()
        clear()
        target_dict = {"p" : op_values, "op": p_values}
        p_char.target_values = target_dict["p"]
        op_char.target_values = target_dict["op"]

        
        break

    elif(answer == "2"):
      
        print_roster()
        print("Input \"0\" to exit.")
        user_input = input()
        clear()
        
        #hard code for now accepted inputs
        answer = check_input(user_input, tuple(str(i) for i in range(0, len(roster)+1)))
        while (answer != "0"):
            print_char_info(answer)
            print_roster()
            print("Please select who you would like to view. Input the number matching the character or \"0\" to exit.")
            user_input = input()
            answer = check_input(user_input, "0123456")
            print_space()
            clear()
 


#named tuples for cards? like the name, id, power, and speed, etc
#game start
#set up the match

#assign main_game variables to data_hub variables
#dictionary of effects that happen during each step of the game

op_board_text = ""
p_board_text = ""
round_phase = ""
#draw hand for player
for i in range(5):
    drawn_card = random.choice(p_deck)
    p_hand.append(drawn_card)
    p_deck.remove(drawn_card)


#draw hand for opponent
for i in range(5):
    drawn_card = random.choice(op_deck)
    op_hand.append(drawn_card)
    op_deck.remove(drawn_card)


#play the game, loop until loser
def display_board_state():
    '''prints out charcter hps, board state effects, and player hand'''
    #if character hp below 0, set it to zero to prevent program from blowing up
    if (op_values["hp"] < 0):
        op_values["hp"] = 0
    if (p_values["hp"]) < 0:
        p_values["hp"] = 0
    

    print_space()
    print(f"{op_char_name}(Opponent): [{op_values["hp"] * " ♥ "}]({op_values["hp"]}♥)")
    print("\n" * 2)
    print(op_board_text)
    print("\n" * 3)
    print(f"VS ({round_phase})")
    print("\n" * 3)
    print(p_board_text)
    print("\n" * 2)
    print(f"{p_char_name}(You): [{p_values["hp"] * " ♥ "}({p_values["hp"]}♥)]")
    print(f"\nYour hand: ")
    for i in range(len(p_hand)):
        print(f"{p_hand[i].display_name}", end=" | ")
    print(f"\n(Deck size = {len(p_deck)})")
    print_space()

def play_card_input():
    '''prompts player to either play a card or view character kit, returns the card they played'''
    make_choice = True
    while make_choice:
        display_board_state()
        print("1)Play a card 2)View character kit")
        user_input = input()
        answer = check_input(user_input, "12")
        print_space()
        if answer == "1":
             
            print(f"Which card would you like to play? Enter the index of the card (1 - {len(p_hand)}):")
            user_input = input()
            #set up possible inputs
            possible_inputs = ""
            for i in range(1, len(p_hand)+1):
                possible_inputs += str(i)

            answer = check_input(user_input, possible_inputs)
            chosen_card = p_hand.pop(int(answer)-1)
            
            return chosen_card
            
        if answer == "2":
            clear()
            print_char_info(roster.index(p_char_name) - 1)
            input("Enter any key to continue")
            print_space()
            clear()
         
    
def reveal_cards():
    '''reveals the chosen and played cards'''
    display_board_state()
    input("Enter any key to continue")
    clear()

def determine_winner():
    '''determines which cards resolve, returns player_win_bool and then op_win_bool'''
    speed_rankings = ["s", "m", "f"]
    op_speed = speed_rankings.index(op_chosen_card.speed)
    op_pow = op_chosen_card.power + get_mod_values(op_values, "pow_mod")
    p_speed = speed_rankings.index(p_chosen_card.speed)
    p_pow = p_chosen_card.power + get_mod_values(p_values, "pow_mod")

    p_win_bool = False
    op_win_bool = False
    #if player wins both speed and power
    if p_pow > op_pow:
        p_win_bool = True
    elif op_pow > p_pow:
        op_win_bool = True

    if p_speed > op_speed:
        p_win_bool = True
    elif op_speed > p_speed:
        op_win_bool = True
    
    return p_win_bool, op_win_bool

def resolve_cards(p_win, op_win):
    '''deals the damage, applies effects, etc.'''
    if (p_win):
        p_card_effect_dict[p_chosen_card.card_id]()
    if (op_win):
        op_card_effect_dict[op_chosen_card.card_id]()

def get_resolution_text(char, chosen_card, win_bool):
    '''Takes in the character, their chosen card, and whether or not they won'''
    unique_bool, text = char.resolution_text(chosen_card.card_id, chosen_card.dmg, win_bool)
    if win_bool:
        if unique_bool:
            #return the unique text 
            return text
        else:
            #return the preset damage
            return char.char_name + " deals " + text + " damage!"
    else:
        if unique_bool:
            return text
        else:
            return char.char_name + "'s attack fails!"
        
def clean_up_step():
    '''Tick down buff durations'''
    #clear player dmg and pow mods
    for i in range(len(p_values["pow_mod"]) -1, -1, -1):
        p_values["pow_mod"][i][1] -= 1
        if p_values["pow_mod"][i][1] <= 0:
            del p_values["pow_mod"][i]
    for i in range(len(p_values["dmg_mod"]) -1, -1, -1):
        p_values["dmg_mod"][i][1] -= 1
        if p_values["dmg_mod"][i][1] <= 0:
            del p_values["dmg_mod"][i]
    #clear op mods
    for i in range(len(op_values["pow_mod"]) -1, -1, -1):
        op_values["pow_mod"][i][1] -= 1
        if op_values["pow_mod"][i][1] <= 0:
            del op_values["pow_mod"][i]
    for i in range(len(op_values["dmg_mod"]) -1, -1, -1):
        op_values["dmg_mod"][i][1] -= 1
        if op_values["dmg_mod"][i][1] <= 0:
            del op_values["dmg_mod"][i]

def get_mod_values(player, mod_type):
    total = 0
    for mod in player[mod_type]:
        total += mod[0]
    return (total)

        
#run the actual game, go through phases
#print(ayato.target_values)
#print(op_values)
while p_values["hp"] > 0 and op_values["hp"] > 0:
    print_space()
    print(f"Round: {round_num})")
    print_space()
    input("Enter any key to continue")
    clear()

    #Start phase: reveal board state, start of round effects, etc
    #everything is displayed through play_card_input
    if round_num != 1:
        drawn_card = random.choice(p_deck)
        p_hand.append(drawn_card)
        p_deck.remove(drawn_card)
        #draw a card for opponent
        drawn_card = random.choice(op_deck)
        op_hand.append(drawn_card)
        op_deck.remove(drawn_card)

#draw hand for opponent

    

    #####Action phase: player choses a card to play
    round_phase = "Action Phase"
    p_chosen_card = play_card_input() #prompt player to play a card and stores it
    op_chosen_card = random.choice(op_hand) #chooses a random card for the opponent played card
    op_hand.pop(op_hand.index(op_chosen_card))
    #bandaid fix I guess?
    try:
      
        p_board_text = p_misc_effects["post_action"]()
    except:
        p_board_text = " "
    try:
        op_board_text = op_misc_effects["post_action"]()

    except:
        op_board_text = " "
    #print(op_values["pow_mod"])
    clear()

    ####Reveal phase: played cards with modifers are revealed
    #creating the proper display text for played cards
    round_phase = "Reveal Phase"
    p_board_text = p_chosen_card.display_name + "(+" + str(get_mod_values(p_values, "pow_mod")) + ")" 
    op_board_text = op_chosen_card.display_name + "(+" + str(get_mod_values(op_values, "pow_mod")) + ")"
    display_board_state()
    input("Enter any key to continue")
    clear()

    #theres an extra space around here somewhere ;-;

    ####Resolution phase: card effects are executed, winner is determined, damage is dealt, etc.
    round_phase = "Resolution Phase"
    p_win_bool, op_win_bool = determine_winner()
    resolve_cards(p_win_bool, op_win_bool)

    #creating proper display text based on win/lose
    p_board_text = get_resolution_text(p_char, p_chosen_card, p_win_bool) 
    op_board_text = get_resolution_text(op_char, op_chosen_card, op_win_bool) 

    display_board_state()
    print()
    input("Enter any key to continue")
    clear()
    p_board_text = " "
    op_board_text = " "

    #####End phase: resolves end of turn effects#####
    if p_values["hp"] < 0 or op_values["hp"] < 0: #break out of program, stop end phase if either character is dead/fallen
        break
    #p_board_text = p_misc_effects[""]
    #op_board_text = op_misc_effects[""]
    if p_board_text != " " and op_board_text != " ":
        display_board_state()
        input("Enter any key to continue")

    clear()
    p_board_text = " "
    op_board_text = " "
    
    #increase round count and reset temp modifier, assigns the card played this turn as "previously played card"
    round_num += 1
    
    clean_up_step()

if p_values["hp"] > 0 and op_values["hp"] <= 0:
    print_space()
    print(f"{p_char_name} wins!")
    print_space()
elif p_values["hp"] <= 0 and op_values["hp"] > 0:
    print_space()
    print(f"{op_char_name} wins!") 
    print_space()
else:
    print("Mutual Destruction! No one wins! Somehow...")
    print("Maybe check for bugs in code?")

