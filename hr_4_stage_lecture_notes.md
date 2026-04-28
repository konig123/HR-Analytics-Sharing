# 1-Hour Lecture Notes: Introducing the 4 Stages of Data Analysis in HR

## Audience
This session is designed for a mixed internal HR audience of around 30 people, including HRBPs, HR operations colleagues, and talent acquisition team members. The audience is expected to have beginner to middle-level familiarity with dashboards and data, so the tone should stay practical, simple, and business-focused.

## Session Goal
By the end of the session, participants should understand the 4 stages of data analysis and see how one HR business issue can be explored through four different levels of thinking: descriptive, diagnostic, predictive, and prescriptive. They should leave with a clearer understanding that analytics is not just about showing data, but about helping HR make better business decisions.

## Session Flow
### Total session length: 60 minutes

### 1. Welcome and framing (5 minutes)
- Introduce the session topic: the 4 stages of data analysis in HR
- Set expectations: this is not a technical analytics lesson, but a business thinking lesson using data
- Explain that the dashboard will be used as a teaching tool, not just as a reporting tool

### 2. What data analysis means in HR (8 minutes)
- Give a simple definition of HR analytics
- Explain why HR teams often collect data but do not always turn it into insight or action
- Introduce the idea that the 4 stages represent increasing depth and business value

### 3. Stage 1: Descriptive analytics (10 minutes)
- Open the Descriptive tab
- Show how descriptive analytics answers the question: "What is happening?"
- Use the workforce snapshot to explain how data can summarize the current situation

### 4. Stage 2: Diagnostic analytics (10 minutes)
- Open the Diagnostic tab
- Show how diagnostic analytics answers the question: "Why is it happening?"
- Use the charts to explain how relationships and patterns give more insight than summary metrics alone

### 5. Stage 3: Predictive analytics (10 minutes)
- Open the Predictive tab
- Show how predictive analytics answers the question: "What is likely to happen next?"
- Explain how scenario thinking helps HR anticipate future risk

### 6. Stage 4: Prescriptive analytics (10 minutes)
- Open the Prescriptive tab
- Show how prescriptive analytics answers the question: "What should we do about it?"
- Explain how this stage connects insight to business action, budget, and expected impact

### 7. Wrap-up and transfer to real HR work (7 minutes)
- Summarize the 4 stages again
- Explain how the same framework can be used for other HR topics
- End with practical takeaways for the audience's day-to-day work

## Opening: What Data Analysis Means in HR
### Suggested talking points
- When many HR colleagues hear the word "analytics," they immediately think of dashboards, reports, or complicated formulas.
- But in practice, data analysis in HR is much simpler to explain.
- It means using workforce data to understand a business problem, explain what is driving it, anticipate what may happen next, and support better decisions.
- In other words, data analysis is not only about numbers. It is about business understanding.
- A useful way to explain this is through four stages:
  - Descriptive: what is happening
  - Diagnostic: why it is happening
  - Predictive: what is likely to happen
  - Prescriptive: what should we do
- These four stages are not four separate worlds. They are four levels of thinking about the same HR problem.
- A strong HR analyst or HR business partner should know how to move up and down these stages depending on the question.

### Suggested speaker wording
"Today I do not want us to think about analytics as a technical subject. I want us to think about it as a way of solving business questions in HR. The dashboard we are looking at is useful because it lets us see the same HR issue through four different stages of analysis. Each stage answers a different type of question, and together they create a stronger business story."

## Stage 1: Descriptive Analytics
### Main message
Descriptive analytics tells us what is happening now. It organizes the facts and gives us a reliable picture of the current workforce situation.

### Dashboard tab to use
Use the `Descriptive` tab.

### Suggested talking points
- Start with the business question: are there concerns about pay competitiveness and retention risk?
- Before trying to explain anything, we first need to understand the current picture.
- This is where descriptive analytics helps.
- In this tab, we look at the current workforce snapshot: headcount, salary, turnover, tenure, representation, promotions, department mix, demographic composition, and salary distribution.
- At this stage, we are not yet explaining causes.
- We are simply answering: what do we see?
- This stage is important because if we misunderstand the current situation, all later analysis becomes weak.

