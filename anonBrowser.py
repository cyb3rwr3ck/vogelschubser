import sys  

try:
    import mechanize, cookielib, random
    from ConfigParser import SafeConfigParser
except:
    print '[-] Error importing modules! We need: \n - mechanize  \n - cookielib \n - random \n - time \n \
           - stem \n \- socks \n - socket \n - re \n - urllib2 \n - configparser \n - subprocess \n - shlex \n - os \n - datetime \n'
    sys.exit(1)

class anonBrowser(mechanize.Browser):

    def __init__(self, user_agents = []):
        mechanize.Browser.__init__(self)
        self.set_handle_robots(False)        
        self.user_agents = user_agents + ['Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/540.0 (KHTML,like Gecko) Chrome/9.1.0.0 Safari/540.0', \
                                          'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.38 Safari/537.36', \
                                          'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0b7) Gecko/20101111 Firefox/4.0b7', \
                                          'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:25.0) Gecko/20100101 Firefox/25.0'] 
        self.cookie_jar = cookielib.LWPCookieJar()
        self.set_cookiejar(self.cookie_jar)
        self.anonymize()
	
    def clear_cookies(self):
        self.cookie_jar = cookielib.LWPCookieJar()
        self.set_cookiejar(self.cookie_jar)
    
    def change_user_agent(self):
        index = random.randrange(0, len(self.user_agents) )
        self.addheaders = [('User-agent',( self.user_agents[index] ))]         
               
    def anonymize(self, sleep = False):
        self.clear_cookies()
        self.change_user_agent()        
    

