# Static Analysis Report - AutoCull 19/09/2025


## Overview
This report will detail issues that have been picked up by static analysis tools Pylint & Flake8 in order to assess objective code quality and locate potential flaws present in the application source code. 

---

## High Severity Issues
- **Undefined / Incorrect Attributes**  
  - Has potential to cause runtime issues
  - Could be false positive as it hasnt caused any issues so far - suppress warning
- **Accessing Attributes Before Initilisation**  
  - Will likely cause runtime issues
  - Should absolutly be fixed
  - Likely not yet picked up as an issue due to inadequate testing
- **Undefined / Incorrect Attribures**  
  - Has potential to cause runtime issues

---

## Medium Severity Issues
- **Classes / Functions too big**  
  - No runtime issues
  - Likely adds difficulty to maintainability & readability
- **Missing Documentation**  
  - No runtime issues
  - Likely adds difficulty to maintainability & readability
- **Overly Broad Exception Handling**  
  - Can cause runtime issues
  - Makes debugging difficult - real errors could be hidden

---

## Low Severity Issues
- **Code Style Violation**  
  - No runtime issues
  - Likely adds difficulty to maintainability & readability
- **Unused Imports/Variables**  
  - No runtime issues
  - Likely adds difficulty to maintainability
  - Adds bloat to code

---

## Conclusions
The majority of issues picked up by the static analysis tools that we have used are minor. Often things which can be fixed automatically with the help of other tools. However, there are a small number of issues which are urgent and require immediate action from the team. 

The team will run tools such as black, isort, and autoflake to ensure that minor issues are dealt with in a timely manner. Group 11 will also spend some time looking into PEP 8, a style guide for Python code, to ensure that any code written from then on is as close to being compliant as possible, reducing the need to revisit old code.

From this exercise, the team can conclude that the regular analysis of code is key to ensuring that new code written is consistently of an acceptable standard, and that old code does not regress. The team will also look into creating configuration files to ensure that the static analysis only shows issues which we are looking for. 

