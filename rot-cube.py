from drawille import Canvas, line, animate
from math import hypot, sqrt, sin, cos, pi
from numpy import array, matmul, ones
from time import sleep


def drawproj(x, y, z, obs, scr, defo):
    lamb = (obs - scr) * (defo - scr) / ((obs - z) * (obs - scr))
    return (lamb * x, lamb * y)


imat = array([[ sqrt(1/2), -sqrt(1/2),        0. ],
              [ sqrt(1/3),  sqrt(1/3), -sqrt(1/3)],
              [ sqrt(1/6),  sqrt(1/6),  sqrt(2/3)]])

scala, fps, omega, o, s, wobble = 60, 60, 2 * pi / 3, 160, 80, 50
bor = scala / (o - wobble) * s + 3

edges = [ (0,1), (1,2), (2,3), (3,4), (4,5), (5,6), (6,7), (7,0), (1,6), (2,5), (4,7), (0,3) ] 


def __main__():
    points = []
    for i in range(8):
        at = i ^ (i >> 1)
        points.append(ones((3, 1)))
        for j in range(3):
            if (at & (1 << j) != 0):
                points[i][j][0] = -1.
        points[i] = scala / 2 * matmul(imat, points[i])

    ft = omega / fps
    rotmat = array([[ cos(ft), 0., -sin(ft) ],
                    [      0., 1.,       0. ],
                    [ sin(ft), 0.,  cos(ft) ]])
    at = 0
    while True:
        frame = []
        frame.extend([coords for coords in line(bor, bor, bor, -bor)])
        frame.extend([coords for coords in line(bor, -bor, -bor, -bor)])
        frame.extend([coords for coords in line(-bor, -bor, -bor, bor)])
        frame.extend([coords for coords in line(-bor, bor, bor, bor)])
        for i in range(8):
            points[i] = matmul(rotmat, points[i])
        for edge in edges:
            x1 = float(points[edge[0]][0][0]) 
            y1 = float(points[edge[0]][1][0])
            z1 = float(points[edge[0]][2][0])
            x2 = float(points[edge[1]][0][0])
            y2 = float(points[edge[1]][1][0])
            z2 = float(points[edge[1]][2][0])

            obloc = o + wobble * sin((1 + sqrt(5)) * ft * at)
            x1p, y1p = drawproj(x1, y1, z1, obloc, s, o)
            x2p, y2p = drawproj(x2, y2, z2, obloc, s, o)
            frame.extend([coords for coords in line(x1p, y1p, x2p, y2p)])
        yield frame
        at += 1

if __name__ == '__main__':
    animate(Canvas(), __main__, 1/fps)
