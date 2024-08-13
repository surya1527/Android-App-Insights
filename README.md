# Android-App-Insights

## Table of Contents

- [Clone the Repository](#clone-the-repository)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [sample_source_data_file](#sample_source_data_file)



## Clone the Repository

To get started with the project, you'll need to clone the repository to your local machine. Follow these steps:

1. Open a terminal window.

2. Use the following command to clone the repository:

   ```bash
   git clone https://github.com/surya1527/Android-App-Insights.git

## getting-started
## prerequisites
Before you begin, make sure you have the following prerequisites installed:<br>

<a href="https://www.python.org/downloads/" target="_blank" rel="noopener">Python 3</a> <br>
<a href="https://spark.apache.org/docs/latest/api/python/getting_started/install.html" target="_blank" rel="noopener">Apache Spark</a>


## installation
Make sure to download and install the appropriate version of Python 3 for your operating system. For PySpark, follow the instructions on the official Apache Spark website to download and set up PySpark.

## sample_source_data_file
Here is the sample data of some of the android apps from playstore.<br>
Access the file from here 
<a href="https://drive.google.com/file/d/1-E6z2zlDT8OOI4MLBNUxwkdMRzccsTZe/view?usp=sharing" target="_blank" rel="noopener">playsore.csv</a>

# About code:
**This code provide count of apps based on various combination of fields that we provide**

After following all the above steps:
1. Navigate to the project directory `cd Android-App-Insights`
2. Run python script.
  - Enter the source file path to run the function (Here the source file path is the parameter to run the function source_file_info)<br>

Now it runs a function **source_file_info** from class **FileInsighs**<br>
This funtions returns the high level information of the source file such as:<br>
   - All numeric columns.
   - The source file as a dataframe.
   - The columns of the source file.
   - Number of records in source file.<br>

**Note: I am printing only columns of the source file to pick the combinations as we like. For more information please use the respected print statements for data you would like to see.**<br>

  - Now it asks us to enter the field names that should be used in combinations.<br> 
    - Pick the field names you want to combine from the print statement above<br>
    - Note: Please make sure to enter the field names in the format specified below<br>
    - Example: column1,column2,column3,column4,column5,.....<br>
  - Now it asks to enter the binning range value (This will be the integer value eg: 5)<br>
  - And finally it asks to enter your output csv file path followed by filename. <br>

Finally it prints the list of columns used for combinations and shows the output csv file path location.
