#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

# ==================== General settings for GUIs/functions within ./utils ====================
ROOTDIR = os.path.dirname(os.path.realpath(__file__))
FILEDIR = os.path.join(ROOTDIR, 'data')
GITHUB_URL = 'https://github.com/dpedrosac/dbsPatients'

# ==================== Parkinson disease specific medication ====================

MEDICATION = ['Levodopa Carbidopa{}',
              'Levodopa Carbidopa CR{}',
              'Entacapone{}',
              'Tolcapone{}',
              'Opicapone{}',
              'Apomorphine{}',
              'Piribedil{}',
              'Pramipexole{}',
              'Ropinirole{}',
              'Rotigotin{}',
              'Rasagilin{}',
              'Safinamid{}',
              'Selegilin oral{}',
              'Selegilin sublingual{}',
              'Amantadine{}',
              'Other{}'
              ]

# ==================== Information on DBS systems ====================

SYSTEMS = [
    'Medtronic PLC. - Activa PC',
    'Medtronic PLC. - Activa RC',
    'Medtronic PLC. - Activa SC',
    'Medtronic PLC. - Percept',
    'Boston Scientific Corp. - Genus P16',
    'Boston Scientific Corp. - Genus P32',
    'Boston Scientific Corp. - Genus R16',
    'Boston Scientific Corp. - Genus R32',
    'Abbott - Infinity'
]

LEADS = {
    'BSc-2201': {
        'Manufacturer': 'Boston Scientific Corp.',
        'Contacts_per_side': 8.0,
        'Contacts_name': [['1', '2', '3', '4', '5', '6', '7', '8'], ['1', '2', '3', '4', '5', '6', '7', '8']]
    },
    'BSc-2202': {
        'Manufacturer': 'Boston Scientific Corp.',
        'Contacts_per_side': 8.0,
        'Contacts_name': [['1', '2', '3', '4', '5', '6', '7', '8'], ['1', '2', '3', '4', '5', '6', '7', '8']]
    },
    'BSc-2203': {
        'Manufacturer': 'Boston Scientific Corp.',
        'Contacts_per_side': 16.0,
        'Contacts_name': [['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16'],
                         ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16']]
    },
    'BSc-2204': {
        'Manufacturer': 'Boston Scientific Corp.',
        'Contacts_per_side': 16.0,
        'Contacts_name': [
            ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16'],
            ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16']
        ]
    },
    'MDT-3387': {
        'Manufacturer': 'Medtronic PLC.',
        'Contacts_per_side': 4.0,
        'Contacts_name': [['0', '1', '2', '3'], ['8', '9', '10', '11']]
    },
    'MDT-3389': {
        'Manufacturer': 'Medtronic PLC.',
        'Contacts_per_side': 4.0,
        'Contacts_name': [['0', '1', '2', '3'], ['8', '9', '10', '11']]
    },
    'MDT-33005': {
        'Manufacturer': 'Medtronic PLC.',
        'Contacts_per_side': 8.0,
        'Contacts_name': [['0', '1a', '1b', '1c', '2a', '2b', '2c', '3'],
                         ['8', '9a', '9b', '9c', '10a', '10b', '10c', '11']]
    },
    'MDT-33015': {
        'Manufacturer': 'Medtronic PLC.',
        'Contacts_per_side': 8.0,
        'Contacts_name': [['0', '1a', '1b', '1c', '2a', '2b', '2c', '3'],
                         ['8', '9a', '9b', '9c', '10a', '10b', '10c', '11']]
    },
    'St-6172': {
        'Manufacturer': 'Abbott',
        'Contacts_per_side': 8.0,
        'Contacts_name': [['1', '2a', '2b', '2c', '3a', '3b', '3c', '4'],
                         ['1', '2a', '2b', '2c', '3a', '3b', '3c', '4']]
    },
}
