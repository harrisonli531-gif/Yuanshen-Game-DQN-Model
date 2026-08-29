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

def display_deck_info(char):
    '''Shows deck size and as well any other character specific values'''
    output = "\n"
    if char.char_values["player"] == "p1":
        output += "(Deck size = " + str(len(p1_deck)) + ")"
    elif char.char_values["player"] == "p2":
        output += "(Deck size = " + str(len(p2_deck)) + ")"
    
    try: #get the character's unique values to be displayed if any
        output += char.get_deck_info()
    except:
        pass
    return output


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
        p1_char_name = roster[int(answer)-1]
        p1_char = char_map[p1_char_name]
        #refers to hub variables like hub.p1_hand (program can't just use p1_char.hand directly)
        p1_hand, p1_deck, p1_card_effect_dict, p1_values, p1_misc_effects = p1_char.hand, p1_char.deck, p1_char.card_effect_dict, p1_char.char_values, p1_char.misc_effects
        p1_values["player"] = "p1"
        print_space()
         
       
        #get opponent
        print_roster()
        print("Please select a character for your opponent.")
        user_input = input()
        clear()
        print_space()
        #hard code for now accepted inputs
        answer = check_input(user_input, tuple(str(i) for i in range(1, len(roster)+1)))
        p2_char_name = roster[int(answer)-1]
        p2_char = char_map[p2_char_name]
        p2_hand, p2_deck, p2_card_effect_dict, p2_values, p2_misc_effects = p2_char.hand, p2_char.deck, p2_char.card_effect_dict, p2_char.char_values, p2_char.misc_effects
        p2_char.char_values["is_ai"] = True
        p2_values["player"] = "p2"

        print_space()
        clear()
        target_dict = {"p" : p2_values, "op": p1_values}
        p1_char.target_values = target_dict["p"]
        p2_char.target_values = target_dict["op"]
        
        
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

p2_board_text = ""
p1_board_text = ""
round_phase = ""
#draw hand for player
for i in range(5):
    drawn_card = random.choice(p1_deck)
    p1_hand.append(drawn_card)
    p1_deck.remove(drawn_card)


#draw hand for opponent
for i in range(5):
    drawn_card = random.choice(p2_deck)
    p2_hand.append(drawn_card)
    p2_deck.remove(drawn_card)


#play the game, loop until loser
def display_board_state():
    '''prints out charcter hps, board state effects, and player hand'''
    #if character hp below 0, set it to zero to prevent program from blowing up
    if (p2_values["hp"] < 0):
        p2_values["hp"] = 0
    if (p1_values["hp"]) < 0:
        p1_values["hp"] = 0
    

    print_space()
    print(f"{p2_char_name}(Opponent): [{p2_values["hp"] * " ♥ "}]({p2_values["hp"]}♥)")
    print(display_deck_info(p2_char))
    print("\n" * 2)
    print(p2_board_text)
    print("\n" * 3)
    print(f"VS ({round_phase})")
    print("\n" * 3)
    print(p1_board_text)
    print("\n" * 2)
    print(f"{p1_char_name}(You): [{p1_values["hp"] * " ♥ "}({p1_values["hp"]}♥)]")
    print(f"\nYour hand: ")
    for i in range(len(p1_hand)):
        print(f"{p1_hand[i].display_name}[{p1_hand[i].speed}]({p1_hand[i].power}) ", end=" | ")
    print(display_deck_info(p1_char))
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
             
            print(f"Which card would you like to play? Enter the index of the card (1 - {len(p1_hand)}):")
            user_input = input()
            #set up possible inputs
            possible_inputs = ""
            for i in range(1, len(p1_hand)+1):
                possible_inputs += str(i)

            answer = check_input(user_input, possible_inputs)
            chosen_card = p1_hand.pop(int(answer)-1)
            
            return chosen_card
            
        if answer == "2":
            clear()
            print_char_info(roster.index(p1_char_name) - 1)
            input("Enter any key to continue")
            print_space()
            clear()
         
    
def reveal_cards():
    '''reveals the chosen and played cards'''
    display_board_state()
    input("Enter any key to continue")
    clear()

def determine_winner():
    '''determines which cards resolve, returns player_win_bool and then p2_win_bool'''
    speed_rankings = ["S", "M", "F"]
    p2_speed = speed_rankings.index(p2_chosen_card.speed)
    p2_pow = p2_chosen_card.power + get_mod_values(p2_values, "pow_mod")
    p1_speed = speed_rankings.index(p1_chosen_card.speed)
    p1_pow = p1_chosen_card.power + get_mod_values(p1_values, "pow_mod")

    p1_win_bool = False
    p2_win_bool = False
    #if player wins both speed and power
    if p1_pow > p2_pow:
        p1_win_bool = True
    elif p2_pow > p1_pow:
        p2_win_bool = True

    if p1_speed > p2_speed:
        p1_win_bool = True
    elif p2_speed > p1_speed:
        p2_win_bool = True
    return p1_win_bool, p2_win_bool