### What to click or show
- Show the executive overview cards
- Show workforce flow
- Show department mix
- Show demographic composition
- Show salary distribution by department

### What to say
- "At this stage, I want the audience to notice what is happening, not why."
- "For example, we may see turnover is higher than expected, certain departments have different salary patterns, or representation varies across the workforce."
- "This is the foundation. If Stage 1 is unclear, the rest of the analysis will be shaky."

### Key point worth paying attention to
Do not rush to conclusions in Stage 1. The purpose here is to establish a shared understanding of the facts, not to jump into explanations or solutions.

## Stage 2: Diagnostic Analytics
### Main message
Diagnostic analytics helps us understand why the patterns in Stage 1 may be happening.

### Dashboard tab to use
Use the `Diagnostic` tab.

### Suggested talking points
- Once we know what is happening, the next question is why.
- This is the stage where HR moves beyond reporting and starts interpreting.
- In this dashboard, diagnostic analysis connects pay, performance, pay equity, and attrition risk.
- The goal is to look for meaningful patterns, relationships, and pockets of concern.
- For example:
  - Are employees who leave being paid differently from those who stay?
  - Are high-risk groups concentrated in certain salary bands or talent segments?
  - Are there equity gaps that may be contributing to risk?
- This stage is often where the business story becomes much clearer.

### What to click or show
- Salary vs attrition by department
- Pay vs risk relationship
- Critical talent pay gap chart
- Pay equity gap view
- Attrition heatmap
- Highest flight-risk pockets chart

### What to say
- "Stage 2 is where we start building explanation."
- "We are no longer only describing the workforce. We are asking what may be driving the patterns we saw earlier."
- "This is usually the stage where HR leaders begin to say: now I can see what is behind the headline numbers."

### Key point worth paying attention to
Do not confuse correlation with proof. Stage 2 helps us identify likely drivers and important patterns, but it still requires judgment and business context.

### Slide-ready speaker script for each diagnostic graph

#### 1. Salary of employees who stayed vs exited
"On this chart, each department is split into two salary distributions: employees who stayed and employees who exited. The central line in each box is the median salary, while the box itself shows the middle half of employees in that group. What I want the audience to notice is whether the exited group consistently sits below the stayed group. If we see that pattern across several departments, it is a useful signal, but HR should be careful not to make a firm judgment that exited employees were definitively paid less than those who stayed, or that lower pay caused the exits. A box plot is descriptive evidence only. It shows the distribution shape and median, not proof of causation. 

The exited group may be smaller, may contain more junior employees, or may differ in tenure, role mix, location, or performance even within the same department. A stronger next step is to run a Welch's two-sample t-test on salary for stayed versus exited employees within the selected filter. That test helps us judge whether the difference in average salary is likely to be real rather than random noise, especially when group sizes and variance are unequal. If the p-value is below the chosen threshold and the exited mean is lower, we can say the salary gap is statistically significant in that segment, but still not that salary alone caused attrition. To make the conclusion more reliable, HR should cross-check sample size, compare the salary versus exit-risk scatter, review attrition by salary band and performance level, and look at market pay gaps by department, location, tenure, or role level. If those views point in the same direction, the pay explanation becomes more credible."

**Mistake demo 1: highest turnover rate does not always mean worst problem**
Use this as a short teaching moment when the audience sees a department-level turnover rate chart. The test being used is a two-proportion test. In plain English, it compares the turnover rate of two groups while also taking into account how many employees are in each group. This matters because a small department can show a very high percentage from only a few exits.

Step 1: Show the diagnostic-tab pattern first. "Before we run any test, look at what the chart is showing us. HR has the highest percentage, but Sales has many more actual exits."

| Department | Total employees | Employees exited | Turnover rate | What the audience may notice |
|---|---:|---:|---:|---|
| HR | 18 | 3 | 16.7% | Highest percentage, but very small group |
| Sales | 150 | 18 | 12.0% | Lower percentage, but many more exits |

