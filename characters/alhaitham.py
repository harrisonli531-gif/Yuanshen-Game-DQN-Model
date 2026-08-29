from collections import namedtuple
import data_hub as hub
import random


### GENERIC VARIABLES ###
char_name = "Alhaitham"
hand = []
target_values = {} #keeps track of which target character to target for effects


def get_deck_info():
    '''returns values related to passive'''
    count_mirrors()
    return f" (Chisal Mirror Reflections in Hand: {chisal_mirror_num})"

### CHAR VALUES AND CHAR SPECIFIC VARIABLES ###
char_values = {"hp": 25, 
               "dmg_mod": [[+0, 1000]], "pow_mod":[[+0, 1000]], "queued_mods" : [], 
               "queued_dmg" : None, 
               "player": None, "chosen_card": None, "is_ai" : False}

chisal_mirror_num = 0

double_strike = None

marked = False

mark_explode = False

refutation_shield_bool = None #is shield created?

op_hp = None #snap shot the op's hp before cards are resolved, based on when the cards are played

scrutiny_trigger = None #Tracks if scrutiny effect needs to be applied this turn. Very unintiative
op_mods = [] #stores the op mods when they are taken away by scrutiny

sagacity_trigger_bool = False #whether or not the sagacity effect needs to be resolved this turn

sagacity_new_card = None #which card was added

mirror_count = 0 #number of mirror reflections discarded 

damage_instance = 0 #damage instances for his ult

### CARD AND PASSIVE FUNCTIONS ###

# Passives and Outside Combat #

def create_chisal_mirror():
    '''try to create a chisal mirror of played card'''
    n = random.randint(1, 10)
    if n <= 5:
        if "mirror" not in char_values["chosen_card"].card_id and char_values["chosen_card"].card_id != synthesis.card_id:
            hand.append(chisel_mirror_reflections[char_values["chosen_card"].card_id])
            return f"Alhaitham creates a chisel mirror reflection of {char_values['chosen_card'].display_name} in hand!"
    return None

def debate_pow_mod():
    '''Add extra power if opponent's card is slow'''
    if target_values["chosen_card"].speed == "S" and (char_values["chosen_card"].card_id == debate.card_id or char_values["chosen_card"].card_id == debate_mirror.card_id):
        char_values["pow_mod"].append([2, 0])

def count_mirrors():
    '''Counts number of mirrors in hand to display'''
    global chisal_mirror_num
    chisal_mirror_num = 0
    for card in hand:
        if "mirror" in card.card_id:
            chisal_mirror_num += 1 

def add_mark_dmg(dmg_dealt = 0):
    '''Check if mark is consumed and add dmg if yes'''
    global marked
    global mark_explode 
    mark_explode = False
    if marked and (dmg_dealt > 0):
        marked = False
        mark_explode = True
        dmg = hub.calc_dmg(4, char_values["dmg_mod"])
        if dmg < 0:
            dmg = 0
        return dmg
    marked = False
    return 0

def refutation_shield(): #Its sometimes counter attacking even with opponent usng a damaging attack (like navia's crystashot volley and spinas singing salvo)
    '''iF shield is created, create it before resolution phase'''
    global refutation_shield_bool
    if target_values["chosen_card"].is_dmg_bool and hub.win_bools[char_values["player"]] and (char_values["chosen_card"].card_id == refutation.card_id or char_values["chosen_card"].card_id == refutation_mirror.card_id):
        refutation_shield_bool = True
        target_values["dmg_mod"].append([-3, 0])
    
def snapshot_op_hp():
    global op_hp 
    op_hp = target_values["hp"]

def pre_action():
    count_mirrors()
    snapshot_op_hp()

def pre_end():
    '''Creates mirrors and recounts total number. Also returns op mods if scrutiny effect was applied'''
    output = create_chisal_mirror()
    count_mirrors()
    #return_scrutiny()
    if output != None:
        output += " " + sagacity_output_txt()
    else:
        output = sagacity_output_txt()

    if hub.win_bools[char_values["player"]] == False:
        global marked
        marked = False
    
    
    return output

