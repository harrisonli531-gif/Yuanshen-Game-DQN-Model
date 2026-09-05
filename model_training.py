import random
import data_hub as hub

#Characters
import characters.alhaitham as alhaitham
import characters.ayato as ayato
import characters.furina as furina
import characters.navia as navia
import characters.eula as eula

import torch
import torch.nn as nn
import copy
import opponent_model as om
import replay_buffer as buffer
import torch.optim as optim

import matplotlib.pyplot as plt

def check_input(user_input, valid_inputs):
    '''Takes user input and compares it to possible valid inputs. Loops until user enters something valid.
    user_input is a string while valid_inputs is a tuple'''
    
    user_input = user_input.strip()
  
    while user_input not in valid_inputs or len(user_input) <= 0:
        try:
            user_input = user_input.lower()
            if user_input in valid_inputs:
                return user_input
            else:
                user_input = input(f"Error! Please enter a valid input! {valid_inputs}")
                hub.print_space()
        except:
            user_input = input(f"Error! Please enter a valid input! {valid_inputs}")
            hub.print_space()
    else:
        return user_input

def print_roster():
    '''prints roster of all characters'''
    
    print("Roster:")
    for i in range(len(roster)):
        print(f"{i+1}) {roster[i]}")
    hub.print_space()

def welcome_screen(answer):
    '''The welcome screen where players are choose between playing '''

def round_start():
    '''sets up the start of the round (print hp, etc)'''

def print_char_info(answer):
    hub.print_space()
    file_name = roster[int(answer)-1].lower() + ".txt"
    with open("C:\\Users\\falco\Documents\\Personal coding stuff\\Yuanshen Game\\character_text\\"+file_name, "r") as character_file:
        char_info = character_file.read()
        char_info = char_info.replace(">", "♦")
        char_info = char_info.replace("~", "◇")
        print(char_info)
    hub.print_space()

def display_deck_info(char):
    '''Shows deck size and as well any other character specific values'''
    output = "\n"
    if char.char_values["player"] == "p1":
        output += "(Deck size = " + str(len(hub.p1_deck)) + ")"
    elif char.char_values["player"] == "p2":
        output += "(Deck size = " + str(len(hub.p2_deck)) + ")"
    
    try: #get the character's unique values to be displayed if any
        output += char.get_deck_info()
    except:
        pass
    return output


#helps assign the right character to the right target value/"target"
char_map = { alhaitham.char_name : alhaitham,
            ayato.char_name : ayato,
            eula.char_name : eula,
            furina.char_name : furina,
            navia.char_name : navia
}


#roster of characters
roster = [alhaitham.char_name, ayato.char_name, eula.char_name, furina.char_name, navia.char_name]


#loop through all possible choices for start menu
while True:
    #Start screen
    
    hub.print_space()
    print("Welcome!")
    print()
    print("Select an option: 1)Play 2)View Characters")
    hub.print_space()
    user_input = input()
    
    hub.print_space()
    answer = "1"

    #execute 
    if (answer == "1"):
      
        #answer = 1 means character select

        #get player character
        print_roster()
        print("Please select your character or \"0\" to exit.")
        user_input = input()
        answer = check_input(user_input, tuple(str(i) for i in range(0, len(roster)+1)))
        hub.print_space()
        
        if answer == "0":
            continue
        p1_char_name = roster[int(answer)-1]
        p1_char = char_map[p1_char_name]
        #refers to hub variables like hub.hub.p1_hand (program can't just use p1_char.hand directly)
        hub.p1_hand, hub.p1_deck, hub.p1_card_effect_dict, hub.p1_values, hub.p1_misc_effects = p1_char.hand, p1_char.deck, p1_char.card_effect_dict, p1_char.char_values, p1_char.misc_effects
        p1_char.char_values["is_ai"] = True
        hub.p1_values["player"] = "p1"
        hub.print_space()
         
       
        #get opponent
        print_roster()
        print("Please select a character for your opponent.")
        user_input = input()
        #hard code for now accepted inputs
        answer = check_input(user_input, tuple(str(i) for i in range(1, len(roster)+1)))
        
        hub.print_space()
        p2_char_name = roster[int(answer)-1]
        p2_char = char_map[p2_char_name]
        hub.p2_hand, hub.p2_deck, hub.p2_card_effect_dict, hub.p2_values, hub.p2_misc_effects = p2_char.hand, p2_char.deck, p2_char.card_effect_dict, p2_char.char_values, p2_char.misc_effects
        p2_char.char_values["is_ai"] = True
        hub.p2_values["player"] = "p2"

        hub.print_space()
        
        target_dict = {"p" : hub.p2_values, "op": hub.p1_values}
        p1_char.target_values = target_dict["p"]
        p2_char.target_values = target_dict["op"]
        
        
        break

    elif(answer == "2"):
      
        print_roster()
        print("Input \"0\" to exit.")
        user_input = input()
        #hard code for now accepted inputs
        answer = check_input(user_input, tuple(str(i) for i in range(0, len(roster)+1)))
        
        while (answer != "0"):
            print_char_info(answer)
            print_roster()
            print("Please select who you would like to view. Input the number matching the character or \"0\" to exit.")
            user_input = input()
            hub.print_space()
            answer = check_input(user_input, tuple(str(i) for i in range(0, len(roster)+1)))
            
 


