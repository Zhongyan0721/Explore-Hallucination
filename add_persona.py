
# add persona and response to hallunication json file

from config import *



file = 'output/ours_hall.json'

persona_file = 'dataset/4.1_eval/4.1/ours_answer.json'

output_file = 'output/ours_hall_test.json'

with open(file, 'r') as f:
    data = json.load(f)

with open(persona_file, 'r') as f:
    persona = json.load(f)

for i in range(50):
    for j in range(len(data[i])):
        data[i][j]['profile'] = persona[i]['profile']
        data[i][j]['response'] = persona[i]['response'][j]


def dump_to_json(answer, output_file):
    with open(output_file, 'w') as f:
        json.dump(answer, f, indent=4)

dump_to_json(data, output_file)