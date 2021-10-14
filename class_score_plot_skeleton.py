import glob, csv
import matplotlib.pyplot as plt

def read_data(filename):
    files = glob.glob(filename)
    all_data = []
    for file in files:
        with open(file, 'r') as f:     # Construct a file object
            csv_reader = csv.reader(f) # Construct a CSV reader object
            data = []
            for line in csv_reader:
                if line and not line[0].strip().startswith('#'): # If 'line' is valid and not a header
                    data.append([int(val) for val in line])      # Append 'line' to 'data' as numbers
            all_data = all_data + data                           # Merge 'data' to 'all_data'
    return all_data

if __name__ == '__main__':
    # Load score data
    class_kr = read_data('data/class_score_kr.csv')
    class_en = read_data('data/class_score_en.csv')

    # Derive miterm, final, and total scores
    midtm_kr = [row[0] for row in class_kr]
    final_kr = [row[1] for row in class_kr]
    total_kr = [row[0]*40/125+row[1]*60/100 for row in class_kr]
    midtm_en = [row[0] for row in class_en]
    final_en = [row[1] for row in class_en]
    total_en = [row[0]*40/125+row[1]*60/100 for row in class_en]

    
    # Plot midterm/final scores as points
    plt.figure()
    plt.plot(midtm_kr,final_kr,'ro',label="Korean")
    plt.plot(midtm_en,final_en,'b+',label="English")
    plt.xlabel('Midterm Scores')
    plt.ylabel('Final Scores')
    plt.legend()
    plt.grid()
    plt.show()
    
    # Plot total scores as a histogram
    plt.figure()
    plt.hist(total_kr,bins=20, range=(0,100), color='r',label='Korean')
    plt.hist(total_en,bins=20, range=(0,100), color='b', alpha=0.3,label='English')
    plt.xlabel('Total scores')
    plt.ylabel('The number of students')
    plt.legend()
    plt.show()
    
    #plot total scores of kr/en class as boxplot
    plt.figure()
    plt.boxplot([total_kr,total_en],labels=['Korean','English'],showmeans=True)
    plt.ylabel('Total Scores')
    plt.title("korea vs english class in Total score")
    plt.show()
    
    
    
    