Step 2: Show the common mistake. "HR has the worst turnover problem because it has the highest turnover rate."

Step 3: Explain why that is risky. "HR is tiny here, so 3 exits create an eye-catching percentage even though Sales lost many more people. We should not judge only by the percentage. We need to check both the numerator, meaning how many people left, and the denominator, meaning how many people were in the group."

Step 4: Set up the comparison. "In this example, HR has 3 exits out of 18 employees, which is 16.7%. Sales has 18 exits out of 150 employees, which is 12.0%. Visually, HR looks higher, but Sales lost many more people in absolute terms."

Step 5: Explain the null hypothesis. "The null hypothesis is the neutral starting point: HR and Sales have the same underlying turnover rate. In other words, the difference between 16.7% and 12.0% may just be random movement caused by different group sizes."

Step 6: Explain the formula. "The two-proportion z-test uses this formula: z = (p1 - p2) / SE. The observed difference is HR's rate minus Sales' rate. The standard error tells us how much random variation we should expect because the group sizes are different."

Step 7: Show the pooled proportion. "Because the null hypothesis assumes the same underlying turnover rate, we first pool the exits: p-hat = (3 + 18) / (18 + 150) = 21 / 168 = 0.125. In plain English, across HR and Sales combined, 12.5% of employees exited."

Step 8: Show the observed difference. "The observed difference is p1 - p2 = 0.167 - 0.120 = 0.047. So HR's turnover rate is 4.7 percentage points higher than Sales."

Step 9: Show the standard error. "The standard error is SE = sqrt(0.125 * 0.875 * (1/18 + 1/150)) = 0.0825. In plain English, this is the amount of difference we might expect simply because HR has a much smaller denominator."

Step 10: Show the z-test result. "The z-value is z = 0.047 / 0.0825 = 0.57. The p-value is 0.5716, so we fail to reject the null hypothesis."

Step 11: Give the safe HR wording. "The visual rate difference is not enough by itself. HR's rate is higher, but because HR is small, the difference is not statistically convincing in this example. HR should not be ignored, but the better conclusion is: check the count, check the rate, and use the two-proportion test before saying one department has a meaningfully worse turnover problem than another."

#### 2. Salary vs predicted exit risk
"Each dot here represents one employee. The x-axis shows salary, the y-axis shows predicted exit risk, color shows performance rating, and dot size reflects tenure. The broad pattern we are looking for is whether risk tends to fall as salary rises. If it does, that suggests pay compression or weak competitiveness is associated with higher retention risk. But we also want to look for the exceptions, especially employees who are strong performers but still sit high on the risk axis. Those are the people telling us pay is not the only issue, or that even valuable talent may still be at risk under the current reward structure."

#### 3. Critical-talent pay gaps by pocket
"This chart focuses only on critical talent, which in this model means employees with higher performance ratings. Each bar represents a department-location pocket, and the x-axis shows the percentage gap between actual median salary and estimated market pay. More negative values mean that group is being paid further below market. The bar color adds another layer by showing attrition rate, so we can see whether under-market pay and turnover are happening together. When a pocket has both a large negative pay gap and a high attrition color, that becomes a very strong signal for compensation intervention."

#### 4. Pay equity heatmap
"This heatmap compares median pay for women and men within the same department and performance level. Each cell shows the percentage gap, and the color helps us quickly spot where the differences are most pronounced. Negative values indicate women are paid below men in that specific segment, while positive values indicate the opposite. The key message is that equity issues are not always evenly spread across the organization. Instead, they may be concentrated in specific departments or performance tiers, which means targeted action is often more effective than broad, generic correction."

#### 5. Attrition hotspot heatmap
"This chart shows attrition rate by salary band and performance rating. Each cell is a combination of pay level and performance level, and the color intensity shows where exits are most concentrated. The point of this slide is to identify hotspots, not just averages. If the brightest cells cluster in the lower salary bands, that suggests compensation pressure is a broad driver of exits. If the pattern is concentrated in only certain performance levels, then the issue may be more specific, such as weak progression, role fit, or uneven management for particular talent groups."

