from random import uniform, choice, randrange, random

base = None # baseline color for monochrome

def bv2rgb(bv): # converts b-v color index (real stars) to rgb
    if bv < -0.40: bv = -0.40
    if bv > 2.00: bv = 2.00

    r = g = b = 0.0

    # red
    if  -0.40 <= bv<0.00:
        t=(bv+0.40)/(0.00+0.40)
        r=0.61+(0.11*t)+(0.1*t*t)
    elif 0.00 <= bv<0.40:
        t=(bv-0.00)/(0.40-0.00)
        r=0.83+(0.17*t)
    elif 0.40 <= bv<2.10:
        t=(bv-0.40)/(2.10-0.40)
        r=1.00

    # green
    if  -0.40 <= bv<0.00:
        t=(bv+0.40)/(0.00+0.40)
        g=0.70+(0.07*t)+(0.1*t*t)
    elif 0.00 <= bv<0.40:
        t=(bv-0.00)/(0.40-0.00)
        g=0.87+(0.11*t)
    elif 0.40 <= bv<1.60:
        t=(bv-0.40)/(1.60-0.40)
        g=0.98-(0.16*t)
    elif 1.60 <= bv<2.00:
        t=(bv-1.60)/(2.00-1.60)
        g=0.82-(0.5*t*t)

    # blue
    if  -0.40 <= bv<0.40:
        t=(bv+0.40)/(0.40+0.40)
        b=1.00
    elif 0.40 <= bv<1.50:
        t=(bv-0.40)/(1.50-0.40)
        b=1.00-(0.47*t)+(0.1*t*t)
    elif 1.50 <= bv<1.94:
        t=(bv-1.50)/(1.94-1.50)
        b=0.63-(0.6*t*t)

    return (round(r*255), round(g*255), round(b*255))

def temperature(): # random color temp based on b-v interval
    global base; base = None # reset base
    return bv2rgb(uniform(-0.4, 2.0))

def rainbow(): # random color from rainbow
    return choice('red orange yellow green blue purple violet'.split())

def pastels(): # random pastel color
    return tuple((randrange(256)+255)//2 for _ in range(3))

def monochrome(option = randrange(3)): # random monochrome color
    global base
    if not base: # if there is no base, make one
        base = tuple(randrange(256) for _ in range(3))
    r, g, b = base
    offset = random()
    for _ in range(2):
        if option == 0:
            r *= offset
        elif option == 1:
            g *= offset
        elif option == 2:
            b *= offset
        option = (r + g + b) % 3
    return (round(r), round(g), round(b))