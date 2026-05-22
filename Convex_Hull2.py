import matplotlib.pyplot as plt
import matplotlib.animation as animation


def orientation(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])

def distance(p, q):
    return (p[0] - q[0])**2 + (p[1] - q[1])**2



def jarvis_march_steps(points):
    n = len(points)
    if n < 3:
        yield points, []
        return

    #finding the lowest and leftmost point
    start = min(points, key=lambda p: (p[1], p[0]))
    hull = [start]
    current = start

    while True:
        candidate = None
        for point in points:
            if point == current:
                continue
            if candidate is None:
                candidate = point
                continue

            o = orientation(current, candidate, point)
            if o < 0 or (o == 0 and distance(current, point) > distance(current, candidate)):
                candidate = point

            # Yield current hull and candidate (for animation)
            yield hull[:], [current, candidate]

        if candidate == start:
            hull.append(start)  # close the loop visually
            yield hull, []  # yield the final frame
            break

        hull.append(candidate)
        current = candidate
        if candidate == start:
            hull.append(start)  # close the loop visually
            yield hull, []  # yield the final frame
            break

        hull.append(candidate)
        current = candidate

        hull.append(candidate)
        current = candidate

    yield hull, []




def animate_jarvis(points):
    fig, ax = plt.subplots()
    ax.set_title("Jarvis March Convex Hull Animation")
    ax.set_xlim(min(x for x, y in points) - 1, max(x for x, y in points) + 1)
    ax.set_ylim(min(y for x, y in points) - 1, max(y for x, y in points) + 1)

    # Plot points
    ax.scatter(*zip(*points), color='black', s=50)

    line_hull, = ax.plot([], [], 'r-', lw=2)       # red line for final hull
    line_candidate, = ax.plot([], [], 'b--', lw=1) # blue dashed line for candidate checking

    steps = list(jarvis_march_steps(points))

    def update(frame):
        hull, candidate_line = steps[frame]
        if hull:
            xs, ys = zip(*hull)
            line_hull.set_data(xs, ys)
        if candidate_line:
            xs, ys = zip(*candidate_line)
            line_candidate.set_data(xs, ys)
        return line_hull, line_candidate

    ani = animation.FuncAnimation(fig, update, frames=len(steps),
                                  interval=500, repeat=False)
    plt.show()



if __name__ == "__main__":
    points = [
        (0, 3), (2, 2), (1, 1), (2, 1),
        (3, 0), (0, 0), (3, 3)
    ]
    animate_jarvis(points)

