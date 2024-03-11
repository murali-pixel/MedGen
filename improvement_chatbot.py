# import requests
# import openai  

# # Give your medgen end point
# MEDGEN_API_ENDPOINT = "medgen api"

# openai.api_key = "api key"

# def get_medgen_summary(text):
#     response = requests.post(MEDGEN_API_ENDPOINT, json={"text": text})
#     if response.status_code == 200:
#         return response.json()["summary"]
#     else:
#         return "Error in MedGen API"

# def get_gpt_response(prompt):
#     response = openai.Completion.create(
#         engine="text-davinci-003",
#         prompt=prompt,
#         max_tokens=150
#     )
#     return response.choices[0].text.strip()

# def main():
#     print("Chatbot: Hi! How can I assist you today?")
#     user_input = input("User: ")

#     if "summarize" in user_input.lower():
#         # Assume the user wants to summarize a document
#         document_text = input("Chatbot: Sure! Please provide the document text: ")
#         summary = get_medgen_summary(document_text)

#         prompt = f"Generate a follow-up question for the summarized text: '{summary}'"
#         follow_up_question = get_gpt_response(prompt)

#         print(f"Chatbot: Here's the summary: {summary}")
#         print(f"Chatbot: And a follow-up question: {follow_up_question}")

#     else:
#         print("Chatbot: I'm sorry, I didn't understand. Please specify if you want to summarize a document.")

# if __name__ == "__main__":
#     main()


#"The below code is to use open AI model generately by the user"
import openai

# replace this key with yours
openai.api_key = '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'

def generate_prompt_with_history(text, history):
    prompt = "The following is a conversation between a human and an AI assistant named Baize (named after a mythical creature in Chinese folklore). Baize is an open-source AI assistant developed by UCSD and Sun Yat-Sen University. The human and the AI assistant take turns chatting. Human statements start with [|Human|] and AI assistant statements start with [|AI|]. The AI assistant always provides responses in as much detail as possible, and in Markdown format. The AI assistant always declines to engage with topics, questions and instructions related to unethical, controversial, or sensitive issues. Complete the transcript in exactly that format.\n[|Human|]Hello!\n[|AI|]Hi!"
    history = ["\n[|Human|]{}\n[|AI|]{}".format(x[0], x[1]) for x in history]
    history.append("\n[|Human|]{}\n[|AI|]".format(text))
    history_text = ""
    flag = False
    for x in history[::-1]:
        if len(prompt + history_text + x) <= 4096:  
            history_text = x + history_text
            flag = True
        else:
            break
    if flag:
        return prompt + history_text
    else:
        return None

def medgen_answer_generation(question, history):
    prompt = generate_prompt_with_history(question, history)
    if prompt:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=256,
            temperature=0.7
        )
        return response.choices[0].text.strip()
    else:
        return "Error: Unable to generate prompt."
    
data = """A neural network is a series of algorithms that endeavors to recognize underlying relationships in a set of " \
            "data through a process that mimics the way the human brain operates. In this sense, neural networks refer to " \
            "systems of neurons, either organic or artificial in nature.

    # reference: https://medlineplus.gov/druginfo/meds/a682878.html
    Prescription aspirin is used to relieve the symptoms of rheumatoid arthritis (arthritis caused by swelling " \
            "of the lining of the joints), osteoarthritis (arthritis caused by breakdown of the lining of the joints), " \
            "systemic lupus erythematosus (condition in which the immune system attacks the joints and organs and causes " \
            "pain and swelling) and certain other rheumatologic conditions (conditions in which the immune system " \
            "attacks parts of the body).

    # reference: https://www.medicalnewstoday.com/articles/161255
    People can buy aspirin over the counter without a prescription. Everyday uses include relieving headache, " \
            "reducing swelling, and reducing a fever. Taken daily, aspirin can lower the risk of cardiovascular events, " \
            "such as a heart attack or stroke, in people with a high risk. Doctors may administer aspirin immediately" \
            " after a heart attack to prevent further clots and heart tissue death."""
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "user",
        
            "content": f"Summarize the text: {data}",
        },
    ],
)
response1 = response["choices"][0]["message"]["content"]

print("OpenAI Generated  " + response1)

print("-------------------------------------------------------------------------------------------------")
question1 = "what is mean by myophia and its symptoms?"
history = []
ans1 = medgen_answer_generation(question1, history).replace("\n[|Human|]", "")

print("OpenAI Generated  " + ans1)


