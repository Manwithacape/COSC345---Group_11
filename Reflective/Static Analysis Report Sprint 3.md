# Static Analysis Report - AutoCull 08/10/2025

## Overview

This report will detail issues that have been picked up by static analysis tools Pylint & Flake8 in order to assess objective code quality and locate potential flaws present in the application source code at the conclusion of sprint 3.

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

## Conclusions

While many of the same issues picked up in the last sprint are still present, many chnages have been made in the code to improve readability, with many unused import removed also.

This has greatly improved the number of low severity issues present in the team's code.

Still to be worked on by the team is better commenting/documentation to improve the onbaording experience for other developers potentially joining the development effort.

Overall, the score given to the entire code directory by Pylint has dropped in the last sprint. This is due to the fact that large amounts of new code has been merged in. This should be addressed within the coming sprint. It should be noted that many of the files that were present in the previous sprint have been improved upon and now score higher. 