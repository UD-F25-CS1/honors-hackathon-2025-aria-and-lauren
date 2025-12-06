from bakery import assert_equal
from drafter import *
from dataclasses import dataclass
from drafter.llm import LLMMessage, LLMResponse, call_gemini, set_gemini_server


#from meta import *

# hide_debug_information()
# set_website_framed(False)
set_website_title("Duck Duck Goose")
set_site_information(
    "Authors: Aria and Lauren.",
    """
    Explore the wonderful fields, forests, towns, and lakes as you search for ducks in this wide world. However, you must beware the wandering
    goose who lusts for blood. Good luck, you'll need it.
    """,
    [],
    [],
    [],
)

"""Concept: Find all the ducks
duck locations:
    forest: up in trees, in a log, if you have a shovel - in cave (on gold, behind stalagmite),
    field: by lake, if you have seeds - in grass, in middle of lake
    town: in well, in house (cabinet), if you have a ladder - on roof, 

if you try to use a hammer to open the cabinet, the duck with a knife will appear and save one of the ducks you have found

item ideas: hammer (town), shovel(field), seeds(forest), ladder(field), key(cave)
locations: forest -> cave, field, town -> house -> kitchen

Will also encounter duck in back of cave

Duck Hunt OR Duck Duck Goose

"""

set_website_style("sakura")

@dataclass
class State:
    name: str
    ducks_found: int
    location: str
    has_key:bool
    inventory: list[str]
    


@route
def index(state: State) -> Page:
    return Page(state, ["Welcome to Duck Duck Goose!",
                        Image("DuckDuckGoose2.png", width=300),
                        "Please enter your name.",
                        TextBox("name"),
                        Button("enter", start_page)
                        ])


@route
def show_inventory(state: State) -> Page:
    """Displays all items in the player's inventory.

    Args:
        state(State): the state of the game.
        
    Returns:
        Page: the player's inventory.
    """
    
    if not state.inventory:
        content = ["Your inventory is empty."]
    else:
        content = ["Your inventory contains:"]
        for item in state.inventory:  # <-- meaningful loop
            content.append("- " + item)  
    
    content.append(Button("Go Back", url="/" + state.location))
    
    return Page(state, content)


@route
def start_page(state: State, name: str) -> Page:
    state.name = name
    state.inventory = []
    state.location = "start_page"
    return Page(state, ["Welcome, " + state.name,
                        "Your goal is to find all 8 ducks.",
                        "You may explore the surounding lands in search of these ducks, using any items you may find.",
                        "Enjoy, and stay safe.",
                        Button("Play Game", main_room)
                        ])

@route
def main_room(state: State) -> Page:
    state.location = "main_room"
    return Page(state, [Image("start.jpg", width = 350),
                        "You are in a grassy field.",
                        "Three options lay before you, where would you like to go?",
                        Button("The Forest", forest),
                        Button("Farther into the Field", field),
                        Button("Around a Bend in the Path", town),
                        "\n",
                        Button(text="Show Inventory", url="/show_inventory"),
                        ])

@route
def forest(state: State) -> Page:
    state.location = "forest"
    if "Shovel" in state.inventory:
        return Page(state, [
                            Image("duck_forest.jpg", width = 350),
                            "You have entered the forest.",
                            "You notice a suspicious patch of dirt.",
                            Button("Check Up in Trees", found_duck),
                            Button("Check Behind Tree", find_seeds),
                            Button("Check Under Rock", no_duck),
                            Button("Check Suspicious Dirt", cave),
                            Button("Check Log", found_duck),
                            "\n",
                            Button("Go Back", main_room),
                            Button(text="Show Inventory", url="/show_inventory"),
                            "You have found " + str(state.ducks_found) + " ducks."
                            ])
    else:
        return Page(state, [Image("duck_forest.jpg", width = 350),
                            "You have entered the forest."
                            "You notice a suspicious patch of dirt.",
                            "The dirt is to dense to dig through at the moment.", #add shovel hint
                            Button("Check Up in Trees", found_duck),
                            Button("Check Behind Tree", no_duck),
                            Button("Check Under Rock", no_duck),
                            Button("Check Log", found_duck),
                            "\n",
                            Button("Go Back", main_room),
                            Button(text="Show Inventory", url="/show_inventory"),
                            "You have found " + str(state.ducks_found) + " ducks."
                            ])
    
