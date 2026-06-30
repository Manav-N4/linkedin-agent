def clean_topic(topic):
    if not isinstance(topic, str):
        raise TypeError("Topic must be a string")   
    topic = topic.strip()
    if len(topic) == 0:
        raise ValueError("Please insert topic")  
    return topic

if __name__ == "__main__":
    result = clean_topic("  Why founders ignore distribution  ")
    print("Test 1 passed:", result)
    try:
        clean_topic("")
    except ValueError as e:
        print("Test 2 caught:", e)
    try:
        clean_topic("  ")
    except ValueError as e:
        print("Test 3 caught:", e)
    try:
        clean_topic(7)
    except TypeError as e:
        print("Test 4 caught:", e)
