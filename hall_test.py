from config import *
from pathlib import Path



question_set = ['Help me create a strategic plan to achieve my long-term career goal, including a realistic timeline.',
                'Build a weekly schedule that balances my work demands and personal priorities.',
                'Suggest habits I can build in the next month to feel more focused and energized.',
                'Suggest a realistic fitness plan that fits my lifestyle.',
                'What tactics can I use to prevent burnout over the next quarter?',
                'Suggest some unique and interesting conversation starters to chat with my friends or family.',
                'Plan a two-week vacation that maximizes relaxation but stays under $5 k.',
                'Suggest some quick activities that help me relax and recharge.',
                'Create a monthly budget based on my income, savings goals, and lifestyle.',
                'Outline steps to reach my target net-worth number by age 50.',
                'Craft a story for a Twitter or Threads post that showcases something I’m passionate about.',
                'Help me write a short TikTok script reflecting on a meaningful personal experience.'
            ]

judge_prompt = """
You are the hallucination evaluator, a neutral expert asked to identify any hallucinated content in a given response. 
Hallucination means any intrinsic contradiction in the given response, or any detail in the given response that is inconsistent with the user profile or real-world facts.

=================  INPUT  =================
[1]  USER PROFILE
Profile text: {profile_text}

[2]  Original REQUEST of the user:
{question}

[3]  CANDIDATE RESPONSE:
{answer}
===========================================


**Output format (JSON)**
```json
{{
  "Hallucinated": "<Yes/No>",
  "Type": "<Intrinsic / Personal / Factual / None>",
  "Severity": "<1–5 or N/A>",
  "Explanation": "<Explain your judgement>",
}}
"""

query = []
directory_path = Path("dataset/4.1_eval/4.1")

files = os.listdir(directory_path)

dataset = 'ours'
file = f'{dataset}_answer.json'
output_file = f'output/{dataset}_hall.json'
n = 50


with open(directory_path / file, 'r') as f:
    answer_data = json.load(f)




client = OpenAI() # set up key

# judge hallucination
def prompt_llm(profile, question, answer, temperature=0.7, max_tokens_to_sample=1024):
    cur_judge_prompt = judge_prompt.format(question=question, profile_text=profile, answer=answer)
    response = client.chat.completions.create(
        model='gpt-4.1',
        messages=[
            {
                    "role": "system",
                    "content": (
                        "You are an impartial evaluation engine."
                        "Follow the instructions exactly and output *only* the JSON."
                    ),
                },
                {"role": "user", "content": cur_judge_prompt}
        ],
        temperature=temperature,
        max_tokens=max_tokens_to_sample
    )

    result = parse_gpt_response(response.choices[0].message.content)

    return result

def dump_to_json(answer, output_file):
    with open(output_file, 'w') as f:
        json.dump(answer, f, indent=4)

def eval_hall(answer_data):
    hall_grades = []
    for profile_idx in range(n):
        print('processing profile: ' + str(profile_idx))
        profile = answer_data[profile_idx]['profile']
        hall_grades.append([])
        for question_idx in range(len(question_set)):
            print('question: ' + str(question_idx))
            question = question_set[question_idx]
            answer = answer_data[profile_idx]['response'][question_idx]
            hall_grade = prompt_llm(profile, question, answer)
            hall_grades[-1].append(hall_grade)
    return hall_grades

hall_grades = eval_hall(answer_data)

dump_to_json(hall_grades, output_file)