@route
def find_seeds(state: State) -> Page:
    if "Seeds" not in state.inventory:
        return Page(state, ["You see some seeds on the ground, would you like to pick them up?",
                            Image("seeds.png", width = 350),
                            Button("Grab Seeds", get_seeds),
                            "\n",
                            Button("Go Back", forest),
                            Button(text="Show Inventory", url="/show_inventory"),
                            "You have found " + str(state.ducks_found) + " ducks."
                            ])
    else:
        return Page(state, ["You have picked up the seeds.",
                            Image("seeds.png", width = 350),
                            "\n",
                            Button("Go Back", forest),
                            Button(text="Show Inventory", url="/show_inventory"),
                            "You have found " + str(state.ducks_found) + " ducks."
                            ])

@route
def get_seeds(state: State) -> Page:
    if "Seeds" not in inventory:
        state.inventory.append("Seeds")
        return find_seeds(state)
    else:
        return find_seeds(state)


@route
def cave(state: State) -> Page:
    state.location = "cave"
    if "Shovel" in state.inventory:
        if "Key" not in state.inventory:
            return Page(state, ["You have entered the cave.",
                            Image("cave.png", width = 350),
                            "Using your shovel, you dig behind the stalagmite and find a key!",
                            Button("Pick up key", get_key),
                            Button("Go deeper into the cave", deeper_cave),
                            Button("Go Back", url="/forest"),
                            "\n",
                            Button(text="Show Inventory", url="/show_inventory"),
                            "You have found " + str(state.ducks_found) + " ducks."
                            ])
        else:
            return Page(state, ["You have entered the cave.",
                            Image("cave.png", width = 350),
                            "You have picked up the key.",
                            Button("Go deeper into the cave", deeper_cave),
                            Button("Go Back", url="/forest"),
                            "\n",
                            Button(text="Show Inventory", url="/show_inventory"),
                            "You have found " + str(state.ducks_found) + " ducks."
                            ])

@route
def get_key(state: State) -> Page:
    state.has_key = True
    if "Key" not in state.inventory:
        state.inventory.append("Key")
        return cave(state)
    else:
        return cave(state)

