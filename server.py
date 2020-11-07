import requests
import json
path_to_agent1 = "/home/kvu/google-research-football/main.py"
path_to_agent2 = "/home/kvu/google-research-football/agents/submission_4/main.py"

agent1_url = f"http://localhost:5001?agents[]={path_to_agent1}"
agent2_url = f"http://localhost:5002?agents[]={path_to_agent2}"

body = {
    "action": "run",
    "environment": "football",
    "agents": [agent1_url, agent2_url]
}
resp = requests.post(url="http://localhost:5000", data=json.dumps(body)).json()

# Inflate the response replay to visualize.
from kaggle_environments import make
env = make("football", steps=resp["steps"], debug=True)
env.render(mode="human", width=800, height=600)
print(resp)