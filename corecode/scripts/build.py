from itertools import chain
from tesis.utils import load_file, write_file

data_300 = load_file('data-300.csv')
p2 = load_file('p2.csv')
tweets_1000 = load_file('new-tweets.csv')
tweets_2000 = load_file('tweets2k.csv')
tweets_more = load_file('traffic1.csv')
tweets_more_more = load_file('traffic2.csv')

################ Generate RELEVANT data
relevant_data = []
for row in chain(data_300, p2):
    relevant_data.append(row)

write_file('../datasets/relevant.csv', relevant_data)

################ Generate TRAFFIC data
traffic_data = []
for row in chain(data_300, p2):
    if  row[1] != '0' and row[3] != '':
        traffic_data.append([row[0], row[3]])

for row in chain(tweets_1000, tweets_2000):
    if row[1] != '0':
        traffic_data.append([row[0], row[2]])

write_file('../datasets/traffic.csv', traffic_data)