import re
import traceback
import json
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage
from structured_assistant.utils import add_to_json_file

llm = ChatOllama(
    model="llama3.1",
    temperature=0,
)

# System prompt as the initial message
messages = [
    HumanMessage(content="""
    You're an chat assistant which chats with the user, you're collecting information about the single issue that has to provide.
    your task is to collect single problem in this interaction and get the following information:
    1. problem title
    2. problem description
    3. problem severity
    Your only objective to collect that information by performing a conversation with the user and asking questions.
    finally after you've collected each information, you'll need to confirm the user with the information you've collected.
    After you've colelcted this information you'll need to wrap it in a function_call format and return it to the user in a structured way.

    syntax for parameters:
    title: string # title of the problem, non-empty string
    description: string # description of the problem, non-empty string
    severity: int # 1-5
    note that contents inside the <create_issue> tags will be used as a function_call, so it needs to be valid json object
    with following keys: 
        title: string # title of the problem, non-empty string
        description: string # description of the problem, non-empty string
        severity: int # 1-5
    example output will be:
    
    ... chat history ...
    <create_issue>
    {
        "title": "problem title",
        "description": "problem description",
        "severity": 1
    }
    </create_issue>
    
    start the conversation by casually asking for the required information to create a single issue.
    """)
]


def can_save_issue(model_response):
    return re.search(r'<create_issue>(.*?)</create_issue>', model_response, re.DOTALL)

def try_save_issue_or_return_error_string(model_response):
    issue_match = can_save_issue(model_response)
    if issue_match:
        try:
            json_data = json.loads(issue_match.group(1))
            add_to_json_file(json_data)
            return True, "Issue successfully added to issues.json"
        except Exception as e:
            print(f"Error handling JSON file: {e}")
            error_string = "Error handling JSON file: {e}"
            import ipdb; ipdb.set_trace()
            return False, error_string
    else:
        return False, "No issue match found"
    

if __name__ == "__main__":
    # First response from the system
    result = llm.invoke(messages)
    print(result.content)
    task_completed = False
    while True:
        try:
            user_input = input("Enter your message (or 'quit' to exit): ")
            if user_input.lower() == 'quit':
                break
            
            messages.append(HumanMessage(content=user_input))
            result = llm.invoke(messages)
            messages.append(AIMessage(content=result.content))
            
            print("result.content", result.content)

            if can_save_issue(result.content):
                success = False
                n_trials = 3
                while not success and n_trials > 0:
                    success, message = try_save_issue_or_return_error_string(result.content)
                    if success:
                        print("Issue successfully added to issues.json, exiting...")
                        task_completed = True
                        break
                    else:
                        messages.append(HumanMessage(content="Failed to save the json file, can you retry giving correct json: " + message))
                        result = llm.invoke(messages)
                        messages.append(AIMessage(content=result.content))
                        n_trials -= 1
                if not success:
                    print("Failed to save the json file, exiting...")
                    break
            else:
                print(result.content)
        except Exception as e:
            print(f"An error occurred: {e}")
    if task_completed:
        print("Task completed, exiting...")
    else:
        print("Task not completed, exiting...")
