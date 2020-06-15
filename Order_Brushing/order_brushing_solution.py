import csv
import bisect
import operator
from datetime import datetime

with open("test.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    dict = {}
    FORMAT = "%Y-%m-%d %H:%M:%S"
    LIMIT_DURATION = 3600
    result = {}

    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        elif len(row) > 0:
            orderId = row[0]
            shopId = row[1]
            userId = row[2]
            eventTime = row[3]
            if not shopId in dict:
                dict[shopId] = []
            bisect.insort(dict[shopId], (datetime.strptime(eventTime, FORMAT), userId, orderId))
            line_count += 1
    for shopId, values in dict.items():
        outputUsers = {}
        for i in range(0, len(values)):
            duration = 0
            dict1 = {}
            for j in range(i, len(values)):
                duration = duration + (values[j][0] - values[i][0]).total_seconds()
                userId = values[j][1]
                if not userId in dict1:
                    dict1[userId] = 0
                dict1[userId] = dict1[userId] + 1
                if duration <= LIMIT_DURATION:
                    numberOfUser = len(dict1)
                    numberOfOrder = 0
                    for key, value in dict1.items():
                        numberOfOrder += value
                    if numberOfUser == 0:
                        isAppend = True
                        continue
                    if numberOfOrder / numberOfUser >= 3:
                        sorted_dict = sorted(dict1.items(), key=operator.itemgetter(1))
                        sorted_dict.reverse()
                        max = sorted_dict[0][1]
                        for user in sorted_dict:
                            if user[1] == max:
                                if not user[0] in outputUsers or outputUsers[user[0]] < user[1]:
                                    outputUsers[user[0]] = user[1]
                            else:
                                break
        if len(outputUsers) == 0:
            result[shopId] = 0
        else:
            sorted_dict = sorted(outputUsers.items(), key=operator.itemgetter(1))
            sorted_dict.reverse()
            s = ""
            i = -1
            for u in sorted_dict:
                i = i + 1
                if i > 0:
                    s = s + "&"
                s = s + u[0]
            result[shopId] = s
    with open('output1.csv', mode='w') as output_file:
        writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['ShopId', 'UserId'])
        for key, value in result.items():
            writer.writerow([key, value])
    print(f'Processed {line_count} lines.')
