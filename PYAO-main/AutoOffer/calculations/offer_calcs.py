from AutoOffer.html_manipulation.HTML import HTML, PropertyProfile
import random, math


# Initialize HTML instance to grab value
html = HTML()
pp = PropertyProfile()

# Function to calculate repair, offer, and earnest money
def offer_calc(prop_dict):

    # Remove "$" from Listing Price and turn into an integer
    listing_price = int((prop_dict[pp.list_price]).replace("$","").replace(",",""))

    # Check if SQFT exists
    if prop_dict[pp.sqft]:
        # Turn SQFT into an int
        sqft = int((prop_dict[pp.sqft]).replace("$","").replace(',',""))

        # Set repair to 30 x SQFT
        prop_dict[pp.repair] = 30 * sqft

        # Check if ARV exits
        if prop_dict[pp.arv]:
            # Remove "$" from ARV and turn into an integer
            arv = int((prop_dict[pp.arv]).replace("$","").replace(',',""))
    
            # Calulate offer as ARV x 75% - Repair - 15,000
            offer = arv * 0.75 - prop_dict[pp.repair] - 15000
        else:
            offer = listing_price * 0.70
    else:
        offer = listing_price * 0.70

    # inputing defualt offer
    prop_dict[pp.offer_price] = offer

    # Check if offer is acceptable
    # Offer is not acceptable if more than list price or
    # less the 60% of list price
    if (offer > listing_price) or (offer < listing_price * 0.60):
        # Make offer 70% of listing price
        offer = listing_price * 0.70

    # Subtract a random amount so offers don't seem robotic
    offer = offer - random.randint(500,3000)     

    # Round offer to the nearest tens place
    offer = math.floor(offer / 10) * 10

    # Set offer in prop_dict
    prop_dict[pp.offer_price] = offer

    # Calculate earnest money as 1% of offer price
    earnest_money = prop_dict[pp.offer_price] * 0.01

    # Check if earnest money is acceptable
    if earnest_money > 950:
        # Max earnest money out at 950
        prop_dict[pp.em] = 950
    
    else:
        # Set earnest money as !% of offer
        prop_dict[pp.em] = earnest_money



    
