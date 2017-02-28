import csv
from nltk.stem.wordnet import WordNetLemmatizer

lmtzr = WordNetLemmatizer()
def stem_and_write_to_file(stemmed_file, original_file):
    p = nltk.PorterStemmer()
    fieldnames = ["Recipe ID", "Name", "Amount", "Unit"]
    with open(stemmed_file,'w') as d:
        writer = csv.DictWriter(d, fieldnames=fieldnames)
        with open(original_file, 'r') as f:
            reader = csv.DictReader(f, fieldnames=fieldnames)
            for row in reader:

                stemmed_ingredient = p.stem(row['Name'].lower())
                print(stemmed_ingredient)
                # split_line = line.split(',') #break it up so we can get access to the word
                # stemmed_ingredient = p.stem(split_line[1])
                # print(stemmed_ingredient)
                # d.write(new_line)

def main():
    stem_and_write_to_file('stemmed_ingredients_to_recipes.csv', 'ingredents_to_recipes_and_quantities.csv')



if __name__ == '__main__':
    main()