#named tuples for cards? like the name, id, power, and speed, etc
#game start
#set up the match

#assign main_game variables to data_hub variables
#dictionary of effects that happen during each step of the game

p2_board_text = " "
p1_board_text = " "
round_phase = ""


#play the game, loop until loser
def display_board_state():
    global p1_board_text
    global p2_board_text
    '''prints out charcter hps, board state effects, and player hand'''
    #if character hp below 0, set it to zero to prevent program from blowing up
    if (hub.p2_values["hp"] < 0):
        hub.p2_values["hp"] = 0
    if (hub.p1_values["hp"]) < 0:
        hub.p1_values["hp"] = 0

    '''
    if p1_board_text is None:
        p1_board_text = " "
    if p2_board_text is None:
        p2_board_text = " "

    hub.print_space()
    print(f"{p2_char_name}(Opponent): [{hub.p2_values["hp"] * " ♥ "}]({hub.p2_values["hp"]}♥)")
    print(display_deck_info(p2_char))
    print("\n" * 2)
    print(p2_board_text)
    print("\n" * 3)
    print(f"VS ({round_phase})")
    print("\n" * 3)
    print(p1_board_text)
    print("\n" * 2)
    print(f"{p1_char_name}(You): [{hub.p1_values["hp"] * " ♥ "}({hub.p1_values["hp"]}♥)]")
    print(f"\nYour hand: ")
    for i in range(len(hub.p1_hand)):
        #if i % 5 == 0: #print out a space every five cards
            #print()
        print(f"{hub.p1_hand[i].display_name}[{hub.p1_hand[i].speed}][{hub.p1_hand[i].power}] ", end=" | ")
    print(display_deck_info(p1_char))
    hub.print_space()
    '''

def play_card_input():
    '''prompts player to either play a card or view character kit, returns the card they played'''
    make_choice = True
    while make_choice:
        display_board_state()
        print("1)Play a card 2)View character kit")
        user_input = input()
        answer = check_input(user_input, ("1", "2"))
        hub.print_space()
        if answer == "1":
             
            print(f"Which card would you like to play? Enter the index of the card (1 - {len(hub.p1_hand)}):")
            user_input = input()
            #set up possible inputs
            possible_inputs = tuple(str(x) for x in range(1, len(hub.p1_hand)+1))
            answer = check_input(user_input, possible_inputs)
            chosen_card = hub.p1_hand.pop(int(answer)-1)
            
            return chosen_card
            
        if answer == "2":
            
            print_char_info(roster.index(p1_char_name) + 1)
        
            hub.print_space()
            
         
    
def reveal_cards():
    '''reveals the chosen and played cards'''
    display_board_state()
    #input("Enter any key to continue")
    