'''
    has_key = True
    state.has_key = has_key
    if has_key:
        state.has_key = True
        if "Key" not in state.inventory:
            state.inventory.append("Key")
    if state.has_key and "Key" not in state.inventory:
        state.inventory.append("Key")
'''
              
    
@route
def deeper_cave(state:State)->Page:
    state.location = "deeper_cave"
    return Page(state,
    content = [
        "You have entered the deeper cave.",
        Image("deep_cave.png", width = 350),


        "A message is etched into the wall: Ť̵̢̳̤̣̰̅h̸̢̧̳̣̮͎̯̺̱͔̙͎͖̣̻́͑̏͑͛̕e̴̛̥̭̠̞͑̽̑̀͋̅͂̆̀͊͋͘ ̷͕̻͔͇̻̺̎̑͘G̸̛͙̩͖͙̮͉̀̈́̊̾͋͐͌̍͆̌͘̚͝o̶̻̟̔̍̐̀ọ̵̯͕͗̋̓̿́̔̄̚s̷̲̟̝͙̱͙̱͈͙͕̓ͅe̴͔̘̦͉̟̳̻̼͑̓̎͊̑̄̄̏̃̿̓͐̕͜͝ ̶̢͈̱̼͉̳̥̈́̉̐͋̓̓͑͐̊̌̕͜͜i̸̹͉̯͂̈͑̐̈́̃̎̐̈͆̏̓͝s̵̛͕̹͌͆̎̓̃̉͋̀͘ ̸͚̝̘́͛͊̓͊c̶̩̥͑̓͒̅̏̕͠o̶̺͈̩͉͛͜͜ḿ̴̢̢̨̪̠̯͎̠͇̲̒̈̊̉̆̿̔̈͊̑̔̀͠͠i̴̧͙̫̞͇̙̙̪̱̼͈̱̞̻̼͋̐̅͌͛͘͠͝n̴̢̛̬͈̠͔̱̬̝̲̺̞̝̟͐̎͑̔͆͊̈́͛́͜͝͠͠g̸̨͈̜̱̺͇̯̰̙̈͐͒̽̏͐̋̋̇͂̆͘̚͝͝ ̸̞͔̻̮̙̖̱͚̦̺̣̼̲̀̎̒̏̕f̴̢̖̃̀̄̎͌͝ỏ̵̩̲͌ṛ̷̢̨̨̧̢̲͖̘͔̠̘̬̘̥̇̀̀́̚ ̶̧̭̏̋̈͐̋̽̓̃͋͜͠y̸̧̧̟̗̗̆͑́́̕͝ơ̴̛̜͔̥̱̖̞̜̭̖̙̰̦̺̦͆̇͐̃̐́̃̓̿̿͛̽ų̸̜̺̣͊͌̇͂̓̇͌͒͠͝ͅ",

        "As you approach, a goose with a knife appears!",
        "You must flee!",
        Button(text="Flee Back to Forest", url="/forest"),
        "\n",
        Button(text="Show Inventory", url="/show_inventory"),
        "You have found " + str(state.ducks_found) + " ducks."
        ])

@route
def field(state: State) -> Page:
    state.location = "field"
    if "Ladder" in state.inventory:
        return Page(state, [
                        Image("field.png", width = 350),
                        "You have entered the field.",
                        "You see a lake off in the distance.",
                        Button("Investigate Lake", lake),
                        "\n",
                        "You have picked up a ladder.",
                        Button("Go Back", main_room),
                        Button(text="Show Inventory", url="/show_inventory"),
                        "You have found " + str(state.ducks_found) + " ducks."
                        ])
    else:
        return Page(state, [
                        Image("field.png", width = 350),
                        "You have entered the field.",
                        "You see a lake off in the distance.",
                        Button("Investigate Lake", lake),
                        "A ladder is lying in the grass, would you like to pick it up?", #check spelling
                        Button("Pick Up Ladder", get_ladder),
                        "\n",
                        Button("Go Back", main_room),
                        Button(text="Show Inventory", url="/show_inventory"),
                        "You have found " + str(state.ducks_found) + " ducks."
                        ])
    
@route
def get_ladder (state: State) -> Page:
    if "Ladder" not in state.inventory:
        state.inventory.append("Ladder")
        return field(state)
    else:
        return field(state)
    

@route
def lake(state: State) -> Page:
    state.location = "lake"
    if "Shovel" not in state.inventory:
        return Page(state, [
                        Image("lake.jpg", width = 350),
                        "You are standing on the shore of a lake.",
                        Button("Check Rock", no_duck),
                        Button("Check Reeds", found_duck),
                        Button("Look out at the lake", lake_warning),
                        "\n",
                        Button("Go Back", field),
                        Button(text="Show Inventory", url="/show_inventory"),
                        "You have found " + str(state.ducks_found) + " ducks."
                        ])
    else:
        return Page(state, [
                        Image("lake.jpg", width = 350),
                        "You are standing on the shore of a lake.",
                        Button("Check Rock", no_duck),
                        Button("Check Reeds", found_duck),
                        "\n",
                        Button("Go Back", field),
                        Button(text="Show Inventory", url="/show_inventory"),
                        "You have found " + str(state.ducks_found) + " ducks."
                        ])

