# **Subject:** Insights for Fetch Rewards Analytics  

Hi [Stakeholder],  

I'm Evan, and I've been working through the Fetch Rewards analytics data for your request. During my review I’ve identified a few areas that need clarification and potential optimization. Below are my observations and some questions to ensure we’re working with accurate and scalable data.  

## **Questions About the Data**  
- Can you confirm whether `"FINISHED"` in `rewardsReceiptStatus` is equivalent to `"ACCEPTED"` for transaction completion?  
- Will we be adding more recent datasets for our analysis? This would help with understanding users in the current year (e.g. users over the last 6 months or month over month).
- Should we be filtering receipts based on additional criteria to remove test data or incomplete transactions?  

## **Data Quality Issues Identified**  
- There are many data inconsistencies, which required conversations to understand the data more thoroughly:
  - Across all datasets, data type inconsistencies (such as object-stored IDs and string-formatted dates) required conversion for accurate analysis and efficient queries.
  - I found duplicates such as repeated user entries and duplicate receipts which required deduplication to ensure data accuracy and reliable analysis.
  - There were multiple null/missing values in key fields like dates, user state, receipt user ids, item numbers, brand codes etc. which required handling to maintain data integrity and accurate reporting.
  - The dataset does not contain data for the current year, so querying for recent months won't apply.   
  - User specific issues
    - I found potential abuse in the user data, with many duplicated users sharing the same last login, as well as multiple users from the same state, source, and even identical IDs.
    - There were also users that had "bulk" sign-ups or were created at the same time indicating some level of abuse.
  - Receipt issues
    - I found receipts with points earned over 5000 and total spent over 1000. Is that normal?
    - I also found users in the receipts dataset that are not on the user dataset which is a data integrity issue.
    - I found receipt purchases that occurred after the data scanned which shouldn't occur.
    - I found duplicate receipts submitted by the same user indicating abuse.
  - Receipt Item Issues
    - There are many receipt item duplicates which could indicate either data ingestion errors, user resubmissions, or possible bugs.
  - Brand Issues
    - Some issues include missing category codes and brand codes which may be issues with data entry or ingestion.

## **What’s Needed to Resolve These Issues?**  
- We should investigate/audit how data entry and ingestion occurs. This could help with data integrity such as nulls and duplications.
- Also, we should standardize data points with a correct mapping of data types so that data is consistent across DB tables.
- Do we have data logging? Reviewing these logs can help with catching data integrity issues like duplications and possible abuse.
- We should also apply **data validation rules** before loading into our analytics pipeline. 

## **Additional Information for Optimization**  
- A **data freshness policy**: How often is this data updated, and should we expect rolling updates?  
- Any business rules for handling incomplete data points? (e.g. logging as mentioned above)

## **Performance & Scaling Considerations**  
- As the dataset grows, queries filtering large date ranges (e.g., rolling 6 months) **may slow down**—would indexing key date fields (such as `date_scanned` etc.) be an option?  
- Ensuring **data is partitioned** efficiently to optimize large-scale aggregation queries.
- Are we currently utilizing stream processing? This could help us understand data in real-time and find issues before data integrity is compromised.

Let me know how you’d like to proceed on these points. Happy to adjust the pipeline based on business needs.  

Regards,  
Evan Rosa 
