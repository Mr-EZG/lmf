from PIL import Image

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

def webp_to_jpg(img_path):
	im = Image.open(img_path).convert("RGB")
	return im

def load_jpg(img_path):
	im = Image.open(img_path)
	return im

def crop_image(img, x_s, y_s):
	left = min(x_s)
	right = max(x_s)
	top = min(y_s)
	bottom = max(y_s)
	new_img = img.crop((left, top, right, bottom))
	return new_img


def split_address(address):
	parts = address.split(",")
	street_address = format_input(parts[0].strip())
	city = format_input(parts[1].strip())
	state_and_zipcode = format_input(parts[2].strip())
	state, zipcode = state_and_zipcode.split(" ")
	state = format_state(state)
	return street_address, city, state, zipcode


def vectorize(word):
	r = dict()
	for l in word:
		if l in r:
			r[l] += 1
		else:
			r[l] = 1
	return r


def similarity_score(word1, word2):
	v1 = vectorize(word1)
	v2 = vectorize(word2)
	n = max([len(word1), len(word2)])
	similarity = 0
	for k in v1.keys():
		if k in v2:
			similarity += min([v1[k], v2[k]])
	return similarity / n

def most_similar_output(input, dict_comparision_value_to_output):
	max_similarity = -1
	similarity_value = None
	similarity_key = None
	comp_value = None
	for comp_value in dict_comparision_value_to_output.keys():
		similarity = similarity_score(input, comp_value)
		if similarity > max_similarity:
			similarity_value = dict_comparision_value_to_output[comp_value]
			max_similarity = similarity
			similarity_key = comp_value
	return similarity_value, comp_value


# if __name__ == '__main__':
	# si1 = '1611 memorial parkway'
	# si2 = 'portland'
	# sample_inputs = [si1, si2]
	# for si in sample_inputs:
	# 	print(format_input(si))
	# ss1 = 'TX'
	# ss2 = 'tx'
	# ss3 = 'texas'
	# ss4 = 'Texas'
	# sample_states = [ss1, ss2, ss3, ss4]
	# for ss in sample_states:
	# 	print(format_state(ss))

	# Test to check equivalence

	# import lmf
	# img_path = "1.webp"
	# im1 = webp_to_jpg(img_path)
	# b_im = lmf.encode_image(im1)
	# b_im2 = lmf.load_image_file_encoded("test.jpg")
	# print(b_im == b_im2)

	# Test address input

	# sample_input = "895 E Broadway, South Boston, MA 02127"
	# print(split_address(sample_input))