def determine_winner():
    '''determines which cards resolve, returns player_win_bool and then p2_win_bool'''
    speed_rankings = ["S", "M", "F"]
    p2_speed = speed_rankings.index(p2_chosen_card.speed)
    p2_pow = p2_chosen_card.power + get_mod_values(hub.p2_values, "pow_mod")
    p1_speed = speed_rankings.index(p1_chosen_card.speed)
    p1_pow = p1_chosen_card.power + get_mod_values(hub.p1_values, "pow_mod")

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
        hub.p1_card_effect_dict[p1_chosen_card.card_id]()
    if (p2_win):
        hub.p2_card_effect_dict[p2_chosen_card.card_id]()

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
    for i in range(len(hub.p1_values["pow_mod"]) -1, -1, -1):
        if hub.p1_values["pow_mod"][i][1] <= 0:
            del hub.p1_values["pow_mod"][i]
            continue
        hub.p1_values["pow_mod"][i][1] -= 1
    for i in range(len(hub.p1_values["dmg_mod"]) -1, -1, -1):
        if hub.p1_values["dmg_mod"][i][1] <= 0:
            del hub.p1_values["dmg_mod"][i]
            continue
        hub.p1_values["dmg_mod"][i][1] -= 1
    #clear op mods
    for i in range(len(hub.p2_values["pow_mod"]) -1, -1, -1):
        if hub.p2_values["pow_mod"][i][1] <= 0:
            del hub.p2_values["pow_mod"][i]
            continue
        hub.p2_values["pow_mod"][i][1] -= 1
    for i in range(len(hub.p2_values["dmg_mod"]) -1, -1, -1):
        if hub.p2_values["dmg_mod"][i][1] <= 0:
            del hub.p2_values["dmg_mod"][i]
            continue
        hub.p2_values["dmg_mod"][i][1] -= 1
        

def get_mod_values(player, mod_type):
    total = 0
    for mod in player[mod_type]:
        total += mod[0]
    return (total)

def resolve_misc_triggers(step, display_text):
    '''Loops through all number hierachies in order to resolve needed triggers. Step is a string that represents the step like post_combat. Display_text is True 
    if need to assign something to board text. Maybe remove the global variable?'''
    global p1_board_text
    global p2_board_text
    for i in range(1, 6):
        if display_text == True:
            try:
                p1_board_text = hub.p1_misc_effects[f"{step}_{i}"]()
            except:
                pass
            try:
                p2_board_text = hub.p2_misc_effects[f"{step}_{i}"]()
            except:
                pass

        elif display_text == False:
            try:
                hub.p1_misc_effects[f"{step}_{i}"]()
            except:
                pass
            try:
                hub.p2_misc_effects[f"{step}_{i}"]()
            except:
                pass


def apply_queued_mods():
    '''Take all the mods queued up for each character add them to the coorposnding categories. Firs item in queued mod is type, then mod value, and duration'''
    players = [hub.p1_values, hub.p2_values]
    for p in players:
        for mod in p["queued_mods"]:
            if mod[0] == "pow":
                p["pow_mod"].append([mod[1], mod[2]])
            elif mod[0] == "dmg":
                p["dmg_mod"].append([mod[1], mod[2]])
        p["queued_mods"].clear()

def deal_dmg():
    '''If a player has damage thats to be dealt, it gets dealt to other player. Then both player's queued dmg is reset'''
    if hub.p2_values["queued_dmg"] != None:
        hub.p1_values["hp"] -= hub.p2_values["queued_dmg"]
    if hub.p1_values["queued_dmg"] != None:
        hub.p2_values["hp"] -= hub.p1_values["queued_dmg"]

def get_reward(prev_state, next_state, p1_win_bool, p2_win_bool):
    '''Calculates the reward for the player based on the previous state and the next state. Rewards for dealing damage, winning a round, or winning the game'''
    reward = 0
    if next_state[1] <= 0: #opponent has 0 hp
            reward = 1
    elif next_state[0] <= 0: #player has 0 hp
            reward = -1
    else:
        if prev_state[1] > next_state[1]: #deal damage
            reward = 0.1
        elif prev_state[0] > next_state[0]:
            reward = -0.1
        if p1_win_bool and not p2_win_bool:
            reward += 0.2
        elif p2_win_bool and not p1_win_bool:
            reward -= 0.2
    return reward

def draw_starting_hands():
    '''Draws the starting hands for both players'''
    # Draw hand for player
    for i in range(5):
        drawn_card = random.choice(hub.p1_deck)
        hub.p1_hand.append(drawn_card)
        hub.p1_deck.remove(drawn_card)

    # Draw hand for opponent
    for i in range(5):
        drawn_card = random.choice(hub.p2_deck)
        hub.p2_hand.append(drawn_card)
        hub.p2_deck.remove(drawn_card)

