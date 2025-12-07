import os
import pickle

from flask import Flask, render_template, request, redirect, url_for, flash

from core import (
    build_user_data,
    validate_total_hours,
    predict_and_generate_response,
    answer_followup_question,
)


app = Flask(__name__)
app.secret_key = os.environ.get("GRADIFY_FLASK_SECRET", "dev-secret-key")


# Load the regression model once at startup
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model_pickel")
with open(MODEL_PATH, "rb") as f:
    regression_model = pickle.load(f)


@app.route("/", methods=["GET"])
def survey_form():
    return render_template("survey.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        name = request.form.get("name", "").strip()
        study = float(request.form.get("study_hours", "0") or 0)
        eca = float(request.form.get("eca_hours", "0") or 0)
        sleep = float(request.form.get("sleep_hours", "0") or 0)
        social = float(request.form.get("social_hours", "0") or 0)
        physical = float(request.form.get("physical_hours", "0") or 0)
        user_text = request.form.get("user_text", "").strip()
    except ValueError:
        flash("All numeric fields must be valid numbers.", "error")
        return redirect(url_for("survey_form"))

    is_valid, total = validate_total_hours(study, eca, sleep, social, physical)
    if not is_valid:
        flash(
            f"Total hours across all activities cannot exceed 24. You entered {total:.1f} hours.",
            "error",
        )
        # Re-render with previous values
        return render_template(
            "survey.html",
            name=name,
            study_hours=study,
            eca_hours=eca,
            sleep_hours=sleep,
            social_hours=social,
            physical_hours=physical,
            user_text=user_text,
        )

    user_data = build_user_data(study, eca, sleep, social, physical, user_text)

    try:
        predicted_gpa, adjusted_gpa, sentences = predict_and_generate_response(
            regression_model, user_data
        )
    except Exception:
        flash("Something went wrong while generating your prediction. Please try again.", "error")
        return render_template("survey.html")

    # Render an intermediate "preparing" page where Gradify speaks and shows advice.
    return render_template(
        "preparing.html",
        name=name,
        predicted_gpa=predicted_gpa,
        adjusted_gpa=adjusted_gpa,
        advice_sentences=sentences,
        study_hours=study,
        eca_hours=eca,
        sleep_hours=sleep,
        social_hours=social,
        physical_hours=physical,
        user_text=user_text,
    )


@app.route("/dashboard", methods=["POST"])
def dashboard():
    """Show the main prediction dashboard after the preparing page.

    We rebuild context from hidden fields but do not re-call Gemini.
    """
    name = request.form.get("name", "").strip()

    try:
        predicted_gpa = float(request.form.get("predicted_gpa", "0") or 0)
        adjusted_gpa = float(request.form.get("adjusted_gpa", "0") or 0)
        study = float(request.form.get("study_hours", "0") or 0)
        eca = float(request.form.get("eca_hours", "0") or 0)
        sleep = float(request.form.get("sleep_hours", "0") or 0)
        social = float(request.form.get("social_hours", "0") or 0)
        physical = float(request.form.get("physical_hours", "0") or 0)
        user_text = request.form.get("user_text", "").strip()
    except ValueError:
        flash("There was an issue with your previous data. Please resubmit the survey.", "error")
        return redirect(url_for("survey_form"))

    return render_template(
        "result.html",
        name=name,
        predicted_gpa=predicted_gpa,
        adjusted_gpa=adjusted_gpa,
        advice_sentences=[],
        followup_question=None,
        followup_answers=[],
        study_hours=study,
        eca_hours=eca,
        sleep_hours=sleep,
        social_hours=social,
        physical_hours=physical,
        user_text=user_text,
    )


@app.route("/ask", methods=["POST"])
def ask():
    # Rebuild context from hidden fields
    name = request.form.get("name", "").strip()
    question = request.form.get("question", "").strip()

    try:
        predicted_gpa = float(request.form.get("predicted_gpa", "0") or 0)
        adjusted_gpa = float(request.form.get("adjusted_gpa", "0") or 0)
        study = float(request.form.get("study_hours", "0") or 0)
        eca = float(request.form.get("eca_hours", "0") or 0)
        sleep = float(request.form.get("sleep_hours", "0") or 0)
        social = float(request.form.get("social_hours", "0") or 0)
        physical = float(request.form.get("physical_hours", "0") or 0)
        user_text = request.form.get("user_text", "").strip()
    except ValueError:
        flash("There was an issue with your previous data. Please resubmit the survey.", "error")
        return redirect(url_for("survey_form"))

    if not question:
        flash("Please enter a question for Gradify.", "error")

    user_data = build_user_data(study, eca, sleep, social, physical, user_text)

    followup_answers = []
    if question:
        try:
            followup_answers = answer_followup_question(user_data, adjusted_gpa, question)
        except Exception:
            followup_answers = [
                "Sorry, I couldn't generate a follow-up response right now. Please try again later.",
            ]

    # Re-render the result page with the new follow-up content
    return render_template(
        "result.html",
        name=name,
        predicted_gpa=predicted_gpa,
        adjusted_gpa=adjusted_gpa,
        advice_sentences=[],  # original advice is not re-used here; optional to include
        followup_question=question,
        followup_answers=followup_answers,
        study_hours=study,
        eca_hours=eca,
        sleep_hours=sleep,
        social_hours=social,
        physical_hours=physical,
        user_text=user_text,
    )


if __name__ == "__main__":
    # For development: listen on all interfaces so other devices on the network can access it.
    # Use a proper WSGI/ASGI server and tighter firewall rules for real deployment.
    app.run(host="0.0.0.0", port=5000, debug=True)
