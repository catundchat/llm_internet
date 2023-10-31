import openai
import requests
from datetime import datetime
from langchain.llms import OpenAI

# Bing Search
subscription_key = 'your-subscription-key'
endpoint = 'your-endpoint'

# Microsoft Azure OpenAI Service
openai.api_type = "azure"
openai.api_base = "azure-openai-endpoint"
openai.api_version = "2023-07-01-preview"
openai.api_key = "azure-openai-key"

def search_bing(query):
    current_date = datetime.now().strftime('%Y-%m-%d')
    full_query = f"{query} {current_date}"
    mkt = 'zh-CN'
    params = {'q': full_query, 'mkt': mkt}
    headers = {'Ocp-Apim-Subscription-Key': subscription_key}

    try:
        response = requests.get(endpoint + '/v7.0/search', headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as ex:
        raise ex

def extract_multiple_snippets_from_search_results(results, num_snippets=1):
    # extract bing search result num_snippets abstracts
    snippets = []
    for i in range(min(num_snippets, len(results["webPages"]["value"]))):
        snippets.append(results["webPages"]["value"][i]["snippet"])
    return "\n".join(snippets)

def ask_gpt_with_multiple_search_results(full_query, search_result):
    combined_snippets = extract_multiple_snippets_from_search_results(search_result, 1)
    prompt = f"你是AI助手并且添加了新的实时信息的知识库，请根据这个身份回答问题。因为我已经将你接进网络，你可以了解到即时的新闻信息.Plz dont say'我不能了解实时信息'"

    response = openai.ChatCompletion.create(
        engine="gpt-35-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "system", "content": combined_snippets},
            {"role": "system", "content": full_query}
        ],
        temperature=0.8,
        max_tokens=800,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
        stream=True
    )
    for i in response:
        try:
            answer += i['choices'][0]['delta']['content']
        except Exception as e:
            break

    answer = response["choices"][0]["message"]["content"]
    return answer

def get_response(question, history=""):
    search_result = search_bing(question)
    gpt_response = ask_gpt_with_multiple_search_results(question, search_result)
    return gpt_response
