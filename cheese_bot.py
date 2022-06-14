#from collections import Counter
#from responses import responses, blank_spot
from selections import selection_of_bread, selection_of_cheese, selection_of_protien
import re
#from user_functions import preprocess, compare_overlap, pos_tag, extract_nouns, compute_similarity
#import spacy
#for efficiency
#word2vec = spacy.load('en_core_web_sm')
#for accuracy
#word2vec = spacy.load(nlp = spacy.load("en_core_web_trf")

negative_responses = ("no", "nope", "nah", "no way", )

exit_commands = ("quit", "goodbye", "exit", "pause", "later", "see ya", "bye")

intro = """
Hello!!! Welcome to Cheese Wiz!!!

Cheese Wiz is the only fully automated grilled cheese shop in the world!!\n
"""

# creating bot class
class CheeseBot:

    def __init__(self):

        self.cheesebabble = {
            "get_menu_intent": r"\w.*see the menu.*", 
            "make_order_intent": r"\w.*make an order.*", 
            "place_order_intent": r"\w.*place an order.*",
            "": r""
        }

        self.bread_list = []
        self.cheese_list = []
        self.protein_list = []
        for bread_type, price in selection_of_bread.items():
            self.bread_list.append((bread_type.lower(), price))
        for cheese_type, price in selection_of_cheese.items():
            self.cheese_list.append((cheese_type.lower(), price))
        for protein_type, price in selection_of_protien.items():
            self.protein_list.append((protein_type.lower(), price))

        
        
    def greet(self):
        print(intro)
        self.name = input("My name is Sheldon and I am your cheese wizard! \
Can i get your name please? \n")
        while self.make_exit(self.name) == True:
            exit()
        need_help = input(f"Thank you very much, {self.name.title()}, it is very nice \
to meet you today. Would you like my assistance with your grilled \
cheese needs today?\n")
        if need_help in negative_responses:
            print("Ok, Thank you for your time today!")
            exit()
        self.chat()

    def make_exit(self, user_message):
        for command in exit_commands:
            if command in user_message:
                print("Thank you for your time, please have a wonderful day!  Goodbye!")
                return True
        

    def chat(self):
        reply = input("How can the Cheese Wiz impress you today?\n").lower()
        while not self.make_exit(reply):
            reply = input(self.match_reply(reply))

    def match_reply(self, reply):
        for intent, regex_pattern in self.cheesebabble.items():
            found_match = re.match(regex_pattern, reply)
            if found_match and intent == "get_menu_intent":
                return self.get_menu_intent()
            elif found_match and intent == "make_order_intent" or found_match and intent == "place_order_intent":
                return self.make_order_intent()
            #else:
                #return "The Cheese Wiz is amazing, but I seem to be having some trouble understanding you at this time.\n"

    def get_menu_intent(self):
        print("Our selection of breads:")
        for bread in self.bread_list:
            print(bread)
        print("Our selction of cheeses:")
        for cheese in self.cheese_list:
            print(cheese)
        print("Our selections of proteins:")
        for protein in self.protein_list:
            print(protein)
        return "What else can I do for you?\n"
        

    def make_order_intent(self):
        self.order = {}
        self.order_total = 0
        self.build_sandwich()
        while self.print_receipt() == True:
            self.build_sandwich()
        return "Thank you! Your order will be ready soon\n"

    def build_sandwich(self):
        self.sandwich_ingredients = []
        self.sandwich_price = 0
        self.select_bread()
        self.select_cheese()
        self.select_protein()
        sandwich_name = ""
        for ingredient in self.sandwich_ingredients:
            sandwich_name += ingredient + "-"
        self.order[sandwich_name] = self.sandwich_price
        self.order_total += self.sandwich_price
        return
        
    def select_bread(self):
        bread_selected = input("Which type of bread would you like to build your grilled cheese on today?\n").lower()
        if bread_selected.title() not in selection_of_bread:
            self.select_bread()
        for bread_type, price in selection_of_bread.items():
            if bread_selected == bread_type.lower():
                self.sandwich_ingredients.append(bread_selected)
                self.sandwich_price += price
                
            

    def select_cheese(self):
        cheese_selected = input("Which type of cheese would you like to build your grilled cheese with today?\n").lower()
        if cheese_selected.title() not in selection_of_cheese:
            self.select_cheese()
        for cheese_type, price in selection_of_cheese.items():
            if cheese_selected == cheese_type.lower():
                self.sandwich_ingredients.append(cheese_selected)
                self.sandwich_price += price
            

    def select_protein(self):
        protein_selected = input("Which type of protein would you like to build your grilled cheese with today?\n").lower()
        if protein_selected.title() not in selection_of_protien:
            self.select_protein()
        for protein_type, price in selection_of_protien.items():
            if protein_selected == protein_type.lower():
                self.sandwich_ingredients.append(protein_selected)
                self.sandwich_price += price
            
    def print_receipt(self):
        print("Your Reciept")
        for order, price in self.order.items():
            print((order, price))
        print("Total:", self.order_total)
        reply = input("Would you like to add another grilled cheese to your order?\n").lower()
        if reply == "y" or reply == "yes":
            return True
        else:
            return False



bot = CheeseBot()
bot.greet()