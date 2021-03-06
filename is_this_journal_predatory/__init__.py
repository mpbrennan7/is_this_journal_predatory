import json
import os
import sys

def get_domain(url):
     website=""
     url=url.replace("http://","")
     url=url.replace("https://","")
     j=0
     
     while(j<len(url) and url[j]!='/'):
         website=website+url[j]
         j=j+1
     return website

class PredatoryInfo():
     predatory_path = os.path.join(os.path.dirname(__file__), "predatory_journals.json")
     def __init__(self):
         self._load(self.predatory_path)
     def _load(self, path):
         with open(path) as handle:
             self._data = json.load(handle)[0]
     def search(self, name):
         def matches_domain(query_domain, db_domains):
             return get_domain(query_domain) in list(get_domain(db_domain) for db_domain in db_domains)
         def matches_name(query_name, db_names):
             return query_name in db_names
         for listing_id in self._data:
             listing = self._data[listing_id]
             if matches_domain(name, listing["url"]):
                 return listing
             if matches_name(name, listing["name"]):
                 return listing
         return {}
     def warn_predatory(self, result):
         return "The journal {0} at {1} is listed as a predatory journal in Beall's List.".format(result["name"][0], result["url"][0])
     def probably_not_predatory(self, name):
         return "{0} is not listed as a predatory journal. To judge for yourself, read more at https://thinkchecksubmit.org/".format(name)
     def is_predatory(self, name):
         result = self.search(name)
         if result:
             return self.warn_predatory(result)
         else:
             return self.probably_not_predatory(name)
