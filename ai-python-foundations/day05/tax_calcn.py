def calculate_tax(amount, tax_rate):
    """
    Calculate the tax for a given amount and tax rate.

    Parameters:
    amount (float): The amount to calculate tax on.
    tax_rate (float): The tax rate as a decimal (e.g., 0.05 for 5%).

    Returns:
    float: The calculated tax.
    """
    return amount * tax_rate
amount = float(input("Enter the amount: "))
tax_rate = float(input("Enter the tax rate (as a decimal): "))
tax = calculate_tax(amount, tax_rate)
print(f"The calculated tax is: {tax}")