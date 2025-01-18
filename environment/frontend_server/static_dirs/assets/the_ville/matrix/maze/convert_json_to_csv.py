import json
import csv
import sys
import os
import ipdb
json_path = "/mnt/data2/ray/multi_agents/environment/frontend_server/static_dirs/assets/the_ville/visuals/the_ville_no_wall_v2.json"
output_name = "collision_maze_no_wall_v2.csv"
output_path ="/mnt/data2/ray/multi_agents/environment/frontend_server/static_dirs/assets/the_ville/matrix/maze"
with open(json_path) as f:
    data = json.load(f)
    for layer in data["layers"]:
        if layer["name"] == "Collisions":
            maze = layer["data"]
            break
# save the maze as a csv file with only one row
with open(os.path.join(output_path, output_name), 'w') as f:
    writer = csv.writer(f)
    writer.writerow(maze)
print("Done converting json to csv")
    