"""Hypothesis Testing"""
import collections
import math
import random
import matplotlib.pyplot as plt

def normal_pdf(x, mu=0, sigma=1):
    """Probability density function for Normal Distribution"""
    sqrt_two_pi = math.sqrt(2 * math.pi)
    return (math.exp(-((x - mu) ** 2) / (2 * (sigma ** 2))) /
            (sqrt_two_pi * sigma))

def normal_cdf(x, mu=0, sigma=1):
    """Cumulative distribution function for the normal distribution"""
    return (1 + math.erf((x- mu) / math.sqrt(2) / sigma)) / 2

def inverse_normal_cdf(p, mu=0, sigma=1, tolerance=0.00001):
    """Find approx inverse cdf using binary search"""

    # If not standard, compute standard and rescale
    if mu != 0 or sigma != 1:
        return mu + sigma * inverse_normal_cdf(p, tolerance=tolerance)

    low_z = -10.0               # normal_cdf(-10) is (very close to) 0
    hi_z = 10.0                 # normal_cdf(10)  is (very close to) 1

    while hi_z - low_z > tolerance:
        mid_z = (low_z + hi_z) / 2
        mid_p = normal_cdf(mid_z)
        if mid_p < p:
            # Midpoint is too low, search above it
            low_z = mid_z
        elif mid_p > p:
            # Midpoint is too high, search below it
            hi_z = mid_z
        else:
            break

    return mid_z

def bernoulli_trial(p):
    return 1 if random.random() < p else 0

def binomial(n, p):
    return sum(bernoulli_trial(p) for _ in range(n))

def make_hist(p, n, num_points):

    data = [binomial(n, p) for _ in range(num_points)]

    #  Use a bar chart to show the actual binomial samples
    histogram = collections.Counter(data)
    plt.bar([x - 0.4 for x in histogram.keys()],
            [v / num_points for v in histogram.values()],
            0.8,
            color='0.75')

    mu = p * n
    sigma = math.sqrt(n * p * (1 - p))

    #  Use a line chart to show the normal approximation
    xs = range(min(data), max(data) + 1)
    ys = [normal_cdf(i + 0.5, mu, sigma) - normal_cdf(i - 0.5, mu, sigma)
          for i in xs]
    plt.plot(xs, ys)
    plt.title("Binomial Distribution vs Normal Approximation")
    plt.show()

def normal_approximation_to_binomial(n, p):
    """Finds mu and sigma corresponding to Binomial(n, p)"""
    mu = p * n
    sigma = math.sqrt(p * (1-p) * n)
    return mu, sigma

#  The normal cdf _is the probability the variable is below a threshold.
normal_probability_below = normal_cdf

#  It's above the threshold if it's not below the threshold.
def normal_probability_above(low, mu=0, sigma=1):
    return 1 - normal_cdf(low, mu, sigma)

#  It's between if it's less than high, but not less than low
def normal_probability_between(low, high, mu=0, sigma=1):
    return normal_cdf(high, mu, sigma) - normal_cdf(low, mu, sigma)

#  It's outside if it's not between
def normal_probability_outside(low, high, mu=0, sigma=1):
    return 1 - normal_probability_between(low, high, mu, sigma)

def main():
    """Plotting a few distributions / density functions"""

    # Plot a few normal_pdf's
    xs = [x / 10.0 for x in range(-50, 50)]
    plt.plot(xs, [normal_pdf(x, sigma=1) for x in xs], '-',
             label='mu = 0, sigma = 1')
    plt.plot(xs, [normal_pdf(x, sigma=2) for x in xs], '--',
             label='mu = 0, sigma = 2')
    plt.plot(xs, [normal_pdf(x, sigma=0.5) for x in xs], ':',
             label='mu = 0, sigma = 0.5')
    plt.plot(xs, [normal_pdf(x, mu=-1) for x in xs], '-.',
             label='mu = -1, sigma = 1')
    plt.legend()
    plt.title("Various Normal pdfs")
    plt.show()

    # Plot a few cumulative distribution functions
    xs = [x / 10.0 for x in range(-50, 50)]
    plt.plot(xs, [normal_cdf(x, sigma=1) for x in xs], '-',
             label='mu = 0, sigma = 1')
    plt.plot(xs, [normal_cdf(x, sigma=2) for x in xs], '--',
             label='mu = 0, sigma = 2')
    plt.plot(xs, [normal_cdf(x, sigma=0.5) for x in xs], ':',
             label='mu = 0, sigma = 0.5')
    plt.plot(xs, [normal_cdf(x, mu=-1) for x in xs], '-.',
             label='mu = -1, sigma = 1')
    plt.legend(loc=4)   # bottom right
    plt.title("Various Normal cdfs")
    plt.show()

    make_hist(0.75, 100, 10000)


if __name__ == "__main__":
    main()
