#!/usr/bin/env python
#
# Project Name : Byte 1 
# Created By : Saba Kazi
#


import webapp2
import logging
import feedparser  
from webapp2_extras import jinja2
import urllib

#################################################################
#  
#  Name : BaseHandler - This class subclasses Request handler so that we can use jinja
#  Parameters : webapp2.RequestHandler
#  
#################################################################
class BaseHandler(webapp2.RequestHandler):
    
    @webapp2.cached_property
    def jinja2(self):
        # Returns a Jinja2 renderer cached in the app registry.
        return jinja2.get_jinja2(app=self.app)
        
    # This will call self.response.write using the specified template and context.
    # The first argument should be a string naming the template file to be used. 
    # The second argument should be a pointer to an array of context variables
    #  that can be used for substitutions within the template
    def render_response(self, _template, **context):
        # Renders a template and writes the result to the response.
        rv = self.jinja2.render_template(_template, **context)
        self.response.write(rv)


#################################################################
#  
#  Name : MainHandler - The main handler now subclasses BaseHandler instead of webapp2
#  Parameters : BaseHandler
#  
#################################################################
class MainHandler(BaseHandler):

   

    #################################################################
    #  
    #  Name : get - This function renders the html that need to be displayed 
    #  Parameters : self
    #  Return :  A context that contains refernces to variables and values that can be used in the html page
    #  
    #################################################################
    def get(self):
        """default landing page"""
        terms = "User Experience"
        loca = "Pittsburgh"
        context  = self.getTheContext(terms,loca)
        self.render_response('index.html', **context)

    

    #################################################################
    #  
    #  Name : post - This function is called once the user enters input and submits the form
    #  Parameters : self
    #  Return :  A context that contains refernces to variables and values that can be used in the html page
    #  
    #################################################################    
    def post(self):

        # this retrieves the contents of the search term 
        terms = self.request.get('search_term')
        loca = self.request.get('location')

        context  = self.getTheContext(terms,loca)
        self.render_response('index.html', **context)

    #################################################################
    #  
    #  Name : getTheContext - This function is called to fetch the feed from the yahoo pipe and convert the feed into a list of dictionaries
    #  Parameters : self 
    #               searchTerm - The Job Search variable
    #               locationQuery - The Location the person is looking for a job in
    #  Return :  A context that contains refernces to variables and values that can be used in the html page
    #  
    #################################################################        
    def getTheContext(self,searchTerm,locationQuery):
        orgLocation = locationQuery
        orgSearch = searchTerm
        if searchTerm.strip() == "":
            searchTerm = "jobs"
        searchTerm = urllib.quote(searchTerm)
        locationQuery = urllib.quote(locationQuery)
        if orgLocation.strip() == "":
            resultMsg = "Results for " + orgSearch + " jobs in Any Location" 
        else:
            resultMsg = "Results for " + orgSearch + " jobs in " + orgLocation 
        feed = feedparser.parse("http://pipes.yahoo.com/pipes/pipe.run?_id=8cf0f416041c38d3be8f23f4292346ea&_render=rss&JobSearchQuery=" + searchTerm + "&LocationQuery=" + locationQuery )
        
        # this sets up feed as a list of dictionaries containing information 
        feed = [{"link": item.link, "title":item.title, "description" : item.description} for item in feed["items"]]
        errorM = "no"
        if len(feed) == 0:
            resultMsg = "Sorry No Results Found" 
            errorM = "yes"
        # this sets up the context with the user's search terms and the search
        # results in feed
        context = {"feed": feed, "search": orgSearch , "location": orgLocation ,"resultMsg":resultMsg,"errorM":errorM}
        return context
 

 #################################################################
#  
#  Name : AutoRefreshHandler - This handles any AJAX calls to refresh pull new data from the pipe and refresh the screen
#  Parameters : BaseHandler
#  
#################################################################       


class AutoRefreshHandler(BaseHandler):
   
      def get(self):
         self.response.write("hello")

    #################################################################
    #  
    #  Name : post - This function is called to fetch the feed from the yahoo pipe and convert the feed into a list of dictionaries
    #  Return : strResp -> a html string that contains a list of all the results.
    #  
    ################################################################# 

      def post(self):
         
         terms = self.request.get('search_term')
         loca = self.request.get('location')
         if loca.strip() == "":
            loca = "Any Location"
         resultMsg = "Results for " + terms + " jobs in " + loca 
         
         if terms.strip() == "":
            terms = "jobs"
        
         terms = urllib.quote(terms)
         loca = urllib.quote(loca)
         feed = feedparser.parse("http://pipes.yahoo.com/pipes/pipe.run?_id=8cf0f416041c38d3be8f23f4292346ea&_render=rss&JobSearchQuery=" + terms + "&LocationQuery=" + loca )
         feed = [{"link": item.link, "title":item.title, "description" : item.description} for item in feed["items"]]
         errorM = "no"
         if len(feed) == 0:
            resultMsg = "Sorry No Results Found" 
            errorM = "yes"
        
         strResp = '<div id="delMe"><br/><br/>'
         if errorM == "no" :
            strResp = strResp + '<h2 style="color:black">' + resultMsg + '</h2><br/>'
         else:
            strResp = strResp + '<h2 style="color:black;text-align:center">' + resultMsg + '</h2><br/>'  
        
         for itemy in feed:             
           strResp = strResp +  '<div class="jobBox"><div class="jobTitle"><a href="' +  item['link'] + '">' + item['title'] +'<br/></div>'
           strResp = strResp +  '<div class="itemDesc" >' + item['description'] + '</div></div></a><br/>'
         strResp = strResp + "</div>"
         self.response.write(strResp)  
        
        

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/aplleyy', AutoRefreshHandler),
    ('/.*', MainHandler),
 ], debug=True)



