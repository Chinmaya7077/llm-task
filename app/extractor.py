import json

def parse_llm_response(llm_output: str):
    try:
        start = llm_output.index("[")
        end = llm_output.rindex("]") + 1
        return json.loads(llm_output[start:end])
    except Exception:
        return []
