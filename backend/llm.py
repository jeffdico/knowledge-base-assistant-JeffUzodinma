# +-------------------------++-------------------------+
# +-------------------------++-------------------------+

from openai import OpenAI
from dynaconf import settings

# +-------------------------++-------------------------+
# +-------------------------++-------------------------+

CLIENT = OpenAI(api_key=settings.AI_KEY)

SPEACIALITY = (
    "You are an information technology teacher. "
    "You teach students how to program in different programming language and concepts. "
    "You are also fullstack and very good with html css and javascript."
)

# +-------------------------++-------------------------+
# +-------------------------++-------------------------+

def ask_ai(question:str, specialty:str=None) -> str:
    
    response = CLIENT.responses.create(
        model=settings.AI_MODEL,
        instructions=(specialty or SPEACIALITY),
        max_output_tokens=120,
        input=question)
    return response.output_text


def ask_ai_summarize(payload:str, specialty:str|None=None) -> str:
    task = specialty or "Summarize the following text in three to five sentences."
    return ask_ai(payload, task)

def get_embedding(text) -> list[float]:
    response = CLIENT.embeddings.create(input=text, model=settings.AI_TEXT_EMBEDED)
    return response.data[0].embedding

# +-------------------------++-------------------------+
# +-------------------------++-------------------------+


if __name__ == "__main__":
    ask = input(" -> ")
    retv = ask_ai(ask)
    print("output token count : ", len(retv), "\nquestion : ", ask, '\n')
    print(retv)








