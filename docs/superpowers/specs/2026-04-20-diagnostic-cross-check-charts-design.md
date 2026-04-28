# Diagnostic Cross-Check Charts Design

## Goal
Add a new "Cross-check the salary story" block directly below the hypothesis-test spotlight in the `Diagnostic` tab so HR users can test whether the lower-pay / higher-exit pattern still holds after looking at role mix, tenure, and performance.

## Audience
Internal HR learners and HRBPs using the dashboard as a teaching tool for descriptive versus diagnostic analysis.

## Approved Scope
- Add exactly 3 supplementary graphs below the t-test section.
- Include at least 1 correlation dot chart.
- Include at least 1 heatmap.
- Show a short conclusion immediately after each graph.
- Use existing fields only; use `Talent_Segment` as the role-mix proxy.

## Non-Goals
- Do not add a new `Job_Level` field.
- Do not redesign the whole diagnostic page.
- Do not remove existing charts.
- Do not change the primary business question or replace the t-test block.

## Proposed Graphs

### 1. Correlation Dot Chart
**Title:** `Salary vs exit risk within talent segments`

**Purpose:** Check whether the negative pay-risk pattern still appears after comparing employees within broad talent groups rather than across the full population.

**Design:**
- Plot `Salary` on the x-axis.
- Plot `Exit_Prob * 100` on the y-axis.
- Color by `Talent_Segment`.
- Size by `Tenure_Years`.
- Keep a manageable sample size, consistent with the existing scatter pattern.

**Conclusion style:**
- Report whether the salary-risk relationship remains negative overall.
- Call out whether one segment still shows high risk despite higher salary overlap.

### 2. Heatmap
**Title:** `Attrition hotspots by tenure and performance`

**Purpose:** Check whether exit concentration is really a pay story or whether the salary signal may partly reflect short-tenure or lower-performance concentration.

**Design:**
- Use `Tenure_Band` on one axis.
- Use `Perf_Rating` on the other axis.
- Cell value = attrition rate.
- Use a continuous color scale with text labels.

**Conclusion style:**
- Identify the hottest cell.
- State whether exits are concentrated in early-tenure pockets, lower-performance pockets, or spread broadly.

### 3. Role-Mix Comparison Chart
**Title:** `Stayed vs exited salary gap by talent segment`

**Purpose:** Check whether the pay gap still exists inside comparable talent groups instead of only at the all-employee level.

**Design:**
- Group by `Talent_Segment` and `Attrition_Status`.
- Compare median salary by segment for `Stayed` versus `Exited`.
- Use grouped bars for easy within-segment comparison.

**Conclusion style:**
- State which segment shows the largest within-group pay gap.
- State whether the lower-pay exit pattern is broad or concentrated in one segment.

## Placement
Insert this new block immediately below the hypothesis-test spotlight and above the existing mid-page charts. Add a local heading such as `#### Cross-check the salary story`.

## Data Handling
- Reuse `filtered_df` inside `render_diagnostic_tab()`.
- Derive `Attrition_Status` from `Left`.
- Reuse existing fields: `Salary`, `Exit_Prob`, `Talent_Segment`, `Tenure_Years`, `Tenure_Band`, `Perf_Rating`, `Left`.
- If any grouped chart becomes empty after filtering, show an `st.info()` message instead of rendering a broken chart.

## UX Notes
- Keep chart heights visually consistent with the current diagnostic charts.
- Use existing dashboard colors and `style_descriptive_figure()`.
- Make the chart summaries business-facing, not technical.
- Keep the summary beneath each graph short: 1-2 sentences.

## Risks
- `Talent_Segment` is only a proxy for role mix, so this block should be framed as a cross-check rather than a full control analysis.
- Some filtered views may create very small exited groups in one segment; those cases should use cautious summary wording.

## Testing
- Verify the app still runs and the diagnostic tab renders.
- Check at least one filtered and one unfiltered view.
- Confirm each new chart displays a conclusion under it.
- Confirm empty-state handling remains readable.
