#YAMA FORMAT CHECKER by bleuflares
import sys
import os
import argparse
from PyPDF2 import PdfFileReader, PdfFileWriter


def replace_text(content, replacements = dict()):
	lines = content.splitlines()

	result = ""
	in_text = False

	for line in lines:
		if line == "BT":
			in_text = True

		elif line == "ET":
			in_text = False

		elif in_text:
			cmd = line[-2:]
			if cmd.lower() == 'tj':
				replaced_line = line
				for k, v in replacements.items():
					replaced_line = replaced_line.replace(k, v)
				result += replaced_line + "\n"
			else:
				result += line + "\n"
			continue

		result += line + "\n"

	return result

def replace_firstpage(content, title_format):
	lines = content.splitlines()

	result = ""
	count = 0

	for line in lines:
		if count == 0:
			line - title_format
		elif count == 1:
			question = line.split()
			question[0] = title_format.split()[1] + '.'
			line - ' '.join(question)
		result += line + "\n"
	print(result)
	return result

def process_data(object, replacements):
	data = object.getData()
	decoded_data = data.decode('utf-8')

	replaced_data = replace_text(decoded_data, replacements)

	encoded_data = replaced_data.encode('utf-8')
	if object.decodedSelf is not None:
		object.decodedSelf.setData(encoded_data)
	else:
		object.setData(encoded_data)

def check(instring, outstring):
	if instring != outstring:
		return outstring
	else:
		return instring


def check_filename(filename, title):
	metas = filename.split('_')
	metas[0] = check(metas[0], title)
	return '_'.join(metas)

def check_first_page(first_page, title_format):
	data = object.getData()
	decoded_data = data.decode('utf-8')

	contents = first_page.getContents()
	replace_firstpage(contents, title_format)
	encoded_data = replaced_data.encode('utf-8')
	if object.decodedSelf is not None:
		object.decodedSelf.setData(encoded_data)
	else:
		object.setData(encoded_data)
"""
def check_last_page(last_page, last_page_format):
"""

if __name__ == "__main__":
	ap = argparse.ArgumentParser()
	ap.add_argument("-i", "--input", required=True, help="path to PDF document")
	ap.add_argument("-t", "--title", required=True, help="path to PDF document")
	args = vars(ap.parse_args())

	in_file = args["input"].decode('utf-8')
	print(in_file)
	title = args["title"].decode('utf-8')
	
	filename_base = in_file.replace(os.path.splitext(in_file)[1], "")
	
	filename_base = check_filename(filename_base, title)
	metas = filename_base.split('_')
	if len(metas[0].split()) > 1:
		title_format = metas[1] + '-' + metas[0].split()[1] + ' ' + metas[2]
	else:
		title_format = metas[1] + '-' + metas[0] + ' ' + metas[2]

	# Provide replacements list that you need here
	replacements = { 'PDF': 'DOC'}

	pdf = PdfFileReader(in_file)
	writer = PdfFileWriter()

	first_page = pdf.getPage(0)
	last_page = pdf.getPage(pdf.getNumPages() - 1)

	check_first_page(first_page, title_format)
	check_last_page(last_page)
	"""
	for page_number in range(0, pdf.getNumPages()):

		page = pdf.getPage(page_number)
		contents = page.getContents()

		if len(contents) > 0:
			for obj in contents:
				streamObj = obj.getObject()
				process_data(streamObj, replacements)
		else:
			process_data(contents, replacements)

		writer.addPage(page)
	"""
	writer.addPage(first_page)
	writer.addPage(last_page)
	with open(filename_base + ".result.pdf", 'wb') as out_file:
		writer.write(out_file)