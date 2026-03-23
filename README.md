# Clustering LinkedIn Job Listings

### Presenation Link:

https://docs.google.com/presentation/d/1TENSPCRmeyJR4EoO5cJjCyton3bUAcBwhlcu5R85FEw/edit?usp=sharing

## Overview
The goal of this project is to use the [LinkedIn Job Postings (2023-2024)](https://www.kaggle.com/datasets/arshkon/linkedin-job-postings?select=postings.csv) dataset to cluster and analyze descriptions for job listings.

This project used a central shell script, manager.sh, to preform the data science workflow for this project. 

### Project Contents

1. **Formating Dataset**: take the postings dataset and add a sequential job ID column.
2. **Derive Word Set from Data**: Comb through the descriptions and aggregate all the words used.
3. **Trim Word Set**: Take the raw word set and cut out unnecessary words (lemmatization and stop-word removal).
4. **Vectorize Dataset**: Convert the job descriptions into vectors where each value represents the relative frequency of a word from the word set in the job description.
5. **Cluster Data:** run the K-means algorithm using the vectorized dataset.
6. **Inspect Clusters:** print sample job descriptions from each cluster for a given k value.

## 1. Format dataset

Take the target [.csv] data-table as, assign a Job Id to each job listing, and output a new [.csv] dataset with a new "job_id" column.

> $ ./manager.sh format -s [source file] -o [output file]

or 

> $ ./manager.sh format --help

### -s (required)

Specifies the source file. **Must be a .csv file.**


### -o (optional)

Specifies the output file. **Must be a .csv file.** If no output file name is given, the output file will be have the same name as the input file with "formatted" appended to it.

### --help (optional)

Prints out the instructions for how to use the format command.

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

Takes the [.csv] dataset (with or without the job_id column), combines all the words into a set of all the words used. Returns a .txt file, separated by newline characters.

> $ ./manager.sh wordset -s [source file] -o [output file]

or 

> $ ./manager.sh wordset --help

### -s (required)

Specifies the source file. **Must be a .csv file.**

### -o (required)

Specifies the output file. **Must be a .txt file.**

### --help (optional)

Prints out the instructions for how to use the wordset command.

#### Examples

```
# creates new wordset named "output.txt" from source file "dataset.csv"
> $ ./manager.sh wordset -s dataset.csv -o output.txt
```

## 3. Trim Word Set

Takes the word set and trims the set using lemmatizaton and stopword removal

$ ./manager.sh trimwordset -s [wordset] -o [output file] -l -w

or 

$ ./manager.sh trimwordset --help

### -s (required)

Specifies the source file. **Must be a .txt file.**

### -o (optional)

Specicies the output file. **Must be a .txt file.** If there is no output file specified, the output file will have the same name as the source file but starting with "trimmed".

### -l (optional)

Trims the word set using lemmatization.

### -w (optional)

Trims the word set using stopword removal

**If you don't use any -l or -w flags, the wordset will not change**

### --help (optional)

Prints out the instructions for how to use the trimwordset command.

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

## 4. Vectorize Dataset

Takes the dataset and the word set and vectorizes the dataset. Each job description is converted into a vector where each value represents the relative frequency of a word from the word set in the job description (fractional of total words in the description). The output is a .csv file where each row is a job listing and each column is a word from the word set.

> $ ./manager.sh vectorize -d [dataset file] -w [word set file] -o [output file]

or 

> $ ./manager.sh vectorize --help

### -d (required)

Specifies the dataset file. **Must be a .csv file.**

### -w (required)

Specifies the word set file. **Must be a .txt file.**

### -o (optional)

Specifies the output file. **Must be a .csv file.** If there is no output file specified, the output file will have the same name as the dataset file but starting with "vectorized".

### --help (optional)

Prints out the instructions for how to use the vectorize command.

#### Examples

```
# vectorizes the dataset "dataset.csv" using the word set "wordset.txt" and outputs to "vectorized_dataset.csv"
> $ ./manager.sh vectorize -d dataset.csv -w wordset.txt -o vectorized_dataset.csv
```

```
# vectorizes the dataset "dataset.csv" using the word set "wordset.txt" and outputs to "vectorizeddataset.csv"
> $ ./manager.sh vectorize -d dataset.csv -w wordset.txt
```

## 5. Cluster Data

Run K-mean algorithm using Scikit-learn on the vectorized dataset using multiple k values.The output is a .csv file where each row is a job listing and there is a new column for each k value with the cluster assignment for that k value. The program will constantly print out the average squared Euclidean distance for each k value to the terminal as it runs. It will preform K-means on k=1 until k equals the maximum value of k. Once the program finishes, the program will also spit out a graph of the average squared Euclidean distance for each k value to help determine the optimal k value, named the same as the output file but with a .png extension.

> $ ./manager.sh cluster -d [dataset file] -o [output file] -k [maximum number of clusters]

or 

> $ ./manager.sh cluster --help

### -d (required)

Specifies the dataset file. **Must be a .csv file.**

### -o (optional)

Specifies the output file. **Must be a .csv file.** If there is no output file specified, the output file will have the same name as the dataset file but starting with "clustered".

### -k (optional)

Specifies the maximum number of clusters to use in the K-means algorithm. If there is no value specified for -k, the default maximum number of clusters will be 10.

### --help (optional)

Prints out the instructions for how to use the cluster command.

#### Examples

```
# runs K-means on the dataset "dataset.csv" using k values from 5 to 10 and outputs to "clustered_dataset.csv"
> $ ./manager.sh cluster -d dataset.csv -o clustered_dataset.csv -k 5
```

```
# runs K-means on the dataset "dataset.csv" using k values from 5 to 10 and outputs to "clustereddataset.csv"
> $ ./manager.sh cluster -d dataset.csv -k 5
```

## 6. Inspect Clusters

Prints 10 sample job descriptions from each cluster for a given k value. Takes the clustered .csv file (output of the cluster command) and the original dataset .csv file, joins them on job_id, and displays descriptions grouped by cluster.

> $ ./manager.sh inspect -c [cluster file] -d [dataset file] -k [k value]

or 

> $ ./manager.sh inspect --help

### -c (required)

Specifies the clustered .csv file (output of the cluster command). **Must be a .csv file.**

### -d (required)

Specifies the original dataset .csv file. **Must be a .csv file.**

### -k (required)

Specifies the k value (number of clusters) to inspect.

### --help (optional)

Prints out the instructions for how to use the inspect command.

#### Examples

```
# prints 10 job descriptions from each cluster for k=5
> $ ./manager.sh inspect -c clustered-data/clustered.csv -d data/postings.csv -k 5
```

```
# prints 10 job descriptions from each cluster for k=10
> $ ./manager.sh inspect -c clustered-data/clustered.csv -d data/postings.csv -k 10
```


