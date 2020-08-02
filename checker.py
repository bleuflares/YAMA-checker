# -*- coding: utf-8 -*- 
#YAMA FORMAT CHECKER by bleuflares

import sys
import os
import argparse
import csv
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
			print(line)
			print(title_format)
			if line != title_format:
				print('title format is wrong! automatically converted... please check')
			line = title_format
		elif count == 1:
			question = line.split()
			question[0] = title_format.split()[1] + '.'
			if line != ' '.join(question):
				print('question number format is wrong! automatically converted... please check')
			line - ' '.join(question)
		result += line + "\n"
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


def check_first_page(first_page, title_format):
	contents = first_page.getContents()
	data = contents.getData()
	decoded_data = data.decode('utf-8')
	replaced_data = replace_firstpage(decoded_data, title_format)
	encoded_data = replaced_data.encode('utf-8')
	if contents.decodedSelf is not None:
		contents.decodedSelf.setData(encoded_data)
	else:
		contents.setData(encoded_data)

if __name__ == "__main__":
	ap = argparse.ArgumentParser()
	ap.add_argument("-i", "--input", required=True, help="path to PDF document")
	ap.add_argument("-u", "--uid", required=True, help="path to PDF document")
	args = vars(ap.parse_args())

	in_file = args["input"].decode('utf-8')
	uid = args["uid"].decode('utf-8')
	print(in_file)

	f = open(in_file, 'r')
	reader = csv.reader(f)
	prob_nums = []
	filenames = []
	name = ''
	subject = ''
	line_count = 0
	line_metas = []
	line_contents = []
	for line in reader:
		if line_count == 0:
			subject = line[0].split()[0]
			line_count += 1
			print(subject)
			continue

		if line_count == 1:
			line_metas = line
			for i in range(len(line_metas)):
				if line_metas[i] == '':
					line_metas[i] = line_metas[i - 1]
			line_count += 1
			continue

		uid_temp = line[0]
		if uid_temp == uid:
			line_contents = line
			name = line_contents[1]
			for i in range(2, len(line_contents)):
				if line_contents[i] != '':
					prob_nums.append((line_metas[i].decode('utf-8') + ' ' + line_contents[i].decode('utf-8')).encode('utf-8'))
	for prob in prob_nums:
		metas = prob.split(' ')
		if len(metas[0].split('-')) > 1:
			filename_base = [metas[0].split('-')[1], metas[0].split('-')[0], metas[1], str(uid), name]
			filenames.append(subject[3:len(subject)] + ' ' + '_'.join(filename_base) + '.pdf')
		else:
			filename_base = [metas[0], metas[1], str(uid), name]
			filenames.append(subject[3:len(subject)] + ' ' + '_'.join(filename_base) + '.pdf')

	temp_count = 0
	
	for filename in filenames:
		print(filename)
		if os.path.isfile(filename):
			pdf = PdfFileReader(filename)
			writer = PdfFileWriter()

			first_page = pdf.getPage(0)
			last_page = pdf.getPage(pdf.getNumPages() - 1)
			check_first_page(first_page, prob_nums[temp_count])
			writer.addPage(first_page)
			for page_number in range(1, pdf.getNumPages()):
				writer.addPage(page_number)
			with open(filename_base + "result.pdf", 'wb') as out_file:
				writer.write(out_file)
			temp_count += 1
		else:
			print(filename + 'is missing... please check')
			temp_count += 1
	

	"""
	filename_base = in_file.replace(os.path.splitext(in_file)[1], "")
	filename_base = check_filename(filename_base, title)
	print(filename_base)
	metas = filename_base.split('_')
	if len(metas[0].split()) > 1:
		title_format = metas[1] + '-' + metas[0].split()[1] + ' ' + metas[2]
	else:
		title_format = metas[1] + '-' + metas[0] + ' ' + metas[2]
	"""
	# Provide replacements list that you need here

	#check_last_page(last_page)
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

	"""
	writer.addPage(first_page)
	print(pdf.getNumPages())
	if pdf.getNumPages() > 1:
		print("here")
		writer.addPage(last_page)
"""