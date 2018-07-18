from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import io

#save the abstracts
driver = webdriver.Chrome("C:/Users/Supreme Ruler/Desktop/chromedriver.exe")

def goto_page(url):
	"""Navigates to given url, url must be string""" 
	driver.get(url)

def enter_query(query):
	"""Enters the wanted query into the pubmed search bar and presses RETURN"""
	text_bar = driver.find_element_by_id("term")
	text_bar.send_keys(query)
	text_bar.send_keys(Keys.RETURN)

def get_href():
	"""Ïterates through all results, adding href and title to list. Returns that list."""
	href_list = []
	total_pages = driver.find_element_by_name("EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.Pubmed_Pager.cPage")
	page_end = total_pages.get_attribute("last")

	for i in range(int(page_end)):
	#for i in range(1):
		print("Collecting data: page {} of {}".format(i+1,page_end))
		for title in driver.find_elements_by_class_name("title"):
			href = title.find_element_by_css_selector('a').get_attribute('href')
			href_list.append(href)
		driver.find_element_by_class_name("next").click()
	return(href_list)

def extract_data():
	"""Gets title, authors and abstract from individual result pages"""
	title = driver.find_element_by_xpath("//div[@class='rprt abstract']/h1").text
	authors = driver.find_element_by_class_name("auths").text
	citation = driver.find_element_by_class_name("cit").text
	abstract_block = driver.find_element_by_class_name("abstract")
	paragraphs = abstract_block.find_elements_by_css_selector("p")
	abstract = ""
	for paragraph in paragraphs:
		abstract += paragraph.text
	#print(title, authors,abstract)
	return [title,authors,citation,abstract]

def write_data_to_file(query,data_list,filename):
	"""writes list within list data into final output csv file.
	Reduces 2D list to csv"""
	query = query
	filename = filename
	data_list = data_list
	with io.open(filename, 'w',encoding = "utf-8") as file:
		file.write("Results for search query:\n")
		file.write(query)
		file.write("\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
		for i in range(len(data_list)):
			for data in data_list[i]:
				file.write(data)
				file.write("\n")
			file.write("------------------------------------------------------------\n")


#______________MAIN______________ 
if __name__ == "__main__":
	#always first go to pubmed page
	print("Connecting to Pubmed")
	goto_page("https://www.ncbi.nlm.nih.gov/pubmed/")
	print("Starting Query")

	#insert search quary below
	query = '"colonic neoplasms"[MeSH Terms] AND ("ethanol"[MeSH Terms] OR "alcohols"[MeSH Terms]) AND Clinical Trial[ptyp])'
	enter_query(query)

	
	#retrieve href and title from all results
	href_list = get_href()

	#extract title, author and abstract for each result.
	full_data_list = []
	print("Extracting abstracts!, this might take a while.")
	for url in href_list:
		goto_page(url)
		full_data_list.append(extract_data())
	driver.close()

	filename = "Colon Cancer and Ethanol Clinical Trials" + ".txt"
	print("Writing To file: {}".format(filename))
	write_data_to_file(query,full_data_list,filename)

	print("process complete, press any key to close window")
	input()






