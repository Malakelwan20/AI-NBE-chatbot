from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader
import os
import joblib
import numpy as np


# ============================================================
# 1. INITIALIZATION
# ============================================================

load_dotenv(override=True)

app = Flask(__name__)

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


# ============================================================
# 2. GROQ CONFIGURATION
# ============================================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    print("❌ ERROR: GROQ_API_KEY was not found in .env")
else:
    print("✅ Groq API key loaded successfully.")


client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)


# ============================================================
# 3. KNOWLEDGE BASE
# ============================================================

KNOWLEDGE_FOLDER = os.path.join(
    BASE_DIR,
    "knowledge"
)

print("\n📁 Knowledge folder:")
print(KNOWLEDGE_FOLDER)


if os.path.exists(KNOWLEDGE_FOLDER):

    print("\n📄 Files found:")
    print(os.listdir(KNOWLEDGE_FOLDER))

else:

    print("❌ KNOWLEDGE FOLDER DOES NOT EXIST")


# ============================================================
# 4. LOAD ML MODEL
# ============================================================

MODEL_PATH = os.path.join(
    BASE_DIR,
    "intent_model.pkl"
)

try:

    intent_model = joblib.load(
        MODEL_PATH
    )

    print(
        "🧠 ML Intent Classifier loaded successfully."
    )

except Exception as e:

    intent_model = None

    print(
        f"❌ Could not load ML model: {e}"
    )


# ============================================================
# 5. LOAD PDF KNOWLEDGE
# ============================================================

def load_pdf_documents():

    documents = []

    if not os.path.exists(
        KNOWLEDGE_FOLDER
    ):
        return documents

    for filename in os.listdir(
        KNOWLEDGE_FOLDER
    ):

        if not filename.lower().endswith(
            ".pdf"
        ):
            continue

        filepath = os.path.join(
            KNOWLEDGE_FOLDER,
            filename
        )

        try:

            reader = PdfReader(
                filepath
            )

            text = ""

            for page in reader.pages:

                try:

                    page_text = (
                        page.extract_text()
                    )

                    if page_text:

                        text += (
                            page_text
                            + "\n"
                        )

                except Exception as e:

                    print(
                        f"⚠️ Page error in "
                        f"{filename}: {e}"
                    )

            text = text.strip()

            if text:

                documents.append({

                    "filename": filename,

                    "text": text

                })

                print(
                    f"📄 Loaded: {filename} "
                    f"| Characters: {len(text)}"
                )

            else:

                print(
                    f"⚠️ {filename} is empty."
                )

        except Exception as e:

            print(
                f"❌ Error loading "
                f"{filename}: {e}"
            )

    return documents


KNOWLEDGE_BASE = load_pdf_documents()


print(
    f"\n📚 Knowledge base loaded: "
    f"{len(KNOWLEDGE_BASE)} documents"
)


# ============================================================
# 6. ML INTENT PREDICTION
# ============================================================

def predict_intent(question):

    if intent_model is None:

        return "unknown", 0.0

    try:

        prediction = (
            intent_model
            .predict([question])[0]
        )

        probabilities = (
            intent_model
            .predict_proba([question])[0]
        )

        confidence = float(
            np.max(probabilities)
        )

        print(
            f"🧠 ML Intent: {prediction}"
        )

        print(
            f"📊 ML Confidence: "
            f"{confidence * 100:.2f}%"
        )

        return (
            prediction,
            confidence
        )

    except Exception as e:

        print(
            f"❌ ML prediction error: {e}"
        )

        return (
            "unknown",
            0.0
        )


# ============================================================
# 7. INTENT → PDF MAPPING
# ============================================================

INTENT_TO_FILES = {

    "cards_information": [
        "cards.pdf"
    ],

    "card_application": [
        "cards.pdf"
    ],

    "card_security": [
        "cards.pdf"
    ],

    "loan_information": [
        "loans.pdf"
    ],

    "loan_application": [
        "loans.pdf"
    ],

    "account_information": [
        "accounts.pdf"
    ],

    "account_opening": [
        "accounts.pdf"
    ]

}


# ============================================================
# 8. SEARCH KNOWLEDGE BASE
# ============================================================

def search_knowledge(
    question,
    intent,
    confidence
):

    print(
        "\n🔎 Searching knowledge base..."
    )

    if (
        confidence >= 0.55
        and
        intent in INTENT_TO_FILES
    ):

        target_files = (
            INTENT_TO_FILES[intent]
        )

        print(
            f"🎯 Intent recognized: "
            f"{intent}"
        )

        print(
            f"📊 Confidence: "
            f"{confidence * 100:.2f}%"
        )

        print(
            f"📄 Searching: "
            f"{target_files}"
        )

    else:

        target_files = [

            "accounts.pdf",
            "cards.pdf",
            "loans.pdf"

        ]

        print(
            "⚠️ ML confidence is low."
        )

        print(
            "📚 Searching all PDFs."
        )

    context_parts = []

    for document in KNOWLEDGE_BASE:

        filename = document[
            "filename"
        ]

        if filename not in target_files:
            continue

        text = document[
            "text"
        ]

        if not text.strip():
            continue

        context_parts.append(

            f"""
==================================================
SOURCE: {filename}
==================================================

{text}
"""

        )

    if not context_parts:

        print(
            "❌ No relevant PDF content found."
        )

        return ""

    context = "\n".join(
        context_parts
    )

    print(
        f"✅ PDF content found: "
        f"{len(context)} characters"
    )

    return context


# ============================================================
# 9. HOME PAGE
# ============================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# ============================================================
# 10. CHAT API
# ============================================================

