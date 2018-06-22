from collections import namedtuple

XYZ = namedtuple("XYZ", ['x', 'y', 'z'])
UV = namedtuple("UV", ['u', 'v'])

cubeV = (
    XYZ(1, 1, 1),
    XYZ(-1, 1, 1),
    XYZ(-1, 1, -1),
    XYZ(1, 1, -1),
    XYZ(1, -1, 1),
    XYZ(-1, -1, 1),
    XYZ(-1, -1, -1),
    XYZ(1, -1, -1)
)

cubeF = (
    (0, 1, 2),
    (0, 2, 3),

    (0, 3, 7),
    (0, 4, 7),

    (1, 2, 6),
    (1, 5, 6),

    (0, 1, 5),
    (0, 4, 5),

    (2, 3, 7),
    (2, 6, 7),

    (4, 5, 6),
    (4, 6, 7)
)

cubeT = (
    # topo
    (UV(1, 0), UV(0, 0), UV(0, 1)),
    (UV(1, 0), UV(0, 1), UV(1, 1)),
    # lat direita
    (UV(0, 1), UV(1, 1), UV(1, 0)),
    (UV(0, 1), UV(0, 0), UV(1, 0)),
    # lat esquerda
    (UV(1, 1), UV(0, 1), UV(0, 0)),
    (UV(1, 1), UV(1, 0), UV(0, 0)),
    # frente
    (UV(1, 1), UV(0, 1), UV(0, 0)),
    (UV(1, 1), UV(1, 0), UV(0, 0)),
    # traz
    (UV(1, 1), UV(0, 1), UV(0, 0)),
    (UV(1, 1), UV(1, 0), UV(0, 0)),
    # baixo
    (UV(1, 0), UV(1, 1), UV(0, 1)),
    (UV(1, 0), UV(0, 1), UV(0, 0))
)

pyramidV = (
    XYZ(-1, 0, 1),
    XYZ(1, 0, 1),
    XYZ(-1, 0, -1),
    XYZ(1, 0, -1),
    XYZ(0, 1, 0)
)

pyramidF = (
    # base
    (0, 1, 3),
    (0, 2, 3),
    # laterais
    (0, 1, 4),
    (0, 2, 4),
    (2, 3, 4),
    (1, 3, 4)
)

pyramidT = (
    # base
    (UV(1, 1), UV(1, 0), UV(0, 0)),
    (UV(1, 1), UV(0, 1), UV(0, 0)),
    # laterais
    (UV(0, 0), UV(0, 1), UV(0.5, 1)),
    (UV(1, 0), UV(0, 0), UV(0.5, 1)),
    (UV(1, 0), UV(0, 0), UV(0.5, 1)),
    (UV(0, 0), UV(0, 1), UV(0.5, 1))
)