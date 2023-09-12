from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain import OpenAI
from langchain.chains import RetrievalQA
from langchain.document_loaders import Docx2txtLoader
from AutoOffer import settings

# Set API key for OpenAI Service
openai_api_key = settings.OPENAI_API_KEY

# Get your loader ready
loader = Docx2txtLoader(settings.offer_training_path)
# Load up your text into documents
documents = loader.load()
# Get your text splitter ready
text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=0)

print(text_splitter)
# Split your documents into texts
texts = text_splitter.split_documents(documents)
# Turn your texts into embeddings
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
# Get your docsearch ready
docsearch = FAISS.from_documents(texts, embeddings)
# Init
# Load up your LLM
llm = OpenAI(openai_api_key=openai_api_key,
             temperature=0.7)
# Create your Retriever
qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=docsearch.as_retriever())
# Run a query
# query = "What did McCarthy discover?"
# qa.run(query)

qa = RetrievalQA.from_chain_type(llm=llm,
                                chain_type="stuff",
                                retriever=docsearch.as_retriever(),
                                return_source_documents=True)
query = "Create a 100 word offer to a property at 123 Smith street where were are offering 70,000 but it is listed for 100,000"
result = qa({"query": query})
print(result['result'])
print(result['source_documents'])
