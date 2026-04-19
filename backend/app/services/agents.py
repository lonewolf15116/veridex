def strategist_agent(prompt: str, mode: str):
    return {"strategy": f"Strategy for {prompt}"}

def architect_agent(prompt: str, mode: str, strategist_output: dict):
    return {"architecture": "System structure defined"}

def planner_agent(prompt: str, mode: str, strategist_output: dict, architect_output: dict):
    return {"plan": "Execution steps created"}

def critic_agent(prompt: str, mode: str, context: dict):
    return {"critique": "Improvements and risks identified"}