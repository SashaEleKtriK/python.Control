import csv


def read_all(path):
    i = 0
    header = []
    farms = []

    for line in csv.reader(open(path), delimiter=','):

        i += 1
        if i == 1:
            for val in line:
                header.append(val)
        else:
            zip_data = {}
            for idx in range(0, len(line)):

                if (header[idx] == "x" or header[idx] == "y") and not(line[idx] == ''):
                    val = float(line[idx])
                else:
                    val = line[idx].replace("'", " ")
                zip_data[header[idx]] = val
            if len(zip_data.keys()) > 0:
                farms.append(zip_data)
    return farms


if __name__ == "__main__":
    all_markets = read_all('Export.csv')
    print(all_markets[0])

