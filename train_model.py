from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import joblib


# ============================================================
# NBE INTENT TRAINING DATA
# ============================================================

training_data = [

    # --------------------------------------------------------
    # CARDS INFORMATION
    # --------------------------------------------------------

    ("What cards are available?", "cards_information"),
    ("What types of cards do you offer?", "cards_information"),
    ("Tell me about your cards", "cards_information"),
    ("What banking cards are available?", "cards_information"),
    ("What debit cards do you have?", "cards_information"),
    ("What credit cards are available?", "cards_information"),
    ("Do you have prepaid cards?", "cards_information"),
    ("Tell me about credit cards", "cards_information"),
    ("I want to know about cards", "cards_information"),
    ("What card options are available?", "cards_information"),
    ("Which cards can I get?", "cards_information"),
    ("What are the different card categories?", "cards_information"),


    # --------------------------------------------------------
    # CARD APPLICATION
    # --------------------------------------------------------

    ("How can I get a credit card?", "card_application"),
    ("How do I apply for a card?", "card_application"),
    ("I want to apply for a credit card", "card_application"),
    ("How can I get a debit card?", "card_application"),
    ("What do I need to get a card?", "card_application"),
    ("How can I request a card?", "card_application"),
    ("I need a new card", "card_application"),
    ("How do I obtain a card?", "card_application"),
    ("What are the requirements for a card?", "card_application"),


    # --------------------------------------------------------
    # CARD SECURITY
    # --------------------------------------------------------

    ("I lost my card", "card_security"),
    ("My card was stolen", "card_security"),
    ("Someone stole my card", "card_security"),
    ("What should I do if I lose my card?", "card_security"),
    ("My card is missing", "card_security"),
    ("I think someone used my card", "card_security"),
    ("My card may be compromised", "card_security"),
    ("How do I protect my card?", "card_security"),


    # --------------------------------------------------------
    # LOANS INFORMATION
    # --------------------------------------------------------

    ("What loans are available?", "loan_information"),
    ("What types of loans do you offer?", "loan_information"),
    ("Tell me about loans", "loan_information"),
    ("What financing options are available?", "loan_information"),
    ("Do you offer personal loans?", "loan_information"),
    ("Do you have auto loans?", "loan_information"),
    ("Do you offer home finance?", "loan_information"),
    ("What financing products are available?", "loan_information"),
    ("I want to know about loans", "loan_information"),
    ("What loan products do you have?", "loan_information"),


    # --------------------------------------------------------
    # LOAN APPLICATION
    # --------------------------------------------------------

    ("How can I apply for a loan?", "loan_application"),
    ("How do I get a loan?", "loan_application"),
    ("I want to apply for a loan", "loan_application"),
    ("What do I need for a loan?", "loan_application"),
    ("What are the loan requirements?", "loan_application"),
    ("How can I request financing?", "loan_application"),
    ("How do I apply for financing?", "loan_application"),
    ("What documents are needed for a loan?", "loan_application"),


    # --------------------------------------------------------
    # ACCOUNT INFORMATION
    # --------------------------------------------------------

    ("What types of accounts are available?", "account_information"),
    ("Tell me about bank accounts", "account_information"),
    ("What accounts do you offer?", "account_information"),
    ("What savings accounts are available?", "account_information"),
    ("Do you have current accounts?", "account_information"),
    ("I want to know about accounts", "account_information"),
    ("What account options are available?", "account_information"),
    ("Tell me about savings accounts", "account_information"),
    ("What types of bank accounts do you have?", "account_information"),


    # --------------------------------------------------------
    # ACCOUNT OPENING
    # --------------------------------------------------------

    ("How do I open an account?", "account_opening"),
    ("I want to open a bank account", "account_opening"),
    ("How can I open an account?", "account_opening"),
    ("What do I need to open an account?", "account_opening"),
    ("What documents are required to open an account?", "account_opening"),
    ("How can I create a savings account?", "account_opening"),
    ("I need a new bank account", "account_opening"),


    # --------------------------------------------------------
    # GENERAL
    # --------------------------------------------------------

    ("Hello", "greeting"),
    ("Hi", "greeting"),
    ("Hello there", "greeting"),
    ("Good morning", "greeting"),
    ("Good afternoon", "greeting"),
    ("Hey", "greeting"),

]


# ============================================================
# SPLIT DATA
# ============================================================

texts = [
    item[0]
    for item in training_data
]

labels = [
    item[1]
    for item in training_data
]


# ============================================================
# CREATE ML PIPELINE
# ============================================================

model = Pipeline([

    (
        "tfidf",

        TfidfVectorizer(

            lowercase=True,

            ngram_range=(1, 2),

            sublinear_tf=True

        )
    ),

    (
        "classifier",

        LogisticRegression(

            max_iter=2000,

            C=4

        )
    )

])


# ============================================================
# TRAIN MODEL
# ============================================================

print("\n🧠 Training NBE Intent Classifier...\n")

model.fit(
    texts,
    labels
)


# ============================================================
# SAVE MODEL
# ============================================================

joblib.dump(
    model,
    "intent_model.pkl"
)


print("✅ Model trained successfully!")

print(
    f"📚 Training examples: {len(texts)}"
)

print(
    f"🎯 Intent categories: {len(set(labels))}"
)

print("\n📌 Intents:")

for intent in sorted(set(labels)):

    print(
        f"   • {intent}"
    )


print(
    "\n💾 Saved as: intent_model.pkl"
)

print(
    "\n🚀 ML model is ready!"
)