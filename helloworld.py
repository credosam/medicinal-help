import webapp2
import sys
import urllib2
import os
import jinja2
import re
import logging
import json
import urlparse

#importing beautifulsoup
sys.path.insert(0, 'libs')
from bs4 import BeautifulSoup

#setting up jinja2 to pick files from templates dir
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)


#Shorthand functions to make life easier
class BaseHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class MainHandler(BaseHandler):
    def get(self):
        self.render("index.html")


class Scrape(BaseHandler):
    def get(self):
        # logging.info(self.request.get('url'))
        url = 'http://search.medicinenet.com/search/search_results/default.aspx?query=' + self.request.get('url')
        content = urllib2.urlopen(url).read()
        # stidx = content.find('<ul class="searchResults_fmt"')
        # enidx = content.find('</ul>', stidx+1)
        soup = BeautifulSoup(content)
        self.response.headers.add_header("Access-Control-Allow-Origin", "*")
        self.response.headers['Content-Type'] = 'application/json'
        items = []        
        results = soup.find_all('ul', 'searchResults_fmt')[0]
        for link in results.find_all('li'):
            item = {}
            if link.a.has_attr("href"):
                item["url"] = link.a["href"]
                item["nam"] = link.a.text
                item["desc"] = link.div.text.encode('ascii', 'replace')
                items.append(item)   
                
        items = json.dumps(items)
        # urls = json.dumps([{'url': content[stidx:enidx+5]}])
        obj = {
               "items" : items
               }
        # logging.info(obj)
        # logging.info("{ \"items\" : " +  items + " }")
        
        # self.response.out.write("{\"items\": " + items + "}")
        self.response.headers['Content-Type'] = 'application/javascript'
        self.response.out.write("%s(%s)" %
                                (urllib2.unquote(self.request.get('callback')),
                                "{ \"items\" : " +  items + " }"))


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/scrape/.*', Scrape)
], debug=True)
