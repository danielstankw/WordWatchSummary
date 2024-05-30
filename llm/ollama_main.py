import argparse
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatOllama
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain_core.output_parsers import StrOutputParser
import json
import re


# Create the PromptTemplate with the read content   
prompt_template = PromptTemplate.from_template("""As a professional summarizer, create a comprehensive summary of the provided text of maximum of 200 words, be it an article, post, conversation, or passage, while adhering to these guidelines:
1. Craft a summary that is detailed, thorough, in-depth, and complex, while maintaining clarity.
2. Incorporate main ideas and essential information, eliminating extraneous language and focusing on critical aspects.
3. Rely strictly on the provided text, without including external information.
4. Format the summary in paragraph form for easy understanding.
5.Conclude your notes with [End of Notes, Message #X] to indicate completion, where "X" represents the total number of messages that I have sent. In other words, include a message counter where you start with #1 and add 1 to the message counter every time I send a message.

By following this optimized prompt, you will generate an effective summary that encapsulates the essence of the given text in a clear, detailed, and reader-friendly manner. Optimize output as markdown file.

"{document}"

Additionally define the sentiment of the article and display it as:
SENTIMENT: positive/ negative/ sad/ happy etc.                                                                                                                                      
DETAILED SUMMARY""")

# file_path = "https___1943.pl_en_artykul_yediot-achronot-on-mila-18-wgm-in-the-media_.json"
# file_path = './data/https___1943.pl_en_artykul_a-matzevah-of-remembrance-unveiled-in-blonie_.json'
file_path = './data/https___www.ilvangelo-israele.it_.json'

with open(file_path, 'r') as file:
    data = json.load(file)
    document_content = data.get('content', '')
    # print(document_content)

# Initialize the LLM and LLMChain
llm = ChatOllama(model="gemma:2b", base_url="http://127.0.0.1:11434", temperature=0.7)
llm_chain = prompt_template | llm | StrOutputParser()

ans = llm_chain.invoke(document_content)
print(ans)