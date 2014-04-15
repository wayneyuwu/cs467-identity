import json
import time

fjson = open('data.json', 'r')
raw_json = json.loads(fjson.readline())
fjson.close()

formatted_data = []
for h in raw_json['WebHistoryDates']:
    try:
        entry = {}
        entry['title'] = h['title']

        url = h['']        
        entry['url'] = url

        url_ls = url.split('/')
        entry['domainName'] = '//'.join([url_ls[0], url_ls[2]])

        timestamp = int(float(h['lastVisitedDate'])) + 978307200
        struct_time = time.localtime(timestamp)
        
        time_dict = {}
        
        time_dict['year'] = struct_time.tm_year
        time_dict['month'] = struct_time.tm_mon
        time_dict['day'] = struct_time.tm_mday
        time_dict['hour'] = struct_time.tm_hour
        time_dict['min'] = struct_time.tm_min
        time_dict['sec'] = struct_time.tm_sec
        
        entry['time'] = time_dict
        entry['category'] = 0
        formatted_data.append(entry)
    except:
        continue

clean_data = 'var data = ' + json.dumps(formatted_data)
fout = open('clean_data.json', 'w')
fout.write(clean_data)
fout.close()
