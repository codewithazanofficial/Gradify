import numpy as np
from typing import Dict, Any, Tuple

from response import Response


def build_user_data(
    study_hours: float,
    eca_hours: float,
    sleep_hours: float,
    social_hours: float,
    physical_hours: float,
    user_text: str,
) -> Dict[str, Any]:
    """Build the user_data dict expected by the model and Response class.

    The numeric features are kept in the same order and shape as in survey.py
    and Model_training.ipynb.
    """
    features = np.array(
        [study_hours, eca_hours, sleep_hours, social_hours, physical_hours],
        dtype=float,
    ).reshape(1, -1)

    return {
        "user_data": features,
        "user_text": user_text,
    }


def validate_total_hours(
    study_hours: float,
    eca_hours: float,
    sleep_hours: float,
    social_hours: float,
    physical_hours: float,
    max_total: float = 24.0,
) -> Tuple[bool, float]:
    """Validate that the total hours across all categories do not exceed max_total.

    Returns (is_valid, total_hours).
    """
    total = (
        float(study_hours)
        + float(eca_hours)
        + float(sleep_hours)
        + float(social_hours)
        + float(physical_hours)
    )
    return total <= max_total, total


def predict_and_generate_response(model, user_data: Dict[str, Any]):
    """Run the regression model and Response helper to generate advice.

    Returns a tuple of (predicted_gpa, adjusted_gpa, advice_sentences).
    """
    # model expects a 2D numpy array like in survey.py
    predicted_gpa = float(model.predict(user_data["user_data"])[0])

    response = Response(user_data)
    adjusted_gpa = float(response.adjust_gpa(user_data["user_text"], predicted_gpa))
    sentences = response.generate_response(adjusted_gpa)

    # For the web app we let the browser handle speech via Web Speech API.
    # The CLI can still call Response.speak directly.
    return predicted_gpa, adjusted_gpa, sentences


def answer_followup_question(
    user_data: Dict[str, Any],
    gpa: float,
    question: str,
):
    """Answer a follow-up question in a web-friendly way.

    This uses the same logic as Response.get_and_respond but without
    printing, recursion, or input(). It simply returns the sentences.
    """
    resp = Response(user_data)
    # store gpa on the instance so the prompt can reference it
    resp.gpa = gpa

    prompt = f"""You are Gradify, an intelligent academic assistant. 
Answer the user's question clearly, briefly, and accurately. 
Focus on helpful academic or personal productivity advice. 
Keep your tone friendly but concise — around 2 to 3 sentences maximum. 
If the question is unclear or unrelated to academics or learning, politely guide the user back to relevant topics.
User's question: {question}
Extras:
While giving response you can use the data given below if needed as context:
The user's Predicted GPA is {resp.gpa}. 
Here is their activity data: {resp.user_data}. 
Note:
Only use the references of the above data in the response if user asks for or if needed. 
"""

    try:
        passage = Response.model.generate_content(prompt) if hasattr(Response, "model") else None
        if passage is None:
            from response import model as module_model  # type: ignore
            passage = module_model.generate_content(prompt)
    except Exception:
        return [
            "Sorry, I couldn't generate a follow-up response right now. Please try again later.",
        ]

    from response import tokenize_sentences

    try:
        sentences = tokenize_sentences(passage.text)
    except Exception:
        # Very defensive: if tokenization fails, return raw text
        return [passage.text]

    # For the web app we let the browser handle speech via Web Speech API.
    return sentences
