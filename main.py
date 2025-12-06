from bakery import assert_equal
from drafter import *
from dataclasses import dataclass

from meta import *

# hide_debug_information()
# set_website_framed(False)
set_website_title("Your Drafter Website")
set_site_information(
    "author",
    """
Your description can go here.
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

item ideas: hammer (town), shovel(field), seeds(forest), ladder(field)

"""

@dataclass
class State:
    name: str
    ducks_found: int
    items: list[str]
    current_room: str
    


@route
def index(state: State) -> Page:
    return Page(state, ["Welcome to the Duck Hunt!",
                        "Please enter your name.",
                        TextBox("name"),
                        Button("enter", start_page)
                        ])

@route
def start_page(state: State, name: str) -> Page:
    state.name = name
    return Page(state, ["Welcome, " + state.name,
                        "Your goal is to find all 10 ducks.",
                        "You may explore the surounding lands in search of these ducks, using any items you may find.",
                        "Enjoy, and stay safe.",
                        Button("Play Game", main_room)
                        ])

@route
def main_room(state: State) -> Page:
    return Page(state, ["You are in a grassy field.",
                        "Three options lay before you, where would you like to go?",
                        Button("The Forest", forest_page),
                        Button("Farther into the Field", field_page),
                        Button("Around a Bend in the Path", town_page)
                        ])

@route
def forest_page(state: State) -> Page:
    return Page(state, [""
                        ])

@route
def field_page(state: State) -> Page:
    return Page(state, [""
                        ])

@route
def town_page(state: State) -> Page:
    return Page(state, [""
                        ])
    
@route
def gain_item(state: State) -> Page:
    
    
    
    
    
start_server(State("", 0, []))
