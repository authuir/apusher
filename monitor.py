import socks
import datetime
import time
import requests
import sys
import os
import json
from threading import Thread
from shadowsocks import shell, daemon, eventloop, tcprelay, udprelay, asyncdns

class SSThread(Thread):
    def __init__(self, ssconfig, thread_num=0, timeout=1.0):
        super(SSThread, self).__init__()
        self.ssconfig = ssconfig
        self.loop     = eventloop.EventLoop()
        self.dns_resolver = asyncdns.DNSResolver()
        self.tcp_server = tcprelay.TCPRelay(self.ssconfig, self.dns_resolver, True)
        self.udp_server = udprelay.UDPRelay(self.ssconfig, self.dns_resolver, True)

    def run(self):
        #print(self.ssconfig)
        self.dns_resolver.add_to_loop(self.loop)
        self.tcp_server.add_to_loop(self.loop)
        self.udp_server.add_to_loop(self.loop)
        self.loop.run()
        #print("End")

    def stop(self):
        self.tcp_server.close(next_tick=True)
        self.udp_server.close(next_tick=True)
        self.loop.stop()

def ping(config):
    cfg_ss = {'server': config['server'], 'server_port': config['server_port'], 'password': config['password'], 'local_port': int(config['report_port']), 'method': config['method'], 'verbose': 1, 'port_password': None, 'timeout': 300, 'fast_open': False, 'workers': 1, 'pid-file': '/var/run/shadowsocks.pid', 'log-file': '/var/log/shadowsocks.log', 'local_address': '127.0.0.1', 'one_time_auth': False, 'prefer_ipv6': False, 'dns_server': None, 'libopenssl': None, 'libmbedtls': None, 'libsodium': None, 'tunnel_remote': '8.8.8.8', 'tunnel_remote_port': 53, 'tunnel_port': 53, 'crypto_path': {'openssl': None, 'mbedtls': None, 'sodium': None}}
    thread = SSThread(cfg_ss)
    thread.start()
    trcp = -1
    stand_data = b"HTTP/1.1 301 "
    while True:
        try:
            s = socks.socksocket()
            s.set_proxy(socks.SOCKS5, "127.0.0.1", int(config['report_port']))
            timenow = int(round(time.time() * 1000))
            s.connect(("google.com", 80))
            s.settimeout(5)
            s.sendall(b"GET google.com HTTP/1.1\r\nAccept: */*\r\nHost: google.com\r\nConnection: Keep-Alive\r\n\r\n")
            recv_data = s.recv(4096)
            if recv_data[0:11] != stand_data[0:11]:
                trcp = -1
                print("{} in {} Delay to Google: {}ms".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), config['tag'], 'Timeout '))
            else:
                timeafter = int(round(time.time() * 1000))
                trcp = timeafter - timenow
                print("{} in {} Delay to Google: {}ms".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), config['tag'], trcp))
        except:
            trcp = -1
            print ("Socks Error")


        posturl = "http://tmon.tms.im/post"  
        data = {'token':'Authuir', 'peerid':config['report_port'], 'responsetime':str(trcp), 'time':str(int(round(time.time() * 1000))), 'tag':config['tag']}  
        try:
            r = requests.post(posturl, data=data, timeout=5)
            print(r.text)
        except requests.exceptions.HTTPError as errh:
            print ("Http Error:",errh)
        except requests.exceptions.ConnectionError as errc:
            print ("Error Connecting:",errc)
        except requests.exceptions.Timeout as errt:
            print ("Timeout Error:",errt)
        except requests.exceptions.RequestException as err:
            print ("OOps: Something Else",err)

        time.sleep(4)

    thread.stop()
    thread.join()

def main():
    with open("./config.json",'r') as config_f:
        config = json.load(config_f)
        for s in config:
            t = Thread(target=ping, args=({'tag':s['tag'],'report_port':s['report_port'], 'server': s['server'], 'server_port': s['server_port'], 'password': s['password'].encode('ascii'), 'method': s['method']},))
            t.start()


if __name__ == '__main__':
    main()
