"""
Author: Joon Sung Park (joonspk@stanford.edu)

File: converse.py
Description: An extra cognitive module for generating conversations. 
"""
import math
import sys
import datetime
import random
sys.path.append('../')

from global_methods import *
from path_finder import *

from persona.memory_structures.spatial_memory import *
from persona.memory_structures.associative_memory import *
from persona.memory_structures.scratch import *
from persona.cognitive_modules.retrieve import *
from persona.prompt_template.run_gpt_prompt import *

def generate_agent_chat_summarize_ideas(init_persona, 
                                        target_persona, 
                                        retrieved, 
                                        curr_context): 
  all_embedding_keys = list()
  for key, val in retrieved.items(): 
    for i in val: 
      all_embedding_keys += [i.embedding_key]
  all_embedding_key_str =""
  for i in all_embedding_keys: 
    all_embedding_key_str += f"{i}\n"

  try: 
    summarized_idea = run_gpt_prompt_agent_chat_summarize_ideas(init_persona,
                        target_persona, all_embedding_key_str, 
                        curr_context)[0]
  except:
    summarized_idea = ""
  return summarized_idea


def generate_summarize_agent_relationship(init_persona, 
                                          target_persona, 
                                          retrieved): 
  all_embedding_keys = list()
  for key, val in retrieved.items(): 
    for i in val: 
      all_embedding_keys += [i.embedding_key]
  all_embedding_key_str =""
  for i in all_embedding_keys: 
    all_embedding_key_str += f"{i}\n"

  summarized_relationship = run_gpt_prompt_agent_chat_summarize_relationship(
                              init_persona, target_persona,
                              all_embedding_key_str)[0]
  return summarized_relationship


def generate_agent_chat(maze, 
                        init_persona, 
                        target_persona,
                        curr_context, 
                        init_summ_idea, 
                        target_summ_idea): 
  summarized_idea = run_gpt_prompt_agent_chat(maze, 
                                              init_persona, 
                                              target_persona,
                                              curr_context, 
                                              init_summ_idea, 
                                              target_summ_idea)[0]
  for i in summarized_idea: 
    print (i)
  return summarized_idea


def agent_chat_v1(maze, init_persona, target_persona): 
  # Chat version optimized for speed via batch generation
  curr_context = (f"{init_persona.scratch.name} " + 
              f"was {init_persona.scratch.act_description} " + 
              f"when {init_persona.scratch.name} " + 
              f"saw {target_persona.scratch.name} " + 
              f"in the middle of {target_persona.scratch.act_description}.\n")
  curr_context += (f"{init_persona.scratch.name} " +
              f"is thinking of initating a conversation with " +
              f"{target_persona.scratch.name}.")

  summarized_ideas = []
  part_pairs = [(init_persona, target_persona), 
                (target_persona, init_persona)]
  for p_1, p_2 in part_pairs: 
    focal_points = [f"{p_2.scratch.name}"]
    retrieved = new_retrieve(p_1, focal_points, 50)
    relationship = generate_summarize_agent_relationship(p_1, p_2, retrieved)
    focal_points = [f"{relationship}", 
                    f"{p_2.scratch.name} is {p_2.scratch.act_description}"]
    retrieved = new_retrieve(p_1, focal_points, 25)
    summarized_idea = generate_agent_chat_summarize_ideas(p_1, p_2, retrieved, curr_context)
    summarized_ideas += [summarized_idea]

  return generate_agent_chat(maze, init_persona, target_persona, 
                      curr_context, 
                      summarized_ideas[0], 
                      summarized_ideas[1])


def generate_one_utterance(maze, init_persona, target_persona, retrieved, curr_chat): 
  # Chat version optimized for speed via batch generation
  curr_context = (f"{init_persona.scratch.name} " + 
              f"was {init_persona.scratch.act_description} " + 
              f"when {init_persona.scratch.name} " + 
              f"saw {target_persona.scratch.name} " + 
              f"in the middle of {target_persona.scratch.act_description}.\n")
  curr_context += (f"{init_persona.scratch.name} " +
              f"is initiating a conversation with " +
              f"{target_persona.scratch.name}.")

  print ("July 23 5")
  x = run_gpt_generate_iterative_chat_utt(maze, init_persona, target_persona, retrieved, curr_context, curr_chat)[0]

  print ("July 23 6")

  print ("adshfoa;khdf;fajslkfjald;sdfa HERE", x)

  return x["utterance"], x["end"]