def resolve_cards(p1_win, p2_win):
    '''deals the damage, applies effects, etc.'''
    if (p1_win):
        p1_card_effect_dict[p1_chosen_card.card_id]()
    if (p2_win):
        p2_card_effect_dict[p2_chosen_card.card_id]()

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
    for i in range(len(p1_values["pow_mod"]) -1, -1, -1):
        p1_values["pow_mod"][i][1] -= 1
        if p1_values["pow_mod"][i][1] <= 0:
            del p1_values["pow_mod"][i]
    for i in range(len(p1_values["dmg_mod"]) -1, -1, -1):
        p1_values["dmg_mod"][i][1] -= 1
        if p1_values["dmg_mod"][i][1] <= 0:
            del p1_values["dmg_mod"][i]
    #clear op mods
    for i in range(len(p2_values["pow_mod"]) -1, -1, -1):
        p2_values["pow_mod"][i][1] -= 1
        if p2_values["pow_mod"][i][1] <= 0:
            del p2_values["pow_mod"][i]
    for i in range(len(p2_values["dmg_mod"]) -1, -1, -1):
        p2_values["dmg_mod"][i][1] -= 1
        if p2_values["dmg_mod"][i][1] <= 0:
            del p2_values["dmg_mod"][i]

def get_mod_values(player, mod_type):
    total = 0
    for mod in player[mod_type]:
        total += mod[0]
    return (total)

        
#run the actual game, go through phases
#print(ayato.target_values)
#print(p2_values)
round_num = 1
while p1_values["hp"] > 0 and p2_values["hp"] > 0:
    print_space()
    print(f"Round: {round_num})")
    print_space()
    input("Enter any key to continue")
    clear()

    #Start phase: reveal board state, start of round effects, etc
    #everything is displayed through play_card_input
    if round_num != 1:
        drawn_card = random.choice(p1_deck)
        p1_hand.append(drawn_card)
        p1_deck.remove(drawn_card)
        #draw a card for opponent
        drawn_card = random.choice(p2_deck)
        p2_hand.append(drawn_card)
        p2_deck.remove(drawn_card)

#draw hand for opponent
    try:
        p1_misc_effects["pre_action"]()
    except:
        pass

    try:
        p2_misc_effects["pre_action"]()
    except:
        pass
    

    #####Action phase: player choses a card to play
    round_phase = "Action Phase"
    p1_chosen_card = play_card_input() #prompt player to play a card and stores it
    p2_chosen_card = random.choice(p2_hand) #chooses a random card for the opponent played card
    p2_hand.pop(p2_hand.index(p2_chosen_card))
    #bandaid fix I guess?
    try:
      
        p1_board_text = p1_misc_effects["post_action"]()
    except:
        p1_board_text = " "
    try:
        p2_board_text = p2_misc_effects["post_action"]()

    except:
        p2_board_text = " "
    #print(p2_values["pow_mod"])
    clear()

    ####Reveal phase: played cards with modifers are revealed
    #creating the proper display text for played cards
    round_phase = "Reveal Phase"
    p1_board_text = p1_chosen_card.display_name + "[" + p1_chosen_card.speed + "]" + "(" + str(p1_chosen_card.power) + ")" + "(+" + str(get_mod_values(p1_values, "pow_mod")) + ")" 
    p2_board_text = p2_chosen_card.display_name + "[" + p2_chosen_card.speed + "]" + "(" + str(p2_chosen_card.power) + ")" +"(+" + str(get_mod_values(p2_values, "pow_mod")) + ")"
    display_board_state()
    input("Enter any key to continue")
    clear()

    #theres an extra space around here somewhere ;-;

    ####Resolution phase: card effects are executed, winner is determined, damage is dealt, etc.
    round_phase = "Resolution Phase"
    p1_win_bool, p2_win_bool = determine_winner()
    resolve_cards(p1_win_bool, p2_win_bool)

    #creating proper display text based on win/lose
    p1_board_text = get_resolution_text(p1_char, p1_chosen_card, p1_win_bool) 
    p2_board_text = get_resolution_text(p2_char, p2_chosen_card, p2_win_bool) 

    display_board_state()
    print()
    furina.test()
    input("Enter any key to continue")
    clear()
    p1_board_text = " "
    p2_board_text = " "

    #####End phase: resolves end of turn effects#####
    if p1_values["hp"] < 0 or p2_values["hp"] < 0: #break out of program, stop end phase if either character is dead/fallen
        break
   
    try:
        p1_board_text = p1_misc_effects["post_resolution"]()
    except:
        p1_board_text = None
    try:
        p2_board_text = p2_misc_effects["post_resolution"]()


    except:
        p2_board_text = None

    if p1_board_text != None or p2_board_text != None:
        display_board_state()
        input("Enter any key to continue")

    clear()

    p1_board_text = " "
    p2_board_text = " "
    
    #increase round count and reset temp modifier, assigns the card played this turn as "previously played card"
    round_num += 1
    
    clean_up_step()

if p1_values["hp"] > 0 and p2_values["hp"] <= 0:
    print_space()
    print(f"{p1_char_name} wins!")
    print_space()
elif p1_values["hp"] <= 0 and p2_values["hp"] > 0:
    print_space()
    print(f"{p2_char_name} wins!") 
    print_space()
else:
    print("Mutual Destruction! No one wins! Somehow...")
    print("Maybe check for bugs in code?")

