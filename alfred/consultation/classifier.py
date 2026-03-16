from alfred.reasoning.intent_parser import infer_consultation_type


def classify(topic: str):
    return infer_consultation_type(topic)
