#!/usr/bin/python

import sys

try:
    from anonBrowser import *
    from random import randint
    from time import sleep
    from stem import Signal
    from stem.control import Controller
    import stem.connection
    from stem import CircStatus
    from ConfigParser import SafeConfigParser
    from datetime import datetime
    import socks,socket,re,urllib2,subprocess,shlex,os

except:
    print '[-] Error importing modules! We need: \n - mechanize  \n - cookielib \n - random \n - time \n \
           - stem \n \- socks \n - socket \n - re \n - urllib2 \n - configparser \n - subprocess \n - shlex \n - os \n - datetime \n'
    sys.exit(1)



def config_parser(configfile):
    global sAuth_token, sTorPwd, sHandle, sKey_0, sKey_1, sKey_2, sKey_3, sCommand_0, sCommand_1, \
           sCommand_2,sCommand_3, lCommand_0, lCommand_1, lCommand_2,lCommand_3

    parser = SafeConfigParser()
    parser.read(configfile)

    sAuth_token =   parser.get('settings', 'Twitter-Auth_token')
    sTorPwd     =   parser.get('settings', 'Tor-Control-Password')
    sHandle     =   parser.get('settings', 'Twitter-Handle')
    sKey_0      =   parser.get('settings', 'Search-Key_0')
    sKey_1      =   parser.get('settings', 'Search-Key_1')
    sKey_2      =   parser.get('settings', 'Search-Key_2')
    sKey_3      =   parser.get('settings', 'Search-Key_3')
    sCommand_0  =   parser.get('commands', 'Command_0')
    sCommand_1  =   parser.get('commands', 'Command_1')
    sCommand_2  =   parser.get('commands', 'Command_2')
    sCommand_3  =   parser.get('commands', 'Command_3')
    
    #getting lists of the OS commands -> later usage in subprocess calls
    lCommand_0 = shlex.split(sCommand_0)
    lCommand_1 = shlex.split(sCommand_1)
    lCommand_2 = shlex.split(sCommand_2)
    lCommand_3 = shlex.split(sCommand_3)


def create_connection(address, timeout=None, source_address=None):
    sock = socks.socksocket()
    sock.connect(address)
    return sock


def requester(sUrl):

    global bCommand_0, bCommand_1, bCommand_2, bCommand_3
    bCommand_0 = False
    bCommand_1 = False
    bCommand_2 = False
    bCommand_3 = False

    global ab
    ab = anonBrowser()

    global twids
    twids = []


    for attempt in range(1, 5):
        ab.anonymize()
        print '[+] Fetching page...'
        try:
            page = ab.open(sUrl)
        except:
            print '[-] Error during initial HTTP connection - EXITING'
            sys.exit(1)
            
        html = page.read()

        
        key_finder_0 = ''
        key_finder_1 = ''
        key_finder_2 = ''
        key_finder_3 = ''

        
        #search for keys by regex, one key_finder per command
       # try:

        print '[+] Searching for key...'
        if sKey_0 != '':
            key_finder_0 = re.search(sKey_0, html.lower())
        if sKey_1 != '':
            key_finder_1 = re.search(sKey_1, html.lower())
        if sKey_2 != '':
            key_finder_2 = re.search(sKey_2, html.lower())
        if sKey_3 != '':
            key_finder_3 = re.search(sKey_3, html.lower())
                 

        #if key1 is found search for the first occurane of "/<handle>/status/" and return the message identifier by regex (at least 18 numbers) -> this is the most recent tweet of the user
        if key_finder_0:

            twpath_finder   =   re.compile('/'+ sHandle + '/status/\d{18,}')
            twpath          =   twpath_finder.findall(html)
            twid_finder     =   re.compile('\d{18,}')
            twid_0          =   twid_finder.findall(twpath[0])
            twids.append(twid_0[0])
            print '[+] Found Command #0 in tweet-id ' + twid_0[0]

            bCommand_0 = True

            if key_finder_1:
                pass
            else:
                break

        if key_finder_1:

            twpath_finder   =   re.compile('/'+ sHandle + '/status/\d{18,}')
            twpath          =   twpath_finder.findall(html)
            twid_finder     =   re.compile('\d{18,}')
            twid_1          =   twid_finder.findall(twpath[0])
            twids.append(twid_1[0])
            print '[+] Found Command #1 in tweet-id ' + twid_1[0]

            bCommand_1 = True

            if key_finder_2:
                pass
            else:
                break


        if key_finder_2:

            twpath_finder   =   re.compile('/'+ sHandle + '/status/\d{18,}')
            twpath          =   twpath_finder.findall(html)
            twid_finder     =   re.compile('\d{18,}')
            twid_2          =   twid_finder.findall(twpath[0])
            twids.append(twid_2[0])
            print '[+] Found Command #2 in tweet-id ' + twid_2[0]

            bCommand_2 = True

            if key_finder_3:
                pass
            else:
                break


        if key_finder_3:

            twpath_finder   =   re.compile('/'+ sHandle + '/status/\d{18,}')
            twpath          =   twpath_finder.findall(html)
            twid_finder     =   re.compile('\d{18,}')
            twid_3          =   twid_finder.findall(twpath[0])
            twids.append(twid_3[0])
            print '[+] Found Command #3 in tweet-id ' + twid_3[0]

            bCommand_3 = True

            break

        sleep(randint(5,20))


