raw = {
    2019: [
        [12, 8, 2, 0, 0, 0, 0],
        [4,  8, 5, 3, 2, 0, 0],
        [0,  3, 8, 7, 2, 2, 0],
        [0,  0, 2, 10, 5, 4, 1],
        [0, 0, 0,5,8,3,6],
    ],
    2020: [
        [27, 11, 3, 3, 0, 0, 0],
        [10, 13, 10, 6, 5, 0, 0],
        [1,6,14,11,5,7,0],
        [0,1,5,10,16,7,5],
        [0,0,1,7,13,11,12],
    ],
    2021: [
        [25,11,9,1,0,0,0],
        [9,15,7,8,7,0,0],
        [0,6,12,10,13,5,0],
        [0,0,5,13,7,17,4],
        [0,0,1,5,13,11,16],
    ],
    2022: [
        [27,9,3,1,0,0,0],
        [7,13,11,7,2,0,0],
        [0,7,11,11,8,3,0],
        [0,0,3,13,14,7,3],
        [0,0,1,4,13,11,11],
    ],
    2023: [
        [24,6,4,2,1,0,0],
        [8,12,7,4,4,2,0],
        [0,7,10,10,4,6,0],
        [0,0,6,11,9,6,5],
        [0,0,0,8,10,10,9],
    ],
    2024: [
        # <1, <5, <30, ~50, >70, >95, >99
        [18, 5,  6, 2, 1, 0,  0],   # 5
        [4,  11, 7, 5, 3, 2,  0],   # 10
        [1,  3,  7, 10, 6, 4, 1],   # 15
        [0,  1,  2, 10, 8, 7, 4],   # 20
        [0,  1,  0, 3, 12, 10, 6],  # 30
    ],
}

def cum(xs):
    return [sum(xs[:i]) for i in range(1, len(xs)+1)]

data = {}
for yr, ds  in raw.items():
    data[yr] = []

    s = None
    for d in ds:
        if s is None:
            s = sum(d)
        else:
            assert s == sum(d)
        data[yr].append([p/s for p in d])

cdata = {yr: [cum(dist) for dist in dists] for yr, dists in data.items()}
print(cdata)
import pprint
pprint.pprint(cdata)

import matplotlib.pyplot as plt
import matplotlib.cm as cm

years = [2019, 2020, 2021, 2022, 2023, 2024]
risks = ['<1%', '<5%', '<30%', '~50%', '>70%', '>95%', '>99%']
crisks = ['>1%', '>5%', '>~50%', '>70%', '>95%', '>99%']
arisks = ['ge-1', 'ge-5', 'ge-50', 'ge-70', 'ge-95', 'ge-99']
timeline = [5, 10, 15, 20, 30]
qyears = list(range(years[0]+timeline[0], years[-1]+timeline[-1]+1))

def plot(tli):
    plt.clf()
    plt.stackplot(
        years, *[
            [data[yr][tli][ri]*100 for yr in years]
            for ri, risk in enumerate(risks)
        ], labels=risks,
        colors= [
            'green',
            'yellow',
            'orange',
            'red',
            'maroon',
            'dimgray',
            'black'
        ]
    )

    plt.title("Quantum threat timeline predictions over the years for\n"
              f"breaking RSA-2048 within {timeline[tli]} years")
    plt.legend()
    plt.ylabel('Fraction of interviewed experts')
    plt.xlabel('Year of interviews')
    plt.savefig(f'{timeline[tli]}-years.png')

plot(0)
plot(1)
plot(2)
plot(3)
plot(4)

def plot2(ri):
    plt.clf()
    plt.title("Quantum threat timeline predictions over the years for\n"
              f"breaking RSA-2048 with probability {crisks[ri]}")
    colormap = [cm.YlGn((i+1)/len(years)) for i in range(len(years))]
    for i, yr in enumerate(years):
        x = [offset+yr for offset in timeline]
        y = [100-cdata[yr][offsetIndex][ri]*100 for offsetIndex in range(len(timeline))]
        plt.scatter(x, y, label=yr, color=colormap[i])
        if i == 0 or i == len(years)-1:
            plt.plot(x, y, color=colormap[i], linewidth=1)
    plt.ylim(0,100)
    plt.xlabel("Q-day")
    plt.ylabel(f"Fraction of interviewed experts agree chance is {crisks[ri]}")
    for offsetIndex, offset in enumerate(timeline):
        for yrIndex, yr in enumerate(years[:-1]):
            x1 = offset+yr
            x2 = offset+yr+1
            y1 = 100-cdata[yr][offsetIndex][ri]*100
            y2 = 100-cdata[yr+1][offsetIndex][ri]*100
            plt.quiver(
                x1, y1, x2-x1, y2-y1, color=colormap[yrIndex],
                angles='xy', scale_units='xy', scale=1, width=0.005,
            )
    plt.legend()
    plt.savefig(f'{arisks[ri]}.png')

plot2(0)
plot2(1)
plot2(2)
plot2(3)
plot2(4)
plot2(5)
