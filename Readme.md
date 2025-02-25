# Google OR-Tool VRP Case

This repo is a case work. A Vehicle Route Problem is solved by using Google OR-Tool 

#### To run:
```run
uvicorn main:app --reload
```


## End Points

#### GET / -> Hello world Page.
#### POST /solver -> Takes a json and returns best routes for all vehicles

## Example Input
```json
    {
        "vehicles": [
            {
                "id": 1,
                "start_index": 0,
                "capacity": [
                    4
                ]
            },
            {
                "id": 2,
                "start_index": 1,
                "capacity": [
                    6
                ]
            },
            {
                "id": 3,
                "start_index": 2,
                "capacity": [
                    6
                ]
            }
        ],
        "jobs": [
            {
                "id": 1,
                "location_index": 3,
                "delivery": [
                    2
                ],
                "service": 327
            },
            {
                "id": 2,
                "location_index": 4,
                "delivery": [
                    1
                ],
                "service": 391
            },
            {
                "id": 3,
                "location_index": 5,
                "delivery": [
                    1
                ],
                "service": 297
            },
            {
                "id": 4,
                "location_index": 6,
                "delivery": [
                    2
                ],
                "service": 234
            },
            {
                "id": 5,
                "location_index": 7,
                "delivery": [
                    1
                ],
                "service": 357
            },
            {
                "id": 6,
                "location_index": 8,
                "delivery": [
                    1
                ],
                "service": 407
            },
            {
                "id": 7,
                "location_index": 9,
                "delivery": [
                    1
                ],
                "service": 382
            }
        ],
        "matrix": [
            [
                0,
                516,
                226,
                853,
                1008,
                1729,
                346,
                1353,
                1554,
                827
            ],
            [
                548,
                0,
                474,
                1292,
                1442,
                2170,
                373,
                1801,
                1989,
                1068
            ],
            [
                428,
                466,
                0,
                1103,
                1175,
                1998,
                226,
                1561,
                1715,
                947
            ],
            [
                663,
                1119,
                753,
                0,
                350,
                1063,
                901,
                681,
                814,
                1111
            ],
            [
                906,
                1395,
                1003,
                292,
                0,
                822,
                1058,
                479,
                600,
                1518
            ],
            [
                1488,
                1994,
                1591,
                905,
                776,
                0,
                1746,
                603,
                405,
                1676
            ],
            [
                521,
                357,
                226,
                1095,
                1167,
                1987,
                0,
                1552,
                1705,
                1051
            ],
            [
                1092,
                1590,
                1191,
                609,
                485,
                627,
                1353,
                0,
                422,
                1583
            ],
            [
                1334,
                1843,
                1436,
                734,
                609,
                396,
                1562,
                421,
                0,
                1745
            ],
            [
                858,
                1186,
                864,
                1042,
                1229,
                1879,
                984,
                1525,
                1759,
                0
            ]
        ]
    }
```