@app.route(
    "/chat",
    methods=["POST"]
)
def chat():

    try:

        # ----------------------------------------------------
        # GET USER MESSAGE
        # ----------------------------------------------------

        data = request.get_json()

        if not data:

            return jsonify({

                "response":
                "Please enter a question."

            })

        user_message = data.get(
            "message",
            ""
        ).strip()

        if not user_message:

            return jsonify({

                "response":
                "Please enter a question."

            })

        print("\n")
        print("=" * 60)

        print(
            f"👤 USER: {user_message}"
        )

        print("=" * 60)


        # ====================================================
        # ML PREDICTION
        # ====================================================

        intent, confidence = (
            predict_intent(
                user_message
            )
        )


        # ====================================================
        # SEARCH PDF
        # ====================================================

        context = search_knowledge(

            user_message,

            intent,

            confidence

        )


        # ====================================================
        # SYSTEM PROMPT
        # ====================================================

        system_prompt = """

You are the NBE Smart Banking Assistant.

You are a professional banking customer-service
assistant for a DEMONSTRATION PROJECT.

Your job is to answer the customer's question
using the provided synthetic NBE knowledge base.

IMPORTANT RULES:

1. Use the provided knowledge base as the source
   of truth.

2. The information in the PDFs is DEMO DATA created
   specifically for this project.

3. NEVER invent:
   - fees
   - interest rates
   - limits
   - eligibility rules
   - banking policies
   - products
   - requirements
   - application decisions

4. If the answer is available in the knowledge base,
   answer it directly.

5. If the answer is not available, clearly explain
   that it is not available in the current demo
   knowledge base.

6. Never pretend to perform an actual banking
   transaction.

7. Never ask for:
   - Passwords
   - PINs
   - OTPs
   - CVV
   - Full card numbers
   - Account passwords

8. Be professional, friendly and natural.

9. Avoid sounding robotic.

10. Use short paragraphs and bullet points when
    useful.

11. Do not describe synthetic demo information as
    official current NBE information.

"""


        # ====================================================
        # USER PROMPT
        # ====================================================

        if context:

            user_prompt = f"""

CUSTOMER QUESTION:

{user_message}


==================================================
ML CLASSIFICATION
==================================================

Detected Intent:
{intent}

ML Confidence:
{confidence * 100:.2f}%


==================================================
NBE DEMO KNOWLEDGE BASE
==================================================

{context}


==================================================
RESPONSE INSTRUCTIONS
==================================================

Answer the customer's question naturally.

Use the knowledge base above.

If the information exists in the knowledge base,
use it directly.

Do NOT invent information.

Keep the answer professional and easy to understand.

"""

        else:

            user_prompt = f"""

CUSTOMER QUESTION:

{user_message}


The current NBE demo knowledge base does not contain
relevant information for this question.

Do not invent an answer.

Politely explain that the requested information is
not currently available in the demo knowledge base.

"""


        # ====================================================
        # CALL GROQ
        # ====================================================

        print(
            "\n🤖 Sending request to Groq..."
        )

        response = (
            client
            .chat
            .completions
            .create(

                model="openai/gpt-oss-20b",

                messages=[

                    {
                        "role": "system",
                        "content": system_prompt
                    },

                    {
                        "role": "user",
                        "content": user_prompt
                    }

                ],

                temperature=0.3,

                max_tokens=700

            )
        )


        # ====================================================
        # DEBUG GROQ RESPONSE
        # ====================================================

        print(
            "✅ Groq response received!"
        )

        print(
            "📝 CONTENT:",
            repr(
                response
                .choices[0]
                .message
                .content
            )
        )

        print(
            "🏁 FINISH REASON:",
            response
            .choices[0]
            .finish_reason
        )

        print(
            "🧠 REASONING:",
            repr(
                response
                .choices[0]
                .message
                .reasoning
            )
        )


        # ====================================================
        # GET ANSWER
        # ====================================================

        answer = (
            response
            .choices[0]
            .message
            .content
        )

        if answer is None:

            answer = ""

        answer = answer.strip()


        # ====================================================
        # FALLBACK IF CONTENT IS EMPTY
        # ====================================================

        if not answer:

            print(
                "⚠️ Groq returned empty content."
            )

            answer = (
                "I received the request, "
                "but the AI did not return "
                "a text answer. Please try again."
            )


        # ====================================================
        # PRINT ANSWER
        # ====================================================

        print(
            "\n🤖 AI ANSWER:"
        )

        print(answer)

        print(
            "\n" + "=" * 60
        )


        # ====================================================
        # RETURN RESPONSE TO FRONTEND
        # ====================================================

        return jsonify({

            "response": answer,

            "intent": intent,

            "confidence": round(
                confidence * 100,
                2
            )

        })


    # ========================================================
    # ERROR HANDLING
    # ========================================================

    except Exception as e:

        print(
            "\n❌ ERROR"
        )

        print(
            "ERROR TYPE:",
            type(e).__name__
        )

        print(
            "ERROR MESSAGE:",
            str(e)
        )

        return jsonify({

            "response":
            "I'm sorry, but I couldn't process your request right now. Please try again.",

            "intent":
            "error",

            "confidence":
            0

        }), 500


# ============================================================
# 11. START SERVER
# ============================================================

if __name__ == "__main__":

    print("\n")

    print("=" * 60)

    print(
        "🏦 NBE SMART BANKING ASSISTANT"
    )

    print("=" * 60)

    print(
        "🧠 ML Intent Classification: ENABLED"
    )

    print(
        "📚 PDF Knowledge Base: ENABLED"
    )

    print(
        "🤖 Groq AI: ENABLED"
    )

    print("=" * 60)

    print(
        "🚀 Starting Flask server..."
    )

    print("=" * 60)

    print("\n")

    app.run(

        host="127.0.0.1",

        port=5000,

        debug=True

    )