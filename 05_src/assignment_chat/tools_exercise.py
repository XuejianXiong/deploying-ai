import requests
import json
import random

from langchain.tools import tool


#######################################
# Create the Tool
#######################################
@tool
def get_body_exercise():
    """
    An API call to a body exercise service is made.
    The API call is to https://wger.de/api/v2/exerciseinfo/.
    """    
    
    try:
          response = get_body_exercise_from_service()
          exercise = get_body_exercise_from_response(response=response)
          return exercise
    except Exception as e:
        return f"Error fetching exercise: {str(e)}"


#######################################
# Get the response from the service API
#######################################
def get_body_exercise_from_service():
    url = "https://wger.de/api/v2/exerciseinfo/"
    params = {
        "language": 2,  # English
        "limit": 20
    }
    response = requests.get(url, params=params, timeout=5)
    return response


#######################################
# Extract results from the response
#######################################
def get_body_exercise_from_response(response:requests.Response) -> str:
    response.raise_for_status()
    rep_data = response.json()
          
    exercise_list = rep_data.get("results", [])
    if not exercise_list:
        return "No exercises found."
          
    exercise = random.choice(exercise_list)
    return json.dumps(exercise)
