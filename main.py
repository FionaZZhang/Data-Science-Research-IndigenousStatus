import subprocess

# some installations needed
'''
subprocess.call(['pip', 'install', 'openpyxl'])
subprocess.call(['pip', 'install', 'statsmodels'])
subprocess.call(['pip', 'install', 'patsy'])
'''
# create index linkage from raw data
exec(open("index_linkage.py").read())

# link several abs data (socio-eco index) entries with a single phidu (inequality/equality index) data entry
exec(open("abs_data_integrate.py").read())

# impute missing value to socio-eco data
exec(open("missing_value.py").read())

# cleanse data from phidu file
exec(open("indigenous_cleanse.py").read())

# calculate inequality index
exec(open("inequality_index.py").read())

# merge the data into a single csv file
exec(open("inequality_socioeco.py").read())

# create a scatter plot
exec(open("scatter_plot.py").read())

# create a stacked area plot
exec(open("stacked_area_plot.py").read())

# calculate pearson correlation, create a heatmap showing correlation value
exec(open("pearson_correlation.py").read())

# calculate spearman correlation, create a heapmap showing correlation value
exec(open("spearman_correlation.py").read())