def delete_tweet(sUrl):

    # prepare list and remove dups -> possible due to multiple commands in a tweet
    twids_unique = list(set(twids))

    for twid in twids_unique:
            sData = '_method=DELETE&id=' + str(twid)
            header = {'Host': 'twitter.com', \
                    'Accept': 'application/json,\ text/javascript, */*; q=0.01', \
                    'Accept-Language': 'en-us', \
                    'Accept-Encoding': 'gzip, deflate, br', \
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8}', \
                    'Referer': 'https://twitter.com/' + sHandle, \
                    'X-Requested-With': 'XMLHttpRequest', \
                    'DNT': '1', \
                    'Cookie': 'auth_token=' + sAuth_token, \
                    'Connection': 'close'}
            ab.anonymize()
            # package the request
            request = urllib2.Request(sUrl,sData,header)
            print '[+] Deleting Twitter Command...'
            response = ab.open(request)

            response.close()



def new_circuit():

    try:
        control_socket = stem.socket.ControlPort(port = 9051)
    except stem.SocketError as exc:
        print '[-] Unable to connect to port 9051 (%s)' % exc
        sys.exit(1)

    with Controller.from_port(port = 9051) as controller:
        try:
            controller.authenticate(sTorPwd)
            controller.signal(Signal.NEWNYM)
            sleep(2)
            print '[+] Sucessfully switched TOR circuit'
        except:
                print('[-] Something went wrong during circuit switching!')

    with Controller.from_port(port = 9051) as controller:
        controller.authenticate(sTorPwd)
        for circ in controller.get_circuits():
            if circ.status != CircStatus.BUILT:
                continue
            exit_fp, exit_nickname = circ.path[-1]
            exit_desc = controller.get_network_status(exit_fp, None)
            exit_address = exit_desc.address if exit_desc else 'unknown'

    print '[+] New exit relay address: %s' % exit_address



def activate_command():
    devnull = open(os.devnull, 'w')
    time = str(datetime.now())

    if bCommand_0:
        try:
            subprocess.Popen(lCommand_0, stdout=devnull, stderr=subprocess.STDOUT)
            print '[+] Executed command #0 @ ' + time
        except:
            print '[-] Something went wrong during OS command execution'
            sys.exit(1)
    if bCommand_1:
        try:
            subprocess.Popen(lCommand_1, stdout=devnull, stderr=subprocess.STDOUT)
            print '[+] Executed command #1@ ' + time
        except:
            print '[-] Something went wrong during OS command execution'
            sys.exit(1)
    if bCommand_2:
        try:
            subprocess.Popen(lCommand_2, stdout=devnull, stderr=subprocess.STDOUT)
            print '[+] Executed command #2 @ ' + time
        except:
            print '[-] Something went wrong during OS command execution'
            sys.exit(1)
    if bCommand_3:
        try:
            subprocess.Popen(lCommand_3, stdout=devnull, stderr=subprocess.STDOUT)
            print '[+] Executed command #3 @ ' + time
        except:
            print '[-] Something went wrong during OS command execution'
            sys.exit(1)
    print '[+] Done, see ya...'



def prepare_socks():
    # set the default proxy to tor socks
    # patch the socket module -> needed because no native socks support in mechanize
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050)
    socket.socket = socks.socksocket
    socket.create_connection = create_connection


def main():
    config_parser('settings.cfg')
    new_circuit()
    prepare_socks()
    requester('https://twitter.com/'+ sHandle)
    delete_tweet('https://twitter.com/i/tweet/destroy')
    activate_command()




if __name__ == '__main__':
    main()
