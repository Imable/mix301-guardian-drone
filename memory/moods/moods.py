from .mood import Mood

raw_moods = [
    Mood(
        'happy',
        [
            (1, [0, 0, 20, 0]),
            (1, [0, 0, -20, 0])
        ]
    ),
    Mood(
        'sad',
        [
            (4, [30, 30, 0, 0]),
            (4, [30, -30, 0, 0]),
            (4, [-30, -30, 0, 0]),
            (4, [-30, 30, 0, 0])
        ],
        [
            (4, [0, 0, -70, 0])
        ],
        True
    ),
    Mood(
        'no_mood',
        [
            (2, [0, 0, 0, 0])
        ]
    ),
    Mood(
        'confused',
        [
            (1, [0, 0, 0, 40]),
            (2, [0, 0, 0, -20])
        ]
    )
]

moods = { mood.name: mood for mood in raw_moods }