def reset_game_state():
    '''Resets the game state for a new episode'''
    hub.p1_values["hp"] = 25
    hub.p2_values["hp"] = 25
    hub.p1_hand.clear()
    hub.p2_hand.clear()
    hub.p1_deck.clear()
    hub.p2_deck.clear()
    hub.p1_deck[:] = [card for card, count in p1_char.deck_list for _ in range(count)]
    hub.p2_deck[:] = [card for card, count in p2_char.deck_list for _ in range(count)]
    hub.other_values["round_ num"] = 1
    hub.p1_values["pow_mod"][:] = [[+0, 1000]]
    hub.p1_values["dmg_mod"][:] = [[+0, 1000]]
    hub.p2_values["pow_mod"][:] = [[+0, 1000]]
    hub.p2_values["dmg_mod"][:] = [[+0, 1000]]
    for values in (hub.p1_values, hub.p2_values):
        values["queued_mods"].clear()
        values["queued_dmg"] = None
        values["chosen_card"] = None
    draw_starting_hands()

def pick_card_with_ai(current_state, model, epsilon=0.1):
    '''Picks a card for the player using the AI model'''
    #Explore
    if (random.random() < epsilon):
        return random.randint(0, len(hub.p1_hand) - 1)
    
    #Exploit
    #get q values for all cards in deck
    q_values = model(current_state)
    #iterate through the player's hand and find the card with the highest q value (from the generated q values)
    best_card_index = None
    best_q_value = -float('inf')
    for card in hub.p1_hand:
        if q_values[p1_char.card_id_to_number[card.card_id]] > best_q_value:
            best_q_value = q_values[p1_char.card_id_to_number[card.card_id]]
            best_card_index = hub.p1_hand.index(card)
    #return the card corresponding to the best action
    return best_card_index

def generate_predicted_target_q_values(model, target_model, experiences, gamma=0.99):
    '''Takes in a number of training experience and testing experiences. Uses prev_state of training experiences to generate predicted q values for each card in the player's deck. Then uses the next_state of the training experience to generate the target q values
    and next_state of testing experiences to generate target q values.'''
    predicted_q_list = []
    target_q_list = []
    for experience in experiences:
        #calculate predicted q value
        generated_q = model (experience[0]) #experience[0] is prev_state
        predicted_q_list.append(generated_q[experience[2]]) #experience[2] is card_played, get q value for the card played in that experience

        #calculate target q value
        with torch.no_grad():
            target_q = 0
            if experience[5]: #experience[5] is done
                target_q = experience[1]
            else:
                generated_q = target_model(experience[3]) #experience[3] is next_state
                max_q_value = generated_q[experience[4][0]] #experience[4] is next_hand
                for i in range(len(experience[4])): #find max q value for each playable card
                    if generated_q[experience[4][i]] > max_q_value:
                        max_q_value = generated_q[experience[4][i]]
                target_q = experience[1] + gamma * max_q_value
            target_q_list.append(target_q)

    return (torch.stack(predicted_q_list), torch.tensor(target_q_list, dtype=torch.float32))

#SET UP GAME VALUES

draw_starting_hands()
hub.other_values["round_ num"] = 1
prev_played_card = -1



#SET UP TRAINING RELATED VALUES
replay_buffer = buffer.replay_buffer(1000)
episodes = 10000
load_model = True

model = om.opponent_model(len(p1_char.deck_list)) #set up the model based on the number of unique cards in the player's deck
optimizer = optim.Adam(model.parameters(), lr=0.001)

if (load_model == True):
    checkpoint = torch.load(
        "model_checkpoint.pth",
        map_location="cpu",
        weights_only=True
    )
    model.load_state_dict(checkpoint["model_state_dict"])
    optimizer.load_state_dict(checkpoint["optimizer_state_dict"])

target_model = copy.deepcopy(model)
loss_function = nn.MSELoss()
batch_size = 64
target_update_interval = 250
epsilon_start = 1.0
epsilon_end = 0.1
epsilon_decay = 3000
gamma = 0.99
num_wins = 0
max_win_rate = 0
total_steps = 0