@route #may want to add a duck here
def lake_warning(state: State) -> Page:
    if "Shovel" not in state.inventory:
        return Page(state, [
                        Image("lake.jpg", width = 350),
                        "You look out at the lake. You see a shovel by the water's edge",
                        Button("Pick Up the Shovel", get_shovel),
                        Button("Return", lake)
                        ])
    else:
        return Page(state, [
                        Image("lake.jpg", width = 350),
                        "You have picked up the shovel.",
                        "An ominous honk echoes over the water.",
                        Button("Return", lake)
                        ])

@route
def get_shovel(state: State) -> Page:
    if "Shovel" not in state.inventory:
        state.inventory.append("Shovel")
        return lake_warning(state)
    else:
        return lake_warning(state)

@route
def town(state: State) -> Page:
    state.location = "town"
    return Page(state, [
                        Image("town.jpg", width = 350),
                        "You have entered the town.",
                        Button("Blue House", house_1),
                        Button("Red House", house_2),
                        Button("Go Back", main_room)
                        ])
   
#blue house
@route
def house_1(state:State)->Page:
    state.location="house_1"
    if state.has_key == True:
        if "Ladder" in state.inventory:
            return Page(state, content=[
            Image("blue.png", width = 350),
            "The house is locked.",
            "You now have a key",
            "Enter the house or good around to the side?",
            Button(text="Enter House", url="/kitchen"),
            Button("Check the Side", check_side),
            Button(text="Go Back", url="/town"),
            "\n",
            Button(text="Show Inventory", url="/show_inventory"),
            "You have found " + str(state.ducks_found) + " ducks."
            ])
    else:
        return Page(
        state,
        content=[
            Image("red.jpg", width = 350),
            "The house is locked.",
            "There might be a key nearby.",
            "Would you like to go back or check around the side of the house?",
            Button("Check the Side", check_side),
            Button(text="Go Back", url="/town"),
            "\n",
            Button(text="Show Inventory", url="/show_inventory"),
            "You have found " + str(state.ducks_found) + " ducks."
        ])
    
@route
def check_side(state: State) -> Page:
    state.location = "check_side"
    if "Ladder" in state.inventory:
        return Page(state, ["You look around the side of the house.",
                            "There is a place a ladder would fit perfectly.",
                            "Would you like to place the ladder and go up?",
                            Button("Place Ladder", roof),
                            Button("Go Back", house_1),
                           "\n",
                            Button(text="Show Inventory", url="/show_inventory"),
                            "You have found " + str(state.ducks_found) + " ducks."
                            ])
    else:
        return Page(state, ["You look around the side of the house.",
                            "There is a place a ladder would fit perfectly.",
                            Button("Go Back", house_1),
                           "\n",
                            Button(text="Show Inventory", url="/show_inventory"),
                            "You have found " + str(state.ducks_found) + " ducks."
                            ])

@route
def roof(state: State) -> Page:
    state.location = "roof"
    return Page(state, ["You are now on the roof.",
                        "You see a duck sitting peacefully by the edge.",
                        "Would you like to collect the duck?",
                        Button("Collect Duck", found_duck),
                        Button("Go Back", check_side)
                        ])

@route
def hallway(state:State)->Page:
    state.location="hallway"
    return Page(
        state,
        content=[
            "You have arrived in hallway.",
            Image("hallway.png", width = 350),
            "There are doors on both sides.",
            "Where will you explore?",
            Button(text="Kitchen", url="/kitchen"),
            Button(text="Bedroom", url="/bedroom"),
            Button(text="Living Room", url="/living_room"),
            "\n",
            Button(text="Show Inventory", url="/show_inventory"),
            Button(text="Go Back", url="/house"),
            "You have found " + str(state.ducks_found) + " ducks."
        ]
    )

@route
def kitchen(state:State)->Page:
    state.location="kitchen"
    return Page(state, content=[
            "You have arrived in the kitchen.",
            Image("kitchen.png", width = 350),
            "A duck may be nearby.",
            Button(text="Check Cabinet", url="/cabinet"),
            Button(text="Check Fridge", url="/fridge"),
            Button(text="Check Oven", url="/oven"),
            Button(text="Go Back", url="/hallway"),
            "\n",
            Button(text="Show Inventory", url="/show_inventory"),
            "You have found " + str(state.ducks_found) + " ducks."
        ]
    )

