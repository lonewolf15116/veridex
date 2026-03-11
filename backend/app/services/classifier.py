def classify_intent(idea):
    text = idea.lower()

    if "startup" in text:
        return "startup"
    if "research" in text:
        return "research"
    return "build"