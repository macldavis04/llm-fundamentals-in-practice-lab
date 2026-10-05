import json
from helper import ask_claude, bedrock, get_model_id


def ask_claude_chat(messages, max_tokens=300):
    body = {"anthropic_version": "bedrock-2023-05-31", "max_tokens": max_tokens, "messages": messages}
    response = bedrock.invoke_model(modelId=get_model_id(), body=json.dumps(body))
    return json.loads(response["body"].read())["content"][0]["text"]


def header(title):
    print("\n" + "=" * 70 + f"\n{title}\n" + "=" * 70)


header("1.1 Memory across conversations")
fact = "My favorite fictional planet is Zorbon-9."
question = "What is my favorite fictional planet?"
first_reply = ask_claude(fact)
same_convo = ask_claude_chat([
    {"role": "user", "content": fact},
    {"role": "assistant", "content": first_reply},
    {"role": "user", "content": question},
])
print("Same conversation ->", same_convo)
print("New conversation  ->", ask_claude(question))

header("1.2 Position sensitivity")
with open("position_test_document.txt") as f:
    document = f.read()
print(f"(document is {len(document.split())} words)")
print(ask_claude(
    f"{document}\n\nThe document above contains three planted facts: an internal code name, "
    "a paper stock designation, and a proofread reference. List all three exactly as written."
))

header("2.1 Vague vs. specific (3 runs each)")
prompt_a = "Give me some tips for a presentation."
prompt_b = ("Give me 5 specific tips for opening a 15-minute client presentation on Q3 "
            "budget performance, aimed at keeping a skeptical finance audience engaged "
            "in the first two minutes.")
for label, p in (("A", prompt_a), ("B", prompt_b)):
    for run in range(1, 4):
        print(f"\n--- Prompt {label}, run {run} ---\n{ask_claude(p, max_tokens=400)}")

header("2.2 Same ask, different words")
p1 = "List three risks of migrating a legacy data warehouse to the cloud, one sentence each."
p2 = ("I'm advising a client who is moving their old on-prem data warehouse into the cloud. "
      "In one sentence apiece, what are 3 things that could go wrong?")
print("Wording 1:\n" + ask_claude(p1))
print("\nWording 2:\n" + ask_claude(p2))

header("2.3 Format instructions")
q = "What are three ways to reduce cloud infrastructure costs?"
for suffix in ("",
               " Answer as a numbered list, one sentence each.",
               ' Answer as a markdown table with exactly two columns: "Strategy" and "Estimated Impact".'):
    print(f"\n--- {q + suffix} ---\n{ask_claude(q + suffix, max_tokens=400)}")

header("3.1 Confidence vs. accuracy")
print(ask_claude("How many people attended the 2014 Hermon, Maine Fourth of July parade?"))

header("3.2 Forcing a fabrication")
leading_q = ("What paper stock designation is famously associated with the second archived draft "
             "of the essay 'A Brief History of Project Management'? Cite your source.")
print(ask_claude(leading_q))

header("3.3 The grounding fix")
print(ask_claude(
    f"Answer using ONLY the source below. If the source does not contain the answer, say so.\n\n"
    f"<source>\n{document}\n</source>\n\nQuestion: {leading_q}"
))