# Clustering LinkedIn Job Listings

## Overview
The goal of this project is to use the [LinkedIn Data Analyst jobs listings](https://www.kaggle.com/datasets/cedricaubin/linkedin-data-analyst-jobs-listings/data) by [Cedric Aubin](https://www.kaggle.com/cedricaubin) to cluster and analyize descrptions for job listings in the US and Canada.

This project used a central shell script, manager.sh, to preform the data science workflow for this project. 

### Project Contents

1. **Formating Dataset**: download the US and Canada dataset and add a job ID Column.
2. **Derive Word Set from Data**: Comb through the descriptions and aggregate all the words used.
3. **Trim Word Set**: Take the raw word set and cut out unnecessary words (lemmatization and stop-word removal).
4. **Vectorize Dataset**: Convert the job descriptions into vectors where each value represents the relative frequency of a word from the word set in the job description.
5. **Cluster Data:** run the K-means algorithm using the vectorized dataset.
6. **Visualize Data:** ...

## 1. Format dataset

Take the target [.csv] data-table as, assign a Job Id to each job listing, and output a new [.csv] dataset with a new "Job ID" column.

> $ ./manager.sh format -s [source file] -o [output file]

### -s (required)

Specifies the source file. **Must be a .csv file.**


### -o (optional)

Specifies the output file. **Must be a .csv file.** If no output file name is given, the output file will be have the same name as the input file with "formatted" appended to it.

#### Examples

```
# creates new formatted dataset named "formatteddata.csv"
> $ ./manager.sh format -s data.csv
```

```
# creates new formatted dataset named "output.csv"
> $ ./manager.sh format -s data.csv -o output.csv
```

## 2. Derive Word Set from Data

Takes the [.csv] dataset (with or without the Job ID Column), combines all the words into a set of all the words used. Returns a .txt file, separated by newline characters.

> $ ./manager.sh wordset -s [source file] -o [output file]

### -s (required)

Specifies the source file. **Must be a .csv file.**

### -o (required)

Specifies the output file. **Must be a .csv file.**

#### Examples

```
# creates new wordset named "output.txt" from source file "dataset.csv"
> $ ./manager.sh wordset -s dataset.csv -o output.txt
```

## 3. Trim Word Set

Takes the word set and trims the set using lemmatizaton and stopword removal

$ ./manager.sh trimwordset -s wordset.txt -o outputfile.txt-l -w

### -s (required)

Specifies the source file. **Must be a .txt file.**

### -o (optional)

Specicies the output file. **Must be a .txt file.** If there is no output file specified, the output file will have the same name as the source file but starting with "trimmed".

### -l (optional)

Trims the word set using lemmatization.

### -w (optional)

Trims the word set using stopword removal

**If you don't use any -l or -w flags, the wordset will not change**

#### Examples

```
# trims the word set using lemmatization and stopword removal
$ ./manager.sh trimwordset -s wordset.txt -l -w
```

```
# trims the word set omly using stopword removal and outputs to "trimmedwordset.txt"
$ ./manager.sh trimwordset -s wordset.txt -o trimmedwordset.txt -w
```

```
# trims the word set only using lemmatization and outputs to "trimmedwordset.txt"
$ ./manager.sh trimwordset -s wordset.txt -o trimmedwordset.txt -l
``` 

```
# does not trim the word set but outputs to "trimmedwordset.txt"
$ ./manager.sh trimwordset -s wordset.txt -o trimmedwordset.txt
```
^ this is technically allowed but does nothing and will just copy the source file to the output file.