**Mistake demo 2: heatmap percentage interpretation**
Use this as a short teaching moment when showing the attrition hotspot heatmap. The calculation behind each cell is not a prediction model. It is a simple observed attrition rate. The dashboard groups employees by tenure band and performance rating, then calculates the share of employees in that group whose `Left` value is 1.

Step 1: Explain what each cell represents. "Each heatmap cell is one small employee group. For example, performance rating 1 and tenure under 1 year means employees who are new to the company and have the lowest performance rating."

Step 2: Explain the formula. "The formula is: number of employees who left in that group divided by total employees in that group, multiplied by 100."

Step 3: Use the 80% example. "If the cell shows 80%, that does not mean 80% will leave in the future. It means that, in this dataset, 80% of employees in that group already left."

Step 4: Show the count behind the percentage. "For example, if there are 5 employees in the performance rating 1 and under-1-year tenure group, and 4 of them left, the attrition rate is 4 divided by 5, which equals 80%."

Step 5: Show the common mistake. "The mistake is to read this as a prediction: '80% of these people will leave.' That is too strong. The correct wording is: 'This group had 80% observed attrition in the data.'"

Step 6: Add the sample-size warning. "Because this cell may be based on only a few employees, HR should not overreact to the percentage alone. A high percentage from a small group is a useful warning signal, but we should check the count, compare nearby cells, and ask whether the pattern is repeated across departments, locations, or time periods."

Step 7: Give the safe HR wording. "This heatmap helps us find hotspots. It does not prove the reason people left, and it does not predict exactly who will leave next. It tells us where HR should ask better follow-up questions."

#### 6. Highest flight-risk pockets
"This final chart brings the diagnostic story together by ranking the highest-risk talent pockets. Each bar represents a department, location, and talent segment combination. The bar length is a composite flight-risk index, which combines attrition, under-market pay, and concentration of strong performers. The color shows pay gap, helping us see whether the highest-risk pockets are also compensation-driven. This is the chart I would use to move from diagnosis to action, because it tells leaders where to prioritize first if they cannot intervene everywhere at once."

#### Suggested transition line after the diagnostic tab
"So if we read the diagnostic tab from left to right and top to bottom, the story becomes clear. First, pay appears related to who leaves. Second, that pressure is not uniform; it is concentrated in certain talent pockets and in some cases linked to equity issues. Third, when we combine pay pressure, attrition, and talent value, we can identify where intervention is likely to have the strongest impact."

## Stage 3: Predictive Analytics
### Main message
Predictive analytics helps us estimate what is likely to happen next if current patterns continue or if different decisions are made.

### Dashboard tab to use
Use the `Predictive` tab.

### Suggested talking points
- After understanding what is happening and why, the next logical question is: what is likely to happen next?
- In HR, this is often where we start discussing risk rather than only historical reporting.
- In this dashboard, the predictive stage is not about advanced technical modeling for its own sake.
- It is about using historical employee patterns to estimate a future-facing outcome.
- In the current Predictive tab, the example uses logistic regression to estimate promotion readiness.
- The model looks at employees who were promoted before and compares them with employees who were not promoted, while considering performance, tenure, training, salary, department, and location together.
- The purpose is not to let the model decide who gets promoted. The purpose is to support HR discussion with a more structured, evidence-based view.

### What to click or show
- The "What is logistic regression?" section and S-curve chart
- The original HR dataset and cleaned model-ready dataset
- The step-by-step regression formula
- The summary table where the learned coefficients appear
- The employee-level score calculation and predicted promotion chance
- The readiness band charts

### What to say
- "Predictive analytics is valuable because it helps us prepare, not just explain."
- "For HR audiences, the most useful prediction is not the technical model itself. It is the practical estimate that helps us discuss risk, readiness, or likely outcomes more clearly."
- "In this example, the model does not replace manager judgment. It helps HR see which employees look more similar to people who were promoted before, after considering several factors together."

### How to explain promotion odds versus promotion chance
Logistic regression often uses the language of "odds", but this can be confusing for HR audiences. It is important not to interpret promotion odds as promotion chance.

