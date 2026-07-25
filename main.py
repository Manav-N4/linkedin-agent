from agents.writing_critic import rate_drafts
from agents.draft import generate_drafts
from agents.hook import generate_hooks
from agents.brief import create_brief
from agents.critic import be_critique
from agents.examples import get_examples
from agents.research import research_agent
from agents.orchestrator import classify_topic

def main(topic):
    print("Classifying topic...")
    classified_topic = classify_topic(topic)
    if classified_topic is None:
        print("Failed to classify topic")
        return
    print("Researching...")
    research = research_agent(classified_topic)
    if len(research) == 0:
        print("Failed to research")
        return
    print("Fetching suitable examples...")
    examples = get_examples(classified_topic, research)
    if len(examples) == 0:
        print("Failed to fetch examples")
        return
    print("Flagging mistakes...")
    critic = be_critique(classified_topic, research, examples)
    if len(critic) == 0:
        print("Failed to flag mistakes")
        return
    print("Creating a brief...")
    brief = create_brief(classified_topic, research, examples, critic)
    if brief is None:
        print("Failed to create brief")
        return
    print("Generating 5 Hooks...")
    hooks = generate_hooks(brief)
    if len(hooks) < 3:
        print("Failed to generate enough hooks")
        return
    print(hooks)
    print("Generating 2 drafts...")
    drafts = generate_drafts(hooks, brief)
    if len(drafts) == 0:
        print("Failed to generate drafts")
        return
    print(drafts)
    print("Scoring the drafts...")
    scoring = rate_drafts(hooks, drafts)
    if scoring is None:
        print("Failed to generate score")
        return
    print(scoring)
    print("Feel free to suggest any changes!")

if __name__ == "__main__":
    topic = input("Enter your topic")
    main(topic)