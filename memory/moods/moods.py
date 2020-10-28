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
            (1, [-20, 0, 0, 0]),
            (1, [20, 0, 0, 0])
        ],
        [
            (1, [0, 0, -20, 0])
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
            (1, [0, 0, 0, 60]),
            (1, [0, 0, 0, -10])
        ]
    )
]

moods = { mood.name: mood for mood in raw_moods }