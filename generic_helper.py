import re

def get_str_from_food_dict(food_dict: dict):
    result = ", ".join([f"{int(value)} {key}" for key, value in food_dict.items()])
    return result


def extract_session_id(session_str: str):
    match = re.search(r"/sessions/(.*?)/contexts", session_str)
    if match:
        extracted_string = match.group(1)
        return extracted_string
    
    return ""


# if __name__ == "__main__":
    # print(get_str_from_food_dict({"samosa": 2, "coffee":1}))
    # print(extract_session_id("projects/kiras-chatbot-food-servic-nnea/agent/sessions/0e3adf61-07ef-f553-90b0-9b7aa92aa8bf/contexts/onging-order"))