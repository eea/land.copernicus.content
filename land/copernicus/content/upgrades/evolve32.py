from plone import api
import logging
# import transaction


logger = logging.getLogger('land.copernicus.content')

COUNTRIES_DATA = {
    'Albania': {
        u'type': u'FeatureCollection',
        u'features': [{
            u'geometry': {
                u'type': u'Polygon',
                u'coordinates': [
                    [39.6447296, 19.121700000000033],
                    [39.6447296, 21.05723940000007],
                    [42.6610819, 21.05723940000007],
                    [42.6610819, 19.121700000000033]
                ]},
            u'type': u'Feature',
            u'bbox': [
                39.6447296, 19.121700000000033,
                42.6610819, 21.05723940000007
            ],
            u'properties': {
                u'description': u'Albania',
                u'tags': [u'country', u'political'],
                u'center': [41.153332, 20.168330999999966],
                u'other': {
                    u'geometry': {
                        u'location_type': u'APPROXIMATE',
                        u'bounds': {
                            u'west': 19.121700000000033,
                            u'east': 21.05723940000007,
                            u'north': 42.6610819,
                            u'south': 39.6447296
                        },
                        u'viewport': {
                            u'west': 19.121700000000033,
                            u'east': 21.05723940000007,
                            u'north': 42.6610819,
                            u'south': 39.6447296
                        },
                        u'location': {
                            u'lat': 41.153332,
                            u'lng': 20.168330999999966
                        }
                    },
                    u'address_components': [{
                        u'long_name': u'Albania',
                        u'types': [u'country', u'political'],
                        u'short_name': u'AL'}],
                    u'place_id': u'ChIJLUwnvfM7RRMR7juY1onlfAc',
                    u'formatted_address': u'Albania',
                    u'types': [u'country', u'political']
                },
                u'title': u'Albania', u'name': u''}
            }
        ]
    },

    'Austria': {
        u'type': u'FeatureCollection',
        u'features': [{
            u'geometry': {
                u'type': u'Polygon',
                u'coordinates': [
                    [46.37233579999999, 9.530783400000018],
                    [46.37233579999999, 17.16068610000002],
                    [49.0206081, 17.16068610000002],
                    [49.0206081, 9.530783400000018]
                ]
            },
            u'type': u'Feature',
            u'bbox': [
                46.37233579999999, 9.530783400000018,
                49.0206081, 17.16068610000002],
            u'properties': {
                u'description': u'Austria',
                u'tags': [u'country', u'political'],
                u'center': [47.516231, 14.550072],
                u'other': {
                    u'geometry': {
                        u'location_type': u'APPROXIMATE',
                        u'bounds': {
                            u'west': 9.530783400000018,
                            u'east': 17.16068610000002,
                            u'north': 49.0206081,
                            u'south': 46.37233579999999
                        },
                        u'viewport': {
                            u'west': 9.530783400000018,
                            u'east': 17.16068610000002,
                            u'north': 49.0206081,
                            u'south': 46.37233579999999
                        },
                        u'location': {
                            u'lat': 47.516231,
                            u'lng': 14.550072
                        }
                    },
                    u'address_components': [{
                        u'long_name': u'Austria',
                        u'types': [u'country', u'political'],
                        u'short_name': u'AT'}],
                    u'place_id': u'ChIJfyqdJZsHbUcRr8Hk3XvUEhA',
                    u'formatted_address': u'Austria',
                    u'types': [u'country', u'political']
                },
                u'title': u'Austria',
                u'name': u''
            }
        }]
    },

    'Belgium': {
        u'type': u'FeatureCollection',
        u'features': [{
            u'geometry': {
                u'type': u'Polygon',
                u'coordinates': [
                    [49.497013, 2.52409990000001],
                    [49.497013, 6.408124100000009],
                    [51.5051449, 6.408124100000009],
                    [51.5051449, 2.52409990000001]
                ]
            },
            u'type': u'Feature',
            u'bbox': [
                49.497013, 2.52409990000001,
                51.5051449, 6.408124100000009],
            u'properties': {
                u'description': u'Belgium',
                u'tags': [u'country', u'political'],
                u'center': [50.503887, 4.4699359999999615],
                u'other': {
                    u'geometry': {
                        u'location_type': u'APPROXIMATE',
                        u'bounds': {
                            u'west': 2.52409990000001,
                            u'east': 6.408124100000009,
                            u'north': 51.5051449,
                            u'south': 49.497013
                        },
                        u'viewport': {
                            u'west': 2.52409990000001,
                            u'east': 6.408124100000009,
                            u'north': 51.5051449,
                            u'south': 49.497013
                        },
                        u'location': {
                            u'lat': 50.503887,
                            u'lng': 4.4699359999999615
                        }
                    },
                    u'address_components': [{
                        u'long_name': u'Belgium',
                        u'types': [u'country', u'political'],
                        u'short_name': u'BE'}], u'place_id':
                    u'ChIJl5fz7WR9wUcR8g_mObTy60c', u'formatted_address':
                    u'Belgium', u'types': [u'country', u'political']},
                u'title': u'Belgium', u'name': u''}
            }
        ]
    },

    'Bosnia and Herzegovina': {
        u'type': u'FeatureCollection',
        u'features': [{
            u'geometry': {
                u'type': u'Polygon',
                u'coordinates': [
                    [42.5564516, 15.722366500000021],
                    [42.5564516, 19.621935000000008],
                    [45.2766262, 19.621935000000008],
                    [45.2766262, 15.722366500000021]
                ]
            },
            u'type': u'Feature',
            u'bbox': [
                42.5564516, 15.722366500000021,
                45.2766262, 19.621935000000008],
            u'properties': {
                u'description': u'Bosnia and Herzegovina',
                u'tags': [u'country', u'political'],
                u'center': [43.915886, 17.67907600000001],
                u'other': {
                    u'geometry': {
                        u'location_type': u'APPROXIMATE',
                        u'bounds': {
                            u'west': 15.722366500000021,
                            u'east': 19.621935000000008,
                            u'north': 45.2766262,
                            u'south': 42.5564516
                        },
                        u'viewport': {
                            u'west': 15.722366500000021,
                            u'east': 19.621935000000008,
                            u'north': 45.2766262,
                            u'south': 42.5564516
                        },
                        u'location': {
                            u'lat': 43.915886,
                            u'lng': 17.67907600000001
                        }
                    },
                    u'address_components': [{
                        u'long_name': u'Bosnia and Herzegovina',
                        u'types': [u'country', u'political'],
                        u'short_name': u'BA'}],
                    u'place_id':
                    u'ChIJ16k3xxWiSxMRDOm3QwPi920',
                    u'formatted_address': u'Bosnia and Herzegovina',
                    u'types': [u'country', u'political']
                },
                u'title': u'Bosnia and Herzegovina',
                u'name': u''}
            }
        ]
    },

    'Bulgaria': {
        u'type': u'FeatureCollection',
        u'features': [{
            u'geometry': {
                u'type': u'Polygon', u'coordinates': [
                    [41.2354469, 22.357344600000033],
                    [41.2354469, 28.72920010000007],
                    [44.2152333, 28.72920010000007],
                    [44.2152333, 22.357344600000033]]},
                u'type': u'Feature',
                u'bbox': [41.2354469, 22.357344600000033,
                          44.2152333, 28.72920010000007],
                u'properties': {
                    u'description': u'Bulgaria',
                    u'tags': [u'country', u'political'],
                    u'center': [42.733883, 25.485829999999964],
                    u'other': {
                        u'geometry': {
                            u'location_type': u'APPROXIMATE',
                            u'bounds': {
                                u'west': 22.357344600000033,
                                u'east': 28.72920010000007,
                                u'north': 44.2152333,
                                u'south': 41.2354469
                            },
                            u'viewport': {
                                u'west': 22.357344600000033,
                                u'east': 28.72920010000007,
                                u'north': 44.2152333,
                                u'south': 41.2354469
                            },
                            u'location': {
                                u'lat': 42.733883,
                                u'lng': 25.485829999999964
                            }
                        },
                        u'address_components': [{
                            u'long_name': u'Bulgaria',
                            u'types': [u'country', u'political'],
                            u'short_name': u'BG'}],
                        u'place_id': u'ChIJifBbyMH-qEAREEy_aRKgAAA',
                        u'formatted_address': u'Bulgaria',
                        u'types': [u'country', u'political']
                    },
                u'title': u'Bulgaria',
                u'name': u''}
                }
            ]
        },

    'Croatia': {
        u'type': u'FeatureCollection',
        u'features': [{
            u'geometry': {
                u'type': u'Polygon',
                u'coordinates': [
                    [42.3385087, 13.364900000000034],
                    [42.3385087, 19.448052299999972],
                    [46.5549857, 19.448052299999972],
                    [46.5549857, 13.364900000000034]]},
            u'type': u'Feature',
            u'bbox': [
                42.3385087, 13.364900000000034,
                46.5549857, 19.448052299999972],
            u'properties': {
                u'description': u'Croatia',
                u'tags': [u'country', u'political'],
                u'center': [45.1, 15.200000100000011],
                u'other': {
                    u'geometry': {
                        u'location_type': u'APPROXIMATE',
                        u'bounds': {
                            u'west': 13.364900000000034,
                            u'east': 19.448052299999972,
                            u'north': 46.5549857,
                            u'south': 42.3385087
                        },
                        u'viewport': {
                            u'west': 13.364900000000034,
                            u'east': 19.448052299999972,
                            u'north': 46.5549857,
                            u'south': 42.3385087},
                        u'location': {
                            u'lat': 45.1,
                            u'lng': 15.200000100000011
                        }
                    },
                    u'address_components': [{
                        u'long_name': u'Croatia',
                        u'types': [u'country', u'political'],
                        u'short_name': u'HR'}],
                    u'place_id': u'ChIJ7ZXdCghBNBMRfxtm4STA86A',
                    u'formatted_address': u'Croatia',
                    u'types': [u'country', u'political']
                },
                u'title': u'Croatia',
                u'name': u''}
            }
        ]
    },

    'Cyprus': {
        u'type': u'FeatureCollection',
        u'features': [{
            u'geometry': {
                u'type': u'Polygon',
                u'coordinates': [
                    [34.6304001, 32.245900000000006],
                    [34.6304001, 34.60450000000003],
                    [35.7071999, 34.60450000000003],
                    [35.7071999, 32.245900000000006]]},
            u'type': u'Feature',
            u'bbox': [
                34.6304001, 32.245900000000006,
                35.7071999, 34.60450000000003],
            u'properties': {
                u'description': u'Cyprus',
                u'tags': [u'country', u'political'],
                u'center': [35.126413, 33.429858999999965],
                u'other': {
                    u'geometry': {
                        u'location_type': u'APPROXIMATE',
                        u'bounds': {
                            u'west': 32.245900000000006,
                            u'east': 34.60450000000003,
                            u'north': 35.7071999,
                            u'south': 34.6304001
                        },
                        u'viewport': {
                            u'west': 32.245900000000006,
                            u'east': 34.60450000000003,
                            u'north': 35.7071999,
                            u'south': 34.6304001},
                        u'location': {
                            u'lat': 35.126413,
                            u'lng': 33.429858999999965}},
                        u'address_components': [{
                            u'long_name': u'Cyprus',
                            u'types': [u'country', u'political'],
                            u'short_name': u'CY'}],
                        u'place_id': u'ChIJVU1JymcX3hQRbhTEf4A8TDI',
                        u'formatted_address': u'Cyprus',
                        u'types': [u'country', u'political']
                },
                u'title': u'Cyprus', u'name': u''}
            }
        ]
    },

    'Czech Republic': {
            u'type': u'FeatureCollection',
            u'features': [{
                u'geometry': {
                    u'type': u'Polygon',
                    u'coordinates': [
                        [48.5518081, 12.090589000000023],
                        [48.5518081, 18.859236099999976],
                        [51.0557185, 18.859236099999976],
                        [51.0557185, 12.090589000000023]]},
                u'type': u'Feature',
                u'bbox': [
                    48.5518081, 12.090589000000023, 51.0557185,
                    18.859236099999976],
                u'properties': {
                    u'description':
                        u'Czechia', u'tags': [u'country', u'political'],
                        u'center': [49.81749199999999, 15.472962000000052],
                        u'other': {u'geometry': {
                            u'location_type':
                            u'APPROXIMATE', u'bounds': {
                                u'west': 12.090589000000023,
                                u'east': 18.859236099999976,
                                u'north': 51.0557185,
                                u'south': 48.5518081
                                },
                            u'viewport': {
                                u'west': 12.090589000000023,
                                u'east': 18.859236099999976,
                                u'north': 51.0557185,
                                u'south': 48.5518081},
                            u'location':
                                {
                                    u'lat': 49.81749199999999,
                                    u'lng': 15.472962000000052}
                                },
                            u'address_components': [{
                                u'long_name': u'Czechia',
                                u'types': [u'country', u'political'],
                                u'short_name': u'CZ'}],
                            u'place_id': u'ChIJQ4Ld14-UC0cRb1jb03UcZvg',
                            u'formatted_address': u'Czechia',
                            u'types': [u'country', u'political']
                        },
                        u'title': u'Czechia', u'name': u''
                }
            }]
        },

    'Denmark': {
        u'type': u'FeatureCollection',
        u'features': [{
            u'geometry': {
                u'type': u'Polygon',
                u'coordinates': [
                    [54.4317001, 7.855200100000047],
                    [54.4317001, 15.229800000000068],
                    [58.02846, 15.229800000000068],
                    [58.02846, 7.855200100000047]]
            },
            u'type': u'Feature',
            u'bbox': [54.4317001, 7.855200100000047,
                      58.02846, 15.229800000000068],
            u'properties': {
                u'description': u'Denmark',
                u'tags': [u'country', u'political'],
                u'center': [56.26392, 9.50178500000004],
                u'other': {
                    u'geometry': {
                        u'location_type': u'APPROXIMATE',
                        u'bounds': {
                            u'west': 7.855200100000047,
                            u'east': 15.229800000000068,
                            u'north': 58.02846,
                            u'south': 54.4317001
                        },
                        u'viewport': {
                            u'west': 7.855200100000047,
                            u'east': 15.229800000000068,
                            u'north': 58.02846,
                            u'south': 54.4317001},
                        u'location': {
                            u'lat': 56.26392,
                            u'lng': 9.50178500000004
                        }
                    },
                    u'address_components': [{
                        u'long_name': u'Denmark',
                        u'types': [u'country', u'political'],
                        u'short_name': u'DK'}
                    ],
                    u'place_id': u'ChIJ-1-U7rYnS0YRzZLgw9BDh1I',
                    u'formatted_address': u'Denmark',
                    u'types': [u'country', u'political']
                },
                u'title': u'Denmark', u'name': u''}
            }
        ]
    },

    'Estonia': {
        u'type': u'FeatureCollection',
        u'features': [{
            u'geometry': {
                u'type': u'Polygon',
                u'coordinates': [
                    [57.50931600000001, 21.654099900000006],
                    [57.50931600000001, 28.210138899999947],
                    [59.7315, 28.210138899999947],
                    [59.7315, 21.654099900000006]
                ]
            },
            u'type': u'Feature',
            u'bbox': [57.50931600000001, 21.654099900000006,
                      59.7315, 28.210138899999947],
            u'properties': {
                u'description': u'Estonia',
                u'tags': [u'country', u'political'],
                u'center': [58.595272, 25.013607099999945],
                u'other': {
                    u'geometry': {
                        u'location_type': u'APPROXIMATE',
                        u'bounds': {
                            u'west': 21.654099900000006,
                            u'east': 28.210138899999947,
                            u'north': 59.7315,
                            u'south': 57.50931600000001
                        },
                        u'viewport': {
                            u'west': 21.654099900000006,
                            u'east': 28.210138899999947,
                            u'north': 59.7315,
                            u'south': 57.50931600000001},
                        u'location': {
                            u'lat': 58.595272, u'lng': 25.013607099999945}
                    },
                    u'address_components': [{
                        u'long_name': u'Estonia',
                        u'types': [u'country', u'political'],
                        u'short_name': u'EE'}],
                    u'place_id': u'ChIJ_UuggpyUkkYRwyW0T7qf6kA',
                    u'formatted_address': u'Estonia',
                    u'types': [u'country', u'political']},
                u'title': u'Estonia',
                u'name': u''}
            }
        ]
    },

    'Finland': {
        u'type': u'FeatureCollection',
        u'features': [{
            u'geometry': {
                u'type': u'Polygon',
                u'coordinates': [
                    [59.693623, 20.456500199999937],
                    [59.693623, 31.5870999],
                    [70.0922932, 31.5870999],
                    [70.0922932, 20.456500199999937]
                ]
            },
            u'type': u'Feature',
            u'bbox': [59.693623, 20.456500199999937, 70.0922932, 31.5870999],
            u'properties': {
                u'description': u'Finland',
                u'tags': [u'country', u'political'],
                u'center': [61.92410999999999, 25.748151099999973],
                u'other': {
                    u'geometry': {
                        u'location_type': u'APPROXIMATE',
                        u'bounds': {
                            u'west': 20.456500199999937,
                            u'east': 31.5870999,
                            u'north': 70.0922932,
                            u'south': 59.693623
                        },
                        u'viewport': {
                            u'west': 20.456500199999937,
                            u'east': 31.5870999,
                            u'north': 70.0922932, u'south': 59.693623},
                        u'location': {u'lat': 61.92410999999999, u'lng':
                                      25.748151099999973}},
                        u'address_components': [{
                            u'long_name': u'Finland',
                            u'types': [u'country', u'political'],
                            u'short_name': u'FI'}],
                        u'place_id': u'ChIJ3fYyS9_KgUYREKh1PNZGAQA',
                        u'formatted_address': u'Finland', u'types':
                            [u'country', u'political']}, u'title': u'Finland',
                    u'name': u''}
            }
        ]
    },

    'France': {
        u'type': u'FeatureCollection',
        u'features': [{
            u'geometry': {
                u'type': u'Polygon',
                u'coordinates': [
                    [41.3253001, -5.559099999999944],
                    [41.3253001, 9.662499900000057],
                    [51.1241999, 9.662499900000057],
                    [51.1241999, -5.559099999999944]]},
            u'type': u'Feature',
            u'bbox': [41.3253001, -5.559099999999944,
                      51.1241999, 9.662499900000057],
            u'properties': {
                u'description': u'France',
                u'tags': [u'country', u'political'],
                u'center': [46.227638, 2.213749000000007],
                u'other': {
                    u'geometry': {
                        u'location_type': u'APPROXIMATE',
                        u'bounds': {
                            u'west': -5.559099999999944,
                            u'east': 9.662499900000057,
                            u'north': 51.1241999,
                            u'south': 41.3253001
                        },
                        u'viewport': {
                            u'west': -5.559099999999944,
                            u'east': 9.662499900000057,
                            u'north': 51.1241999,
                            u'south': 41.3253001},
                        u'location': {
                            u'lat': 46.227638,
                            u'lng': 2.213749000000007}
                    },
                    u'address_components': [{
                        u'long_name': u'France',
                        u'types': [u'country', u'political'],
                        u'short_name': u'FR'}],
                    u'place_id': u'ChIJMVd4MymgVA0R99lHx5Y__Ws',
                    u'formatted_address': u'France',
                    u'types': [u'country', u'political']
                },
                u'title': u'France', u'name': u''}
            }
        ]
    },

    'Germany': {
        u'type': u'FeatureCollection',
        u'features': [{
            u'geometry': {
                u'type': u'Polygon',
                u'coordinates': [
                    [47.2701115, 5.866342499999973],
                    [47.2701115, 15.041896199999996],
                    [55.0815, 15.041896199999996],
                    [55.0815, 5.866342499999973]
                ]
            },
            u'type': u'Feature',
            u'bbox': [47.2701115, 5.866342499999973,
                      55.0815, 15.041896199999996],
            u'properties': {
                u'description': u'Germany',
                u'tags': [u'country', u'political'],
                u'center': [51.165691, 10.451526000000058],
                u'other': {
                    u'geometry': {
                        u'location_type': u'APPROXIMATE',
                        u'bounds': {
                            u'west': 5.866342499999973,
                            u'east': 15.041896199999996,
                            u'north': 55.0815,
                            u'south': 47.2701115},
                        u'viewport': {
                            u'west': 5.866342499999973,
                            u'east': 15.041896199999996,
                            u'north': 55.0815,
                            u'south': 47.2701115
                        },
                        u'location': {
                            u'lat': 51.165691,
                            u'lng': 10.451526000000058}
                    },
                    u'address_components': [{
                        u'long_name': u'Germany',
                        u'types': [u'country', u'political'],
                        u'short_name': u'DE'}],
                    u'place_id':
                        u'ChIJa76xwh5ymkcRW-WRjmtd6HU',
                        u'formatted_address': u'Germany',
                        u'types': [u'country', u'political']},
                    u'title': u'Germany', u'name': u''}
            }
        ]
    },

    'Greece': {
        u'type': u'FeatureCollection',
        u'features': [{
            u'geometry': {
                u'type': u'Polygon',
                u'coordinates': [
                    [34.5428, 19.309799999999996],
                    [34.5428, 29.65279989999999],
                    [41.7488784, 29.65279989999999],
                    [41.7488784, 19.309799999999996]
                ]
            },
            u'type': u'Feature',
            u'bbox': [34.5428, 19.309799999999996,
                      41.7488784, 29.65279989999999],
            u'properties': {
                u'description': u'Greece',
                u'tags': [u'country', u'political'],
                u'center': [39.074208, 21.824311999999964],
                u'other': {
                    u'geometry': {
                        u'location_type': u'APPROXIMATE',
                        u'bounds': {
                            u'west': 19.309799999999996,
                            u'east': 29.65279989999999,
                            u'north': 41.7488784,
                            u'south': 34.5428
                        },
                        u'viewport': {
                            u'west': 19.309799999999996,
                            u'east': 29.65279989999999,
                            u'north': 41.7488784,
                            u'south': 34.5428
                        },
                        u'location': {
                            u'lat': 39.074208,
                            u'lng': 21.824311999999964}},
                        u'address_components': [{
                            u'long_name': u'Greece',
                            u'types': [u'country', u'political'],
                            u'short_name': u'GR'}], u'place_id':
                        u'ChIJY2xxEcdKWxMRHS2a3HUXOjY', u'formatted_address':
                        u'Greece', u'types': [u'country', u'political']
                },
                u'title': u'Greece', u'name': u''}
            }
        ]
    },

    'Hungary': {
        u'type': u'FeatureCollection',
        u'features': [{
            u'geometry': {
                u'type': u'Polygon',
                u'coordinates': [
                    [45.7370889, 16.11330780000003],
                    [45.7370889, 22.898121599999968],
                    [48.585234, 22.898121599999968],
                    [48.585234, 16.11330780000003]
                ]
            },
            u'type': u'Feature',
            u'bbox': [45.7370889, 16.11330780000003,
                      48.585234, 22.898121599999968],
            u'properties': {
                u'description': u'Hungary',
                u'tags': [u'country', u'political'],
                u'center': [47.162494, 19.503304100000037],
                u'other': {
                    u'geometry': {
                        u'location_type': u'APPROXIMATE',
                        u'bounds': {
                            u'west': 16.11330780000003,
                            u'east': 22.898121599999968,
                            u'north': 48.585234,
                            u'south': 45.7370889
                        },
                        u'viewport': {
                            u'west': 16.11330780000003,
                            u'east': 22.898121599999968,
                            u'north': 48.585234,
                            u'south': 45.7370889},
                        u'location': {
                            u'lat': 47.162494,
                            u'lng': 19.503304100000037}},
                        u'address_components': [{
                            u'long_name': u'Hungary',
                            u'types': [u'country', u'political'],
                            u'short_name': u'HU'}],
                        u'place_id': u'ChIJw-Q333uDQUcREBAeDCnEAAA',
                        u'formatted_address': u'Hungary',
                        u'types': [u'country', u'political']
                    },
                u'title': u'Hungary', u'name': u''}
            }
        ]
    },

    'Iceland': {
        u'type': u'FeatureCollection',
        u'features': [{
            u'geometry': {
                u'type': u'Polygon',
                u'coordinates': [
                    [62.4819, -26.25729990000002],
                    [62.4819, -12.238800099999935],
                    [67.2466, -12.238800099999935],
                    [67.2466, -26.25729990000002]]},
                u'type': u'Feature',
                u'bbox': [62.4819, -26.25729990000002,
                          67.2466, -12.238800099999935],
                u'properties': {
                    u'description': u'Iceland',
                    u'tags': [u'country', u'political'],
                    u'center': [64.963051, -19.020835000000034],
                u'other': {
                    u'geometry': {
                        u'location_type': u'APPROXIMATE',
                        u'bounds': {
                            u'west': -26.25729990000002,
                            u'east': -12.238800099999935,
                            u'north': 67.2466,
                            u'south': 62.4819},
                        u'viewport': {
                            u'west': -26.25729990000002,
                            u'east': -12.238800099999935,
                            u'north': 67.2466,
                            u'south': 62.4819},
                        u'location': {
                            u'lat': 64.963051, u'lng': -19.020835000000034}},
                        u'address_components': [{
                            u'long_name': u'Iceland',
                            u'types': [u'country', u'political'],
                            u'short_name': u'IS'}],
                    u'place_id': u'ChIJQ2Dro1Ir0kgRmkXB5TQEim8',
                    u'formatted_address': u'Iceland',
                    u'types': [u'country', u'political']
                    },
                u'title': u'Iceland',
                u'name': u''}
            }
        ]
    },

    'Ireland': {
        u'type': u'FeatureCollection',
        u'features': [{
            u'geometry': {
                u'type': u'Polygon',
                u'coordinates': [
                    [51.4475448, -10.480023699999947],
                    [51.4475448, -5.431910000000016],
                    [55.38294149999999, -5.431910000000016],
                    [55.38294149999999, -10.480023699999947]
                ]
            },
            u'type': u'Feature',
            u'bbox': [51.4475448, -10.480023699999947, 55.38294149999999,
                      -5.431910000000016],
            u'properties': {
                u'description': u'Ireland',
                u'tags': [u'establishment', u'natural_feature'],
                u'center': [53.1423672, -7.692053600000008],
                u'other': {
                    u'geometry': {
                        u'location_type': u'APPROXIMATE',
                        u'bounds': {
                            u'west': -10.480023699999947,
                            u'east': -5.431910000000016,
                            u'north': 55.38294149999999,
                            u'south': 51.4475448
                        },
                        u'viewport': {
                            u'west': -10.480023699999947,
                            u'east': -5.431910000000016,
                            u'north': 55.38294149999999,
                            u'south': 51.4475448
                        },
                        u'location': {
                            u'lat': 53.1423672,
                            u'lng': -7.692053600000008}},
                        u'address_components': [{
                            u'long_name': u'Ireland',
                            u'types': [u'establishment', u'natural_feature'],
                            u'short_name': u'Ireland'}],
                        u'place_id': u'ChIJj2lzXZ5hXkgRjcZqTUQ5m8o',
                        u'formatted_address': u'Ireland',
                        u'types': [u'establishment', u'natural_feature']
                },
                u'title': u'Ireland',
                u'name': u''
                }
            }
        ]
    },

    'Italy': {
        u'type': u'FeatureCollection',
        u'features': [{
            u'geometry': {
                u'type': u'Polygon',
                u'coordinates': [
                    [35.4897, 6.626720100000057],
                    [35.4897, 18.797599900000023],
                    [47.092, 18.797599900000023],
                    [47.092, 6.626720100000057]
                ]
            },
            u'type': u'Feature',
            u'bbox': [35.4897, 6.626720100000057, 47.092, 18.797599900000023],
            u'properties': {
                u'description': u'Italy',
                u'tags': [u'country', u'political'],
                u'center': [41.87194, 12.567379999999957],
                u'other': {
                    u'geometry': {
                        u'location_type': u'APPROXIMATE',
                        u'bounds': {
                            u'west': 6.626720100000057,
                            u'east': 18.797599900000023,
                            u'north': 47.092,
                            u'south': 35.4897
                        },
                        u'viewport': {
                            u'west': 6.626720100000057,
                            u'east': 18.797599900000023,
                            u'north': 47.092,
                            u'south': 35.4897
                        },
                        u'location': {
                            u'lat': 41.87194, u'lng': 12.567379999999957}
                    },
                    u'address_components': [{
                        u'long_name': u'Italy',
                        u'types': [u'country', u'political'],
                        u'short_name': u'IT'}],
                    u'place_id': u'ChIJA9KNRIL-1BIRb15jJFz1LOI',
                    u'formatted_address': u'Italy',
                    u'types': [u'country', u'political']
                },
                u'title': u'Italy',
                u'name': u''}
            }
        ]
    },

    'Kosovo': {
        u'type': u'FeatureCollection',
        u'features': [{
            u'geometry': {
                u'type': u'Polygon',
                u'coordinates': [
                    [41.857641, 20.014283999999975],
                    [41.857641, 21.789866899999993],
                    [43.2688985, 21.789866899999993],
                    [43.2688985, 20.014283999999975]
                ]
            },
            u'type': u'Feature',
            u'bbox': [41.857641, 20.014283999999975,
                      43.2688985, 21.789866899999993],
            u'properties': {
                u'description': u'Kosovo',
                u'tags': [u'country', u'political'],
                u'center': [42.6026359, 20.902976999999964],
                u'other': {
                    u'geometry': {
                        u'location_type': u'APPROXIMATE',
                        u'bounds': {
                            u'west': 20.014283999999975,
                            u'east': 21.789866899999993,
                            u'north': 43.2688985,
                            u'south': 41.857641
                        },
                        u'viewport': {
                            u'west': 20.014283999999975,
                            u'east': 21.789866899999993,
                            u'north': 43.2688985,
                            u'south': 41.857641
                        },
                        u'location': {
                            u'lat': 42.6026359,
                            u'lng': 20.902976999999964}
                    },
                    u'address_components': [{
                        u'long_name': u'Kosovo',
                        u'types': [u'country', u'political'],
                        u'short_name': u'XK'}],
                    u'place_id': u'ChIJ8X2_VPN6UxMRkRfDq9_u_78',
                    u'formatted_address': u'Kosovo',
                    u'types': [u'country', u'political']
                },
                u'title': u'Kosovo',
                u'name': u''
                }
            }
        ]
    },

    'Latvia': {
        u'type': u'FeatureCollection',
        u'features': [{
            u'geometry': {
                u'type': u'Polygon',
                u'coordinates': [
                    [55.6747769, 20.8465999],
                    [55.6747769, 28.241402900000026],
                    [58.0855688, 28.241402900000026],
                    [58.0855688, 20.8465999]
                ]
            },
            u'type': u'Feature',
            u'bbox': [55.6747769, 20.8465999, 58.0855688, 28.241402900000026],
            u'properties': {
                u'description': u'Latvia',
                u'tags': [u'country', u'political'],
                u'center': [56.879635, 24.60318899999993],
                u'other': {
                    u'geometry': {
                        u'location_type': u'APPROXIMATE',
                        u'bounds': {
                            u'west': 20.8465999,
                            u'east': 28.241402900000026,
                            u'north': 58.0855688,
                            u'south': 55.6747769
                        },
                        u'viewport': {
                            u'west': 20.8465999,
                            u'east': 28.241402900000026,
                            u'north': 58.0855688,
                            u'south': 55.6747769
                        },
                        u'location': {
                            u'lat': 56.879635,
                            u'lng': 24.60318899999993
                        }
                    },
                    u'address_components': [{
                        u'long_name': u'Latvia',
                        u'types': [u'country', u'political'],
                        u'short_name': u'LV'}],
                    u'place_id': u'ChIJ_ZqKe2cw6UYREPzyaM3PAAA',
                    u'formatted_address': u'Latvia',
                    u'types': [u'country', u'political']
                },
                u'title': u'Latvia',
                u'name': u''
                }
            }
        ]
    },

    'Liechtenstein': {
        u'type': u'FeatureCollection',
        u'features': [{
            u'geometry': {
                u'type': u'Polygon',
                u'coordinates': [
                    [47.04828999999999, 9.47162000000003],
                    [47.04828999999999, 9.63565010000002],
                    [47.2705467, 9.63565010000002],
                    [47.2705467, 9.47162000000003]
                ]
            },
            u'type': u'Feature',
            u'bbox': [47.04828999999999, 9.47162000000003,
                      47.2705467, 9.63565010000002],
            u'properties': {
                u'description': u'Liechtenstein',
                u'tags': [u'country', u'political'],
                u'center': [47.166, 9.555373000000031],
                u'other': {
                    u'geometry': {
                        u'location_type': u'APPROXIMATE',
                        u'bounds': {
                            u'west': 9.47162000000003,
                            u'east': 9.63565010000002,
                            u'north': 47.2705467,
                            u'south': 47.04828999999999
                        },
                        u'viewport': {
                            u'west': 9.47162000000003,
                            u'east': 9.63565010000002,
                            u'north': 47.2705467,
                            u'south': 47.04828999999999
                        },
                        u'location': {
                            u'lat': 47.166,
                            u'lng': 9.555373000000031
                        }
                    },
                    u'address_components': [{
                        u'long_name': u'Liechtenstein',
                        u'types': [u'country', u'political'],
                        u'short_name': u'LI'}],
                    u'place_id': u'ChIJ_S9HHUQxm0cRibFa3Ta16mA',
                    u'formatted_address': u'Liechtenstein',
                    u'types': [u'country', u'political']
                },
                u'title': u'Liechtenstein',
                u'name': u''
                }
            }
        ]
    },

    'Lithuania': {
        u'type': u'FeatureCollection',
        u'features': [{
            u'geometry': {
                u'type': u'Polygon',
                u'coordinates': [
                    [53.89687869999999, 20.93100000000004],
                    [53.89687869999999, 26.8355914],
                    [56.45032089999999, 26.8355914],
                    [56.45032089999999, 20.93100000000004]
                ]
            },
            u'type': u'Feature',
            u'bbox': [53.89687869999999, 20.93100000000004,
                      56.45032089999999, 26.8355914],
            u'properties': {
                u'description': u'Lithuania',
                u'tags': [u'country', u'political'],
                u'center': [55.169438, 23.88127499999996],
                u'other': {
                    u'geometry': {
                        u'location_type': u'APPROXIMATE',
                        u'bounds': {
                            u'west': 20.93100000000004,
                            u'east': 26.8355914,
                            u'north': 56.45032089999999,
                            u'south': 53.89687869999999
                        },
                        u'viewport': {
                            u'west': 20.93100000000004,
                            u'east': 26.8355914,
                            u'north': 56.45032089999999,
                            u'south': 53.89687869999999
                        },
                        u'location': {
                            u'lat': 55.169438,
                            u'lng': 23.88127499999996
                        }
                    },
                    u'address_components': [{
                        u'long_name': u'Lithuania',
                        u'types': [u'country', u'political'],
                        u'short_name': u'LT'}],
                    u'place_id': u'ChIJE74zDxSU3UYRubpdpdNUCvM',
                    u'formatted_address': u'Lithuania',
                    u'types': [u'country', u'political']
                },
                u'title': u'Lithuania',
                u'name': u''
                }
            }
        ]
    },

    'Luxembourg': {
        u'type': u'FeatureCollection',
        u'features': [{
            u'geometry': {
                u'type': u'Polygon',
                u'coordinates': [
                    [49.447779, 5.735669899999948],
                    [49.447779, 6.5309700999999905],
                    [50.18282, 6.5309700999999905],
                    [50.18282, 5.735669899999948]
                ]
            },
            u'type': u'Feature',
            u'bbox': [49.447779, 5.735669899999948,
                      50.18282, 6.5309700999999905],
            u'properties': {
                u'description': u'Luxembourg',
                u'tags': [u'country', u'political'],
                u'center': [49.815273, 6.129583000000025],
                u'other': {
                    u'geometry': {
                        u'location_type': u'APPROXIMATE',
                        u'bounds': {
                            u'west': 5.735669899999948,
                            u'east': 6.5309700999999905,
                            u'north': 50.18282,
                            u'south': 49.447779
                        },
                        u'viewport': {
                            u'west': 5.735669899999948,
                            u'east': 6.5309700999999905,
                            u'north': 50.18282,
                            u'south': 49.447779
                        },
                        u'location': {
                            u'lat': 49.815273, u'lng': 6.129583000000025
                        }
                    },
                    u'address_components': [{
                        u'long_name': u'Luxembourg',
                        u'types': [u'country', u'political'],
                        u'short_name': u'LU'
                    }],
                    u'place_id': u'ChIJRyEhyrlFlUcR75LTAvZg22Q',
                    u'formatted_address': u'Luxembourg',
                    u'types': [u'country', u'political']
                },
                u'title': u'Luxembourg',
                u'name': u''
            }
        }]
    },

    'Macedonia the former Yugoslavian Republic of': {
            u'type': u'FeatureCollection',
            u'features': [{
                u'geometry': {
                    u'type': u'Polygon',
                    u'coordinates': [
                        [40.8537826, 20.452422999999953],
                        [40.8537826, 23.034092999999984],
                        [42.373646, 23.034092999999984],
                        [42.373646, 20.452422999999953]
                    ]
                },
                u'type': u'Feature',
                u'bbox': [40.8537826, 20.452422999999953,
                          42.373646, 23.034092999999984],
                u'properties': {
                    u'description': u'Macedonia (FYROM)',
                    u'tags': [u'country', u'political'],
                    u'center': [41.608635, 21.745274999999992],
                    u'other': {
                        u'geometry': {
                            u'location_type': u'APPROXIMATE',
                            u'bounds': {
                                u'west': 20.452422999999953,
                                u'east': 23.034092999999984,
                                u'north': 42.373646,
                                u'south': 40.8537826
                            },
                            u'viewport': {
                                u'west': 20.289999999999964,
                                u'east': 24.182000000000016,
                                u'north': 42.535,
                                u'south': 39.705
                            },
                            u'location': {
                                u'lat': 41.608635,
                                u'lng': 21.745274999999992}
                        },
                        u'formatted_address': u'Macedonia (FYROM)',
                        u'place_id': u'ChIJCUi8cJ8VVBMRscUfyNZa8uA',
                        u'address_components': [{
                            u'long_name': u'Macedonia (FYROM)',
                            u'types': [u'country', u'political'],
                            u'short_name': u'MK'}],
                        u'partial_match': True,
                        u'types': [u'country', u'political']
                    },
                    u'title': u'Macedonia (FYROM)',
                    u'name': u''
                    }
                }
            ]
        },

    'Malta': {
        u'type': u'FeatureCollection',
        u'features': [{
            u'geometry': {
                u'type': u'Polygon',
                u'coordinates': [
                    [35.79960000000001, 14.180100100000004],
                    [35.79960000000001, 14.57659990000002],
                    [36.0853, 14.57659990000002],
                    [36.0853, 14.180100100000004]
                ]
            },
            u'type': u'Feature',
            u'bbox': [35.79960000000001, 14.180100100000004,
                      36.0853, 14.57659990000002],
            u'properties': {
                u'description': u'Malta',
                u'tags': [u'country', u'political'],
                u'center': [35.937496, 14.375415999999973],
                u'other': {
                    u'geometry': {
                        u'location_type': u'APPROXIMATE',
                        u'bounds': {
                            u'west': 14.180100100000004,
                            u'east': 14.57659990000002,
                            u'north': 36.0853,
                            u'south': 35.79960000000001
                        },
                        u'viewport': {
                            u'west': 14.180100100000004,
                            u'east': 14.57659990000002,
                            u'north': 36.0853,
                            u'south': 35.79960000000001
                        },
                        u'location': {
                            u'lat': 35.937496,
                            u'lng': 14.375415999999973
                        }
                    },
                    u'address_components': [{
                        u'long_name': u'Malta',
                        u'types': [u'country', u'political'],
                        u'short_name': u'MT'}],
                    u'place_id': u'ChIJxUeGHShFDhMROUK-NmHYgvU',
                    u'formatted_address': u'Malta',
                    u'types': [u'country', u'political']
                },
                u'title': u'Malta',
                u'name': u''
                }
            }
        ]
    },

    'Montenegro': {
        u'type': u'FeatureCollection',
        u'features': [{
            u'geometry': {
                u'type': u'Polygon',
                u'coordinates': [
                    [41.8297, 18.433792100000005],
                    [41.8297, 20.357486900000026],
                    [43.558743, 20.357486900000026],
                    [43.558743, 18.433792100000005]
                ]
            },
            u'type': u'Feature',
            u'bbox': [41.8297, 18.433792100000005,
                      43.558743, 20.357486900000026],
            u'properties': {
                u'description': u'Montenegro',
                u'tags': [u'country', u'political'],
                u'center': [42.708678, 19.37438999999995],
                u'other': {
                    u'geometry': {
                        u'location_type': u'APPROXIMATE',
                        u'bounds': {
                            u'west': 18.433792100000005,
                            u'east': 20.357486900000026,
                            u'north': 43.558743,
                            u'south': 41.8297
                        },
                        u'viewport': {
                            u'west': 18.433792100000005,
                            u'east': 20.357486900000026,
                            u'north': 43.558743,
                            u'south': 41.8297
                        },
                        u'location': {
                            u'lat': 42.708678,
                            u'lng': 19.37438999999995
                        }
                    },
                    u'address_components': [{
                        u'long_name': u'Montenegro',
                        u'types': [u'country', u'political'],
                        u'short_name': u'ME'}],
                    u'place_id': u'ChIJyx8sJBcyTBMRRtP_boadTDg',
                    u'formatted_address': u'Montenegro',
                    u'types': [u'country', u'political']
                },
                u'title': u'Montenegro',
                u'name': u''
                }
            }
        ]
    },

    'Netherlands': {
        u'type': u'FeatureCollection',
        u'features': [{
            u'geometry': {
                u'type': u'Polygon',
                u'coordinates': [
                    [50.75038379999999, 3.3316001000000597],
                    [50.75038379999999, 7.227510199999983],
                    [53.6316, 7.227510199999983],
                    [53.6316, 3.3316001000000597]
                ]
            },
            u'type': u'Feature',
            u'bbox': [50.75038379999999, 3.3316001000000597,
                      53.6316, 7.227510199999983],
            u'properties': {
                u'description': u'Netherlands',
                u'tags': [u'country', u'political'],
                u'center': [52.132633, 5.2912659999999505],
                u'other': {
                    u'geometry': {
                        u'location_type': u'APPROXIMATE',
                        u'bounds': {
                            u'west': 3.3316001000000597,
                            u'east': 7.227510199999983,
                            u'north': 53.6316,
                            u'south': 50.75038379999999
                        },
                        u'viewport': {
                            u'west': 3.3315999999999804,
                            u'east': 7.227140500000019,
                            u'north': 53.6756,
                            u'south': 50.7503837
                        },
                        u'location': {
                            u'lat': 52.132633,
                            u'lng': 5.2912659999999505
                        }
                    },
                    u'address_components': [{
                        u'long_name': u'Netherlands',
                        u'types': [u'country', u'political'],
                        u'short_name': u'NL'}],
                    u'place_id': u'ChIJu-SH28MJxkcRnwq9_851obM',
                    u'formatted_address': u'Netherlands',
                    u'types': [u'country', u'political']
                },
                u'title': u'Netherlands',
                u'name': u''
                }
            }
        ]
    },

    'Norway': {
        u'type': u'FeatureCollection',
        u'features': [{
            u'geometry': {
                u'type': u'Polygon',
                u'coordinates': [
                    [57.8097, 4.064899999999966],
                    [57.8097, 31.35499989999994],
                    [71.30780000000001, 31.35499989999994],
                    [71.30780000000001, 4.064899999999966]
                ]
            },
            u'type': u'Feature',
            u'bbox': [57.8097, 4.064899999999966,
                      71.30780000000001, 31.35499989999994],
            u'properties': {
                u'description': u'Norway',
                u'tags': [u'country', u'political'],
                u'center': [60.47202399999999, 8.46894599999996],
                u'other': {
                    u'geometry': {
                        u'location_type': u'APPROXIMATE',
                        u'bounds': {
                            u'west': 4.064899999999966,
                            u'east': 31.35499989999994,
                            u'north': 71.30780000000001,
                            u'south': 57.8097
                        },
                        u'viewport': {
                            u'west': 4.064899999999966,
                            u'east': 31.35499989999994,
                            u'north': 71.30780000000001,
                            u'south': 57.8097
                        },
                        u'location': {
                            u'lat': 60.47202399999999,
                            u'lng': 8.46894599999996
                        }
                    },
                    u'address_components': [{
                        u'long_name': u'Norway',
                        u'types': [u'country', u'political'],
                        u'short_name': u'NO'}],
                    u'place_id': u'ChIJv-VNj0VoEkYRK9BkuJ07sKE',
                    u'formatted_address': u'Norway',
                    u'types': [u'country', u'political']
                    },
                u'title': u'Norway', u'name': u''
                }
            }
        ]
     },

    'Poland': {
        u'type': u'FeatureCollection',
        u'features': [{
            u'geometry': {
                u'type': u'Polygon',
                u'coordinates': [
                    [49.0020252, 14.122864100000015],
                    [49.0020252, 24.145893200000046],
                    [54.9054761, 24.145893200000046],
                    [54.9054761, 14.122864100000015]
                ]
            },
            u'type': u'Feature',
            u'bbox': [49.0020252, 14.122864100000015,
                      54.9054761, 24.145893200000046],
            u'properties': {
                u'description': u'Poland',
                u'tags': [u'country', u'political'],
                u'center': [51.919438, 19.14513599999998],
                u'other': {
                    u'geometry': {
                        u'location_type': u'APPROXIMATE',
                        u'bounds': {
                            u'west': 14.122864100000015,
                            u'east': 24.145893200000046,
                            u'north': 54.9054761,
                            u'south': 49.0020252
                        },
                        u'viewport': {
                            u'west': 14.122864100000015,
                            u'east': 24.145893200000046,
                            u'north': 54.9054761,
                            u'south': 49.0020252
                        },
                        u'location': {
                            u'lat': 51.919438,
                            u'lng': 19.14513599999998
                        }
                    },
                    u'address_components': [{
                        u'long_name': u'Poland',
                        u'types': [u'country', u'political'],
                        u'short_name': u'PL'}],
                    u'place_id': u'ChIJuwtkpGSZAEcR6lXMScpzdQk',
                    u'formatted_address': u'Poland',
                    u'types': [u'country', u'political']
                },
                u'title': u'Poland',
                u'name': u''
                }
            }
        ]
    },

    'Portugal': {
        u'type': u'FeatureCollection',
        u'features': [{
            u'geometry': {
                u'type': u'Polygon',
                u'coordinates': [
                    [32.2895, -31.464799900000003],
                    [32.2895, -6.189159199999949],
                    [42.1543111, -6.189159199999949],
                    [42.1543111, -31.464799900000003]
                ]
            },
            u'type': u'Feature',
            u'bbox': [32.2895, -31.464799900000003,
                      42.1543111, -6.189159199999949],
            u'properties': {
                u'description': u'Portugal',
                u'tags': [u'country', u'political'],
                u'center': [39.39987199999999, -8.224454000000037],
                u'other': {
                    u'geometry': {
                        u'location_type': u'APPROXIMATE',
                        u'bounds': {
                            u'west': -31.464799900000003,
                            u'east': -6.189159199999949,
                            u'north': 42.1543111,
                            u'south': 32.2895
                        },
                        u'viewport': {
                            u'west': -31.464799900000003,
                            u'east': -6.189159199999949,
                            u'north': 42.1543111,
                            u'south': 32.2895
                        },
                        u'location': {
                            u'lat': 39.39987199999999,
                            u'lng': -8.224454000000037
                        }
                    },
                    u'address_components': [{
                        u'long_name': u'Portugal',
                        u'types': [u'country', u'political'],
                        u'short_name': u'PT'}],
                    u'place_id': u'ChIJ1SZCvy0kMgsRQfBOHAlLuCo',
                    u'formatted_address': u'Portugal',
                    u'types': [u'country', u'political']
                },
                u'title': u'Portugal',
                u'name': u''
                }
            }
        ]
    },

    'Romania': {
        u'type': u'FeatureCollection',
        u'features': [{
            u'geometry': {
                u'type': u'Polygon',
                u'coordinates': [
                    [43.6186193, 20.261759299999994],
                    [43.6186193, 29.77839999999992],
                    [48.265274, 29.77839999999992],
                    [48.265274, 20.261759299999994]
                ]
            },
            u'type': u'Feature',
            u'bbox': [43.6186193, 20.261759299999994,
                      48.265274, 29.77839999999992],
            u'properties': {
                u'description': u'Romania',
                u'tags': [u'country', u'political'],
                u'center': [45.943161, 24.966760000000022],
                u'other': {
                    u'geometry': {
                        u'location_type': u'APPROXIMATE',
                        u'bounds': {
                            u'west': 20.261759299999994,
                            u'east': 29.77839999999992,
                            u'north': 48.265274,
                            u'south': 43.6186193
                        },
                        u'viewport': {
                            u'west': 20.261759299999994,
                            u'east': 29.77839999999992,
                            u'north': 48.265274,
                            u'south': 43.6186193
                        },
                        u'location': {
                            u'lat': 45.943161,
                            u'lng': 24.966760000000022
                        }
                    },
                    u'address_components': [{
                        u'long_name': u'Romania',
                        u'types': [u'country', u'political'],
                        u'short_name': u'RO'}],
                    u'place_id': u'ChIJw3aJlSb_sUARlLEEqJJP74Q',
                    u'formatted_address': u'Romania',
                    u'types': [u'country', u'political']
                },
                u'title': u'Romania',
                u'name': u''
                }
            }
        ]
    },

    'Serbia': {
        u'type': u'FeatureCollection',
        u'features': [{
            u'geometry': {
                u'type': u'Polygon',
                u'coordinates': [
                    [42.2315029, 18.838522099999977],
                    [42.2315029, 23.006309500000043],
                    [46.190032, 23.006309500000043],
                    [46.190032, 18.838522099999977]
                ]
            },
            u'type': u'Feature',
            u'bbox': [42.2315029, 18.838522099999977,
                      46.190032, 23.006309500000043],
            u'properties': {
                u'description':
                    u'Serbia',
                    u'tags': [u'country', u'political'],
                    u'center': [44.016521, 21.005858999999987],
                    u'other': {
                        u'geometry': {
                            u'location_type': u'APPROXIMATE',
                            u'bounds': {
                                u'west': 18.838522099999977,
                                u'east': 23.006309500000043,
                                u'north': 46.190032,
                                u'south': 42.2315029
                            },
                            u'viewport': {
                                u'west': 18.838522099999977,
                                u'east': 23.006309500000043,
                                u'north': 46.190032,
                                u'south': 42.2315029
                            },
                            u'location': {
                                u'lat': 44.016521,
                                u'lng': 21.005858999999987
                            }
                        },
                        u'address_components': [{
                            u'long_name': u'Serbia',
                            u'types': [u'country', u'political'],
                            u'short_name': u'RS'}],
                        u'place_id': u'ChIJlYCJ8t8dV0cRXYYjN-pQXgU',
                        u'formatted_address': u'Serbia',
                        u'types': [u'country', u'political']
                    },
                    u'title': u'Serbia',
                    u'name': u''
                }
            }
        ]
    },

    'Slovakia': {
        u'type': u'FeatureCollection',
        u'features': [{
            u'geometry': {
                u'type': u'Polygon',
                u'coordinates': [
                    [47.731159, 16.83318209999993],
                    [47.731159, 22.558933799999977],
                    [49.61380510000001, 22.558933799999977],
                    [49.61380510000001, 16.83318209999993]
                ]
            },
            u'type': u'Feature',
            u'bbox': [47.731159, 16.83318209999993,
                      49.61380510000001, 22.558933799999977],
            u'properties': {
                u'description': u'Slovakia',
                u'tags': [u'country', u'political'],
                u'center': [48.669026, 19.69902400000001],
                u'other': {
                    u'geometry': {
                        u'location_type': u'APPROXIMATE',
                        u'bounds': {
                            u'west': 16.83318209999993,
                            u'east': 22.558933799999977,
                            u'north': 49.61380510000001,
                            u'south': 47.731159
                        },
                        u'viewport': {
                            u'west': 16.83318209999993,
                            u'east': 22.558933799999977,
                            u'north': 49.61380510000001,
                            u'south': 47.731159
                        },
                        u'location': {
                            u'lat': 48.669026,
                            u'lng': 19.69902400000001
                        }
                    },
                    u'address_components': [{
                        u'long_name': u'Slovakia',
                        u'types': [u'country', u'political'],
                        u'short_name': u'SK'}],
                    u'place_id': u'ChIJf8Z8rrlgFEcRfTpysWdha80',
                    u'formatted_address': u'Slovakia',
                    u'types': [u'country', u'political']
                },
                u'title': u'Slovakia',
                u'name': u''
            }
        }]
    },

    'Slovenia': {
        u'type': u'FeatureCollection',
        u'features': [{
            u'geometry': {
                u'type': u'Polygon',
                u'coordinates': [
                    [45.4218356, 13.375335500000006],
                    [45.4218356, 16.61070380000001],
                    [46.876659, 16.61070380000001],
                    [46.876659, 13.375335500000006]
                ]
            },
            u'type': u'Feature',
            u'bbox': [45.4218356, 13.375335500000006, 46.876659,
                      16.61070380000001],
            u'properties': {
                u'description': u'Slovenia',
                u'tags': [u'country', u'political'],
                u'center': [46.151241, 14.995462999999972],
                u'other': {
                    u'geometry': {
                        u'location_type': u'APPROXIMATE',
                        u'bounds': {
                            u'west': 13.375335500000006,
                            u'east': 16.61070380000001,
                            u'north': 46.876659,
                            u'south': 45.4218356
                        },
                        u'viewport': {
                            u'west': 13.375335500000006,
                            u'east': 16.61070380000001,
                            u'north': 46.876659,
                            u'south': 45.4218356
                        },
                        u'location': {
                            u'lat': 46.151241,
                            u'lng': 14.995462999999972
                        }
                    },
                    u'address_components': [{
                        u'long_name': u'Slovenia',
                        u'types': [u'country', u'political'],
                        u'short_name': u'SI'}],
                    u'place_id': u'ChIJYYOWXuckZUcRZdTiJR5FQOc',
                    u'formatted_address': u'Slovenia',
                    u'types': [u'country', u'political']
                },
                u'title': u'Slovenia',
                u'name': u''
                }
            }
        ]
    },

    'Spain': {
        u'type': u'FeatureCollection',
        u'features': [{
            u'geometry': {
                u'type': u'Polygon',
                u'coordinates': [
                    [27.4985, -18.264800100000002],
                    [27.4985, 4.636200000000031],
                    [43.8504, 4.636200000000031],
                    [43.8504, -18.264800100000002]
                ]
            },
            u'type': u'Feature',
            u'bbox': [27.4985, -18.264800100000002,
                      43.8504, 4.636200000000031],
            u'properties': {
                u'description': u'Spain',
                u'tags': [u'country', u'political'],
                u'center': [40.46366700000001, -3.7492200000000366],
                u'other': {
                    u'geometry': {
                        u'location_type': u'APPROXIMATE',
                        u'bounds': {
                            u'west': -18.264800100000002,
                            u'east': 4.636200000000031,
                            u'north': 43.8504,
                            u'south': 27.4985
                        },
                        u'viewport': {
                            u'west': -12.524000000000001,
                            u'east': 5.097999999999956,
                            u'north': 45.244,
                            u'south': 35.17300000000001
                        },
                        u'location': {
                            u'lat': 40.46366700000001,
                            u'lng': -3.7492200000000366
                        }
                    },
                    u'address_components': [{
                        u'long_name': u'Spain',
                        u'types': [u'country', u'political'],
                        u'short_name': u'ES'}],
                    u'place_id': u'ChIJi7xhMnjjQgwR7KNoB5Qs7KY',
                    u'formatted_address': u'Spain',
                    u'types': [u'country', u'political']
                },
                u'title': u'Spain',
                u'name': u''
                }
            }
        ]
    },

    'Sweden': {
        u'type': u'FeatureCollection',
        u'features': [{
            u'geometry': {
                u'type': u'Polygon',
                u'coordinates': [
                    [55.0059799, 10.579799999999977],
                    [55.0059799, 24.1773101],
                    [69.0599709, 24.1773101],
                    [69.0599709, 10.579799999999977]
                ]
            },
            u'type': u'Feature',
            u'bbox': [55.0059799, 10.579799999999977, 69.0599709,
                      24.1773101],
            u'properties': {
                u'description': u'Sweden',
                u'tags': [u'country', u'political'],
                u'center': [60.12816100000001, 18.643501000000015],
                u'other': {
                    u'geometry': {
                        u'location_type': u'APPROXIMATE',
                        u'bounds': {
                            u'west': 10.579799999999977,
                            u'east': 24.1773101,
                            u'north': 69.0599709,
                            u'south': 55.0059799
                        },
                        u'viewport': {
                            u'west': 10.579799999999977,
                            u'east': 24.1773101,
                            u'north': 69.0599709,
                            u'south': 55.0059799
                        },
                        u'location': {
                            u'lat': 60.12816100000001,
                            u'lng': 18.643501000000015}
                        },
                    u'address_components': [{
                        u'long_name': u'Sweden',
                        u'types': [u'country', u'political'],
                        u'short_name': u'SE'}],
                    u'place_id': u'ChIJ8fA1bTmyXEYRYm-tjaLruCI',
                    u'formatted_address': u'Sweden',
                    u'types': [u'country', u'political']
                },
                u'title': u'Sweden',
                u'name': u''
                }
            }
        ]
    },

    'Switzerland': {
        u'type': u'FeatureCollection',
        u'features': [{
            u'geometry': {
                u'type': u'Polygon',
                u'coordinates': [
                    [45.81792, 5.956079999999929],
                    [45.81792, 10.492340099999979],
                    [47.8084546, 10.492340099999979],
                    [47.8084546, 5.956079999999929]
                ]
            },
            u'type': u'Feature',
            u'bbox': [45.81792, 5.956079999999929,
                      47.8084546, 10.492340099999979],
            u'properties': {
                u'description': u'Switzerland',
                u'tags': [u'country', u'political'],
                u'center': [46.818188, 8.227511999999933],
                u'other': {
                    u'geometry': {
                        u'location_type': u'APPROXIMATE',
                        u'bounds': {
                            u'west': 5.956079999999929,
                            u'east': 10.492340099999979,
                            u'north': 47.8084546,
                            u'south': 45.81792
                        },
                        u'viewport': {
                            u'west': 5.956079999999929,
                            u'east': 10.492340099999979,
                            u'north': 47.8084546,
                            u'south': 45.81792
                        },
                        u'location': {
                            u'lat': 46.818188, u'lng': 8.227511999999933
                        }
                    },
                    u'address_components': [{
                        u'long_name': u'Switzerland',
                        u'types': [u'country', u'political'],
                        u'short_name': u'CH'}],
                    u'place_id': u'ChIJYW1Zb-9kjEcRFXvLDxG1Vlw',
                    u'formatted_address': u'Switzerland',
                    u'types': [u'country', u'political']
                },
                u'title': u'Switzerland',
                u'name': u''
                }
            }
        ]
    },

    'Turkey': {
        u'type': u'FeatureCollection',
        u'features': [{
            u'geometry': {
                u'type': u'Polygon',
                u'coordinates': [
                    [35.808592, 25.537699999999973],
                    [35.808592, 44.817844899999955],
                    [42.3666999, 44.817844899999955],
                    [42.3666999, 25.537699999999973]
                ]
            },
            u'type': u'Feature',
            u'bbox': [35.808592, 25.537699999999973,
                      42.3666999, 44.817844899999955],
            u'properties': {
                u'description': u'Turkey',
                u'tags': [u'country', u'political'],
                u'center': [38.963745, 35.243322000000035],
                u'other': {
                    u'geometry': {
                        u'location_type': u'APPROXIMATE',
                        u'bounds': {
                            u'west': 25.537699999999973,
                            u'east': 44.817844899999955,
                            u'north': 42.3666999,
                            u'south': 35.808592
                        },
                        u'viewport': {
                            u'west': 25.537699999999973,
                            u'east': 44.817844899999955,
                            u'north': 42.3666999,
                            u'south': 35.808592
                        },
                        u'location': {
                            u'lat': 38.963745,
                            u'lng': 35.243322000000035
                        }
                    },
                    u'address_components': [{
                        u'long_name': u'Turkey',
                        u'types': [u'country', u'political'],
                        u'short_name': u'TR'}],
                    u'place_id': u'ChIJcSZPllwVsBQRKl9iKtTb2UA',
                    u'formatted_address': u'Turkey',
                    u'types': [u'country', u'political']
                },
                u'title': u'Turkey',
                u'name': u''
                }
            }
        ]
    },

    'United Kingdom': {
        u'type': u'FeatureCollection',
        u'features': [{
            u'geometry': {
                u'type': u'Polygon',
                u'coordinates': [
                    [34.5614, -8.89889990000006],
                    [34.5614, 33.91655489999994],
                    [60.91569999999999, 33.91655489999994],
                    [60.91569999999999, -8.89889990000006]
                ]
            },
            u'type': u'Feature',
            u'bbox': [34.5614, -8.89889990000006, 60.91569999999999,
                      33.91655489999994],
            u'properties': {
                u'description': u'United Kingdom',
                u'tags': [u'country', u'political'],
                u'center': [55.378051, -3.43597299999999],
                u'other': {
                    u'geometry': {
                        u'location_type': u'APPROXIMATE',
                        u'bounds': {
                            u'west': -8.89889990000006,
                            u'east': 33.91655489999994,
                            u'north': 60.91569999999999,
                            u'south': 34.5614
                        },
                        u'viewport': {
                            u'west': -8.89889990000006,
                            u'east': 33.91655489999994,
                            u'north': 60.91569999999999,
                            u'south': 34.5614
                        },
                        u'location': {
                            u'lat': 55.378051,
                            u'lng': -3.43597299999999
                        }
                    },
                    u'address_components': [{
                        u'long_name': u'United Kingdom',
                        u'types': [u'country', u'political'],
                        u'short_name': u'GB'}],
                    u'place_id': u'ChIJqZHHQhE7WgIReiWIMkOg-MQ',
                    u'formatted_address': u'United Kingdom',
                    u'types': [u'country', u'political']
                },
                u'title': u'United Kingdom', u'name': u''
            }
        }]
    }
}


