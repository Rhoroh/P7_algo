from csv import DictReader
from glob import glob
import time


def loading_data(file):
    """
    loading function
    :param file: csv file name to analyse
    :return: None, call knapsack function
    """

    # reading *.csv file
    data = DictReader(open(file))

    shares = []

    # Cleaning data at this step, if a share have an incoherent price or
    # profit value, it's not include.

    # price*100 to only deal with int,
    # profit*1000 to deal with int, and to avoid rounding errors.
    # price int(round) to avoid rounding error with cents
    for row in data:
        if float(row['price']) > 0 and float(row['profit']) > 0:
            price = float(row['price'])
            profit = price * float(row['profit']) / 100
            share = [row['name'], int(round(price * 100, 0)),
                     int(profit * 1000)]
            shares.append(share)
    knapsack(shares, 500)


def knapsack(data, max_budget):
    """
    function that calculate the best set of shares for maximizing profits.
    :param data: list extract from csv file : [name, price, profit]
    :param max_budget: int, max value to spend.
    :return: None, call display_best function
    """

    # values
    profits = []
    # weight
    prices = []
    # limit, *100 for avoiding index error with float numbers
    budget = int(max_budget * 100)
    best_shares = []

    for share in data:
        profits.append(share[2])
        prices.append(share[1])

    # knapsack dynamic programming algo
    n = len(profits)

    # creating a table, rows are shares, columns are prices from 0 to max,
    # in cents.
    table = [[0 for _ in range(budget + 1)] for _ in range(n + 1)]

    # placing shares value in the table
    for i in range(n + 1):
        for j in range(budget + 1):
            if i == 0 or j == 0:
                table[i][j] = 0
            elif prices[i - 1] <= j:
                table[i][j] = max(profits[i - 1]
                                  + table[i - 1][j - prices[i - 1]],
                                  table[i - 1][j])
            else:
                table[i][j] = table[i - 1][j]

    # max profit is the value in the last line, last column.
    result = table[n][budget]

    # getting shares: comparing result to results in the last column, in an
    # upward manner
    for i in range(n, 0, -1):
        if result <= 0:
            break
        # if result is equal to the value in the case above it, it
        # means that this share wasn't include in result
        if result == table[i - 1][budget]:
            continue
        # if result isn't the same than the case above it, it means that this
        # share was in the result
        else:
            best_shares.append(data[i - 1])
            result = result - profits[i - 1]
            budget = budget - prices[i - 1]

    display_best(best_shares, get_price(best_shares))


def get_price(data):
    """
    function to get the total cost of a set of shares
    :param data: list of shares : [name, price, profit]
    :return: float
    """

    price = 0
    for share in data:
        price += share[1]
    return price / 100


def display_best(shares, budget):
    """
    function to display the best shares combination, their total cost, and
    their profits
    :param shares: list of shares : [name, price, profit]
    :param budget: float, total cost of the shares
    :return:  None, print the results
    """

    total_profit = 0
    for share in shares:
        print(share[0])
        total_profit += share[2] / 1000
    rendement = (total_profit / budget) * 100
    print('\n Cout : {:.2f} €.'.format(budget))
    print('\n Benefice total : {:.2f} €,'
          ' rendement : {:.2f} %.'.format(total_profit, rendement))

def main():
    """
    Main function, user choose which file to analyse.
    :return: None, call loading_data function
    """

    csv_files = glob("csv_files/*.csv")

    for index, file in enumerate(csv_files):
        print(index, file[10:])

    sel = int(input("Entrez l'index du fichier à analyser : "))
    start = time.time()
    loading_data(csv_files[sel])
    end = time.time()
    elapsed = end - start
    print(f' Temps d\'exécution : {elapsed:.2}ms',
          '\n')
    return main()

if __name__ == '__main__':
    main()
