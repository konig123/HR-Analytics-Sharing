import json
import math
import unittest
from pathlib import Path
from unittest.mock import patch

import app
import plotly.express as px
from streamlit.testing.v1 import AppTest


class DashboardDataTests(unittest.TestCase):
    def test_inject_dashboard_css_styles_native_streamlit_text_regions(self):
        with patch.object(app.st, "markdown") as markdown_mock:
            app.inject_dashboard_css()

        injected_css = markdown_mock.call_args.args[0]
        self.assertIn('[data-testid="stSidebar"]', injected_css)
        self.assertIn('[data-baseweb="tab-list"]', injected_css)
        self.assertIn('[data-baseweb="select"]', injected_css)
        self.assertIn(".board-panel strong", injected_css)
        self.assertIn(".board-panel li", injected_css)

    def test_load_data_includes_demographic_columns(self):
        df = app.load_data()

        expected_columns = {
            "Gender",
            "Age",
            "Age_Band",
            "Tenure_Band",
            "Salary_Band",
            "Report_Month",
            "Hire_Event",
            "Exit_Event",
        }

        self.assertTrue(expected_columns.issubset(df.columns))
        self.assertGreater(df["Left"].nunique(), 1)

    def test_prepare_workforce_flow_returns_monthly_hires_and_exits(self):
        df = app.load_data()

        flow = app.prepare_workforce_flow(df)

        self.assertEqual(list(flow.columns), ["Report_Month_Label", "Hires", "Exits"])
        self.assertEqual(len(flow), 12)
        self.assertTrue((flow["Hires"] >= 0).all())
        self.assertTrue((flow["Exits"] >= 0).all())

    def test_prepare_workforce_flow_keeps_fixed_reporting_window_when_filtered(self):
        df = app.load_data()
        filtered = df[df["Report_Month"] >= "2024-07-01"]

        flow = app.prepare_workforce_flow(filtered)

        self.assertEqual(flow["Report_Month_Label"].iloc[0], "Jan 2024")
        self.assertEqual(flow["Report_Month_Label"].iloc[-1], "Dec 2024")
        self.assertEqual(len(flow), 12)

    def test_summarize_descriptive_metrics_returns_key_metrics(self):
        df = app.load_data()

        metrics = app.summarize_descriptive_metrics(df)

        for key in [
            "headcount",
            "turnover_rate",
            "avg_salary",
            "avg_tenure",
            "female_share",
            "promotion_rate",
            "median_age",
        ]:
            self.assertIn(key, metrics)

    def test_prepare_pay_segment_summary_returns_expected_columns(self):
        df = app.load_data()

        summary = app.prepare_pay_segment_summary(df)

        self.assertFalse(summary.empty)
        self.assertEqual(
            list(summary.columns),
            [
                "Department",
                "Location",
                "Talent_Segment",
                "Employees",
                "Median_Salary",
                "Market_Pay",
                "Pay_Gap_Pct",
                "Attrition_Rate",
                "High_Performer_Share",
                "Flight_Risk_Index",
            ],
        )

    def test_prepare_pay_equity_summary_returns_expected_columns(self):
        df = app.load_data()

        equity = app.prepare_pay_equity_summary(df)

        self.assertFalse(equity.empty)
        self.assertEqual(
            list(equity.columns),
            [
                "Department",
                "Perf_Rating",
                "Women_Median",
                "Men_Median",
                "Gap_Dollar",
                "Gap_Pct",
            ],
        )

    def test_forecast_retention_scenarios_returns_three_ranked_actions(self):
        df = app.load_data()

        scenarios = app.forecast_retention_scenarios(df, budget=450000)

        self.assertEqual(len(scenarios), 3)
        self.assertEqual(
            list(scenarios.columns),
            [
                "Scenario",
                "Target_Group",
                "Investment",
                "Estimated_Exits_Avoided",
                "Retention_Lift_Pct_Pts",
                "Estimated_Savings",
                "ROI",
            ],
        )
        self.assertTrue((scenarios["Investment"] > 0).all())

    def test_forecast_retention_scenarios_handles_empty_population(self):
        empty = app.load_data().iloc[0:0]

        scenarios = app.forecast_retention_scenarios(empty, budget=250000)

        self.assertEqual(len(scenarios), 3)
        self.assertTrue((scenarios["Estimated_Exits_Avoided"] == 0).all())
        self.assertTrue((scenarios["Estimated_Savings"] == 0).all())

    def test_recommend_cb_action_returns_single_best_scenario(self):
        df = app.load_data()
        scenarios = app.forecast_retention_scenarios(df, budget=450000)

        recommended = app.recommend_cb_action(scenarios)

        self.assertEqual(recommended["Estimated_Exits_Avoided"], scenarios["Estimated_Exits_Avoided"].max())
        self.assertLessEqual(recommended["Estimated_Exits_Avoided"], scenarios["Estimated_Exits_Avoided"].sum())

    def test_prepare_promotion_prescriptive_actions_returns_expected_outputs(self):
        df = app.load_data()

        result = app.prepare_promotion_prescriptive_actions(df)

        self.assertIn("recommendations", result)
        self.assertIn("action_summary", result)
        self.assertIn("fairness_summary", result)
        self.assertIn("capacity_check", result)
        self.assertIn("business_constraints", result)
        self.assertIn("missing_evidence", result)
        self.assertIn("bias_audit", result)
        self.assertIn("business_priority", result)
        self.assertIn("priority_deep_dive", result)
        self.assertIn("priority_candidate_ranking", result)
        self.assertIn("priority_case_studies", result)
        self.assertFalse(result["recommendations"].empty)
        self.assertEqual(
            list(result["recommendations"].columns),
            [
                "Employee_ID",
                "Department",
                "Location",
                "Gender",
                "Perf_Rating",
                "Tenure_Years",
                "Predicted_Promotion_Chance",
                "Recommended_Action",
                "HR_Rationale",
                "Required_Checks",
            ],
        )
        self.assertTrue(any("Promotion panel review" in action for action in result["action_summary"]["Recommended_Action"]))
        self.assertEqual(
            list(result["missing_evidence"].columns),
            ["Evidence_Needed", "Seen_By_Model", "Employees_Needing_Check", "Example_HR_Question"],
        )
        self.assertTrue(any("Manager feedback" in value for value in result["missing_evidence"]["Evidence_Needed"]))
        self.assertEqual(
            set(result["missing_evidence"]["Evidence_Needed"]),
            {
                "Manager feedback",
                "Role scope",
                "Business need",
                "Leadership behavior",
                "Critical skills",
                "Mobility preference",
                "Performance consistency",
                "Promotion budget / headcount availability",
            },
        )
        self.assertEqual(
            list(result["bias_audit"].columns),
            ["Check", "Group", "Current_Value", "Comparison", "HR_Interpretation"],
        )
        self.assertTrue(any("Departments over-recommended" in value for value in result["bias_audit"]["Check"]))
        self.assertEqual(
            set(result["bias_audit"]["Check"]),
            {
                "Departments over-recommended",
                "Women or minority groups under-recommended",
                "Does the model reproduce old promotion bias?",
                "Are high-potential employees being missed?",
            },
        )
        self.assertEqual(
            list(result["business_priority"].columns),
            ["Business_Priority", "Employees", "Panel_Review_Count", "Stretch_Count", "Attrition_Rate", "HR_Use"],
        )
        self.assertTrue(any("Leadership pipeline gaps" in value for value in result["business_priority"]["Business_Priority"]))
        self.assertEqual(
            set(result["business_priority"]["Business_Priority"]),
            {
                "Critical roles",
                "Succession risk",
                "Retention risk",
                "Business growth areas",
                "Scarce skills",
                "Leadership pipeline gaps",
            },
        )
        retention_row = result["business_priority"].set_index("Business_Priority").loc["Retention risk"]
        current_employee_exit_cutoff = df.loc[df["Left"].eq(0), "Exit_Prob"].quantile(0.75)
        expected_retention_risk_count = int(
            (df["Left"].eq(0) & df["Exit_Prob"].ge(current_employee_exit_cutoff)).sum()
        )
        self.assertEqual(retention_row["Employees"], expected_retention_risk_count)
        self.assertLess(retention_row["Attrition_Rate"], 100)
        self.assertEqual(
            list(result["priority_deep_dive"].columns),
            [
                "Business_Priority",
                "Segment_Definition",
                "Employees",
                "Avg_Promotion_Chance",
                "Avg_Exit_Risk",
                "Panel_Review_Count",
                "Stretch_Count",
                "Top_Department",
                "Top_Location",
                "HR_Conclusion",
            ],
        )
        self.assertEqual(set(result["priority_deep_dive"]["Business_Priority"]), set(result["business_priority"]["Business_Priority"]))
        self.assertEqual(
            list(result["priority_candidate_ranking"].columns),
            [
                "Employee_ID",
                "Department",
                "Location",
                "Perf_Rating",
                "Tenure_Years",
                "Predicted_Promotion_Chance",
                "Recommended_Action",
                "Priority_Fit_Score",
                "Matched_Priorities",
                "Promotion_Suggestion",
            ],
        )
        self.assertGreater(result["priority_candidate_ranking"]["Priority_Fit_Score"].max(), 0)
        current_employee_ids = set(df.loc[df["Left"].eq(0), "Employee_ID"])
        self.assertTrue(set(result["recommendations"]["Employee_ID"]).issubset(current_employee_ids))
        self.assertTrue(set(result["priority_candidate_ranking"]["Employee_ID"]).issubset(current_employee_ids))
        self.assertTrue(set(result["priority_case_studies"]["Employee_ID"]).issubset(current_employee_ids))
        if "Promotion panel review" in set(result["priority_candidate_ranking"]["Recommended_Action"]):
            self.assertEqual(result["priority_candidate_ranking"].iloc[0]["Recommended_Action"], "Promotion panel review")
        self.assertEqual(
            list(result["priority_case_studies"].columns),
            ["Employee_ID", "Matched_Priorities", "Evidence_To_Check", "Suggested_HR_Wording"],
        )
        self.assertEqual(
            list(result["capacity_check"].columns),
            ["Constraint", "Current_Value", "Guideline", "Status", "Recommended_Response"],
        )
        self.assertTrue(any("Promotion review capacity" in value for value in result["capacity_check"]["Constraint"]))
        self.assertTrue(any("Fairness review" in check for check in result["business_constraints"]["Required_Check"]))

    def test_prepare_promotion_prescriptive_actions_handles_exited_only_population(self):
        df = app.load_data()
        exited_only = df[df["Left"].eq(1)]

        result = app.prepare_promotion_prescriptive_actions(exited_only)

        self.assertTrue(result["recommendations"].empty)
        self.assertTrue(result["priority_candidate_ranking"].empty)
        self.assertTrue(result["priority_case_studies"].empty)
        self.assertEqual(list(result["business_priority"].columns), ["Business_Priority", "Employees", "Panel_Review_Count", "Stretch_Count", "Attrition_Rate", "HR_Use"])

    def test_prepare_salary_attrition_hypothesis_test_returns_expected_fields(self):
        df = app.load_data()

        result = app.prepare_salary_attrition_hypothesis_test(df)

        for key in [
            "test_name",
            "null_hypothesis",
            "alternative_hypothesis",
            "stayed_n",
            "exited_n",
            "stayed_mean",
            "exited_mean",
            "stayed_median",
            "exited_median",
            "mean_gap",
            "t_stat",
            "p_value",
            "decision",
            "interpretation",
        ]:
            self.assertIn(key, result)

        self.assertGreater(result["stayed_n"], 0)
        self.assertGreater(result["exited_n"], 0)
        self.assertTrue(math.isfinite(result["t_stat"]))
        self.assertGreaterEqual(result["p_value"], 0.0)
        self.assertLessEqual(result["p_value"], 1.0)

    def test_prepare_salary_risk_by_talent_segment_returns_expected_columns(self):
        df = app.load_data()

        result = app.prepare_salary_risk_by_talent_segment(df)

        self.assertFalse(result.empty)
        self.assertEqual(
            list(result.columns),
            [
                "Salary",
                "Exit_Prob",
                "Risk_Pct",
                "Talent_Segment",
                "Tenure_Years",
                "Department",
                "Location",
                "Gender",
            ],
        )

    def test_prepare_attrition_by_tenure_performance_returns_expected_columns(self):
        df = app.load_data()

        result = app.prepare_attrition_by_tenure_performance(df)

        self.assertFalse(result.empty)
        self.assertEqual(
            list(result.columns),
            ["Tenure_Band", "Perf_Rating", "Attrition_Rate"],
        )
        self.assertTrue((result["Attrition_Rate"] >= 0).all())
        self.assertTrue((result["Attrition_Rate"] <= 100).all())

    def test_prepare_salary_gap_by_talent_segment_returns_expected_columns(self):
        df = app.load_data()

        result = app.prepare_salary_gap_by_talent_segment(df)

        self.assertFalse(result.empty)
        self.assertEqual(
            list(result.columns),
            ["Talent_Segment", "Attrition_Status", "Median_Salary"],
        )
        self.assertTrue({"Stayed", "Exited"}.issubset(set(result["Attrition_Status"])))

    def test_prepare_promotion_logit_demo_returns_expected_shapes(self):
        df = app.load_data()

        result = app.prepare_promotion_logit_demo(df)

        self.assertIn("summary_table", result)
        self.assertIn("model_stats", result)
        self.assertIn("readiness_view", result)
        self.assertIn("employee_sample", result)
        self.assertIn("concept_view", result)
        self.assertIn("logistic_curve", result)
        self.assertIn("calculation_example", result)
        self.assertIn("sklearn_demo", result)
        self.assertIn("statsmodels_summary", result)
        self.assertIn("interpretation", result)
        self.assertFalse(result["summary_table"].empty)
        self.assertFalse(result["readiness_view"].empty)
        self.assertFalse(result["employee_sample"].empty)
        self.assertFalse(result["concept_view"].empty)
        self.assertFalse(result["logistic_curve"].empty)
        self.assertFalse(result["calculation_example"].empty)
        self.assertFalse(result["sklearn_demo"]["prediction_preview"].empty)
        self.assertFalse(result["sklearn_demo"]["probability_preview"].empty)
        self.assertIn("train_test_split", result["sklearn_demo"]["code"])
        self.assertIn("LogisticRegression(max_iter=1000)", result["sklearn_demo"]["fit_output"])
        self.assertIn("sm.Logit", result["statsmodels_summary"]["code"])
        self.assertIn("result.summary()", result["statsmodels_summary"]["code"])
        self.assertIn("Logit Regression Results", result["statsmodels_summary"]["output"])
        self.assertIn("coef", result["statsmodels_summary"]["output"])
        self.assertEqual(
            list(result["summary_table"].columns),
            ["Variable", "coef", "std err", "z", "P>|z|", "[0.025", "0.975]"],
        )
        self.assertEqual(
            list(result["calculation_example"].columns),
            ["Variable", "Coefficient", "Employee_Value", "Contribution"],
        )
        self.assertEqual(
            list(result["sklearn_demo"]["prediction_preview"].columns),
            ["Actual", "Predicted", "Predicted_Promotion_Chance"],
        )
        self.assertEqual(
            list(result["sklearn_demo"]["probability_preview"].columns),
            ["P_Not_Promoted", "P_Promoted"],
        )
        self.assertEqual(
            list(result["readiness_view"].columns),
            ["Readiness_Band", "Avg_Predicted_Chance", "Actual_Promotion_Rate", "Employees"],
        )
        for key in ["nobs", "pseudo_r2", "llf", "llr_pvalue", "converged"]:
            self.assertIn(key, result["model_stats"])
        for key in ["top_positive_factor", "top_negative_factor", "highest_readiness_band"]:
            self.assertIn(key, result["interpretation"])

    def test_prepare_hiring_offer_rate_analysis_returns_expected_fields(self):
        _, hiring_demo = app.prepare_diagnostic_teaching_examples()

        result = app.prepare_hiring_offer_rate_analysis(hiring_demo)

        for key in [
            "source_summary",
            "job_board_offers",
            "employee_referral_offers",
            "job_board_rate",
            "employee_referral_rate",
            "pooled_rate",
            "standard_error",
            "observed_difference",
            "z_stat",
            "p_value",
            "decision",
            "interpretation",
            "chi_square_stat",
            "chi_square_df",
            "chi_square_p_value",
            "chi_square_decision",
            "chi_square_interpretation",
            "regression_formula",
            "regression_reference",
            "regression_table",
            "regression_interpretation",
        ]:
            self.assertIn(key, result)

        self.assertGreater(result["job_board_offers"], 0)
        self.assertGreater(result["employee_referral_offers"], 0)
        self.assertGreater(result["standard_error"], 0.0)
        self.assertTrue(math.isfinite(result["z_stat"]))
        self.assertGreater(result["chi_square_stat"], 0.0)
        self.assertGreater(result["chi_square_df"], 0)
        self.assertGreaterEqual(result["p_value"], 0.0)
        self.assertLessEqual(result["p_value"], 1.0)
        self.assertGreaterEqual(result["chi_square_p_value"], 0.0)
        self.assertLessEqual(result["chi_square_p_value"], 1.0)
        self.assertFalse(result["source_summary"].empty)
        self.assertFalse(result["regression_table"].empty)
        self.assertIn("Odds Ratio", result["regression_table"].columns)

    def test_style_descriptive_figure_sets_high_contrast_label_colors(self):
        fig = px.bar(x=["A", "B"], y=[1, 2], text=[1, 2])

        styled = app.style_descriptive_figure(fig)

        self.assertEqual(styled.layout.font.color, app.EMPHASIS_TEXT)
        self.assertEqual(styled.layout.xaxis.tickfont.color, app.EMPHASIS_TEXT)
        self.assertEqual(styled.layout.yaxis.tickfont.color, app.EMPHASIS_TEXT)
        self.assertEqual(styled.layout.legend.font.color, app.EMPHASIS_TEXT)
        self.assertEqual(styled.data[0].textfont.color, app.EMPHASIS_TEXT)

    def test_render_diagnostic_tab_uses_high_contrast_chart_text(self):
        app_dir = Path(__file__).resolve().parents[1]
        diagnostic_script = f"""
import sys
sys.path.insert(0, {str(app_dir)!r})
import app

df = app.load_data()
app.render_diagnostic_tab(df)
"""

        at = AppTest.from_string(diagnostic_script)
        at.run(timeout=60)

        self.assertEqual(len(at.exception), 0)
        self.assertEqual(len(at.get("plotly_chart")), 6)
        self.assertTrue(any("Hypothesis test spotlight" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("Cross-check the salary story" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("Null hypothesis" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("Common interpretation mistakes" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("Name the common mistake" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("Choose the correct statistical approach" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("two-proportion" in markdown.value.lower() for markdown in at.markdown))
        self.assertTrue(any("offer conversion rate" in markdown.value.lower() for markdown in at.markdown))
        self.assertTrue(any("HR vs Sales" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("Step 1: Read the diagnostic pattern" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("Step 2: Name the common mistake" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("Step 3: Check numerator and denominator" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("HR has the highest percentage, but Sales has many more actual exits" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("What is a two-proportion test?" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("compare two percentages" in markdown.value.lower() for markdown in at.markdown))
        self.assertTrue(any("What is p-hat?" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("combined turnover rate" in markdown.value.lower() for markdown in at.markdown))
        self.assertTrue(any("z = (p1 - p2) / SE" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("SE = sqrt" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("p-hat = (3 + 18) / (18 + 150)" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("number of offers by hiring source" in markdown.value.lower() for markdown in at.markdown))
        self.assertTrue(any("Job Board is clearly the best source because it generated the most offers" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("Job Board vs Employee Referral" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("offer count mostly reflects volume" in markdown.value.lower() for markdown in at.markdown))
        self.assertTrue(any("Step 4: Normalize by exposure" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("Step 5: Chi-square test across all sources" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("Step 6: Regression with controls" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("observed pattern is far enough from the expected pattern" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("Observed offer / no-offer table used for the chi-square test" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("No offer" in str(dataframe.value) for dataframe in at.dataframe))
        self.assertTrue(any("Chi-square calculation steps" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("Contribution to chi-square" in str(dataframe.value) for dataframe in at.dataframe))
        self.assertTrue(any("Expected = row total" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("degrees of freedom describe how many parts of the table can vary" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("Chi-square result" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("Odds ratio" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("role mix and job level" in markdown.value.lower() for markdown in at.markdown))

        for chart in at.get("plotly_chart"):
            spec = json.loads(chart.proto.spec)
            layout = spec["layout"]

            self.assertEqual(layout["font"]["color"], app.EMPHASIS_TEXT)
            self.assertEqual(layout["xaxis"]["tickfont"]["color"], app.EMPHASIS_TEXT)
            self.assertEqual(layout["xaxis"]["title"]["font"]["color"], app.EMPHASIS_TEXT)
            self.assertEqual(layout["yaxis"]["tickfont"]["color"], app.EMPHASIS_TEXT)
            self.assertEqual(layout["yaxis"]["title"]["font"]["color"], app.EMPHASIS_TEXT)

            if "legend" in layout and "font" in layout["legend"]:
                self.assertEqual(layout["legend"]["font"]["color"], app.EMPHASIS_TEXT)

    def test_render_predictive_tab_uses_high_contrast_chart_text(self):
        app_dir = Path(__file__).resolve().parents[1]
        predictive_script = f"""
import sys
sys.path.insert(0, {str(app_dir)!r})
import app

df = app.load_data()
app.render_predictive_tab(df)
"""

        at = AppTest.from_string(predictive_script)
        at.run(timeout=60)

        self.assertEqual(len(at.exception), 0)
        self.assertEqual(len(at.get("plotly_chart")), 2)
        self.assertTrue(any("Promotion Readiness With Logistic Regression" in markdown.value for markdown in at.markdown))
        self.assertFalse(any("Model Outcome" in markdown.value for markdown in at.markdown))
        self.assertFalse(any("Employees In Model" in markdown.value for markdown in at.markdown))
        self.assertFalse(any("Top Readiness Band" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("Business question" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("Common HR shortcut that can go wrong" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("What is logistic regression?" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("Logistic regression vs. linear regression" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("Linear regression predicts a continuous number" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("Linear regression equation" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("Salary = intercept + slope" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("tenure and salary move in a roughly linear pattern" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("bounded between 0 and 1" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("sigmoid" in markdown.value.lower() for markdown in at.markdown))
        self.assertTrue(any("Why logistic regression fits this problem" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("Prepare the model" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("Run the model and read the summary table" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("Statsmodels script using the same model-ready dataset" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("Raw `result.summary()` output" in markdown.value for markdown in at.markdown))
        self.assertFalse(any("How HR should read this table" in markdown.value for markdown in at.markdown))
        self.assertFalse(any("Show predicted promotion chance" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("Major indicators to notice in `result.summary()`" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("How to interpret the current values" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("Performance rating and tenure are the clearest positive predictors" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("do not over-interpret variables whose confidence interval crosses zero" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("Score equation using the `coef` column" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("Meaningful shorthand equation" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("0.531(Performance)" in code.value and "0.175(Tenure)" in code.value for code in at.code))
        self.assertTrue(any("How HR can use this equation for promotion advice" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("What do the score and predicted promotion chance mean?" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("A higher score means the employee looks more similar to employees who were promoted before" in markdown.value for markdown in at.markdown))
        self.assertTrue(
            any("use higher scores to prioritize review, not to automatically decide promotion" in markdown.value.lower() for markdown in at.markdown)
        )
        self.assertTrue(any("Numeric demonstration using the current sample employee" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("Promotion advice from the numeric result" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("Shorthand score" in str(dataframe.value) for dataframe in at.dataframe))
        self.assertTrue(any("Use the score to structure a talent-review conversation" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("Presentation wording" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("Performance rating" in code.value and "Tenure years" in code.value for code in at.code))
        self.assertFalse(any("Captured output from the current promotion example" in markdown.value for markdown in at.markdown))
        self.assertFalse(any("first rows compared with the actual historical outcome" in markdown.value for markdown in at.markdown))
        self.assertFalse(any("What the model learns" in str(dataframe.value) for dataframe in at.dataframe))
        self.assertFalse(any("Example calculation for one employee" in markdown.value for markdown in at.markdown))
        self.assertFalse(
            any("The example below pulls the coefficient values directly from the `coef` column above" in markdown.value for markdown in at.markdown)
        )
        self.assertTrue(any("predicted promotion chance" in markdown.value.lower() for markdown in at.markdown))
        self.assertTrue(any("decision support" in markdown.value.lower() for markdown in at.markdown))
        self.assertTrue(any("Important framing" in markdown.value for markdown in at.markdown))
        markdown_values = [markdown.value for markdown in at.markdown]
        step_3_index = next(
            idx for idx, value in enumerate(markdown_values) if "Step 3: Let the model learn" in value
        )
        summary_index = next(
            idx for idx, value in enumerate(markdown_values) if "Run the model and read the summary table" in value
        )
        self.assertLess(step_3_index, summary_index)

        linear_chart_spec = json.loads(at.get("plotly_chart")[0].proto.spec)
        self.assertEqual(
            linear_chart_spec["layout"]["title"]["text"],
            "Linear Regression Concept: Tenure To Salary",
        )
        self.assertEqual(linear_chart_spec["layout"]["xaxis"]["title"]["text"], "Tenure (Years)")
        self.assertEqual(linear_chart_spec["layout"]["yaxis"]["title"]["text"], "Salary")

        intro_chart_spec = json.loads(at.get("plotly_chart")[1].proto.spec)
        self.assertEqual(
            intro_chart_spec["layout"]["title"]["text"],
            "Traditional Logistic S-Curve: Model Score To Probability",
        )
        self.assertEqual(
            intro_chart_spec["layout"]["xaxis"]["title"]["text"],
            "Promotion Readiness Score (model score)",
        )
        self.assertEqual(
            intro_chart_spec["layout"]["yaxis"]["title"]["text"],
            "Predicted Promotion Chance",
        )

        for chart in at.get("plotly_chart"):
            spec = json.loads(chart.proto.spec)
            layout = spec["layout"]

            self.assertEqual(layout["font"]["color"], app.EMPHASIS_TEXT)

            if "xaxis" in layout and "tickfont" in layout["xaxis"]:
                self.assertEqual(layout["xaxis"]["tickfont"]["color"], app.EMPHASIS_TEXT)
            if "xaxis" in layout and "title" in layout["xaxis"] and "font" in layout["xaxis"]["title"]:
                self.assertEqual(layout["xaxis"]["title"]["font"]["color"], app.EMPHASIS_TEXT)
            if "yaxis" in layout and "tickfont" in layout["yaxis"]:
                self.assertEqual(layout["yaxis"]["tickfont"]["color"], app.EMPHASIS_TEXT)
            if "yaxis" in layout and "title" in layout["yaxis"] and "font" in layout["yaxis"]["title"]:
                self.assertEqual(layout["yaxis"]["title"]["font"]["color"], app.EMPHASIS_TEXT)
            if "legend" in layout and "font" in layout["legend"]:
                self.assertEqual(layout["legend"]["font"]["color"], app.EMPHASIS_TEXT)

    def test_render_prescriptive_tab_uses_high_contrast_chart_text(self):
        app_dir = Path(__file__).resolve().parents[1]
        prescriptive_script = f"""
import sys
sys.path.insert(0, {str(app_dir)!r})
import app

df = app.load_data()
app.render_prescriptive_tab(df)
"""

        at = AppTest.from_string(prescriptive_script)
        at.run(timeout=60)

        self.assertEqual(len(at.exception), 0)
        self.assertEqual(len(at.get("plotly_chart")), 10)
        self.assertTrue(any("Phase 4: Prescriptive - Promotion Action Recommendations" in header.value for header in at.header))
        self.assertTrue(any("From prediction to recommendation" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("Recommended action table" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("Action rules" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("Fairness check" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("What evidence is missing?" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("Fairness and bias concerns" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("Business priority alignment" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("How HR combines the business-priority data" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("Deep dive by business priority" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("Final ranked promotion suggestion" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("Employee case study examples" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("Does the model reproduce old promotion bias?" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("Are high-potential employees being missed?" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("Business constraint check" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("promotion panel and managers have enough capacity" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("Final HR recommendation" in markdown.value for markdown in at.markdown))
        self.assertFalse(any("Board budget assumption" in slider.label for slider in at.slider))

        for chart in at.get("plotly_chart"):
            spec = json.loads(chart.proto.spec)
            layout = spec["layout"]

            self.assertEqual(layout["font"]["color"], app.EMPHASIS_TEXT)

            if "xaxis" in layout and "tickfont" in layout["xaxis"]:
                self.assertEqual(layout["xaxis"]["tickfont"]["color"], app.EMPHASIS_TEXT)
            if "xaxis" in layout and "title" in layout["xaxis"] and "font" in layout["xaxis"]["title"]:
                self.assertEqual(layout["xaxis"]["title"]["font"]["color"], app.EMPHASIS_TEXT)
            if "yaxis" in layout and "tickfont" in layout["yaxis"]:
                self.assertEqual(layout["yaxis"]["tickfont"]["color"], app.EMPHASIS_TEXT)
            if "yaxis" in layout and "title" in layout["yaxis"] and "font" in layout["yaxis"]["title"]:
                self.assertEqual(layout["yaxis"]["title"]["font"]["color"], app.EMPHASIS_TEXT)
            if "legend" in layout and "font" in layout["legend"]:
                self.assertEqual(layout["legend"]["font"]["color"], app.EMPHASIS_TEXT)

    def test_render_ai_adaptation_strategy_tab_explains_four_layers(self):
        app_dir = Path(__file__).resolve().parents[1]
        ai_strategy_script = f"""
import sys
sys.path.insert(0, {str(app_dir)!r})
import app

app.render_ai_adaptation_strategy_tab()
"""

        at = AppTest.from_string(ai_strategy_script)
        at.run(timeout=60)

        self.assertEqual(len(at.exception), 0)
        self.assertTrue(any("AI Adaptation Strategy" in header.value for header in at.header))
        self.assertTrue(any("4-layer AI adoption strategy" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("Layer 1: Give AI the business question" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("Layer 2: Let AI generate the Python dashboard script" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("Layer 3: Use AI to interpret aggregated patterns" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("Layer 4: Summarise a skill for consistent HR reports" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("Do not upload raw employee-level data" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("Example prompt" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("Sensitive data stays inside the company environment" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("Excel or Google Sheets" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("Power BI" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("Tableau" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("Streamlit / Python handled by analytics team" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("No-code / low-code BI tools" in markdown.value for markdown in at.markdown))
        self.assertTrue(any("Expected output by tool" in markdown.value for markdown in at.markdown))

    def test_streamlit_app_renders_redesigned_tabs_without_exceptions(self):
        app_path = Path(__file__).resolve().parents[1] / "app.py"

        at = AppTest.from_file(str(app_path))
        at.run(timeout=60)

        self.assertEqual(
            [tab.label for tab in at.tabs],
            ["Descriptive", "Diagnostic", "Predictive", "Prescriptive", "AI Adaptation Strategy"],
        )
        self.assertEqual(len(at.exception), 0)
        self.assertGreaterEqual(len(at.get("plotly_chart")), 10)
        self.assertGreaterEqual(len(at.markdown), 12)
        self.assertEqual(
            at.header[0].value,
            "Phase 1: Descriptive - Workforce Snapshot",
        )
        self.assertTrue(
            any("A denser executive view of workforce composition" in markdown.value for markdown in at.markdown)
        )


if __name__ == "__main__":
    unittest.main()
