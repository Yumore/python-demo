# Sample CSV files

This repository contains sample [Comma Separated Value (CSV)](https://www.datablist.com/learn/csv/csv-meaning) files. CSV is a generic flat file format used to store structured data. Datasets are split in 3 categories: Customers, Users and Organizations. For each, sample CSV files range from 100 to
2 millions records. Those CSV files can be used for testing purpose. They can be open by any application compatible with CSV files or with a [CSV editor](https://www.datablist.com/csv-editor).

The datasets are generated using random values. Mosly using Python [Faker](https://faker.readthedocs.io/en/master/) package.

## Customers CSV Sample

- [customers-100.csv](https://github.com/datablist/sample-csv-files/raw/main/files/customers/customers-100.csv) - [Zip version](https://github.com/datablist/sample-csv-files/raw/main/files/customers/customers-100.zip) - Customers CSV with 100 records
- [customers-1000.csv](https://github.com/datablist/sample-csv-files/raw/main/files/customers/customers-1000.csv) - [Zip version](https://github.com/datablist/sample-csv-files/raw/main/files/customers/customers-1000.zip) - Customers CSV with 1000 records
- [customers-10000.csv](https://github.com/datablist/sample-csv-files/raw/main/files/customers/customers-10000.csv) - [Zip version](https://github.com/datablist/sample-csv-files/raw/main/files/customers/customers-10000.zip) - Customers CSV with 10000 records
- [customers-100000.csv](https://github.com/datablist/sample-csv-files/raw/main/files/customers/customers-100000.csv) - [Zip version](https://github.com/datablist/sample-csv-files/raw/main/files/customers/customers-100000.zip) - Customers CSV with 100000 records
- [customers-500000.csv](https://github.com/datablist/sample-csv-files/raw/main/files/customers/customers-500000.zip) - Customers CSV with 500000 records
- [customers-1000000.csv](https://github.com/datablist/sample-csv-files/raw/main/files/customers/customers-1000000.zip) - Customers CSV with 1000000 records
- [customers-2000000.csv](https://github.com/datablist/sample-csv-files/raw/main/files/customers/customers-2000000.zip) - Customers CSV with 2000000 records

### Customer Schema

- Index
- Customer Id
- First Name
- Last Name
- Company
- City
- Country
- Phone 1
- Phone 2
- Email
- Subscription Date
- Website

## People CSV Samples

- [people-100.csv](https://github.com/datablist/sample-csv-files/raw/main/files/people/people-100.csv) - [Zip version](https://github.com/datablist/sample-csv-files/raw/main/files/people/people-100.zip) - People CSV with 100 records
- [people-1000.csv](https://github.com/datablist/sample-csv-files/raw/main/files/people/people-1000.csv) - [Zip version](https://github.com/datablist/sample-csv-files/raw/main/files/people/people-1000.zip) - People CSV with 1000 records
- [people-10000.csv](https://github.com/datablist/sample-csv-files/raw/main/files/people/people-10000.csv) - [Zip version](https://github.com/datablist/sample-csv-files/raw/main/files/people/people-10000.zip) - People CSV with 10000 records
- [people-100000.csv](https://github.com/datablist/sample-csv-files/raw/main/files/people/people-100000.csv) - [Zip version](https://github.com/datablist/sample-csv-files/raw/main/files/people/people-100000.zip) - People CSV with 100000 records
- [people-500000.csv](https://github.com/datablist/sample-csv-files/raw/main/files/people/people-500000.zip) - People CSV with 500000 records
- [people-1000000.csv](https://github.com/datablist/sample-csv-files/raw/main/files/people/people-1000000.zip) - People CSV with 1000000 records
- [people-2000000.csv](https://github.com/datablist/sample-csv-files/raw/main/files/people/people-2000000.zip) - People CSV with 2000000 records

### People Schema

- Index
- User Id
- First Name
- Last Name
- Sex
- Email
- Phone
- Date of birth
- Job Title

## Organizations CSV Samples

- [organizations-100.csv](https://github.com/datablist/sample-csv-files/raw/main/files/organizations/organizations-100.csv) - [Zip version](https://github.com/datablist/sample-csv-files/raw/main/files/organizations/organizations-100.zip) - Organizations CSV with 100 records
- [organizations-1000.csv](https://github.com/datablist/sample-csv-files/raw/main/files/organizations/organizations-1000.csv) - [Zip version](https://github.com/datablist/sample-csv-files/raw/main/files/organizations/organizations-1000.zip) - Organizations CSV with 1000 records
- [organizations-10000.csv](https://github.com/datablist/sample-csv-files/raw/main/files/organizations/organizations-10000.csv) - [Zip version](https://github.com/datablist/sample-csv-files/raw/main/files/organizations/organizations-10000.zip) - Organizations CSV with 10000 records
- [organizations-100000.csv](https://github.com/datablist/sample-csv-files/raw/main/files/organizations/organizations-100000.csv) - [Zip version](https://github.com/datablist/sample-csv-files/raw/main/files/organizations/organizations-100000.zip) - Organizations CSV with 100000 records
- [organizations-500000.csv](https://github.com/datablist/sample-csv-files/raw/main/files/organizations/organizations-500000.zip) - Organizations CSV with 500000 records
- [organizations-1000000.csv](https://github.com/datablist/sample-csv-files/raw/main/files/organizations/organizations-1000000.zip) - Organizations CSV with 1000000 records
- [organizations-2000000.csv](https://github.com/datablist/sample-csv-files/raw/main/files/organizations/organizations-2000000.zip) - Organizations CSV with 2000000 records

### Organization Schema

- Index
- Organization Id
- Name
- Website
- Country
- Description
- Founded
- Industry
- Number of employees

## Local Set up to generate files

#### Python Environments

Create a Python virtual env:

```
python3 -m venv venv/sample-csv
```

Activate it

```
source venv/sample-csv/bin/activate
```

So you can install dependencies:

```
pip install -r requirements.txt
```

#### Run script

```
python src/main.py
```
