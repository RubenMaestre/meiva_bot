import json
from config import FAQ_JSONL_PATH

def cargar_preguntas_respuestas():
    data = []
    with open(FAQ_JSONL_PATH, "r", encoding="utf-8") as file:
        for line in file:
            entry = json.loads(line.strip())
            user_question = entry["messages"][0]["content"]
            assistant_answer = entry["messages"][1]["content"]
            data.append((user_question, assistant_answer))
    return data