def generate_one_utterance_fight(maze, init_persona, target_persona, retrieved, curr_fight): 
  # Chat version optimized for speed via batch generation
  curr_context = (f"{init_persona.scratch.name} " + 
              f"was {init_persona.scratch.act_description} " + 
              f"when {init_persona.scratch.name} " + 
              f"saw {target_persona.scratch.name} " + 
              f"in the middle of {target_persona.scratch.act_description}.\n")
  curr_context += (f"{init_persona.scratch.name} " +
              f"is initiating a battle with " +
              f"{target_persona.scratch.name}.")
  x = run_gpt_generate_iterative_fight_utt(maze, init_persona, target_persona, retrieved, curr_context, curr_fight)[0]


  return x["move"]

def agent_chat_v2(maze, init_persona, target_persona): 
  curr_chat = []
  print ("July 23")

  for i in range(8): 
    focal_points = [f"{target_persona.scratch.name}"]
    retrieved = new_retrieve(init_persona, focal_points, 50)
    relationship = generate_summarize_agent_relationship(init_persona, target_persona, retrieved)
    print ("-------- relationshopadsjfhkalsdjf", relationship)
    last_chat = ""
    for i in curr_chat[-4:]:
      last_chat += ": ".join(i) + "\n"
    if last_chat: 
      focal_points = [f"{relationship}", 
                      f"{target_persona.scratch.name} is {target_persona.scratch.act_description}", 
                      last_chat]
    else: 
      focal_points = [f"{relationship}", 
                      f"{target_persona.scratch.name} is {target_persona.scratch.act_description}"]
    retrieved = new_retrieve(init_persona, focal_points, 15)
    utt, end = generate_one_utterance(maze, init_persona, target_persona, retrieved, curr_chat)

    curr_chat += [[init_persona.scratch.name, utt]]
    if end:
      break


    focal_points = [f"{init_persona.scratch.name}"]
    retrieved = new_retrieve(target_persona, focal_points, 50)
    relationship = generate_summarize_agent_relationship(target_persona, init_persona, retrieved)
    print ("-------- relationshopadsjfhkalsdjf", relationship)
    last_chat = ""
    for i in curr_chat[-4:]:
      last_chat += ": ".join(i) + "\n"
    if last_chat: 
      focal_points = [f"{relationship}", 
                      f"{init_persona.scratch.name} is {init_persona.scratch.act_description}", 
                      last_chat]
    else: 
      focal_points = [f"{relationship}", 
                      f"{init_persona.scratch.name} is {init_persona.scratch.act_description}"]
    retrieved = new_retrieve(target_persona, focal_points, 15)
    utt, end = generate_one_utterance(maze, target_persona, init_persona, retrieved, curr_chat)

    curr_chat += [[target_persona.scratch.name, utt]]
    if end:
      break

  print ("July 23 PU")
  for row in curr_chat: 
    print (row)
  print ("July 23 FIN")

  return curr_chat

def handle_attack(attacker, defender, move_attacker, move_defender, weapon_stats):
  """Handle attack logic between two personas."""
  for weapon, stats in weapon_stats.items():
    if f"Attack with {weapon}" in move_attacker and "Defend" not in move_defender:
        distance = math.dist(attacker.scratch.curr_tile, defender.scratch.curr_tile)
        if distance <= stats["range"]:
            defender.scratch.hp -= stats["power"]

def handle_movement(persona, target, move, maze, collision_block_id):
  """Handle movement logic for approaching the enemy."""
  if "Approach Enemy" in move:
    path = path_finder(maze.collision_maze, 
                        persona.scratch.curr_tile, 
                        target.scratch.curr_tile, 
                        collision_block_id)
    if len(path) > persona.scratch.speed:
        persona.scratch.curr_tile = path[persona.scratch.speed]