- Promotion chance means the percentage probability of promotion. For example, a 20% promotion chance means that out of 100 similar employees, around 20 are expected to be promoted.
- Promotion odds compare promotion with non-promotion. If promotion chance is 20%, then 20 out of 100 are promoted and 80 are not promoted. The odds are 20 divided by 80, or 0.25.
- Because of this, an odds ratio does not translate directly into the same percentage increase in promotion chance.
- For example, if the model says the odds are 80% higher, we should not say the promotion chance is 80% higher. The actual chance depends on the employee's starting probability.

### HR-friendly interpretation
Instead of saying:

"A 1-point increase in performance rating increases the odds of promotion by 80%."

Say:

"Employees with stronger performance ratings tend to have a higher predicted chance of promotion, after considering the other factors together."

Or:

"The model suggests that performance rating is a positive predictor of promotion readiness, but HR should read this as decision support, not an automatic promotion rule."

### How to get promotion chance
If HR wants promotion chance, use the model's predicted probability rather than the odds ratio.

- The model first creates a promotion readiness score from the learned coefficients.
- The score is then converted through the logistic curve into a predicted probability.
- That predicted probability can be shown as a promotion chance, such as 18%, 35%, or 62%.
- This is usually easier for HR audiences to understand than odds or odds ratios.

### Key point worth paying attention to
Do not present predictions as certainty. Stage 3 is about likely outcomes and decision support, not perfect forecasts or automatic people decisions.

## Stage 4: Prescriptive Analytics
### Main message
Prescriptive analytics turns insight into action. It answers the question: what should we do, in what order, and with what expected impact?

### Dashboard tab to use
Use the `Prescriptive` tab.

### Suggested talking points
- This is the highest stage in the framework because it connects analysis to recommendation.
- In HR, leaders do not just want insight. They want to know what action should be taken.
- In this dashboard, the prescriptive stage takes the findings from earlier stages and converts them into:
  - a recommended priority area
  - possible actions
  - budget allocation thinking
  - estimated business value
- This is where analytics becomes decision support rather than information sharing.

### What to click or show
- Board snapshot at the top
- Executive answer panel
- Recommended actions area
- Budget allocation chart
- Estimated result chart
- Closing recommendation panel

### What to say
- "Stage 4 is where analytics becomes truly useful for leadership."
- "At this point, we are not only saying what we know. We are saying what we recommend."
- "This is also where HR needs to think commercially: what action matters most, what can we afford, and what business return do we expect?"

### Key point worth paying attention to
Do not jump to prescriptions without the earlier stages. Good recommendations depend on good description, diagnosis, and prediction.

## Key Points to Pay Attention to in Each Stage
### Stage 1: Descriptive
- Focus on facts and patterns
- Build a shared understanding of the current situation
- Avoid jumping to reasons too early

### Stage 2: Diagnostic
- Explore relationships and possible drivers
- Look for patterns across groups, departments, or segments
- Be careful not to overclaim causation

### Stage 3: Predictive
- Use scenarios to support forward-looking thinking
- Frame outputs as estimates, not certainties
- Keep the discussion practical and business-relevant

### Stage 4: Prescriptive
- Translate insights into action
- Prioritize actions rather than listing everything
- Consider business feasibility, budget, and expected impact

### One overall teaching message
The most important idea is that each stage builds on the one before it. Strong HR analytics is not about jumping straight to recommendations. It is about moving through the logic in the right order.

## How to Use the Dashboard During the Lecture
### Recommended approach
- Keep the dashboard open throughout the session
- Use each tab as a live visual anchor for one stage of the framework
- Spend a medium amount of time clicking, enough to keep attention, but not so much that the audience gets lost in the details

### Suggested facilitation tips
- At the start of each section, tell the audience the key question for that stage
- Then open the relevant tab
- Point to 2 or 3 visuals only, not every chart in detail
- Use simple transitions such as:
  - "Now that we know what is happening, let us ask why."
  - "Now that we understand the likely drivers, let us think ahead."
  - "Now that we see the likely future risk, let us discuss action."

