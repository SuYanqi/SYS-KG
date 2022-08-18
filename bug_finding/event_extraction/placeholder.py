class Placeholder:
    URL = "PLH_URL_"
    CONCEPT = "CONCEPT_"

    # the Tag is from html
    CATEGORY_TAG_DICT = {'RadioButton': ["radio"], "Checkbox": ["checkbox"], "Button": ["button"],
                         'Dropdown': ["menuitem", "option"],
                         'Panel': ["richlistitem", "appmenuitem"],
                         'TextField': ["textbox", "input"],
                         'Hyperlink': ["a", "link"],
                         'Text': ["title", "description", "subtitle", "header", "treecol", "message", "text",
                                  "heading",
                                  # "instruction", "intro",
                                  "label"],
                         "Page": [],
                         "Key": [],
                         "App": [],
                         "Others": [],
                         }

    # APP_ALIAS = ['Firefox', 'browser', 'Nightly', 'Firefox browser', 'the Latest Nightly browser', 'Latest Nightly']

    ACTION_DICT = {'click': {'alias': ['click on'], },
                   'right click': {'alias': [], },
                   'check': {'alias': [], },
                   'uncheck': {'alias': [], },
                   # 'toggle': {'alias': [], },
                   'tick': {'alias': [], },
                   'untick': {'alias': [], },
                   'enable': {'alias': [], },
                   'disable': {'alias': [], },
                   'go to': {'alias': ['navigate to', 'access', 'visit']},
                   'open': {'alias': ['start', 'launch']},
                   'close': {'alias': []},
                   'quit': {'alias': []},
                   'restart': {'alias': []},
                   'refresh': {'alias': []},
                   'select': {'alias': ['choose']},
                   'hold': {'alias': []},
                   'release': {'alias': []},
                   'drag': {'alias': []},
                   'hover': {'alias': ['hover the cursor above', 'hover over']},
                   'press': {'alias': []},
                   # 'scroll': {'alias': ['scroll to']},
                   'scroll up': {'alias': ['scroll up to', 'scroll up until']},
                   'scroll down': {'alias': ['scroll down to', 'scroll down until']},
                   'observe': {'alias': ['inspect', 'see']},
                   'freeze': {'alias': []},
                   'return to': {'alias': ['go back to', 'switch back to', 'focus back to']},
                   'switch': {'alias': ['switch to']},
                   'type': {'alias': ['enter', 'fill']},
                   'change': {'alias': []},
                   'resize': {'alias': []},
                   }

    CATEGORY_ACTION_RELATION_DICT = {
        'RadioButton': {'check': {'equivalent': ['click', 'tick', 'enable'],
                                  'opposite': ['uncheck', 'untick', 'disable']},
                        'uncheck': {'equivalent': ['untick', 'disable'],
                                    'opposite': ['check', 'click', 'tick', 'enable']},
                        },
        "Checkbox": {'check': {'equivalent': ['click', 'tick', 'enable'],
                               'opposite': ['uncheck', 'untick', 'disable']},
                     'uncheck': {'equivalent': ['untick', 'disable'],
                                 'opposite': ['check', 'click', 'tick', 'enable']},
                     },
        "Button": {'click': {'equivalent': [],
                             'opposite': []},
                   'hold': {'equivalent': [],
                            'opposite': ['release']},
                   'release': {'equivalent': [],
                               'opposite': ['hold']},
                   'hover': {'equivalent': [],
                             'opposite': []},
                   'scroll up': {'equivalent': [],
                                 'opposite': ['scroll down']},
                   'scroll down': {'equivalent': [],
                                   'opposite': ['scroll up']},
                   'observe': {'equivalent': ['check'],
                               'opposite': []},
                   },
        'Dropdown': {'click': {'equivalent': [],
                               'opposite': []},
                     'select': {'equivalent': [],
                                'opposite': []},
                     # 'hold': {'equivalent': [],
                     #          'opposite': ['release']},
                     # 'release': {'equivalent': [],
                     #             'opposite': ['hold']},
                     'hover': {'equivalent': [],
                               'opposite': []},
                     # 'scroll up': {'equivalent': [],
                     #               'opposite': ['scroll down']},
                     # 'scroll down': {'equivalent': [],
                     #                 'opposite': ['scroll up']},
                     'observe': {'equivalent': ['check'],
                                 'opposite': []},
                     },
        'Panel': {'click': {'equivalent': [],
                            'opposite': []},
                  'select': {'equivalent': [],
                             'opposite': []},
                  'observe': {'equivalent': ['check'],
                              'opposite': []},
                  },
        'TextField': {'click': {'equivalent': [],
                                'opposite': []},
                      'right click': {'equivalent': [],
                                      'opposite': []},
                      'type': {'equivalent': [],
                               'opposite': []},
                      },
        'Hyperlink': {'click': {'equivalent': [],
                                'opposite': []},
                      'right click': {'equivalent': [],
                                      'opposite': []},
                      'hover': {'equivalent': [],
                                'opposite': []},
                      'observe': {'equivalent': ['check'],
                                  'opposite': []},
                      },
        'Text': {'observe': {'equivalent': ['check'],
                             'opposite': []},
                 'scroll up': {'equivalent': [],
                               'opposite': ['scroll down']},
                 'scroll down': {'equivalent': [],
                                 'opposite': ['scroll up']},
                 'go to': {'equivalent': ['switch'],
                           'opposite': []},
                 },
        "Page": {'go to': {'equivalent': ['open'],
                           'opposite': ['close']},
                 'close': {'equivalent': [],
                           'opposite': ['open', 'go to']},
                 'observe': {'equivalent': ['check'],
                             'opposite': []},
                 'refresh': {'equivalent': [],
                             'opposite': []},
                 'return to': {'equivalent': [],
                               'opposite': []},
                 'switch': {'equivalent': [],
                            'opposite': []},
                 'resize': {'equivalent': [],
                            'opposite': []},
                 },
        "Key": {'press': {'equivalent': ['type'],
                          'opposite': []},
                },
        "App": {
            # 'click': {'equivalent': ['open'],
            #           'opposite': ['close']},
            'open': {'equivalent': ['click'],  # click?
                     'opposite': ['close', 'quit']},
            'close': {'equivalent': ['quit'],
                      'opposite': ['open', 'click']},
            'restart': {'equivalent': [],
                        'opposite': ['close', 'quit']},
            'freeze': {'equivalent': [],
                       'opposite': []},
        },
        "Others": {},
    }

    # "label", "placeholder", "aria-label", "tooltiptext", "labelnotsyncing", "labelsyncing"
    ATTRIBUTE_IDS = ["label", "placeholder", "tooltiptext"]

    """
    external knowledge:
        Category-> Key: Keyboard shortcuts: https://support.mozilla.org/en-US/kb/keyboard-shortcuts-perform-firefox-tasks-quickly    
         
    """
    EXTERNAL_KNOWLEDGE_DICT = {
        # keyboard shortcuts
        'Key': {
            # Current Page
            "Tab": {'alias': [],
                    'related_concepts': ["Shift+Tab", ], },  # Focus Next Link or Input Field
            "Shift+Tab": {'alias': [],
                          'related_concepts': ["Tab", ], },  # Focus Previous Link or Input Field
            "Command+P": {'alias': ["Command-P", ],
                          'related_concepts': [], },  # Print
            "Command+S": {'alias': [],
                          'related_concepts': [], },  # Save Page As
        },

        # maybe don't need this category
        'App': {
            "Firefox": {'alias': ['Firefox', 'browser', 'Nightly', 'Firefox browser', 'the Latest Nightly browser',
                                  'Latest Nightly'],
                        'related_concepts': [], },
        }

    }
