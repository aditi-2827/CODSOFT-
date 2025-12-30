def calculator():
    while True:
        print("\nSimple Calculator")
        print("Operations:")
        print("1. Addition (+)")
        print("2. Subtraction (-)")
        print("3. Multiplication (*)")
        print("4. Division (/)")
        print("5. Exit (q)")
        
        try:
            num1 = input("\nEnter first number (or 'q' to quit): ")
            if num1.lower() == 'q':
                print("Thank you for using the calculator!")
                break
            num1 = float(num1)
            
            num2 = input("Enter second number: ")
            num2 = float(num2)
            
            operation = input("Enter operation (+, -, *, /): ")
            
            if operation == '+':
                result = num1 + num2
                print(f"\n{num1} + {num2} = {result}")
            elif operation == '-':
                result = num1 - num2
                print(f"\n{num1} - {num2} = {result}")
            elif operation == '*':
                result = num1 * num2
                print(f"\n{num1} * {num2} = {result}")
            elif operation == '/':
                if num2 != 0:
                    result = num1 / num2
                    print(f"\n{num1} / {num2} = {result}")
                else:
                    print("\nError: Cannot divide by zero!")
            else:
                print("\nInvalid operation! Please use +, -, *, or /")
        
        except ValueError:
            print("\nError: Please enter valid numbers!")
        except Exception as e:
            print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    calculator()