### Practical note
The dashboard is a teaching device here. The goal is not to explain every chart technically. The goal is to use the dashboard to help the audience understand the logic of the four stages.

## Other HR Examples Beyond This Dashboard
To help the audience generalize the framework, explain that the same four stages can be used in other HR topics.

### Example 1: Hiring
- Descriptive: How many hires, time to fill, source mix, offer acceptance rate
- Diagnostic: Why are some roles harder to fill than others?
- Predictive: Which roles are likely to remain hard to fill next quarter?
- Prescriptive: What sourcing or employer branding actions should we prioritize?

**Mini example: offer / no-offer pattern by source**
Use a chi-square test when you want to compare the offer / no-offer pattern across all sources at once instead of only comparing two channels. In plain English, the test asks: "Does the offer outcome look independent of source, or do some sources appear to produce a different offer pattern?"

| Candidate source | Offer | No offer | Total candidates | Offer rate |
|---|---:|---:|---:|---:|
| Employee referral | 32 | 68 | 100 | 32% |
| LinkedIn | 24 | 96 | 120 | 20% |
| Job board | 18 | 132 | 150 | 12% |
| Campus recruiting | 26 | 74 | 100 | 26% |
| Agency | 15 | 85 | 100 | 15% |

Teaching note: this table is called a contingency table. The rows are sourcing channels and the columns are outcomes. If offer and no-offer proportions are very different across the rows, the chi-square test helps HR judge whether the pattern is large enough to investigate further, instead of assuming the differences are just random noise.

### Example 2: Learning and Development
- Descriptive: Who attended training and what completion rates do we see?
- Diagnostic: Why do some teams show lower participation or weaker outcomes?
- Predictive: Which groups may struggle to build capability without intervention?
- Prescriptive: Which learning investments should be prioritized?

### Example 3: Engagement
- Descriptive: What are current engagement scores?
- Diagnostic: Why are some teams or groups scoring lower?
- Predictive: Which areas may face increased turnover risk if nothing changes?
- Prescriptive: What action plan should leaders take?

### Suggested speaker wording
"This dashboard is about pay, performance, and retention, but the framework is much bigger than this one topic. The same four-stage thinking can be applied across almost every important HR question."

## Closing Summary
### Suggested talking points
- Today’s key message is that the four stages are not just analytics labels. They are a way of structuring HR thinking.
- Descriptive tells us what is happening.
- Diagnostic helps us understand why.
- Predictive helps us anticipate what may happen next.
- Prescriptive helps us decide what to do.
- Many HR teams spend most of their time in Stage 1.
- The real value of analytics grows when we move toward Stages 2, 3, and 4.
- But we should not skip the order.
- The stages work best when they build on one another.

### Final closing line
"If there is one idea I want you to remember, it is this: good HR analytics is not about creating more charts. It is about using data to move from observation to understanding, from understanding to foresight, and from foresight to action."

## Likely Audience Questions
### 1. Do we always need to go through all four stages?
No. Not every HR problem needs all four stages. But every good analysis should start with a clear understanding of what is happening.

### 2. Is predictive analytics only for data scientists?
No. In many HR settings, predictive thinking starts with practical scenario analysis, not highly technical models.

### 3. What stage do most HR teams spend the most time in?
Usually Stage 1, descriptive reporting. That is useful, but it is only the beginning.

### 4. What is the biggest mistake people make?
Jumping too quickly to solutions without first understanding the facts and likely drivers.

### 5. How can HRBPs use this if they are not analytics specialists?
They can use the framework as a questioning tool: what is happening, why, what may happen next, and what should we do?

### 6. What is the business value of this framework?
It helps HR move from reporting information to supporting better business decisions.

### 7. If AI can already do analysis for us, why do we still need to learn HR analytics?
Because AI can help generate analysis, but HR professionals still need to ask the right business question, judge whether the data is reliable, interpret the result in context, and decide what action makes sense. If we do not understand HR analytics, we may accept weak analysis, miss bad assumptions, or make poor decisions based on outputs we do not fully understand. Learning HR analytics is therefore not about competing with AI. It is about using AI responsibly and intelligently so that HR can guide better business decisions.
