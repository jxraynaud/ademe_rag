import os
import yaml
from dotenv import load_dotenv
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.agents.agent_toolkits import VectorStoreToolkit, VectorStoreInfo
from langchain.agents import initialize_agent, AgentType, load_tools
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage


SYSTEM_PROMPT = """
Tu es un expert dans le calcul du bilan carbone de produits.
Tu utilises pour cela la base de données de l'ADEME.
Tu sais que cette base est relativement complète mais qu'elle ne contient pas tous les produits, par conséquent tu sais qu'il faut parfois chercher un produit plus générique.
"""

def read_yaml_settings(filename):
    with open(filename, 'r') as f:
        settings = yaml.safe_load(f)
    return settings


if __name__ == '__main__':
    # load environment variables and the vector store.
    load_dotenv()
    settings = read_yaml_settings('settings.yaml')
    faiss_db = os.path.join(settings['faiss_db_path'], 'faiss_db')
    faiss_store = FAISS.load_local(faiss_db, OpenAIEmbeddings())

    # Question:
    product = 'jambon blanc sans nitrite de marque Herta'
    quantity = 300
    unit = 'g'
    question = 'Quel serait le coût carbone de {quantity} {unit} de {product} en magasin?'.format(product=product, quantity=quantity, unit=unit)

    # System messages
    agent_kwargs = {
        "system_message": SystemMessage(content=SYSTEM_PROMPT)
    }

    # initialize the agent toolkit
    vectorstore_info = VectorStoreInfo(
        vectorstore=faiss_store,
        name="BaseCarbone",
        description="Contient les données de la base Carbone de l'ADEME. Permet de trouver un produit. Les metadata contienne un champs unit qui indique l'unité de mesure utilisée et un champs co2_equiv avec la valeur de l'équivalent CO2 dans l'unité indiquée.",
    )
    toolkit = VectorStoreToolkit(vectorstore_info=vectorstore_info)
    print(question)


    # DA VINCI 003
    print("\033[92m" + "-" * 40)
    print("\033[92m" + "Da Vinci 003" + "\033[0m")
    
    da_vinci003 = OpenAI(temperature=0)
    math_tools_da_vinci003 = load_tools(['llm-math'], llm=da_vinci003)
    agent_da_vinci003 = initialize_agent(
        tools=toolkit.get_tools() + math_tools_da_vinci003,
        llm=da_vinci003,
        verbose=True,
    )
    agent_da_vinci003.run(question)
    # agent_executor = create_vectorstore_agent(llm=da_vinci003, toolkit=toolkit, verbose=True)
    # agent_executor.run(question)

    # initialize the chat model based agent toolkit
    print("\033[92m" + "-" * 40)
    print("\033[92m" + "GPT 3.5 Turbo" + "\033[0m")
    
    gpt35 = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")
    math_tools_gpt35 = load_tools(['llm-math'], llm=gpt35)
    agent_gpt35 = initialize_agent(
        tools=toolkit.get_tools() + math_tools_gpt35,
        llm=gpt35,
        agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        agent_kwargs=agent_kwargs,
    )
    agent_gpt35.run(question)

    # initialize the chat model based agent toolkit
    print("\033[92m" + "-" * 40)
    print("\033[92m" + "GPT 4" + "\033[0m")
    gpt4 = ChatOpenAI(temperature=0, model="gpt-4-0613")
    math_tools_gpt4 = load_tools(['llm-math'], llm=gpt4)
    agent_gpt4 = initialize_agent(
        tools=toolkit.get_tools() + math_tools_gpt4,
        llm=gpt4,
        agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        agent_kwargs=agent_kwargs,
    )
    agent_gpt4.run(question)
