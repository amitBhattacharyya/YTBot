import os
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter  # New import
from search_youtube import search_youtube
from transcript_call_orchastrate import get_cached_transcript
from langchain_openai import ChatOpenAI
from openai import OpenAI


api_key = os.environ.get("OPENAI_API_KEY")
yt_pi_key = os.environ.get("YOUTUBE_API_KEY")
text_folder = os.environ.get("STORAGE_LOCATION")  
raw_documents = []
retriever = None

def parse_yt_reponse_and_download_ts(search_query):
    response = search_youtube(search_query, yt_pi_key)
    for item in response.get("items", []):
        video_id = item["id"]["videoId"]
        title = item["snippet"]["title"]
        channel = item["snippet"]["channelTitle"]
        get_cached_transcript(video_id)
        file_path = os.path.join(text_folder, text_folder + video_id + ".txt")
        loader = TextLoader(file_path)
        raw_documents.extend(loader.load())

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=100
    )
    all_documents = text_splitter.split_documents(raw_documents)
    embeddings = OpenAIEmbeddings(openai_api_key=api_key)
    vector_store = FAISS.from_documents(all_documents, embeddings)     
    return vector_store.as_retriever()




def main():
    print("Welcome to the RAG Assistant. Type 'exit' to quit.\n")

    llm = ChatOpenAI(openai_api_key=api_key, model="gpt-4.1-mini", temperature=0.3)
    
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "exit":
            print("Exiting…")
            break

        # get relevant documents
        relevant_docs = retriever.get_relevant_documents(user_input)
        retrieved_context = "\n\n".join([doc.page_content for doc in relevant_docs])

        # system prompt
        system_prompt = (
            "You are a helpful assistant. "
            "Use ONLY the following knowledge base context to answer the user. "
            "If the answer is not in the context, say you don't know.\n\n"
            f"Context:\n{retrieved_context}"
        )

        # messages for LLM 
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]

        # generate response
        response = llm.invoke(messages)
        assistant_message = response.content.strip()
        print(f"\nAssistant: {assistant_message}\n")

if __name__ == "__main__":
    search_query = "acer nitro v 16s review"
    retriever = parse_yt_reponse_and_download_ts(search_query)      
    main() 
