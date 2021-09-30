def read_data(filename):
    data = []
    with open(filename,'r') as f:
        for line in f.readlines():
            data.append(line.split(','))
    del data[0]
        

def add_weighted_average(data, weight):
    for row in data:
        row.append(0)   # TODO

def analyze_data(data):
    mean = 0            # TODO
    var = 0             # TODO
    median = 0          # TODO
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
        
        
        
data=[]     
with open("data/class_score_en.csv", 'r') as f:
    for line in f.readlines():
        data.append(int(line.strip().split(',')))
    

data[0:1]=[]
del a[0]

data[0][0]
parseInt(data[0])
 
a='hi \n'
print(a.strip())     
        
        
        
        
        
        
        
        
f=open("data/class_score_en.csv",'r')
while True:
    line=f.readline()
    if not line: break
    print(line)
f.close()        
        
        
        
        
        