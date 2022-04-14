# PII Scan

This application will scan down the directory tree, from which it is launched, an look for Personally Identifiable Information (PII) in specific file types. 
A report will be generated with a list of file paths and the type of data which was matched. This tool is not meant as a full replacement for file analysis, 
but as a method to quickly identify a subset of files that could be set aside for further analysis. The file types scanned are:
- Word (.docx)
- Portable Document Format (.pdf)
- Plain Text (.txt)
- Excel (.xls and .xlsx)
- Comma separated value (.csv)

This application uses Regular Expression patterns to look for the following PII:
- Social Security Number (xxx-xx-xxxx)
- Employee ID Number (10-digit number)
- Bank Account Numbers (12-digit or 17-digit)
- Credit Card Numbers (16-digit or 17-digit)
- email Addresses
- Federal Tax ID (xx-xxxxxxx)
- Washington Drivers License
- Gender
- Race
- Family Status
- Employment Status