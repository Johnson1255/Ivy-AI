import csv
import random

def load_responses(file_path):
    responses = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            question = row['question']
            personality = row['personality']
            answers = row['answers'].split('|')
            
            if question not in responses:
                responses[question] = {}
            responses[question][personality] = answers
    return responses

def get_response(question, responses, personality=None):
    if question in responses:
        if personality and personality in responses[question]:
            return random.choice(responses[question][personality])
        return random.choice([resp for resp_list in responses[question].values() for resp in resp_list])
    return "Lo siento, no tengo una respuesta para esa pregunta."

# Uso
responses = load_responses('ivy_responses.csv')
question = "¿Quién eres?"
personality = "Friendly"
print(get_response(question, responses, personality))
