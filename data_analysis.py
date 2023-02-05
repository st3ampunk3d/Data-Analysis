#Import required packages
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd

#Create a class to contain dataset and the functions that manipulate it.
class Data():
    def __init__(self):
        #Create a DataFrame from the csv file.
        self.data = pd.read_csv("dog_breeds.csv")
        self.data.dropna(inplace=True) #drop null values

        #Split the Height and Longevity columns so they are easier to use
        self.data.rename(columns={'Height (in)': 'Min Height', 'Longevity (yrs)': 'Min Years'}, inplace=True)
        self.data[['Min Height', 'Max Height']] = self.data['Min Height'].str.split('-', expand=True)
        self.data[['Min Years', 'Max Years']] = self.data['Min Years'].str.split('-', expand=True)

        #Splitting the columns adds the newly created columns to the end of the of the table.
        #Rearrange the columns into a more logical order.
        self.data = self.data[['Breed', 'Country of Origin', 'Fur Color', 'Color of Eyes', 'Min Height', 'Max Height', 'Min Years', 'Max Years', 'Character Traits', 'Common Health Problems']]


    def furColorStats(self):
        #Split the health problems into a usable dataFrame
        self.data['Fur Color'] = self.data['Fur Color'].str.lower()
        furColor = self.data['Fur Color'].str.get_dummies(sep=', ')

        #Determine what the most common and least comon color/colors are
        mostCommon = furColor.sum().idxmax()
        leastCommon = furColor.sum().idxmin()

        #Print the results to the console.
        print(f'The most common color for a dog to be is {mostCommon}')
        print(f'The least common color for a dog to be is {leastCommon}')

    def longevityStats(self):
        #Convert the values for min and max years to type int so they can be compared as numeric values
        self.data['Min Years'] = pd.to_numeric(self.data['Min Years'])
        self.data['Max Years'] = pd.to_numeric(self.data['Max Years'])

        #Determine what the smallest and largest breeds are
        shortest = self.data.iloc[self.data['Min Years'].idxmin()]
        longest = self.data.iloc[self.data['Max Years'].idxmax()]

        #Print the results to the console.
        print(f"The shortest living breed is the {shortest['Breed']} which only lives as few as {shortest['Min Years']} years.")
        print(f"The longest living breed is the {longest['Breed']} which can can live as many as {longest['Max Years']} years.")

    def sizeStats(self):
        #Convert the values for min and max height to type int so they can be compared as numeric values
        self.data['Min Height'] = pd.to_numeric(self.data['Min Height'])
        self.data['Max Height'] = pd.to_numeric(self.data['Max Height'])

        #Determine what the smallest and largest breeds are
        smallest = self.data.iloc[self.data['Min Height'].idxmin()]
        largest = self.data.iloc[self.data['Max Height'].idxmax()]

        #Print the results to the console.
        print(f"The smallest breed is the {smallest['Breed']} which can be as short as {smallest['Min Height']} inches.")
        print(f"The largest breed is the {largest['Breed']} which can be as tall as {largest['Max Height']} inches.")


    def healthIssueStats(self):
        #Split the health problems into a usable dataFrame
        self.data['Common Health Problems'] = self.data['Common Health Problems'].str.lower()
        self.health = self.data['Common Health Problems'].str.get_dummies(sep=', ')

        #There are too many health issue categories to reasonably display them all.
        #This will combine health issues that affect fewer than 10 total breeds into a single "Other" column
        other = []
        MainCategories = []
        for col in self.health.columns:
            if self.health[col].sum() < 10:
                other.append(col)
            else:
                MainCategories.append(col)

        self.health['other'] = self.health[other].sum(axis=1)
        MainCategories.append('other')

        #Sort the values in descending order and plot them as a pie chart.
        plot = self.health[MainCategories].sum().sort_values(ascending=False).plot.pie(y="Issue")
        print("See the graph popup for the answer to this question.\nClose the popup to continue.")
        plt.show()


    def breedTraitStats(self):
        #Split the traits column into a usable dataFrame.
        self.data['Character Traits'] = self.data['Character Traits'].str.lower()
        self.traits = self.data['Character Traits'].str.get_dummies(sep=', ')

        #Determine what the most and least common character traits are.
        traits = self.traits.sum().sort_values(ascending=False)
        mostCommon  = str(traits[[0]]).split(' ')[0]
        leastCommon = str(traits[[-1]]).split(' ')[0]

        #Print the results to the console.
        print(f'Of the traits listed in the dataset:\n'
              f'\t{mostCommon} is the most common, describing {traits[0]} breeds.\n'
              f'\t{leastCommon} is the least common, describing {traits[-1]} breed(s).\n')


    def breedOriginStats(self):
        #Determine which country is the origin of the most breeds
        breedOrigins = self.data.groupby(['Country of Origin']).count().sort_values(by=['Breed'], ascending=True)

        #Display the results as a bar graph
        plt.style.use('Solarize_Light2')
        plot = breedOrigins.plot.barh(y=0) #y=0 means that data[0] (breeds) will be the label for the y axis.
        print("See the graph popup for the answer to this question.\nClose the popup to continue.")
        plt.show()


def main():
    dataset = Data()
    running = True

    print("DOG BREED DATA ANALYSIS\n"
          "-----------------------\n\n")

    #Run the main program in the loop so the user has the opportunity to ask multiple questions.
    while running:
        option = int(input("What would you like to know?\n\n"
                           "\t1. What is the least common color of fur?\n"
                           "\t2. Which breed lives the longest?\n"
                           "\t3. Which breed is the smallest?\n"
                           "\t4. What is the most common health issue?\n"
                           "\t5. What is the most common character trait?\n"
                           "\t6. Where did the most Breeds originate?\n"
                           "\t7. Exit\n\n"
                           "Enter the number corrosponding to your question: "))

        #If the user chooses "Exit" as the option or if the value entered is out of range, exit the program.
        if option >= 7 or option == 0:
            running = False
        
        #If a valid option was entered, pass the option and the dataset to the Display function.
        else:
            display(option, dataset)

    #Say goodby and close the program when the loop ends.
    print("\nThe program will close now. Thank you.")
        

def display(option, dataset):
    #Create a list of the functions that will answer the questions. This will save several lines of code because we can pass in an index value instead of 
    #coparing values with several if/else statements
    answers = [dataset.furColorStats, dataset.longevityStats, dataset.sizeStats, dataset.healthIssueStats, dataset.breedTraitStats, dataset.breedOriginStats]


    print("\n")
    #Call the appropriate function to answer the question.
    answers[option-1]()
    print("\n")

    #Pause to let the user read the answer before continuing the program.
    input("Press any key to continue")
    return

#run the main program.
if __name__ == "__main__":
    main()