@route
def fridge(state:State)->Page:
    state.location="fridge"
    return Page(
        state,
        content=[
            "You have arrived in the kitchen.",
            Image("fridge.jpg", width = 350),
            "Ominous Music Plays.",
            "It was a trap.",
            "The Goose is coming for you.",
            Button(text="Flee!", url="/hallway"),
            "\n",
            Button(text="Show Inventory", url="/show_inventory"),
            "You have found " + str(state.ducks_found) + " ducks."
        ]
    )

    
@route
def oven(state:State)->Page:
    state.location="oven"
    return Page(
        state,
        content=[
            Image("cooked.png", width = 350),
            "What did you expect?",
            Button(text="Go Back", url="/kitchen"),
            "\n",
            Button(text="Show Inventory", url="/show_inventory"),
            "You have found " + str(state.ducks_found) + " ducks."
        ]
    )

@route
def cabinet(state:State)->Page:
    state.location="cabinet"
    return Page(
        state,
        content=[
            Image("cabinet.png", width = 350),
            "You have opened the cabinet.",
            "An odd duck is in the corner.",
            Button(text="Collect Duck", url="/found_duck"),
            Button(text="Go Back", url="/kitchen"),
            "\n",
            Button(text="Show Inventory", url="/show_inventory"),
            "You have found " + str(state.ducks_found) + " ducks."
        ]
    )

@route
def bedroom (state: State) -> Page:
    state.location = "bedroom"
    return Page(state, [
                        Image("bedroom.jpg", width = 350),
                        "You have entered the bedroom",
                        Button("Check Closet", no_duck),
                        Button("Check Under Bed", found_duck),
                        Button("Check Dresser", no_duck),
                        Button("Check Under Covers", found_duck),
                        Button(text="Go Back", url="/hallway"),
                        "\n",
                        Button(text="Show Inventory", url="/show_inventory"),
                        "You have found " + str(state.ducks_found) + " ducks."
                        ])

@route
def living_room(state: State) -> Page:
    state.location = "living_room"
    return Page(state, [
                        Image("living_room.jpg", width = 350),
                        "You have entered the bedroom",
                        Button("Check Behind Couch", found_duck),
                        Button("Check Fireplace", no_duck),
                        Button(text="Go Back", url="/hallway"),
                        "\n",
                        Button(text="Show Inventory", url="/show_inventory"),
                        "You have found " + str(state.ducks_found) + " ducks."
                        ])

#red house
@route
def house_2(state:State)->Page:
    state.location="house_2"
    return Page(
        state,
        content=[
            Image("house2.png", width = 350),
            "The front door is open.",
            "There are breadcrumbs outside.",
            "You have a bad feeing about this.",
            "...",
            "Enter the house?",
            Button(text="Enter House", url="/death"),
            Button(text="Go Back", url="town"),
            "\n",
            Button(text="Show Inventory", url="/show_inventory"),
            "You have found " + str(state.ducks_found) + " ducks."
            ]
        )
@route
def death(state: State) -> Page:
    return Page(state, ["It's a trap!",
                        "The goose has caught you!",
                        Image("death.png", width = 350),
                        "Game Over.",
                        Button("Restart", index)
                        ])

@route
def found_duck(state: State) -> Page:
    state.ducks_found += 1
    return Page(state, ["Congratulations! You have found a duck.",
                        Image(""),
                        Button("Go Back", state.location),
                        "You have found " + str(state.ducks_found) + " ducks."
                        ])
    
@route
def no_duck(state: State) -> Page:
    return Page(state, ["There is no duck here...",
                        Button("Return", state.location),
                        "You have found " + str(state.ducks_found) + " ducks."
                        ])
    
    
    
start_server(State("", 0, "", False, []))
