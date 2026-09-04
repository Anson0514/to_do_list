class Calculator:
    def add(self, a, b):
        """回傳兩個數字的總和"""
        return a + b

    def multiply(self, a, b):
        """回傳兩個數字的乘積"""
        return a * b


if __name__ == "__main__":
    calc = Calculator()
    print(calc.add(3, 5))
    print(calc.multiply(4, 6))
