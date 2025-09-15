import random
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain import OpenAI, PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA, LLMChain
from langchain.document_loaders import Docx2txtLoader
from langchain.agents import initialize_agent
from AutoOffer import settings
from langchain.callbacks import get_openai_callback
from AutoOffer.html_manipulation import HTML
from AutoOffer.db import db_funct
import time, schedule, locale


pp = HTML.PropertyProfile()


def create_query(prop): 
    # Define values from property
    offer = locale.format_string("%d", prop[pp.offer_price], grouping=True)
    address = prop[pp.steet_address]
    agent_firstname = prop[pp.agent_first_name]
    public_remarks = prop[pp.public_remarks]

    # Define defualt values
    investor_name = 'Charles Watkins'

    # Select Houston number if location is HOU
    if prop[pp.location] == "HOU":
        investor_number = '832-263-6157'
        investor_location = 'Houston'

    # Select San Antonio number if location is SA
    if prop[pp.location] == "SA":
        investor_number = "210-405-5118"
        investor_location = 'San Antonio'

    # List out the possible intros
    intros = [
    f"Hey {agent_firstname},",
    f"Hey there, {agent_firstname},",
    f"Warm greetings, {agent_firstname},",
    f"Trust you're doing well, {agent_firstname},",
    f"Congratulations on the listing {agent_firstname},",
    f"Delighted to connect with you again, {agent_firstname},",
    f"Hello {agent_firstname},",
    f"Hi there, {agent_firstname},",
    f"Thrilled to be reaching out to you, {agent_firstname},",
    f"Hope you're having a great day, {agent_firstname},",
    f"Sending my best regards, {agent_firstname},",
    f"Hello again, {agent_firstname},",
    f"Hi, {agent_firstname},",
    f"Hope all is well, {agent_firstname},",
    f"Hey {agent_firstname}, hope you're doing great!",
    ]

    # Pick a random intro
    rand_intro = random.choice(intros)
            
    prompts = [
    f"""
        As a local investor from {investor_location}, named {investor_name}, you are engaged in acquiring properties for investment. Your current task is to draft a personable email to a real estate agent, {agent_firstname}, with an offer of ${offer} for their MLS listing at {address}. Begin the email with a unique introduction such as "{rand_intro} This is...", and ensure the email is direct and engaging.

        When referring to {agent_firstname}'s realtor's remarks ({public_remarks}), creatively interpret and paraphrase the positive attributes of the property. It's crucial to avoid direct quotes; instead, express these attributes in your own words, showing how the property meets your investment criteria. Justify your offer by emphasizing the investment potential and equity considerations, drawing on the essence of the realtor's remarks without direct repetition. If the remarks include any negatives about the property, tactfully use these as part of your negotiation strategy. Stress your financial readiness by mentioning your capacity for a cash payment, a quick closing process, and minimal closing costs. Conclude with a statement showing your keenness to work with the agent and provide your contact number ({investor_number}). Remember not to use the word "fair" and aim for a well-composed email of about 300-400 words. The tone should be professional, yet approachable, focusing on originality and clear communication of your intentions.
    """,

    f"""
        You are a local {investor_location} investor named {investor_name}, buying properties for investment purposes. 
        Your goal is to write an personable email to real estate agent, {agent_firstname}, to present an offer of ${offer} on the thier MLS listing located at {address}.
        Start the email with "{rand_intro} This is..." then continue with intent of email
        Do not start off mulitple sentences with the same word.


        REALTOR'S REMARKS FROM {agent_firstname}:
        {public_remarks}

        INCLUDE THE FOLLOWING PIECES IN YOUR RESPONSE:
            Using the realtor's remarks craft a sentence detailing positives about the home and why it's a good fit for you. Do not reference the realtor's remarks word for word in the email.
            Jutsify your offfer baecause it gives you the neceassary amount of equity.
            If there are anything negative about the property mentioned in the realtor remarks, use that a justification as well.
            Craft 1 sentence emphasizing cash funding for the deal, a quick close, and little to no closing costs.
            End the email by displaying an eagerness to work together and provide your contact number: {investor_number}.
            DO NOT USE THE WORD "FAIR"
            Keep the email between 300 to 400 words
    """,

    f"""
        As a local {investor_location} investor named {investor_name}, your task is to write a professional and relaxed message to real estate agent {agent_firstname}, offering ${offer} for their MLS listing at {address}. 
        Start the email with "{rand_intro} This is...".
        There should only be one positive sentence about the house based on the realtors remarks: {public_remarks}
        If there are any negative aspects mentioned in the realtor's remarks, use them subtly to support your offer. 
        Highlight your ability to provide cash funding, a quick close, and minimal closing costs, though you would need decent equity in the property.
        Conclude with an expression of eagerness to collaborate and your contact number ({investor_number}). 
        Avoid using the word "fair" and aim for an email length of 200-250 words.
    """,

    f"""
        As {investor_name} from {investor_location}, draft a straightforward yet relaxed msg to realtor {agent_firstname} with a ${offer} offer for the property at {address}. Start with '{rand_intro} This is...'.

        Focus on the investment merits of the property, like size, location, and ROI potential, using factual language.
        
        Briefly acknowledge any positive points from the realtor's notes, linking them to investment value.

        Refer to "potential repairs" seen in the listing pictures to subtly bolster your offer, don't mention specific repairs.

        Emphasize your readiness for a cash transaction, swift closure, and low closing costs, stressing the need for equity.

        Conclude with a note on cooperation and provide your contact ({investor_number}). Aim for 200-250 words, avoiding 'fair'

        Only respond with the raw msg.
    """
    ]

    query = prompts[3]

    return query

def generate_email_body(prop):

    query = create_query(prop)

    # Set API key for OpenAI Service
    openai_api_key = settings.OPENAI_API_KEY

    llm = OpenAI(openai_api_key=openai_api_key,
                temperature=0.7,
                model_name='gpt-5-nano')

    # est_tokens = llm.get_num_tokens(query)   
    # print(est_tokens)                   

    # Query the OpenAI database and get the details on the cost
    with get_openai_callback() as cb:
        query_result = llm(query)

        if query_result:

            # Write the created email to the db
            db_funct.multi_db_update(
                mls_id=prop[pp.mls_id],
                data_dict={pp.email_body: query_result,
                           # Store the cost of generating the email
                           pp.ai_cost: cb.total_cost,},
                overwrite=True
            )
        print(cb)

    print(query_result)

def main ():
    # Create a db if there isn't one
    db_funct.create_db()

    # Find all the properties that need an email body made by checking if the Offer_Path is not NULL and the Email_Made is NULL
    props = db_funct.get_sorted_rows_with_null_and_not_null(
                sort_column=pp.last_updated,
                null_list=[
                    pp.offer_sent,
                    pp.email_body
                ],
                not_null_list=[
                    pp.pdf_offer_path,
                ],
            )
    
    # Generate and email body for every selected property
    if props:
        for prop in props:
            generate_email_body(prop)
    else:
        print(f"No properties to create emails for. Will wait for next run")

    print(f'Email body made, waiting for next scheduled run')

if __name__ == '__main__':
    main()

    # This will run the code as soon as it's starting rather than waiting
    schedule.every(1).minutes.do(main)

    while True:
        schedule.run_pending()
        time.sleep(1)