y_coordinates = []
for i in range(episodes):
    #print(f"Episode {i+1} of {episodes}")

    while hub.p1_values["hp"] > 0 and hub.p2_values["hp"] > 0:

        '''
        hub.print_space()
        print(f"Round: {hub.other_values["round_ num"]})")
        hub.print_space()
        '''
        

        #Start phase: reveal board state, start of round effects, etc

        resolve_misc_triggers("pre_action", False)

        #GET PREV_STATE
        prev_state = torch.tensor([hub.p1_values["hp"], hub.p2_values["hp"], hub.other_values["round_ num"], prev_played_card, get_mod_values(hub.p1_values, "pow_mod"), get_mod_values(hub.p1_values, "dmg_mod")], dtype=torch.float32)


        #####Action phase: player choses a card to play
        round_phase = "Action Phase"
        epsilon = epsilon_end + (epsilon_start - epsilon_end) * max(0, 1 - total_steps / epsilon_decay)
        p1_chosen_card = hub.p1_hand[pick_card_with_ai(prev_state, model, epsilon)] # PICK CARD HERE
        total_steps += 1
        hub.p1_hand.pop(hub.p1_hand.index(p1_chosen_card))

        
        card_played_num = p1_char.card_id_to_number[p1_chosen_card.card_id] 

        
        hub.p1_values["chosen_card"] = p1_chosen_card
        p2_chosen_card = random.choice(hub.p2_hand) #chooses a random card for the opponent played card
        hub.p2_values["chosen_card"] = p2_chosen_card
        hub.p2_hand.pop(hub.p2_hand.index(p2_chosen_card))
        p1_board_text, p2_board_text = " ", " "
        resolve_misc_triggers("post_action", True)


        
    
        resolve_misc_triggers("pre_determine_winner", False) #determine winner before revealing played cards
        hub.win_bools["p1"], hub.win_bools["p2"] = determine_winner()

        ####Reveal phase: played cards with modifers are revealed
        #creating the proper display text for played cards
        round_phase = "Reveal Phase"

        #display the chosen cards and their mods
        p1_pow_mod = get_mod_values(hub.p1_values, "pow_mod")
        if p1_pow_mod < 0:
            #don't display "+" if power mod is negative
            p1_board_text = p1_chosen_card.display_name + "[" + p1_chosen_card.speed + "]" + "[" + str(p1_chosen_card.power) + "]" + "(" + str(p1_pow_mod) + ")" 
        else:
            p1_board_text = p1_chosen_card.display_name + "[" + p1_chosen_card.speed + "]" + "[" + str(p1_chosen_card.power) + "]" + "(+" + str(p1_pow_mod) + ")" 

        p2_pow_mod = get_mod_values(hub.p2_values, "pow_mod")
        if p2_pow_mod < 0:
            p2_board_text = p2_chosen_card.display_name + "[" + p2_chosen_card.speed + "]" + "[" + str(p2_chosen_card.power) + "]" + "(" + str(p2_pow_mod) + ")" 
        else:
            p2_board_text = p2_chosen_card.display_name + "[" + p2_chosen_card.speed + "]" + "[" + str(p2_chosen_card.power) + "]" + "(+" + str(p2_pow_mod) + ")"

        display_board_state()
        #input("Enter any key to continue") 
        
        
        
        
        ####Resolution phase: card effects are executed, winner is determined, damage is dealt, etc.
        round_phase = "Resolution Phase"
        
        
        resolve_misc_triggers("pre_resolve_cards", False)

    
        resolve_cards(hub.win_bools["p1"], hub.win_bools["p2"])

        resolve_misc_triggers("pre_deal_dmg", False)
        deal_dmg() 

    

        #creating proper display text based on win/lose
        p1_board_text = get_resolution_text(p1_char, p1_chosen_card, hub.win_bools["p1"]) 
        p2_board_text = get_resolution_text(p2_char, p2_chosen_card, hub.win_bools["p2"]) 

        hub.p1_values["queued_dmg"] = None
        hub.p2_values["queued_dmg"] = None


        resolve_misc_triggers("post_resolution", False)

        display_board_state()

        resolve_misc_triggers("post_resolution_board_reveal", False)

        #GET NEXT STATE, PREV_PLAYED_CARD, NEXT_HAND, REWARD
        prev_played_card = p1_char.card_id_to_number[p1_chosen_card.card_id]
        next_hand = [p1_char.card_id_to_number[card.card_id] for card in hub.p1_hand]
        next_state = torch.tensor([hub.p1_values["hp"], hub.p2_values["hp"], hub.other_values["round_ num"], prev_played_card, get_mod_values(hub.p1_values, "pow_mod"), get_mod_values(hub.p1_values, "dmg_mod")], dtype=torch.float32)
        reward = get_reward(prev_state, next_state, hub.win_bools["p1"], hub.win_bools["p2"])
        replay_buffer.push(prev_state, reward, card_played_num, next_state, next_hand, hub.p1_values["hp"] <= 0 or hub.p2_values["hp"] <= 0)
    
        p1_board_text = " "
        p2_board_text = " "

        #####End phase: resolves end of turn effects#####
        if hub.p1_values["hp"] < 0 or hub.p2_values["hp"] < 0: #break out of program, stop end phase if either character is dead/fallen
            break
    
        p1_board_text, p2_board_text = " ", " "
        resolve_misc_triggers("pre_end", True)

        if (not p1_board_text is None and p1_board_text != " ") or (not p2_board_text is None and p2_board_text != " "):
            round_phase = "End Phase"
            display_board_state()


        

        p1_board_text = None
        p2_board_text = None
        
        #increase round count and reset temp modifier, assigns the card played this turn as "previously played card"
        hub.other_values["round_ num"] += 1

        draw_bool = True
        try:
            draw_bool = hub.p1_misc_effects["draw_phase"]()
        except:
            pass
        if draw_bool:
            if (len(hub.p1_deck) <= 0):
                #print("Player 1 deck is empty, cannot draw a card!")
                #print(hub.other_values["round_ num"])
                break
            else:
                drawn_card = random.choice(hub.p1_deck)
                hub.p1_hand.append(drawn_card)
                hub.p1_deck.remove(drawn_card)

        #draw a card for opponent
        draw_bool = True
        try:
            draw_bool = hub.p2_misc_effects["draw_phase"]()
        except:
            pass
        if draw_bool:
            if (len(hub.p2_deck) <= 0):
                #print("Player 2 deck is empty, cannot draw a card!")
                #print(hub.other_values["round_ num"])
                break
            else:
                drawn_card = random.choice(hub.p2_deck)
                hub.p2_hand.append(drawn_card)
                hub.p2_deck.remove(drawn_card)

        apply_queued_mods()
        clean_up_step()

    
    if hub.p1_values["hp"] > 0 and hub.p2_values["hp"] <= 0:
        num_wins += 1

   


    #Reset the game state
    reset_game_state()
    prev_played_card = -1
    #replay_buffer.print()

    #calculate loss and perform back progagation
    if (len(replay_buffer.buffer) < 64): #don't try to sample if not enough experiences in the replay buffer
        continue

    predicted_target_q_values = generate_predicted_target_q_values(
        model, target_model, replay_buffer.sample(batch_size), gamma
    )
    loss = loss_function(predicted_target_q_values[0], predicted_target_q_values[1])
    loss.backward()
    torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
    optimizer.step()
    optimizer.zero_grad()
    if (i + 1) % 100 == 0:
        win_rate = 100 * num_wins / 100
        print(f"Episode {i+1} of {episodes} Loss: {loss.item():.4f}, Win Rate: {win_rate:.1f}%, Epsilon: {epsilon:.3f}")
        y_coordinates.append(win_rate)
        if win_rate > max_win_rate:
            max_win_rate = win_rate
            torch.save({
                'episode': i + 1,
                'win_rate': win_rate,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
            }, 'best_model_checkpoint.pth')
        num_wins = 0

    if (i + 1) % target_update_interval == 0:
            target_model.load_state_dict(model.state_dict())

x_coordinates = [x for x in range(100, 10100, 100)]
plt.plot(x_coordinates, y_coordinates)
plt.show()

checkpoint = {
    'model_state_dict': model.state_dict(),
    'optimizer_state_dict': optimizer.state_dict(),
}
torch.save(checkpoint, 'model_checkpoint.pth')
    