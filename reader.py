# reader.py
# functions for a reader

import re

# get data from a file and format into a list (same as generator version of this fcn but more general)
# input such as Game Data - All Games
# or Game Log - All Players
def extract_data(data_type, input_type, extension='csv'):
	catalog_filename = "data/" + data_type.title() + " - " + input_type.title() + "." + extension

	lines = []
	data = []
	all_data = []

	with open(catalog_filename, encoding="UTF8") as catalog_file:

		current_line = ""
		for catalog_info in catalog_file:
			current_line = catalog_info.strip()
			lines.append(current_line)

		catalog_file.close()

	# skip header line
	for line in lines[1:]:
		if len(line) > 0:
			if extension == "csv":
				data = line.split(",")
			else:
				data = line.split("\t")
		all_data.append(data)
	
	print("all_data: " + str(all_data))


	return all_data