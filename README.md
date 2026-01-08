# Zorg-styled text based Pokemon adventure game
This project is a zorg-styled text-based adventure game. The game runs on Python terminal and doesnt need any additional installments or plugins.
The game loosely follows the structure of the original Pokemon story and allows you to explore, solve puzzles, catch Pokemon and gather a party strong enough to beat the Gym Leader Brock in Pewter City and earn the Boulderbadge.

## How do you play?
The game is played entirely trough the terminal. You need get creative and write actions based on the queues the environment and NPC's offer. The actions you write change the game state and allow you to progress.
Heres a brief explanation of how you play the game:

<img width="2120" height="1036" alt="image" src="https://github.com/user-attachments/assets/0e9beb07-ac16-4096-8437-0ff1e052990f" />
<img width="2116" height="1093" alt="image" src="https://github.com/user-attachments/assets/76121ea7-2acc-4b2b-859c-7053fa20edd5" />
<img width="2115" height="267" alt="image" src="https://github.com/user-attachments/assets/aeaa7519-2b58-4bb1-be2e-aa408818091b" />


## How does it work?
The game runs on infinite loop that asks for player input. Lets call it the "response engine".
Response engine takes the terminal input, removes certain words from it and tries to match it with a __command handler__.
These words are removed: FILLER_WORDS = {"to", "at", "the", "a", "an", "on", "in"}.

"Talk to the professor oak" => "talk professor oak" => trigger handle_talk function.

Examples of some allowed words and their handlers:

  EXAMINE COMMANDS
  "examine": handle_examine,
  "inspect": handle_examine,
  "check": handle_examine,
  "view": handle_examine,
  "observe": handle_examine,
  "scan": handle_examine,

  CHECK ROOM
  "look around": handle_look,
  "look": handle_look,

  MOVE COMMANDS
  "go": handle_move,
  "walk": handle_move,
  "move": handle_move,
  "head": handle_move,
  "run": handle_move,

  TAKE / PICK UP COMMANDS
  "take": handle_take,
  "pick": handle_take,
  "grab": handle_take,
  "collect": handle_take,
  "get": handle_take,
  "gather": handle_take,
  "loot": handle_take,
  "pocket": handle_take,


Handlers are responsible for changing the game state and can do actions such as:
- Add or remove objects from rooms
- Update the room description
- Add Pokemon to players party
- Check if player has certain key item
- Trigger battle with other Gym leader Brock


## Classes

The game uses a variety of different classes and subclasses.

### Player class
- Player class has inventory, party and current room. Players location in the game is stored inside the player class.
<img width="416" height="130" alt="image" src="https://github.com/user-attachments/assets/4ffba3da-69ea-49a0-963e-7f71dbfa54fa" />


### Room class
- Room class contains spesific rooms exists, game objects and Pokemon.
<img width="600" height="174" alt="image" src="https://github.com/user-attachments/assets/7a6f62bc-13c8-4707-bded-c9fc82fd3b8f" />


### Game objects
- GameObject main class contains two subclasses: Item and HeavyItem. Items are pickable, while HeavyItems are not.
<img width="1124" height="862" alt="image" src="https://github.com/user-attachments/assets/413df6d2-f3eb-45dc-8765-dfcccbb74864" />

### Pokemon and move class
- Pokemons have their type, stats and moves defined as they are spawned into a room. Pokemon objects have an attribute self.moves that contains an __Array__ for __Move__ objects.
<img width="1121" height="661" alt="image" src="https://github.com/user-attachments/assets/c823027e-cceb-4b06-bd5c-70112264001c" />
<img width="753" height="146" alt="image" src="https://github.com/user-attachments/assets/1e3f314d-10a5-4e6e-9980-120c448105ce" />


### NPC class
- Non-playable characters are created using classes as well. NPC's are talkable, but not takeable.
<img width="699" height="560" alt="image" src="https://github.com/user-attachments/assets/d0712a4a-023c-47b9-aa35-eb7ff4ee5be4" />
<img width="1379" height="587" alt="image" src="https://github.com/user-attachments/assets/288968a1-094b-4184-9291-30cb38ade8ae" />


## How the game starts?

Response engine starts with the line: starting_room = build_world(). This triggers the creation of the entire world, where rooms are created and connected to each other. Items, NPC's and Pokemon are generated and placed as objects into their corresponding room objects.

starting_room = build_world() returns the starting room for the player and the infinite response loop begins.
You may exit the game by writing "quit".


Cheers!
<img width="211" height="209" alt="image" src="https://github.com/user-attachments/assets/04003581-4be6-4544-b8b2-f2bb91786450" />



