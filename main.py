# e necessario far partire il programma dal terminale con i seguenti comandi:
# sudo python main.py
# cosi facendo si hanno i permessi di root

import sys
import os
import netifaces as ni

#########################################################################################################

# variabile statica globale presente all interno del file configured.txt che
# in base al valore capisco se non e configurato, e un host o e un gateway
file = open("configured.txt", "r")
configured = file.read()

# print 'Name wireless interface:'
wlan = "en1"  # <- - - - - - - - - - - - - - -  [MODIFICARE INTERFACCIA WIFI]

print '1) start'
print '2) reset'
start = raw_input()
if not start == '1':
    print '****************** reset configuration *************************'
    file = open("configured.txt", "w")
    file.write("null")
    sys.exit(0)

# il mio indirizzo IP
# prima configurazione oppure sono sia client,server o superclient
if str(configured) == "null" or str(configured) == "client" or str(configured) == "superclient" or str(
        configured) == "server":
    ni.ifaddresses(wlan)
    myIP = ni.ifaddresses(wlan)[2][0]['addr']
    print '- - - - - - - - - - ' + myIP + ' - - - - - - - - - - - - -\n'

    print os.system('iwconfig | grep ' + wlan)
    print '- - - - - - - - - - - - - - - - - - - - - - - - - - - -'
# sono un gateway
else:
    ni.ifaddresses(wlan)
    myIP = ni.ifaddresses(wlan + ':1')[2][0]['addr']
    print '- - - - - - - - - - ' + myIP + ' - - - - - - - - - - - \n'

    print os.system('iwconfig | grep ' + wlan)
    print '- - - - - - - - - - - - - - - - - - - - - - - - - - - -'

#########################################################################################################

# non sono configurato
if str(configured) == "null":
    print '\nconfiguration:'

    print '0) gateway'
    print '1) super-client (network 1) 172.30.1.2'
    print '2) client (network 1) 172.30.1.3'
    print '3) client (network 1) 173.30.1.4'
    print '4) server (network 2) 172.30.2.2'

    print '\nchoose configuration:'
    option = raw_input()

    # prima configurazione

    # CONFIGURAZIONE GATEWAY
    if option == '0':
        option = None
        # impostazione indirizzi IP
        os.system('sudo ifconfig -v ' + wlan + ':1 172.30.1.1/24')
        os.system('sudo ifconfig -v ' + wlan + ':2 172.30.2.1/24')

        # cancella le route di default
        os.system('sudo route del default')

        # aggiunge route per vedere le reti
        os.system('sudo route add -net 172.30.1.0 netmask 255.255.255.0 gw 172.30.1.1 dev ' + wlan + ':1')
        os.system('sudo route add -net 172.30.2.0 netmask 255.255.255.0 gw 172.30.2.1 dev ' + wlan + ':2')

        # abilitare il forwarding dei pacchetti
        os.system('sudo sysctl -w net.ipv4.ip_forward=1')

        # disabilita ICMP redirect
        os.system('sudo sysctl -w net.ipv4.conf.all.accept_redirects=0')
        os.system('sudo sysctl -w net.ipv4.conf.all.send_redirects=0')

        # default
        os.system('sudo sysctl -w net.ipv4.conf.default.accept_redirects=0')
        os.system('sudo sysctl -w net.ipv4.conf.default.send_redirects=0')

        # dev wlan
        os.system('sudo sysctl -w net.ipv4.conf.' + wlan + '.accept_redirects=0')
        os.system('sudo sysctl -w net.ipv4.conf.' + wlan + '.send_redirects=0')

        # lo
        os.system('sudo sysctl -w net.ipv4.conf.lo.accept_redirects=0')
        os.system('sudo sysctl -w net.ipv4.conf.lo.send_redirects=0')

        print 'gateway configured!'
        file = open("configured.txt", "w")
        file.write("gateway")

    # CONFIGURAZIONE SUPER-CLIENT
    elif option == '1':
        os.system('ifconfig ' + wlan + ' 172.30.1.2/24')
        os.system('route del default')
        os.system('route add default gw 172.30.1.1')

        print 'super-client configured!'
        file = open("configured.txt", "w")
        file.write("superclient")

    # CONFIGURAZIONE ALTRI CLIENT
    elif option == '2':
        os.system('ifconfig ' + wlan + ' 172.30.1.3/24')
        os.system('route del default')
        os.system('route add default gw 172.30.1.1')

        print 'normal client configured!'
        file = open("configured.txt", "w")
        file.write("client")

    elif option == '3':
        os.system('ifconfig ' + wlan + ' 172.30.1.4/24')
        os.system('route del default')
        os.system('route add default gw 172.30.1.1')

        print 'normal client configured!'
        file = open("configured.txt", "w")
        file.write("client")

    # CONFIGURAZIONE SERVER
    elif option == '4':
        os.system('ifconfig ' + wlan + ' 172.30.2.2/24')
        os.system('route del default')
        os.system('route add default gw 172.30.2.1')

        print 'server configured!'
        file = open("configured.txt", "w")
        file.write("server")
    else:
        print '****************** reset configuration *************************'
        file = open("configured.txt", "w")
        file.write("null")
        sys.exit(0)

#########################################################################################################

# gia configurato (configured = 1)
else:
    int_option = None

    print '* you are a ' + str(configured) + ' *\n'

    while int_option is None:

        # sono un client / superclient / server
        # hanno le medesime funzioni
        if str(configured) == "client":
            print "boh"

            try:
                option1 = raw_input()
            except SyntaxError:
                option = None

            if option1 == '1':
                print ""
            else:
                print '****************** reset configuration *************************'
                file = open("configured.txt", "w")
                file.write("null")
                sys.exit(0)

            int_option = None

        ###########################################################################################################

        # sono un gateway
        else:
            print "1) boh"

            try:
                option2 = raw_input()
            except SyntaxError:
                option = None

            # assegnare un mark per una specifica classe data nel punto 1
            if option2 == '1':
                print ""

            else:
                print '****************** reset configuration *************************'
                file = open("configured.txt", "w")
                file.write("null")
                sys.exit(0)



