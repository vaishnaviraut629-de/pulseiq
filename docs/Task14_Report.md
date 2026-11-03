# Task 14: AI Signals Dashboard - Final Report

## 1. Project Overview
In this task I built an AI Signals Dashboard in Streamlit. The goal was to show where company is losing money due to attendance anomalies, how good our forecast is, and which employees have high attrition risk.

File: `pages/14_AI_Signals.py`

## 2. What I Built (4 Charts)

1.  **Anomalies by Money at Risk:** I calculated how much money is at risk for each anomaly type (like NO_ATTENDANCE, SHORT_SHIFT). This helps HR to focus on biggest loss first.

2.  **Forecast vs Actual with 80% Confidence Band:** I plotted actual hours vs forecasted hours. I also added a light band which shows 80% confidence interval. If actual line is inside band, forecast is good.

3.  **Forecast Error Table:** This table shows forecast error % for last months and reason for error (like festival, low data).

4.  **Attrition Risk Top 10:** I listed top 10 employees who have highest chance to leave job, based on AI model. This is only a signal, not final.

All charts have caption "AI-generated, for human review" as per guidelines.

## 3. Think Yourself - Questions and Answers

**Q1. Forecast error was 12% last month. Is that good? What would you need to know?**

Ans: Honestly 12% error is decent for starting, but I would not say it is good yet.

Because whether 12% is good depends on many things. If last month had many holidays like Diwali or if many people took sick leave together, then forecast going wrong by 12% is understandable. But if it was a normal working month, then 12% is on higher side, ideally we want below 8%.

To judge properly I need to know - first, which month we are talking about and was there any seasonal effect. Second, what was our average error in last 3-4 months, are we improving or not. Third, what is the actual money impact of that 12%, if it is 10k then fine but if it is 1 lakh then it is serious. So without knowing context I can't directly say good or bad.

**Q2. Which anomaly type is costing most and what action will you take?**

Ans: NO_ATTENDANCE is costing most, around 190k. Action would be to check why so many NO_ATTENDANCE cases are happening, is it fake attendance or system issue. I will talk to shift manager and verify.

**Q3. What does wide confidence band mean?**

Ans: Wide band means model is not confident. It happens when past data is less or when month has many leaves. In that case we should not fully trust AI and take human decision.

## 4. My Learnings

- AI is only for giving signal, final decision should be human.
- Money at Risk helps to prioritize problems.
- Labeling AI output is very important to avoid blind trust.
- Seasonal data affects forecast a lot.

## 5. Evidence Screenshots (in docs/screenshots/)

- Task14_1_Anomaly_MoneyAtRisk.png
- Task14_2_Forecast_ConfidenceBand.png
- Task14_3_Forecast_Error_Table.png
- Task14_4_Attrition_Risk.png