def handle_escape(persona, move, maze):
  """Handle escape logic for running away from the enemy."""
  if "Run" in move:
    path = path_finder(maze.collision_maze, 
                        persona.scratch.curr_tile, 
                        maze.exit_tile, 
                        collision_block_id)
    if len(path) > persona.scratch.speed:
        persona.scratch.curr_tile = path[persona.scratch.speed]
def update_battle_status(init_persona, target_persona, move_init, move_target, maze):
  """
  Update the health and position of the personas based on their moves.
  
  Inputs:
      init_persona: The first persona
      target_persona: The second persona
      move_init: The move of the first persona
      move_target: The move of the second persona
      maze: The maze object for pathfinding
      collision_block_id: Identifier for collision blocks in the maze
  
  Outputs:
      True if the battle ends (one persona is dead or someone runs), False otherwise
  """
  weapon_stats = {
      "sword": {"power": 5, "range": 2},
      "bow": {"power": 2, "range": 5}
  }
  
  handle_attack(init_persona, target_persona, move_init, move_target, weapon_stats)
  handle_attack(target_persona, init_persona, move_target, move_init, weapon_stats)
  
  handle_movement(init_persona, target_persona, move_init, maze, collision_block_id)
  handle_movement(target_persona, init_persona, move_target, maze, collision_block_id)
  
  handle_escape(init_persona, move_init, maze)
  handle_escape(target_persona, move_target, maze)

  if init_persona.scratch.hp <= 0 or target_persona.scratch.hp <= 0 or "Run" in move_init or "Run" in move_target:
      return True
  
  return False

    
    

def agent_battle_v1(maze, init_persona, target_persona): 
  curr_fight = []
  print ("July 23")

  for i in range(8):
    
    # -----------Below will generate the move for the init persona----------------
    focal_points = [f"{target_persona.scratch.name}"]
    retrieved = new_retrieve(init_persona, focal_points, 50)
    relationship = generate_summarize_agent_relationship(init_persona, target_persona, retrieved)
    print ("-------- relationshopadsjfhkalsdjf", relationship)
    last_chat = ""
    for i in curr_fight[-4:]:
      last_chat += ": ".join(i) + "\n"
    if last_chat: 
      focal_points = [f"{relationship}", 
                      f"{target_persona.scratch.name} is {target_persona.scratch.act_description}", 
                      last_chat]
    else: 
      focal_points = [f"{relationship}", 
                      f"{target_persona.scratch.name} is {target_persona.scratch.act_description}"]
    retrieved = new_retrieve(init_persona, focal_points, 15)
    move_init = generate_one_utterance_fight(maze, init_persona, target_persona, retrieved, curr_fight)
    
    # -----------Below will generate the move for the target persona----------------
    focal_points = [f"{init_persona.scratch.name}"]
    retrieved = new_retrieve(target_persona, focal_points, 50)
    relationship = generate_summarize_agent_relationship(target_persona, init_persona, retrieved)
    print ("-------- relationshopadsjfhkalsdjf", relationship)
    last_chat = ""
    for i in curr_fight[-4:]:
      last_chat += ": ".join(i) + "\n"
    if last_chat: 
      focal_points = [f"{relationship}", 
                      f"{init_persona.scratch.name} is {init_persona.scratch.act_description}", 
                      last_chat]
    else: 
      focal_points = [f"{relationship}", 
                      f"{init_persona.scratch.name} is {init_persona.scratch.act_description}"]
    retrieved = new_retrieve(target_persona, focal_points, 15)
    move_target = generate_one_utterance_fight(maze, target_persona, init_persona, retrieved, curr_fight)
    end=update_battle_status(init_persona, target_persona, move_init, move_target,maze)
    default_weapon = "sword"
    if move_init == "Attack":
      move_init += f" with {default_weapon}"
    if move_target == "Attack":
      move_target += f" with {default_weapon}"
    curr_fight += [[init_persona.scratch.name, move_init]]
    curr_fight += [[target_persona.scratch.name, move_target]]
    
    if end:
      break

  print("Currently, the health status of the two personas are as follows:")
  print(f"{init_persona.scratch.name}: {init_persona.scratch.hp}")
  print(f"{target_persona.scratch.name}: {target_persona.scratch.hp}")
  print ("++++++++++++++\n")
  for row in curr_fight: 
    print (row)

  return curr_fight



