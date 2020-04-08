from coffeehouse import LydiaAI

# Create the CoffeeHouse API instance
api_key = input("API Key: ")

# Create Lydia instance
lydia = LydiaAI(api_key)

# Create a new chat session (Like a conversation)
session = lydia.create_session()
print("Session ID: {0}".format(session.id))
print("Session Available: {0}".format(str(session.available)))
print("Session Language: {0}".format(str(session.language)))
print("Session Expires: {0}".format(str(session.expires)))

# Talk to the bot!
while True:
    output = session.think_thought(input("Input: "))
    print("Output: {0}".format(output))

# In the case you want to save the Session ID to reuse the session
# Use lydia to invoke think_thought instead, for example;
#
# while(True):
#     output = lydia.think_thought(session.id, input("Input: "))
#     print("Output: {0}".format(output))
#
# This is the same effect as above but uses the lydia instance directly.
