# Day 1 - Think Question

Question: What if new unexpected column comes in source data?

My Answer:
According to me we should not stop the pipeline. If we stop pipeline for one column then daily load will fail.

Better approach is to give a warning like "new column found" and ignore that column for now.

Raw data should be kept as it is, but for processing we can ignore extra columns. Later if needed we can add it to contract.

So my solution is WARN + IGNORE, not FAIL.

- vaishnavi