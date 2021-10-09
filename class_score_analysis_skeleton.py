def read_data(filename):
    data = []
    with open(filename,'r') as f:
        for line in f.readlines():
            if not line.startswith('#'):
                values=[]
                for text in line.split(','):
                    values.append(int(text))
                data.append(values)
    return data
        

def add_weighted_average(data, weight):
    for row in data:
        total=weight[0]*row[0]+weight[1]*row[1]
        row.append(total)   # TODO
        
      
def analyze_data(data):
    mean = sum(data)/len(data)          # TODO
    var = sum([(data[i]-mean)**2  for i in range(len(data))])/len(data)             # TODO
    median =  sorted(data)[int((len(data)+1)/2 - 1)]         # TODO
    return mean, var, median, min(data), max(data)

if __name__ == '__main__':
    data = read_data('data/class_score_en.csv')
    if data and len(data[0]) == 2:
        add_weighted_average(data, [40/125, 60/100])
        if len(data[0]) == 3:
            print('### Individual Score')
            print()
            print('| Midterm | Final | Total |')
            print('| ------- | ----- | ----- |')
            for row in data:
                print(f'| {row[0]} | {row[1]} | {row[2]:.3f} |')
            print()

            print('### Examination Analysis')
            col_n = len(data[0])
            col_name = ['Midterm', 'Final', 'Total']
            colwise_data = [ [row[c] for row in data] for c in range(col_n) ]
            for c, score in enumerate(colwise_data):
                mean, var, median, min_, max_ = analyze_data(score)
                print(f'* {col_name[c]}')
                print(f'  * Mean: **{mean:.3f}**')
                print(f'  * Variance: {var:.3f}')
                print(f'  * Median: **{median:.3f}**')
                print(f'  * Min/Max: ({min_:.3f}, {max_:.3f})')
        



        