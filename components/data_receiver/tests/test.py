# -*- coding: utf-8 -*-

import codecs
import json

jobj = {'параметр1':'значение1', 'параметр2':'значение2', 'ברי צקלה':'ברי צקלה'}
with codecs.open(r'C:\git\github\cstat\tmp\reports_dumps\test_dump.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(jobj, ensure_ascii=False))

with codecs.open(r'C:\git\github\cstat\tmp\reports_dumps\test_dump.json', 'r', encoding='utf-8') as f:
    jobj2 = json.load(f )

print(jobj)
print(jobj2)