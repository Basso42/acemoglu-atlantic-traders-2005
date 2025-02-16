# The Rise of Europe: Reproduction of Acemoglu, Johnson, and Robinson (2005)

This repository provides a Python-based replication of the results from:

**"The Rise of Europe: Atlantic Trade, Institutional Change, and Economic Growth"**  
Daron Acemoglu, Simon Johnson, and James Robinson  
*American Economic Review, Vol. 95, No. 3, June 2005, pp. 546–579.*  

## Overview

This project aims to reproduce the tables and figures from the paper in python.

## Repository Structure

```
📂 acemoglu-atlantic-traders-2005
│-- 📄 README.md         # Project description and instructions
│-- 📄 requirements.txt  # List of dependencies
│-- 📂 data/             # Folder containing datasets (included in the repo)
│-- 📂 src/              # Python scripts for data processing and analysis
```

## Data Sources

The dataset includes:
- Historical GDP and population data
- Measures of institutional quality (e.g., constraints on the executive from the Polity IV dataset)
- Data on Atlantic trade (imports, exports, slave trade involvement)

## Installation

To set up the project, first clone the repository:

```sh
$ git clone https://github.com/Basso42/acemoglu-atlantic-traders-2005.git
$ cd acemoglu-atlantic-traders-2005
```

Create a virtual environment and install dependencies:

```sh
$ python -m venv venv
$ source venv/bin/activate  # On Windows use `venv\Scripts\activate`
$ pip install -r requirements.txt
```

## Dependencies

This project requires the following Python libraries:

- `pandas`
- `statsmodels`
- `matplotlib`

All dependencies can be installed via:
```sh
$ pip install -r requirements.txt
```

## References

- Acemoglu, D., Johnson, S., & Robinson, J. (2005). *The Rise of Europe: Atlantic Trade, Institutional Change, and Economic Growth*. American Economic Review, 95(3), 546-579.
- Original replication materials: [AER website](https://www.aeaweb.org/articles?id=10.1257/0002828054201305)


