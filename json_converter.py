import json
import time
from random import randint

fjson = open('data.json', 'r')
raw_json = json.loads(fjson.readline())
fjson.close()

entries = []
for h in raw_json['WebHistoryDates']:
    try:
        entry = {}
        entry['title'] = h['title']

        if all(ord(c) < 128 for c in h['title']):
            entry['country'] = 1
        else:
            entry['country'] = 0

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
        time_dict['wday'] = struct_time.tm_wday
        time_dict['tday'] = (struct_time.tm_yday - 212) + \
            (time_dict['year'] - 2013) * 365
        time_dict['hour'] = struct_time.tm_hour
        time_dict['min'] = struct_time.tm_min
        time_dict['sec'] = struct_time.tm_sec
        
        entry['time'] = time_dict
        entry['category'] = randint(0, 4)

        entries.append(entry)
    except:
        continue

# entries.reverse()

ebuff = []
day_ls = []
curr_tday = entries[0]['time']['tday']
place_holder = {'time':{'tday': -1000}}
for e in entries + [place_holder]:
    if e['time']['tday'] == curr_tday:
        ebuff.append(e)
    else:
        chn_count = 0
        eng_count = 0
        chn_categ_stats = {}
        chn_categ_count = 0
        eng_categ_stats = {}
        eng_categ_count = 0
        for ej in ebuff:
            if ej['country'] == 0:
                chn_count += 1
                cat = ej['category']
                if cat in chn_categ_stats:
                    chn_categ_stats[cat] += 1
                else:
                    chn_categ_stats[cat] = 1
                chn_categ_count += 1
            else:
                eng_count += 1
                cat = ej['category']
                if cat in eng_categ_stats:
                    eng_categ_stats[cat] += 1
                else:
                    eng_categ_stats[cat] = 1
                eng_categ_count += 1
        day_entry = {}
        day_entry['year'] = ebuff[0]['time']['year']
        day_entry['month'] = ebuff[0]['time']['month']
        day_entry['date'] = ebuff[0]['time']['day']
        day_entry['day'] = ebuff[0]['time']['wday'] + 1
        day_entry['totalDay'] = ebuff[0]['time']['tday']
        
        chn_ls = []
        eng_ls = []
        for i in range(5):
            if i in chn_categ_stats:
                chn_ls.append(chn_categ_stats[i] / float(chn_categ_count))
            else:
                chn_ls.append(0.0)

            if i in eng_categ_stats:
                eng_ls.append(eng_categ_stats[i] / float(eng_categ_count))
            else:
                eng_ls.append(0.0)

        day_entry['chinese'] = {'amount': chn_count,
                                'categories': chn_ls}
        day_entry['english'] = {'amount': eng_count,
                                'categories': eng_ls}
        curr_tday = e['time']['tday']
        day_ls.append(day_entry)
        ebuff = [e]
        
clean_data = 'var data = ' + json.dumps(day_ls)
fout = open('clean_data.json', 'w')
fout.write(clean_data)
fout.close()
