I thought about attrition...

If 100 people are at start and 10 leave, end is 90.

If I divide by start: 10/100 = 10%
If I divide by end: 10/90 = 11.1%
If I divide by average (95): 10/95 = 10.5%

Number changes a lot. End method always shows higher %. If 50 people leave from 100, start method shows 50% but end method shows 100%. That is too much difference.

I will choose average. Because it is in middle and more fair. Start and end are just one day numbers, average is full month feeling. In real HR dashboards also they use average, I checked cube and dbt github, they also use average.

Also for small team like D00 where only 1 person is there, if that 1 leaves, it becomes 100% attrition which is wrong. So we hide it as <NA> with min group 5 rule. That is better.