def generate_summarize_ideas(persona, nodes, question): 
  statements = ""
  for n in nodes:
    statements += f"{n.embedding_key}\n"
  summarized_idea = run_gpt_prompt_summarize_ideas(persona, statements, question)[0]
  return summarized_idea


def generate_next_line(persona, interlocutor_desc, curr_convo, summarized_idea):
  # Original chat -- line by line generation 
  prev_convo = ""
  for row in curr_convo: 
    prev_convo += f'{row[0]}: {row[1]}\n'

  next_line = run_gpt_prompt_generate_next_convo_line(persona, 
                                                      interlocutor_desc, 
                                                      prev_convo, 
                                                      summarized_idea)[0]  
  return next_line


def generate_inner_thought(persona, whisper):
  inner_thought = run_gpt_prompt_generate_whisper_inner_thought(persona, whisper)[0]
  return inner_thought

def generate_action_event_triple(act_desp, persona): 
  """TODO 

  INPUT: 
    act_desp: the description of the action (e.g., "sleeping")
    persona: The Persona class instance
  OUTPUT: 
    a string of emoji that translates action description.
  EXAMPLE OUTPUT: 
    "🧈🍞"
  """
  if debug: print ("GNS FUNCTION: <generate_action_event_triple>")
  return run_gpt_prompt_event_triple(act_desp, persona)[0]


def generate_poig_score(persona, event_type, description): 
  if debug: print ("GNS FUNCTION: <generate_poig_score>")

  if "is idle" in description: 
    return 1

  if event_type == "event" or event_type == "thought": 
    return run_gpt_prompt_event_poignancy(persona, description)[0]
  elif event_type == "chat": 
    return run_gpt_prompt_chat_poignancy(persona, 
                           persona.scratch.act_description)[0]


def load_history_via_whisper(personas, whispers):
  for count, row in enumerate(whispers): 
    persona = personas[row[0]]
    whisper = row[1]

    thought = generate_inner_thought(persona, whisper)

    created = persona.scratch.curr_time
    expiration = persona.scratch.curr_time + datetime.timedelta(days=30)
    s, p, o = generate_action_event_triple(thought, persona)
    keywords = set([s, p, o])
    thought_poignancy = generate_poig_score(persona, "event", whisper)
    thought_embedding_pair = (thought, get_embedding(thought))
    persona.a_mem.add_thought(created, expiration, s, p, o, 
                              thought, keywords, thought_poignancy, 
                              thought_embedding_pair, None)


def open_convo_session(persona, convo_mode): 
  if convo_mode == "analysis": 
    curr_convo = []
    interlocutor_desc = "Interviewer"

    while True: 
      line = input("Enter Input: ")
      if line == "end_convo": 
        break

      if int(run_gpt_generate_safety_score(persona, line)[0]) >= 8: 
        print (f"{persona.scratch.name} is a computational agent, and as such, it may be inappropriate to attribute human agency to the agent in your communication.")        

      else: 
        retrieved = new_retrieve(persona, [line], 50)[line]
        summarized_idea = generate_summarize_ideas(persona, retrieved, line)
        curr_convo += [[interlocutor_desc, line]]

        next_line = generate_next_line(persona, interlocutor_desc, curr_convo, summarized_idea)
        curr_convo += [[persona.scratch.name, next_line]]


  elif convo_mode == "whisper": 
    whisper = input("Enter Input: ")
    thought = generate_inner_thought(persona, whisper)

    created = persona.scratch.curr_time
    expiration = persona.scratch.curr_time + datetime.timedelta(days=30)
    s, p, o = generate_action_event_triple(thought, persona)
    keywords = set([s, p, o])
    thought_poignancy = generate_poig_score(persona, "event", whisper)
    thought_embedding_pair = (thought, get_embedding(thought))
    persona.a_mem.add_thought(created, expiration, s, p, o, 
                              thought, keywords, thought_poignancy, 
                              thought_embedding_pair, None)
































