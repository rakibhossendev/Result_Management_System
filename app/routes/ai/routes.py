import os
from dotenv import load_dotenv
import json
from flask import Blueprint, render_template, request, jsonify, session
from mistralai.client import Mistral
from app.ai.tools import (
    get_student_data, 
    get_student_by_roll,
    get_student_attendance,
    get_student_marks,
    get_class_attendance,
    get_class_marks_summary
)


ai_bp = Blueprint("ai", __name__, url_prefix="")

load_dotenv() # Loading all the vars from the .env file. Make life ezzy.

MODEL_NAME = "mistral-small-latest"

def get_mistral_client():
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise RuntimeError("MISTRAL_API_KEY is not set")
    return Mistral(api_key=api_key)


# ---------------------------------------------------------------------------
# Tool registry
#
# Each entry maps a tool name (what the model calls) to:
#   - "fn": the actual Python function to run (from app/ai/tools.py)
#   - "schema": the JSON schema the model sees, describing when/how to call it
#
# To add a new tool later: write the function in app/ai/tools.py (same
# pattern as get_student_data — scoped by teacher_id, returns a plain dict),
# then add one entry here. No other route changes needed.
# ---------------------------------------------------------------------------

TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "get_student_by_roll",
            "description": (
                "Fetch a single student's profile (name, semester, group, CGPA, "
                "department) by roll number. This is the human-facing student ID. "
                "Only returns students belonging to the current teacher."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "student_roll": {
                        "type": "integer",
                        "description": "The student's roll number (unique, user-facing ID).",
                    },
                },
                "required": ["student_roll"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_student_data",
            "description": (
                "Fetch a single student's profile by internal student ID. "
                "Prefer get_student_by_roll for user-facing lookups. "
                "Only returns students belonging to the current teacher."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "student_id": {
                        "type": "integer",
                        "description": "The student's internal student_id (auto-increment).",
                    },
                },
                "required": ["student_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_student_attendance",
            "description": (
                "Fetch all attendance records for a student by their roll number. "
                "Scoped to the current teacher. Returns a list of dates and statuses."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "student_roll": {
                        "type": "integer",
                        "description": "The student's roll number (unique, user-facing ID).",
                    },
                },
                "required": ["student_roll"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_student_marks",
            "description": (
                "Fetch all marks for a student by roll number. Scoped to the current teacher. "
                "Returns subject, topic, full marks, and obtained marks."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "student_roll": {
                        "type": "integer",
                        "description": "The student's roll number.",
                    },
                },
                "required": ["student_roll"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_class_attendance",
            "description": (
                "Fetch attendance summary for all students in a given semester and group. "
                "Scoped to the current teacher. Returns each student's attendance percentage."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "semester": {
                        "type": "integer",
                        "description": "Semester number (e.g., 1, 2, 3).",
                    },
                    "group": {
                        "type": "string",
                        "description": "Group letter (single character, e.g., 'A').",
                    },
                },
                "required": ["semester", "group"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_class_marks_summary",
            "description": (
                "Fetch marks summary for all students in a given semester and group. "
                "Scoped to the current teacher. Returns average, min, max per subject."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "semester": {
                        "type": "integer",
                        "description": "Semester number.",
                    },
                    "group": {
                        "type": "string",
                        "description": "Group letter (single character).",
                    },
                },
                "required": ["semester", "group"],
            },
        },
    },
]


def dispatch_tool_call(tool_name, arguments):
    """
    Runs a tool call by name, injecting the current teacher_id from the
    session so every tool stays scoped to "this teacher's data" without
    the model ever needing to know or supply that id itself.
    """
    teacher_id = session.get("teacher_id")
    if tool_name == "get_student_by_roll":
        result = get_student_by_roll(
            student_roll=arguments.get("student_roll"),
            teacher_id=teacher_id,
        )
        return result if result is not None else {"error": "student not found"}

    if tool_name == "get_student_data":
        result = get_student_data(
            student_id=arguments.get("student_id"),
            teacher_id=teacher_id,
        )
        return result if result is not None else {"error": "student not found"}

    if tool_name == "get_student_attendance":
        result = get_student_attendance(
            student_roll=arguments.get("student_roll"),
            teacher_id=teacher_id,
        )
        return result if result is not None else {"error": "student not found"}

    if tool_name == "get_student_marks":
        result = get_student_marks(
            student_roll=arguments.get("student_roll"),
            teacher_id=teacher_id,
        )
        return result if result is not None else {"error": "student not found"}

    if tool_name == "get_class_attendance":
        result = get_class_attendance(
            semester=arguments.get("semester"),
            group=arguments.get("group"),
            teacher_id=teacher_id,
        )
        return result if result is not None else {"error": "no data found"}

    if tool_name == "get_class_marks_summary":
        result = get_class_marks_summary(
            semester=arguments.get("semester"),
            group=arguments.get("group"),
            teacher_id=teacher_id,
        )
        return result if result is not None else {"error": "no data found"}

    return {"error": f"unknown tool: {tool_name}"}

@ai_bp.route("/ask", methods=["GET"])
def ask_page():
    """
    Renders the chat page. This is what the user visits directly:
    http://localhost:5000/ask
    """
    # Optional: gate this behind login like your other dashboards
    # if not session.get("teacher_id") and not session.get("principal_id") and not session.get("admin_id"):
    #     return redirect(url_for("auth.login"))
    return render_template("ai/ask.html")


@ai_bp.route("/ask/message", methods=["POST"])
def ask_message():
    """
    Backend endpoint the chat page calls via fetch() under the hood.
    The user never sees this URL or interacts with it directly —
    it's invisible plumbing behind the chatbox on /ask.

    Flow:
      1. Send the user's message + tool schema to Mistral.
      2. If Mistral wants to call a tool, run it via dispatch_tool_call
         and send the result back as a "tool" message.
      3. Return Mistral's final natural-language reply.
    """
    data = request.get_json(silent=True) or {}
    user_message = (data.get("message") or "").strip()

    if not user_message:
        return jsonify({"error": "message is required"}), 400
    try:
        client = get_mistral_client()

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant for school teachers. "
                    "You help teachers look up student data, attendance, and marks. "
                    "Always use the available tools to fetch data — never guess or invent student information. "
                    "Only answer questions relevant to the school system. "
                    "DO NOT use any extra formatting. Respond in plain text. "
                    "When a user asks about anything, don't just give the data only factually. Respond with natural language. "
                    "Have a Gen-Z tone. Respond with energy!"
                )
            },
            {"role": "user", "content": user_message}
        ]

        response = client.chat.complete(
            model=MODEL_NAME,
            messages=messages,
            tools=TOOLS_SCHEMA,
            tool_choice="auto",
        )
        choice_message = response.choices[0].message
        tool_calls = getattr(choice_message, "tool_calls", None)
        if tool_calls:
            # Echo the assistant's tool-call message back into the
            # conversation, then append one "tool" message per call
            # with the result, then ask the model to produce the
            # final natural-language answer.
            messages.append(choice_message)

            for call in tool_calls:
                tool_name = call.function.name
                try:
                    arguments = json.loads(call.function.arguments)
                except (TypeError, json.JSONDecodeError):
                    arguments = {}

                tool_result = dispatch_tool_call(tool_name, arguments)

                messages.append({
                    "role": "tool",
                    "name": tool_name,
                    "tool_call_id": call.id,
                    "content": json.dumps(tool_result),
                })

            follow_up = client.chat.complete(
                model=MODEL_NAME,
                messages=messages,
            )
            reply_text = follow_up.choices[0].message.content
        else:
            reply_text = choice_message.content
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500
    return jsonify({"reply": reply_text})