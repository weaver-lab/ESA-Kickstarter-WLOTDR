"""mesh node configuations"""
""" Weaver Labs 2019 """

config =    {'id'      : '3',
            'network':{'ip'      : "172.16.3.199",
                       'netmask' : "255.255.255.0",
                       'gateway' : "172.16.0.1",
                       'dns'     : "172.16.0.1",
                       'ssid'    : "BG-WIFI",
                       'password': "a1fdc1db99",
                },

             'key_list': ["recipient_id",
                          "sender"      ,
                          "seq_id"      ,
                          "num_of_msgs" ,
                          "payload"
                ],

             'url'     : 'http://18.184.150.89/api/handover',
             'byte_length': 130
             }
