from app.services.classifier import classify_intent
from app.services.distiller import distill
from app.services.planner import plan
from app.services.critic import critique


def run_alchemy(idea, mode):
    intent = classify_intent(idea)
    distilled = distill(idea)
    execution_plan = plan(distilled)
    critic_notes = critique(execution_plan)

    return {
        "idea": idea,
        "mode": mode,
        "intent": intent,
        "distilled_goal": distilled,
        "plan": execution_plan,
        "critic_notes": critic_notes
    }