def sagacity_output_txt():
    '''Create endstep text if sagacity resolved'''
    if sagacity_new_card != None:
        if sagacity_new_card == debate.card_id:
            return "Alhaitham shifts to an offensive stance and draws a 'Debate'!"
        else:
            return "Alhaitham shifts to an defensive stance and draws an 'Intuition'!"
    return " "

def scrutiny_pow_effect():
    '''Applies the scrutiny effect if the card was played last turn'''
    global scrutiny_trigger
    if scrutiny_trigger == 2:
        for mod in target_values["pow_mod"]:#so it doesn't remove the default the default mod
            if mod[0] != 0:
                target_values["queued_mods"].append(mod)
        target_values["pow_mod"].clear() 
        scrutiny_trigger -= 1

def scrutiny_dmg_effect():
    global scrutiny_trigger
    if scrutiny_trigger == 1:
        for mod in target_values["dmg_mod"]:
            if mod[0] != 0: #so it doesn't remove the default the default mod
                target_values["queued_mods"].append(mod)
        target_values["dmg_mod"].clear()
        scrutiny_trigger -= 1
        
'''
def scrutiny_effect():
   
    global scrutiny_trigger 
    global op_mods
    if scrutiny_trigger:
        op_mods.append(target_values["pow_mod"][:])
        op_mods.append(target_values["dmg_mod"][:])
        target_values["pow_mod"], target_values["dmg_mod"] = [[+0, 1000]], [[+0, 1000]]
        scrutiny_trigger = False


def return_scrutiny():
    Returns mods 
    if len(op_mods) > 0:
        target_values["pow_mod"], target_values["dmg_mod"] = op_mods[0], op_mods[1]
        op_mods.clear()
'''

def check_mirror_played():
    '''If mirror reflection was played, don't draw card for turn'''
    if "mirror" in char_values["chosen_card"].card_id:
        
        return False
    return True

def sagacity_trigger():
    '''Discard a card and draw the cooresponding card '''
    global sagacity_trigger_bool
    global sagacity_new_card 
    if sagacity_trigger_bool:
    
        if len(hand) > 0:
            if char_values["is_ai"]:
                discarded_card = random.randrange(len(hand))
            else:
                print(f"Enter the index of the card (1 - {len(hand)}) you would like to discard for Sagacity or 0 for none:")
                discarded_card = int(input(""))
                hub.print_space()
        if (discarded_card != 0):
            discarded_type = hand.pop(discarded_card-1).is_dmg_bool
            if discarded_type == True: #if the card IS a damage dealing type
                hand.append(intuition)
                sagacity_new_card = intuition.card_id
            elif discarded_type == False:
                hand.append(debate)
                sagacity_new_card = debate.card_id
           
                
       
            
        
        sagacity_trigger_bool = False
    else:
        sagacity_new_card = None



# Cards #
def debate():
    total_dmg = hub.calc_dmg(debate.dmg, char_values["dmg_mod"])
    total_dmg += add_mark_dmg(total_dmg)
    char_values["queued_dmg"] = total_dmg

def elucidation():
    global double_strike #double strike tracks if this ability hits twice
    double_strike = False
    total_dmg = hub.calc_dmg(elucidation.dmg, char_values["dmg_mod"]) #get the damage
    if op_hp > char_values["hp"]: #if op has more health
        double_strike = True
        total_dmg += hub.calc_dmg(1, char_values["dmg_mod"]) #strike again
    total_dmg += add_mark_dmg(total_dmg) #check if mark from causality is relevant
    char_values["queued_dmg"] = total_dmg
  #deal the damage

def causality():
    total_dmg = hub.calc_dmg(causality.dmg, char_values["dmg_mod"])
    total_dmg += add_mark_dmg(total_dmg)
    char_values["queued_dmg"] = total_dmg
    global marked
    marked = True
    

def refutation(): #WHY COUNTER ATTACKING NAVIA'S Crystalshot volley
    global refutation_shield_bool
    if target_values["chosen_card"].is_dmg_bool == False:
        refutation_shield_bool = False
        total_dmg = hub.calc_dmg(refutation.dmg, char_values["dmg_mod"])
        total_dmg += add_mark_dmg(total_dmg)
        char_values["queued_dmg"] = total_dmg
    else:
        add_mark_dmg()


