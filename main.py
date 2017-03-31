# e necessario far partire il programma dal terminale con i seguenti comandi:
# sudo python main.py
#cosi facendo si hanno i permessi di root

import sys
import os
#import netifaces as ni

#########################################################################################################

#variabile statica globale presente all interno del file configured.txt che
# in base al valore capisco se non e configurato, e un host o e un gateway
file = open("configured.txt", "r")
configured = file.read()

file2 = open("interface.txt", "r")
wlan = file2.read()

if wlan == "null":
    print "insert your wlan interface:"
    wlan_interface=raw_input()
    file2 = open("interface.txt", "w")
    file2.write(wlan_interface)
    sys.exit(0)


print '1) start'
print '2) reset'
start = raw_input()

if start == '0':
    print "insert name your interface:"
    wlan_interface=raw_input()
    file2 = open("interface.txt", "w")
    file2.write(str(wlan_interface))

elif not start == '1':
    print '****************** reset configuration *************************'
    file = open("configured.txt", "w")
    file.write("null")
    file2 = open("interface.txt", "w")
    file2.write("null")
    sys.exit(0)

# #il mio indirizzo IP
# #prima configurazione oppure sono sia client,server o superclient
# if str(configured) == "null" or str(configured) == "client" or str(configured) == "superclient" or str(configured) == "server":
#     ni.ifaddresses(wlan)
#     myIP = ni.ifaddresses(wlan)[2][0]['addr']
#     print '- - - - - - - - - - '+myIP+' - - - - - - - - - - - \n'
#
#     print os.system('iwconfig | grep '+wlan)
#     print '- - - - - - - - - - - - - - - - - - - - - - - - - -'
# #sono un gateway
# else:
#     ni.ifaddresses(wlan)
#     myIP = ni.ifaddresses(wlan+':1')[2][0]['addr']
#     print '- - - - - - - - - - ' + myIP + ' - - - - - - - - - - - \n'
#
#     print os.system('iwconfig | grep ' + wlan)
#     print '- - - - - - - - - - - - - - - - - - - - - - - - - - -'

########################################################################################################

