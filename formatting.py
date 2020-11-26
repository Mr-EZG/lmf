us_state_abbrev = {
'Alabama': 'AL',
'Alaska': 'AK',
'American Samoa': 'AS',
'Arizona': 'AZ',
'Arkansas': 'AR',
'California': 'CA',
'Colorado': 'CO',
'Connecticut': 'CT',
'Delaware': 'DE',
'District of Columbia': 'DC',
'Florida': 'FL',
'Georgia': 'GA',
'Guam': 'GU',
'Hawaii': 'HI',
'Idaho': 'ID',
'Illinois': 'IL',
'Indiana': 'IN',
'Iowa': 'IA',
'Kansas': 'KS',
'Kentucky': 'KY',
'Louisiana': 'LA',
'Maine': 'ME',
'Maryland': 'MD',
'Massachusetts': 'MA',
'Michigan': 'MI',
'Minnesota': 'MN',
'Mississippi': 'MS',
'Missouri': 'MO',
'Montana': 'MT',
'Nebraska': 'NE',
'Nevada': 'NV',
'New Hampshire': 'NH',
'New Jersey': 'NJ',
'New Mexico': 'NM',
'New York': 'NY',
'North Carolina': 'NC',
'North Dakota': 'ND',
'Northern Mariana Islands':'MP',
'Ohio': 'OH',
'Oklahoma': 'OK',
'Oregon': 'OR',
'Pennsylvania': 'PA',
'Puerto Rico': 'PR',
'Rhode Island': 'RI',
'South Carolina': 'SC',
'South Dakota': 'SD',
'Tennessee': 'TN',
'Texas': 'TX',
'Utah': 'UT',
'Vermont': 'VT',
'Virgin Islands': 'VI',
'Virginia': 'VA',
'Washington': 'WA',
'West Virginia': 'WV',
'Wisconsin': 'WI',
'Wyoming': 'WY'
}

def format_state(input_state):
	input_state = input_state.strip()
	if input_state.upper() in us_state_abbrev.values():
		return input_state.upper()
	input_state = input_state.lower()
	for state in us_state_abbrev.keys():
		l_state = state.lower()
		if input_state in l_state:
			return us_state_abbrev[state]
	return None

def format_input(input):
	address = input.split(" ")
	new_address = []
	for part in address:
		if part:
			first_part = part[0]
			other_parts = part[1:]
			first_part = first_part.upper()
			other_parts = other_parts.lower()
			new_part = first_part + other_parts
			new_address.append(new_part)
	return " ".join(new_address)

if __name__ == '__main__':
	si1 = '1611 memorial parkway'
	si2 = 'portland'
	sample_inputs = [si1, si2]
	for si in sample_inputs:
		print(format_input(si))
	ss1 = 'TX'
	ss2 = 'tx'
	ss3 = 'texas'
	ss4 = 'Texas'
	sample_states = [ss1, ss2, ss3, ss4]
	for ss in sample_states:
		print(format_state(ss))