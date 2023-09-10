from AutoOffer import settings

def ghl_api(location):
	if location == "HOU":
		return settings.GHL_HOU_API_KEY
	elif location == "SA":
		return settings.GHL_SA_API_KEY