#non sono configurato
if str(configured) == "null":

    print '\nconfiguration:(# '+wlan+' #)'

    print '1) router1 (192.168.1.1 - 1.1.1.1 - 3.3.3.1)'
    print '2) router2 (192.168.0.1 - 1.1.1.2 - 2.2.2.1)'
    print '3) router3 (3.3.3.2 - 2.2.2.2)'
    print '4) hostA (192.168.1.100)'
    print '5) hostB (192.168.0.100)'

    print '\n6) quagga OFF'
    print '7) quagga ON'
    print '8) network OFF'
    print '9) network ON'

    print '\nchoose configuration:'
    option = raw_input()

    # prima configurazione

    # CONFIGURAZIONE ROUTER1
    if option == '1':
        option = None
        #impostazione indirizzi IP
        os.system('sudo ifconfig -v '+wlan+' 192.168.1.1/24')
        os.system('sudo ifconfig -v '+wlan+':2 1.1.1.1/24')
        os.system('sudo ifconfig -v '+wlan+':3 3.3.3.1/24')

        # cancella le route di default
        os.system('sudo route del default')

        # aggiunge route per vedere le reti
        os.system('sudo route add -net 192.168.1.0 netmask 255.255.255.0 gw 192.168.1.1 dev '+wlan)
        os.system('sudo route add -net 1.1.1.0 netmask 255.255.255.0 gw 1.1.1.1 dev '+wlan+':2')
        os.system('sudo route add -net 3.3.3.0 netmask 255.255.255.0 gw 3.3.3.1 dev '+wlan+':3')

        # abilitare il forwarding dei pacchetti
        os.system('sudo sysctl -w net.ipv4.ip_forward=1')

        # disabilita ICMP redirect
        os.system('sudo sysctl -w net.ipv4.conf.all.accept_redirects=0')
        os.system('sudo sysctl -w net.ipv4.conf.all.send_redirects=0')

        # default
        os.system('sudo sysctl -w net.ipv4.conf.default.accept_redirects=0')
        os.system('sudo sysctl -w net.ipv4.conf.default.send_redirects=0')

        #general wlan
        os.system('sudo sysctl -w net.ipv4.conf.' + wlan + '.accept_redirects=0')
        os.system('sudo sysctl -w net.ipv4.conf.' + wlan + '.send_redirects=0')

        # dev wlan:1
        #os.system('sudo sysctl -w net.ipv4.conf.'+wlan+':1.accept_redirects=0')
        #os.system('sudo sysctl -w net.ipv4.conf.'+wlan+':1.send_redirects=0')

        # dev wlan:2
        #os.system('sudo sysctl -w net.ipv4.conf.'+wlan+':2.accept_redirects=0')
        #os.system('sudo sysctl -w net.ipv4.conf.'+wlan+':2.send_redirects=0')

        # dev wlan:3
        #os.system('sudo sysctl -w net.ipv4.conf.'+wlan+':3.accept_redirects=0')
        #os.system('sudo sysctl -w net.ipv4.conf.'+wlan+':3.send_redirects=0')

        # lo
        os.system('sudo sysctl -w net.ipv4.conf.lo.accept_redirects=0')
        os.system('sudo sysctl -w net.ipv4.conf.lo.send_redirects=0')

        # riavvio quagga
        os.system('sudo /etc/init.d/quagga restart')

        print 'router1 configured!'
        file = open("configured.txt", "w")
        file.write("router")


    # CONFIGURAZIONE ROUTER2
    elif option == '2':
        option = None
        #impostazione indirizzi IP
        os.system('sudo ifconfig -v '+wlan+' 192.168.0.1/24')
        os.system('sudo ifconfig -v '+wlan+':2 1.1.1.2/24')
        os.system('sudo ifconfig -v '+wlan+':3 2.2.2.1/24')

        # cancella le route di default
        os.system('sudo route del default')

        # aggiunge route per vedere le reti
        os.system('sudo route add -net 192.168.0.0 netmask 255.255.255.0 gw 192.168.0.1 dev '+wlan)
        os.system('sudo route add -net 1.1.1.0 netmask 255.255.255.0 gw 1.1.1.2 dev '+wlan+':2')
        os.system('sudo route add -net 2.2.2.0 netmask 255.255.255.0 gw 2.2.2.1 dev '+wlan+':3')

        # abilitare il forwarding dei pacchetti
        os.system('sudo sysctl -w net.ipv4.ip_forward=1')

        # disabilita ICMP redirect
        os.system('sudo sysctl -w net.ipv4.conf.all.accept_redirects=0')
        os.system('sudo sysctl -w net.ipv4.conf.all.send_redirects=0')

        # default
        os.system('sudo sysctl -w net.ipv4.conf.default.accept_redirects=0')
        os.system('sudo sysctl -w net.ipv4.conf.default.send_redirects=0')

        # general wlan
        os.system('sudo sysctl -w net.ipv4.conf.' + wlan + '.accept_redirects=0')
        os.system('sudo sysctl -w net.ipv4.conf.' + wlan + '.send_redirects=0')

        # dev wlan:1
        #os.system('sudo sysctl -w net.ipv4.conf.'+wlan+':1.accept_redirects=0')
        #os.system('sudo sysctl -w net.ipv4.conf.'+wlan+':1.send_redirects=0')

        # dev wlan:2
        #os.system('sudo sysctl -w net.ipv4.conf.'+wlan+':2.accept_redirects=0')
        #os.system('sudo sysctl -w net.ipv4.conf.'+wlan+':2.send_redirects=0')

        # dev wlan:3
        #os.system('sudo sysctl -w net.ipv4.conf.'+wlan+':3.accept_redirects=0')
        #os.system('sudo sysctl -w net.ipv4.conf.'+wlan+':3.send_redirects=0')

        # lo
        os.system('sudo sysctl -w net.ipv4.conf.lo.accept_redirects=0')
        os.system('sudo sysctl -w net.ipv4.conf.lo.send_redirects=0')

        # riavvio quagga
        os.system('sudo /etc/init.d/quagga restart')

        print 'router2 configured!'
        file = open("configured.txt", "w")
        file.write("router")



    # CONFIGURAZIONE ROUTER2
    elif option == '3':
        option = None
        #impostazione indirizzi IP
        os.system('sudo ifconfig -v '+wlan+' 3.3.3.2/24')
        os.system('sudo ifconfig -v '+wlan+':2 2.2.2.2/24')

        # cancella le route di default
        os.system('sudo route del default')

        # aggiunge route per vedere le reti
        os.system('sudo route add -net 3.3.3.0 netmask 255.255.255.0 gw 3.3.3.2 dev '+wlan)
        os.system('sudo route add -net 2.2.2.0 netmask 255.255.255.0 gw 2.2.2.2 dev '+wlan+':2')

        # abilitare il forwarding dei pacchetti
        os.system('sudo sysctl -w net.ipv4.ip_forward=1')

        # disabilita ICMP redirect
        os.system('sudo sysctl -w net.ipv4.conf.all.accept_redirects=0')
        os.system('sudo sysctl -w net.ipv4.conf.all.send_redirects=0')

        # default
        os.system('sudo sysctl -w net.ipv4.conf.default.accept_redirects=0')
        os.system('sudo sysctl -w net.ipv4.conf.default.send_redirects=0')

        # general wlan
        os.system('sudo sysctl -w net.ipv4.conf.' + wlan + '.accept_redirects=0')
        os.system('sudo sysctl -w net.ipv4.conf.' + wlan + '.send_redirects=0')

        # dev wlan:1
        #os.system('sudo sysctl -w net.ipv4.conf.'+wlan+':1.accept_redirects=0')
        #os.system('sudo sysctl -w net.ipv4.conf.'+wlan+':1.send_redirects=0')

        # dev wlan:2
        #os.system('sudo sysctl -w net.ipv4.conf.'+wlan+':2.accept_redirects=0')
        #os.system('sudo sysctl -w net.ipv4.conf.'+wlan+':2.send_redirects=0')

        # lo
        os.system('sudo sysctl -w net.ipv4.conf.lo.accept_redirects=0')
        os.system('sudo sysctl -w net.ipv4.conf.lo.send_redirects=0')

        # riavvio quagga
        os.system('sudo /etc/init.d/quagga restart')

        print 'router3 configured!'
        file = open("configured.txt", "w")
        file.write("router")

    # hostA
    elif option == '4':
        os.system('ifconfig ' + wlan + ' 192.168.1.100/24')
        os.system('route del default')
        os.system('route add default gw 192.168.1.1')

        # disabilitare il forwarding dei pacchetti
        os.system('sudo sysctl -w net.ipv4.ip_forward=0')

        # disabilita ICMP redirect
        os.system('sudo sysctl -w net.ipv4.conf.all.accept_redirects=0')
        os.system('sudo sysctl -w net.ipv4.conf.all.send_redirects=0')

        # default
        os.system('sudo sysctl -w net.ipv4.conf.default.accept_redirects=0')
        os.system('sudo sysctl -w net.ipv4.conf.default.send_redirects=0')

        # dev wlan
        os.system('sudo sysctl -w net.ipv4.conf.'+wlan+'.accept_redirects=0')
        os.system('sudo sysctl -w net.ipv4.conf.'+wlan+'.send_redirects=0')

        # lo
        os.system('sudo sysctl -w net.ipv4.conf.lo.accept_redirects=0')
        os.system('sudo sysctl -w net.ipv4.conf.lo.send_redirects=0')

        print 'hostA!'
        file = open("configured.txt", "w")
        file.write("host")

    # hostB
    elif option == '5':
        os.system('ifconfig ' + wlan + ' 192.168.0.100/24')
        os.system('route del default')
        os.system('route add default gw 192.168.0.1')

        # disabilitare il forwarding dei pacchetti
        os.system('sudo sysctl -w net.ipv4.ip_forward=0')

        # disabilita ICMP redirect
        os.system('sudo sysctl -w net.ipv4.conf.all.accept_redirects=0')
        os.system('sudo sysctl -w net.ipv4.conf.all.send_redirects=0')

        # default
        os.system('sudo sysctl -w net.ipv4.conf.default.accept_redirects=0')
        os.system('sudo sysctl -w net.ipv4.conf.default.send_redirects=0')

        # dev wlan
        os.system('sudo sysctl -w net.ipv4.conf.'+wlan+'.accept_redirects=0')
        os.system('sudo sysctl -w net.ipv4.conf.'+wlan+'.send_redirects=0')

        # lo
        os.system('sudo sysctl -w net.ipv4.conf.lo.accept_redirects=0')
        os.system('sudo sysctl -w net.ipv4.conf.lo.send_redirects=0')

        print 'hostB!'
        file = open("configured.txt", "w")
        file.write("host")

    elif option == '6':
        os.system("sudo /etc/init.d/quagga stop")
        print "quagga service STOP!"

    elif option == '7':
        os.system("sudo /etc/init.d/quagga restart")
        print "quagga service START!"

    elif option == '8':
        os.system('sudo ifconfig '+wlan+' off')
        print wlan+" service OFF!"

    elif option == '9':
        os.system('sudo ifconfig ' + wlan + ' on')
        print wlan+" service ON!"

    else:
        print '****************** reset configuration *************************'
        file = open("configured.txt", "w")
        file.write("null")
        file2 = open("interface.txt", "w")
        file2.write("null")
        sys.exit(0)

#########################################################################################################

# gia configurato (configured = 1)
else:

    file2 = open("interface.txt", "r")
    wlan = file2.read()

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
                file2 = open("interface.txt", "w")
                file2.write("null")
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
                file2 = open("interface.txt", "w")
                file2.write("null")
                sys.exit(0)