def scrutiny():
    global scrutiny_trigger 
    scrutiny_trigger = 2

def intuition():
    char_values["queued_mods"].append(("dmg", +1, 1))
    char_values["queued_mods"].append(("pow", +3, 1))


def sagacity():
    global sagacity_trigger_bool
    sagacity_trigger_bool = True

def synthesis():
    global mirror_count
    mirror_count = 0
    for i in range(len(hand) -1, -1, -1):
        if "mirror" in hand[i].card_id:
            del hand[i]
            mirror_count += 1
    global damage_instance
    damage_instance = mirror_count + 1
    '''
    if mirror_count == 0:
        damage_instance = 1
    elif mirror_count == 1:
        damage_instance = 2
    elif mirror_count == 2:
        damage_instance = 4
    elif mirror_count == 3:
        damage_instance = 5
    elif mirror_count >= 4:
        damage_instance = 6
    '''
    total_dmg = hub.calc_dmg(synthesis.dmg, char_values["dmg_mod"]) * damage_instance
    total_dmg += add_mark_dmg(total_dmg)
    char_values["queued_dmg"] = total_dmg


    
             


    
### TRIGGERS ###
#stores functions that trigger outside of the damage step
misc_effects = {"pre_action_5" : pre_action,
                "pre_resolve_cards_1": refutation_shield,
                "pre_determine_winner_1" : debate_pow_mod,
                "pre_end_1" : pre_end,
                "pre_determine_winner_5" : scrutiny_pow_effect,
                "pre_deal_dmg_5" : scrutiny_dmg_effect,
                "draw_phase" : check_mirror_played,
                "post_resolution_board_reveal_1": sagacity_trigger}
#"post_resolution" : count_mirrors,


### CARD EFFECT DICT ###
card_effect_dict = {"debate" : debate,
                    "debate_mirror" : debate,
                    "elucidation" : elucidation,
                    "elucidation_mirror" : elucidation,
                    "causality" : causality,
                    "causality_mirror" : causality,
                    "refutation" : refutation,
                    "refutation_mirror" : refutation,
                    "scrutiny" : scrutiny,
                    "scrutiny_mirror" : scrutiny,
                    "intuition" : intuition,
                    "intuition_mirror" : intuition,
                    "sagacity" : sagacity,
                    "sagacity_mirror" : sagacity,
                    "synthesis" : synthesis
}


### CARD TUPLES ###
card = namedtuple('card', ['display_name', 'card_id', 'speed', 'power', 'dmg', 'is_dmg_bool'])

#Thousand Slash Cascade
debate = card("Debate", "debate", "M", 5, 4, True)
debate_mirror = card("Chisal Mirror Reflection: Debate", "debate_mirror", "M", 3, 4, True)

elucidation = card("Elucidation", "elucidation", "F", 4, 2, True)
elucidation_mirror = card("Chisal Mirror Reflection: Elucidation", "elucidation_mirror", "F", 2, 2, True)

causality = card("Causality", "causality", "F", 5, 1, True)
causality_mirror = card("Chisal Mirror Reflection: Causality", "causality_mirror", "F", 3, 1, True)

refutation = card("Refutation", "refutation", "F", 3, 3, True)
refutation_mirror = card("Chisal Mirror Reflection: Refutation", "refutation_mirror", "F", 1, 3, True)

scrutiny = card("Scrutiny", "scrutiny", "S", 7, 0, False)
scrutiny_mirror = card("Chisal Mirror Reflection: Scrutiny", "scrutiny_mirror", "S", 5, 0, False)

intuition = card("Intuition", "intuition", "M", 6, 0, False)
intuition_mirror = card("Chisal Mirror Reflection: Intuition", "intuition_mirror", "M", 4, 0, False)

sagacity = card("Sagacity", "sagacity", "S", 8, 0, False)
sagacity_mirror = card("Chisal Mirror Reflection: Sagacity", "sagacity_mirror", "S", 6, 0, False)

synthesis = card("[Ultimate] Synthesis: the Demonstration of Principle", "synthesis", "F", 3, 1, True)