def generate_data(locations):
    """ Input: locations - list of countries
        Output: the data to be saved in annotations in eea.geotags format
    """
    features = []
    for location in locations:
        country = COUNTRIES_DATA.get(location, None)
        if country is not None:
            features.append(country['features'][0])
        else:
            print "!!! Unknown location: {0}".format(location)

    data = {
        u'type': u'FeatureCollection',
        u'features': features
    }

    if len(features) > 0:
        return data
    else:
        return None


def do_migration(landitem):
    tool = api.portal.get_tool('portal_languages')
    countries = dict(tool.listAvailableCountries())

    locations = [
        countries.get(t, t) for t in landitem.getGeographicCoverage()
    ]

    # if "test-landitem" in landitem.absolute_url():
    #     locations = ['Austria', 'Albania']
    #     anno = getattr(landitem, '__annotations__', {})
    #     print anno.get('eea.geotags.tags')
    #     data = generate_data(locations)
    #
    #     import pdb; pdb.set_trace()
    # if "test-landitem" in landitem.absolute_url():
    #     locations = [
    #         countries.get(t, t) for t in landitem.getGeographicCoverage()
    #     ]
    #
    #     import pdb; pdb.set_trace()
    #     locations = ['Bulgaria', 'Romania']
    #     # landitem.geographicCoverageGT = locations
    #     landitem.getField('geographicCoverageGT').set(landitem, locations)
    #     landitem.reindexObject()
    #     transaction.commit()

    # print "WIP getGeographicCoverage -> getGeographicCoverageGT"


def run(_):
    catalog = api.portal.get_tool(name='portal_catalog')
    landitems = [b.getObject() for b in catalog(portal_type='LandItem')]
    for landitem in landitems:
        # logger.info('Migrating: %s!', landitem.absolute_url(1))
        do_migration(landitem)
        # logger.info('Success: %s!', landitem.absolute_url(1))
