#!/usr/bin/python
import pickle
status = [
    {
        'desc': u'wifi',
        'status': u'on',
    },
    {
        'desc': u'umts',
        'status': u'off',
    },
    {
        'desc': u'webcam',
        'status': u'off',
    },
    {
        'desc': u'ipcam',
        'status': u'off',
    },
    {
        'desc': u'robot',
        'status': u'off',
    },
    {
        'desc': u'move',
        'status': u'stop',
    },
    {
        'desc': u'armed',
        'status': u'off',

    },
    {
        'desc': u'lamp',
        'status': u'off',
    },
]

with open('robot_status.pickle', 'wb') as handle:
        pickle.dump(status, handle)

with open('robot_status.pickle', 'rb') as handle:
        curr_status = pickle.load(handle)


print curr_status

