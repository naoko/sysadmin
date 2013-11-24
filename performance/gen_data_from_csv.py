#!/usr/bin/python
import os
import glob
import csv

stats_scv = glob.glob("%s/stats_*.csv" % os.getcwd())

time = []
data_lists = []
file_count = 0
label = ["time"]
	
for f in stats_scv:
	label.append(f[len(os.getcwd())+1:-4].replace(".","_"))
	file_count+=1
	with open(f, 'rb') as stats:
		reader = csv.reader(stats)
		data=[]
		for row in reader:
			if file_count==1:
				# get time
				time.append(row[0])
			# get data
			data.append(row[1])
		if file_count==1:
			data_lists.append(time)
		data_lists.append(data)
	
		
with open('data.js', 'w+') as data_file:
	# build data source
	data_file.write("var dataSource = [\r")
	list_count = len(data_lists)
	
	row_count = len(data_lists[0])
	for idx in range(row_count):
		row_data = []
		for l, d_list in zip(label, data_lists):
			try:
				if l == "time":
					row_data.append("%(label)s: '%(data)s'" % {"label": l, "data": d_list[idx]})
				else:
					row_data.append("%(label)s: %(data)s" % {"label": l, "data": d_list[idx]})
			except:
				print("index error")
 				row_data = []
 		if row_data:
	 		data_file.write("\t{%s},\r" % ",".join(row_data))
	
	data_file.write("\r];\r")
	
	# build series
	data_file.write("var series = [\r")
	for l in label[1:]:
		data_file.write("{ valueField: '%(label)s', name: '%(label)s' },\r" % {"label": l})
	data_file.write("]\r")
	data_file.close()