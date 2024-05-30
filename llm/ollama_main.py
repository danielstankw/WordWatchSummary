import argparse
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatOllama
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain_core.output_parsers import StrOutputParser
import json
import re
import os

MODEL_NAME = "gemma:2b"
BASE_URL = "http://127.0.0.1:11434"
TEMP = 0.7

# path where LLM output will be saved
summary_path = "./data/summary"
# path where the scraped articles are
scrape_path = "./data/scrape"

# Create the PromptTemplate with the read content
prompt_template = PromptTemplate.from_template(
    """As a professional summarizer, create a comprehensive summary of the provided text of maximum of 200 words, be it an article, post, conversation, or passage, while adhering to these guidelines:
1. Craft a summary that is detailed, thorough, in-depth, and complex, while maintaining clarity.
2. Incorporate main ideas and essential information, eliminating extraneous language and focusing on critical aspects.
3. Rely strictly on the provided text, without including external information.
4. Format the summary in paragraph form for easy understanding.
5.Conclude your notes with [End of Notes, Message #X] to indicate completion, where "X" represents the total number of messages that I have sent. In other words, include a message counter where you start with #1 and add 1 to the message counter every time I send a message.

By following this optimized prompt, you will generate an effective summary that encapsulates the essence of the given text in a clear, detailed, and reader-friendly manner. Optimize output as markdown file.

"{document}"

Additionally define the sentiment of the article and display it as:
SENTIMENT: positive/ negative/ sad/ happy etc.                                                                                                                                      
DETAILED SUMMARY"""
)

if not os.path.exists(summary_path):
    os.makedirs(summary_path)

# Initialize the LLM and LLMChain
llm = ChatOllama(model=MODEL_NAME, base_url=BASE_URL, temperature=TEMP)
llm_chain = prompt_template | llm | StrOutputParser()

# loop through files in scraped directory
for filename in os.listdir(scrape_path):
    file_path = os.path.join(scrape_path, filename)
    # open each file in the scraped folder
    with open(file_path, "r") as scraped_file:
        data = json.load(scraped_file)
        # parse content and url
        doc_content = data.get("content", "")
        doc_url = data.get("url", "")

        # print(doc_url)

        # if document content exists
        if doc_content:
            llm_summary = llm_chain.invoke(doc_content)
            print(llm_summary)
            
            # save the summary under same name in summary path!
            summary_file = {
                "url": doc_url,
                "summary": llm_summary
            }
            summary_json = json.dumps(summary_file, indent=4)
            summary_file_path = os.path.join(summary_path, filename)

            # Save the output to a new JSON file
            with open(summary_file_path, "w") as summary_file:
                summary_file.write(summary_json)
