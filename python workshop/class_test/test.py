import math

class Frac:
    def __init__(self, numerator, denominator):
        self.numerator = numerator
        self.denominator = denominator

    def __str__(self):
        return f"{self.numerator}/{self.denominator}"

    def averageWith(self, other):
        new_numerator = self.numerator * other.denominator + other.numerator * self.denominator
        new_denominator = 2 * self.denominator * other.denominator
        # Simplify the fraction
        gcd = math.gcd(new_numerator, new_denominator)
        new_numerator //= gcd
        new_denominator //= gcd
        return Frac(new_numerator, new_denominator)

    def invert(self):
        return Frac(self.denominator, self.numerator)

# Main routine to calculate the harmonic mean
a = int(input())
b = int(input())
print(Frac(1, a).averageWith(Frac(1, b)).invert())