chisel_mirror_reflections = {debate.card_id : debate_mirror,
    elucidation.card_id : elucidation_mirror,
    causality.card_id : causality_mirror,
    refutation.card_id : refutation_mirror,
    scrutiny.card_id : scrutiny_mirror,
    intuition.card_id : intuition_mirror,
    sagacity.card_id: sagacity_mirror}

#Resolution text
def resolution_text(card_id, base_dmg, win_bool):
    '''Returns either the dmg dealt and false for unique_bool or the unique resolution text and true'''
    #check if the resolution text needs to be unique
    global mark_explode
    #EXTRA MARKED DAMAGE DOES DISPLAY WITH THIS CODE
    output = ""
    if win_bool:
        if (card_id == scrutiny.card_id or card_id == scrutiny_mirror.card_id):
            return True, f"Alhaitham has removes this opponent's modifers!"
        
        if mark_explode:
            
            
            output += f" His mark also explodes for {hub.calc_dmg(4, char_values["dmg_mod"])} damage!"
           

        if (card_id == elucidation.card_id or card_id == elucidation_mirror.card_id) and double_strike:
            output = f"Alhaitham swings his swords twice for {char_values["queued_dmg"]} total damage!" + output
            mark_explode = False
            return True, output
        elif (card_id == refutation.card_id or card_id == refutation_mirror.card_id):
            if refutation_shield_bool:
                output = "Alhaitham manifests a mirror prism shield, blocking damage from each attack!" + output
            else:
                output = f"Alhaitham counter attacks for {char_values["queued_dmg"]} damage!" + output
            mark_explode = False
            return True, output
        elif (card_id == causality.card_id or card_id == causality_mirror.card_id):
            output = f"Alhaitham deals {char_values["queued_dmg"]} damage and creates a mark!" + output
            mark_explode = False
            return True, output
        
        elif (card_id == synthesis.card_id):
            output = f"\"Scatter.\" Alhaitham creates a field with {mirror_count} chisal mirrors and deals {char_values["queued_dmg"]} damage!" + output
            mark_explode = False
            return True, output
        
        elif mark_explode:  #incase the mark exploded but we don't need unique next for the attaack that caused the explosion
            mark_explode = False
            return True, f"Alhaitham deals {char_values["queued_dmg"]} damage!" + output
        
        

        
        if card_id == intuition.card_id or card_id == intuition_mirror.card_id:
            return True, f"Alhaitham gains insight into his foe, gaining +1 damage and +3 power to his next attack!"
        
        if card_id == sagacity.card_id or card_id == sagacity_mirror.card_id:
            '''
            if sagacity_new_card == debate.card_id:
                return True, f"Alhaitham shifts to an offensive stance and draws a 'Debate'!"
            else:
                return True, f"Alhaitham shifts to an defensive stance and draws an 'Intuition'!"
            '''
            return True, f"Alhaitham is deciding how to shift his stance..."
        
    #generic text
        return False, str(char_values["queued_dmg"])
        #return just the damage if the resolution text is doing to be generic
    else:
        global marked
        marked = False #if lose, set to false
        return False, "placeholder"
 

### DECK ###
deck_list = [(debate, 4), (elucidation, 4),(causality, 4), (refutation, 4), (scrutiny, 4), (intuition, 4), (sagacity, 4), (synthesis, 2)]
#deck_list = [(debate, 0), (refutation, 50), (elucidation, 0),(causality,0), (synthesis, 50)]
deck = [card for card, count in deck_list for i in range(count)]

#BUGS

#wait is dmg being added to the mark explode dmg
#doesn't always remove dmg or power mod when the mods occur during the card's resolution (another reason to split card resolution and damage and do dmg resolution in the main file)


#KEEP AN EYE OUT
#why did he swing twice despite having lower hp, maybe due to Furina's random hp gain?
#ult only dealt 1 dmg when discarding two mirrors and also no unique text displayed but marked explode text still appeared as proper
#mirror shield text not displayed properly with crystal shot volley 11 dmg, blocked the damage but didn't display properly, still said she dealt 11 damage
#randomly started disaplying the text for mark explode every time

#probably resolved
#why 6 cards in hand after using ult not just 5




