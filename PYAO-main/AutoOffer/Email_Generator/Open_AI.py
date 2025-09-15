import os
import random
import time
import schedule
import locale

from openai import OpenAI
from AutoOffer import settings
from AutoOffer.html_manipulation import HTML
from AutoOffer.db import db_funct

pp = HTML.PropertyProfile()

# Set API key
client = OpenAI(api_key=getattr(settings, "OPENAI_API_KEY", os.getenv("OPENAI_API_KEY")))

# --- Pricing constants for gpt-5-nano (adjust if OpenAI updates them) ---
COST_PER_MILLION_INPUT = 0.15   # USD
COST_PER_MILLION_OUTPUT = 0.60  # USD


def calculate_cost(usage):
    """Estimate cost in USD based on OpenAI token usage for gpt-5-nano."""
    if not usage:
        return 0.0
    input_cost = (usage.prompt_tokens / 1_000_000) * COST_PER_MILLION_INPUT
    output_cost = (usage.completion_tokens / 1_000_000) * COST_PER_MILLION_OUTPUT
    return round(input_cost + output_cost, 6)  # 6 decimal places for precision


def create_query(prop):
    offer = locale.format_string("%d", prop[pp.offer_price], grouping=True)
    address = prop[pp.steet_address]  # check typo in your schema
    agent_firstname = prop[pp.agent_first_name]
    public_remarks = prop[pp.public_remarks]

    investor_name = "Charles Watkins"

    if prop[pp.location] == "HOU":
        investor_number = "832-263-6157"
        investor_location = "Houston"
    elif prop[pp.location] == "SA":
        investor_number = "210-405-5118"
        investor_location = "San Antonio"
    else:
        investor_number = "000-000-0000"
        investor_location = "Texas"

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

    rand_intro = random.choice(intros)

    prompt = f"""
As {investor_name} from {investor_location}, draft a professional yet relaxed email to realtor {agent_firstname}
with an offer of ${offer} for the property at {address}. Start with "{rand_intro} This is...".

Use the following realtor remarks (paraphrase, don’t quote directly):
{public_remarks}

Requirements:
- Mention at least one positive about the property.
- If negatives exist, use them tactfully as part of your negotiation.
- Justify the offer in terms of equity and investment potential.
- Emphasize cash funding, quick close, and low closing costs.
- Conclude with eagerness to work together and include my contact number: {investor_number}.
- Avoid using the word "fair".
- Target ~300–400 words.
"""
    return prompt


def generate_email_body(prop):
    query = create_query(prop)

    response = client.chat.completions.create(
        model="gpt-5-nano",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that drafts investment offer emails."},
            {"role": "user", "content": query}
        ],
    )

    email_text = response.choices[0].message.content.strip()
    usage = response.usage
    cost = calculate_cost(usage)

    # Save to DB (email body + cost)
    db_funct.multi_db_update(
        mls_id=prop[pp.mls_id],
        data_dict={
            pp.email_body: email_text,
            pp.ai_cost: cost
        },
        overwrite=True
    )

    print(f"Email generated for MLS {prop[pp.mls_id]} | Tokens used: {usage.total_tokens} | Cost: ${cost}")
    print(email_text)


def main():
    db_funct.create_db()

    props = db_funct.get_sorted_rows_with_null_and_not_null(
        sort_column=pp.last_updated,
        null_list=[pp.offer_sent, pp.email_body],
        not_null_list=[pp.pdf_offer_path],
    )

    if props:
        for prop in props:
            generate_email_body(prop)
    else:
        print("No properties to create emails for. Will wait for next run")

    print("Email body made, waiting for next scheduled run")


if __name__ == "__main__":
    main()
    schedule.every(1).minutes.do(main)
    while True:
        schedule.run_pending()
        time.sleep(1)
