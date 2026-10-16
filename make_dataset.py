"""Step 1: creates data/tickets.csv (a practice dataset).
Later you can replace it with a real Kaggle dataset that has the same two columns: text,category
"""
import random
import pandas as pd

random.seed(42)

openers = ["", "Hi, ", "Hello, ", "Hey team, ", "Urgent: ", "Please help. ", "To whom it may concern, "]
closers = ["", " Please help.", " Thanks.", " This is frustrating.", " Need this fixed soon.", " Waiting for your reply."]

data = {
    "Billing": [
        "I was charged twice for my subscription this month",
        "Please refund my last payment",
        "My invoice shows the wrong amount",
        "Why was my credit card billed after I cancelled",
        "I need a receipt for my payment",
        "The discount code was not applied at checkout",
        "I want to change my billing plan to yearly",
        "My payment failed but the money left my account",
        "There is an unknown charge on my bank statement",
        "How do I update my card details for payments",
    ],
    "Technical Issue": [
        "The app crashes whenever I open the settings page",
        "The website is very slow and keeps freezing",
        "I get error 500 when I upload a file",
        "The page does not load on my phone",
        "Notifications are not working on my device",
        "The search feature returns no results",
        "The app shows a blank screen after the update",
        "Videos keep buffering and will not play",
        "The download button does nothing when I click it",
        "I keep getting a timeout error when saving my work",
    ],
    "Account Access": [
        "I forgot my password and cannot log in",
        "My account has been locked after too many attempts",
        "I did not receive the verification email",
        "How can I change the email address on my account",
        "Two factor authentication code is not working",
        "I want to delete my account permanently",
        "I cannot reset my password the link has expired",
        "Someone else may have accessed my account",
        "My username is not recognised when I sign in",
        "Please unlock my profile so I can sign in again",
    ],
    "Feedback": [
        "Love the new design great work",
        "It would be nice to have a dark mode option",
        "Your support team was very helpful thank you",
        "Please add an option to export data to Excel",
        "The latest update made everything easier to use",
        "I suggest adding more language support",
        "Great product but the tutorial could be clearer",
        "Thanks for the quick delivery I am very happy",
        "Could you add a feature to schedule tasks",
        "The interface looks clean and modern well done",
    ],
     "Shipping": [
        "Where is my order it has not arrived yet",
        "My package is delayed and the tracking is not updating",
        "I received the wrong item in my parcel",
        "The delivery person left my package at the wrong address",
        "How long will shipping take to my city",
        "My order arrived damaged in the box",
        "Can I change the delivery address for my order",
        "The courier says delivered but I never got the package",
        "Do you ship internationally and what are the delivery charges",
        "I want to return an item and need a return label",
    ],
}

rows = []
for category, sentences in data.items():
    for s in sentences:
        for _ in range(10):
            text = random.choice(openers) + s + random.choice(closers)
            rows.append({"text": text, "category": category})

df = pd.DataFrame(rows).sample(frac=1, random_state=1).reset_index(drop=True)
df.to_csv("data/tickets.csv", index=False)
print("Created data/tickets.csv with", len(df), "rows")
