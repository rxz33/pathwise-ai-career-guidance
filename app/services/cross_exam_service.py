from app.services.mongo_service import update_user_by_email
import random

async def analyze_cross_exam_answers(email: str, answers: dict):
    """
    Analyze user answers from cross-examination step.
    (Dummy implementation for now – will later connect to Groq AI)
    """
    # Generate a simple consistency score
    score = random.randint(60, 95)  # placeholder logic
    
    summary = "User provided {} answers. Overall consistency looks {}.".format(
        len(answers), "good" if score > 75 else "moderate"
    )

    insights = {
        "strengths": ["clear communication", "self-awareness"],
        "weaknesses": ["needs clarity in long-term goals"],
        "gaps": ["technical depth in chosen career field"]
    }

    # Prepare result
    result = {
        "cross_exam": {
            "answers": answers,
            "summary": summary,
            "consistency_score": score,
            "insights": insights
        }
    }

    # Store in MongoDB under this user
    await update_user_by_email(email, {"tests": result})

    return result
