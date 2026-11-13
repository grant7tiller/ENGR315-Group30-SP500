# Exploring Company Size, Dividends, and Stock Prices in the S&P 500

**ENGR 315 – Computational Methods | Team: Group 30**

**Contributors:** Aden Pierce, Grant Tiller, Sawyer Dole

---

## Objective and Motivation

We chose the S&P 500 because we are interested in how basic company financials relate to stock prices and valuation. The project also gives us a chance to use Python on real data instead of a made-up example. Our goal is to compare companies at one point in time and see which relationships hold up under testing. We are **not** trying to predict which stocks to buy.

As college students preparing to enter the workforce, we find this project personally interesting because it connects our engineering coursework with financial questions that will become more relevant as we begin earning salaries and planning for the future. Studying company size, earnings, dividends, and stock prices helps us understand the financial terms we encounter in discussions about businesses and investing. For Sawyer, this also connects with an interest in entrepreneurship and eventually owning a business. For our team and peers, the project makes statistics and Python more tangible by applying them to recognizable companies. We want to become more confident interpreting financial data and evaluating claims critically, while recognizing that these analyses alone cannot determine whether a stock is a good investment.

### Dataset

| Item | Details |
|---|---|
| Source | DataHub, *S&P 500 Companies with Financial Information* [1] |
| File | `constituents-financials.csv` (503 companies, 14 columns, ~95 KB) |
| Origin | Company list compiled from Wikipedia; financial measures gathered from Yahoo Finance using Python tools |
| Type | A single snapshot in time (**not** a historical time series) |
| Columns used | Price, Earnings/Share, Price/Earnings, Dividend Yield, Market Cap, 52 Week High |
| Direct download | https://datahub.io/core/s-and-p-500-companies-financials/_r/-/data/constituents-financials.csv |

A copy of the CSV is stored in [`data/`](data/) so the analysis can be reproduced.

### Questions, Expected Form of Answers, and Benefits

| # | Question | Form of the expected answer | Potential benefit |
|---|---|---|---|
| **Q2** | How do P/E ratios differ between dividend-paying and non-dividend-paying companies? | Group sizes, medians, and means; a Welch t-test p-value; a Mann–Whitney p-value; an effect size | Shows whether dividend policy goes along with how highly the market values a company's earnings |
| **Q3** | How does company size relate to proximity to the 52-week stock-price high? | Mean and median % of 52-week high for the larger and smaller halves; Welch t-test and Mann–Whitney p-values; an effect size; Spearman ρ | Shows whether large companies have held up better against their recent highs than smaller ones |
| **Q4** | How does earnings per share relate to current share price? | A fitted line (slope, intercept), R², Pearson r, Spearman ρ, and how the fit changes when influential points are removed | Tests how much of a share price is explained by earnings alone, and how much is left over |

**Questions we considered but did not select**
- **Q1:** How strongly is EBITDA related to market capitalization? (Feasible, but not selected.)
- **Q5:** How do changes in interest rates relate to five-year stock returns? (Not feasible: the dataset has no historical prices, interest rates, or dates.)

---

## Introduction / Context

Definitions of the financial terms used in this project:

- **Share price (Price):** what one share of the company's stock costs.
- **Earnings per share (EPS):** the company's profit divided by its number of shares. A negative value means the company reported a loss.
- **Price/Earnings ratio (P/E):** Price ÷ EPS, or how many dollars investors pay for each $1 of yearly earnings. A higher P/E usually means investors expect more growth.
- **Dividend Yield:** yearly dividend per share ÷ share price, as a percentage. A yield of 0 means the company pays no dividend.
- **Market capitalization (Market Cap):** share price × number of shares, a common measure of company size.
- **52 Week High:** the highest price the stock reached in the previous year.

Because P/E = Price ÷ EPS, Price is equal to P/E × EPS. This ties Q4 to Q2. In Q4, the slope of Price vs. EPS acts like a "typical" P/E across all companies, and the scatter around the line comes from differences in P/E between companies.

---

## Implementation Details

### General workflow (applies to all questions)

1. Load `constituents-financials.csv` with **pandas**.
2. Check data types and count missing values in each column.
3. Apply the filtering rules for each question (listed below) and report the number of companies (**n**) used in each analysis.
4. Compute the comparison variables with **pandas/NumPy**.
5. Run the statistical tests and fits with **SciPy** (and **statsmodels** where noted).
6. Make the figures with **Matplotlib** and save them to [`figures/`](figures/).
7. Use a significance level of **α = 0.05** and report **effect sizes** along with p-values.

**Python packages**

| Package | Purpose |
|---|---|
| `pandas` | Load, clean, filter, and group the data |
| `numpy` | Numerical calculations |
| `matplotlib` | All plots |
| `scipy.stats` | `linregress`, `pearsonr`, `spearmanr`, `ttest_ind` (Welch), `mannwhitneyu` |
| `statsmodels` | OLS regression with confidence intervals; influence diagnostics (Cook's distance) for Q4 |

---

### Q2: Dividend status vs. P/E ratio

**Data preparation**
- Label each company a **dividend payer** if Dividend Yield > 0, and a **non-payer** if Dividend Yield = 0.
- Keep only valid, positive P/E values (P/E is not meaningful when earnings are zero or negative).
- Report n for each group, and the number of companies removed by filtering.

**Metrics**
- n, mean, median, standard deviation, and interquartile range (IQR) of P/E for each group
- **Welch's t-test** (does not assume equal variances): t statistic and p-value
- **Mann–Whitney U test** as a check, because P/E is strongly right-skewed: U statistic and p-value
- **Effect size:** Cohen's d (for the t-test) and rank-biserial correlation (for Mann–Whitney)
- *Added after initial analysis:* **Welch's t-test on log(P/E)** as a robustness check, because the raw P/E values turned out to be heavily skewed by a few extreme outliers

**Tools:** `scipy.stats.ttest_ind(..., equal_var=False)`, `scipy.stats.mannwhitneyu`, `numpy.log`

**Plots**
- Side-by-side **boxplots** of P/E by dividend status (log-scaled y-axis)
- Overlaid **histograms** of log(P/E) for the two groups, to show the shape and skew of each distribution
---

### Q3: Company size vs. proximity to the 52-week high

**Data preparation**
- Keep companies with valid Price, 52 Week High, and Market Cap.
- Compute **% of 52-week high = 100 × Price / 52 Week High**.
- Split companies into a **larger half** and a **smaller half** at the median Market Cap.
- Report n for each half.

**Metrics**
- n, mean, median, standard deviation, and IQR of % of 52-week high for each half
- **Welch's t-test** and **Mann–Whitney U test** (statistic and p-value for each)
- **Effect size:** Cohen's d and rank-biserial correlation
- **Spearman ρ** between Market Cap and % of 52-week high, using every company (no split), as a supporting check that keeps the full size information

**Tools:** `scipy.stats.ttest_ind(..., equal_var=False)`, `scipy.stats.mannwhitneyu`, `scipy.stats.spearmanr`

**Plots**
- Side-by-side **boxplots** of % of 52-week high for the smaller and larger halves
- **Scatter plot** of log(Market Cap) vs. % of 52-week high

---

### Q4: Earnings per share vs. share price

**Data preparation**
- Remove rows with missing Earnings/Share or Price.
- **Keep negative EPS values**, so companies reporting losses are included.
- Report n.

**Metrics**
- **Simple linear regression** of Price on EPS: slope, intercept, and **R²**
- **Pearson r** (with p-value) and **Spearman ρ** (less affected by extreme values)
- **Residuals** (actual Price − predicted Price) to judge how well a straight line fits
- **Influence diagnostics:** Cook's distance, to find the companies with the most influence on the fitted line
- **Sensitivity check:** fit the line again without the most influential points and compare the slope and R²

**Tools:** `scipy.stats.linregress`, `scipy.stats.spearmanr`, `statsmodels.api.OLS` with `get_influence()`

**Plots**
- **Scatter plot** of EPS (x) vs. Price (y) with the fitted line, with extreme companies labeled
- **Residual plot** (residual vs. EPS)
- Scatter plots of the fit **with and without** the influential points, side by side

Log axes are not used here, because negative EPS values cannot be log-transformed.

---

### Preliminary plots (from the proposal)

These quick exploratory views show that the data supports each question. Fitted models and test results will be added in later phases.

<!-- Upload the proposal figure images to figures/ and update the file names below if they differ -->
| Q4: EPS vs. share price | Q2: P/E by dividend status | Q3: % of 52-week high by size |
|---|---|---|
| ![EPS vs price](figures/prelim_eps_vs_price.png) | ![P/E by dividend](figures/prelim_pe_by_dividend.png) | ![52-week high by size](figures/prelim_52wk_by_size.png) |

### Limitations

- The CSV has missing values (including Earnings/Share, Price, and P/E), so sample sizes differ by question.
- The data is one snapshot, so we cannot infer cause and effect.
- Differences between industries and a few extreme financial values may influence the results. We will discuss these limitations instead of treating any relationship as universal.

*Screenshots of key code, block diagrams, and the top-level script will be added in the coming phases.*

---
### Results ###

Results (Answers to the Questions)
Q2: How do P/E ratios differ between dividend-paying and non-dividend-paying companies?

We completed Q2 using the S&P 500 dataset and the methods described above. Out of 503 companies, 458 had a usable positive P/E ratio and a nonnegative dividend yield. The other 45 companies were removed because they were missing data or had a P/E ratio of zero or less, which means they were not profitable and their P/E ratio is not meaningful. Our results therefore apply to profitable companies only. We grouped companies by whether their Dividend Yield was greater than zero.

Measurement	Pays dividend	No dividend
Number of companies	380	78
Mean P/E	28.928	124.077
Median P/E	22.473	27.190
Standard deviation	34.522	610.315
IQR	15.485	27.317

For the Welch t-test, the null hypothesis was that the two groups have the same population mean P/E ratio. Our alternative was that the means are different. We used a significance level of 0.05 for all tests.

Welch t-test: t = -1.3764, p = 0.172672. We fail to reject the null hypothesis because p is greater than 0.05. This test did not find a statistically significant difference in the group means.
Mann–Whitney U test: U = 11901, p = 0.00612574. We reject the null hypothesis. Non-dividend-paying companies tend to have higher P/E ratios than dividend-paying companies.
Welch t-test on log(P/E) (robustness check): t = -2.6974, p = 0.00840847. We reject the null hypothesis. We added this test after seeing that the P/E values were heavily skewed (the no-dividend group's standard deviation is about 18 times larger than the dividend group's). Taking the natural log reduces the effect of extreme values, which is a standard approach for skewed data like this.
Effect sizes: rank-biserial correlation = -0.197 and Cohen's d = -0.376. The negative signs mean dividend-paying companies tend to have lower P/E values. We treat the rank-biserial correlation as our main effect size because it matches the Mann–Whitney test and is not affected much by outliers; it indicates a small effect. Cohen's d depends on the standard deviations, which the outliers inflate, so it is less reliable here.

The median P/E was lower for dividend-paying companies (22.473 versus 27.190). The mean for non-dividend-paying companies was much higher, but its standard deviation was also very large. A few extreme P/E values in that group had a strong effect on the mean and standard deviation, which weakened the raw Welch t-test. Both outlier-resistant methods (the Mann–Whitney test and the log-scale Welch t-test) found a significant difference, so we conclude that the two groups' P/E ratios do differ.

Figure 1. P/E ratios by dividend status. Boxplots compare the two groups using a logarithmic y-axis. The non-dividend group has a higher median and several especially large outliers.

P/E boxplots by dividend status

Figure 2. Distribution of log(P/E) by dividend status. The histograms show the distributions after taking the natural log of P/E, which makes the wide range of values easier to view. The bars are company counts, and the dividend-paying group has many more companies.

Histogram of log P/E by dividend status

Running the Q2 Python code

Keep Q2 Dividends.py in the main project folder (or in a subfolder one level down), with the CSV saved at data/constituents-financials.csv. The script finds the data folder relative to its own location, so it can be run from any terminal folder. Install the required packages if needed:

bash
python -m pip install numpy pandas scipy matplotlib

Then run:

bash
python "Q2 Dividends.py"

On Windows, py can be used in place of python. The program prints the statistics and test results, then saves both PNG graphs in the figures folder.

Command-line output from Q2
text
Q2: Dividend status compared with P/E ratio
Total companies in CSV: 503
Companies used after filtering: 458
Companies removed (missing data or P/E <= 0): 45

                            Pays dividend    No dividend
Number of companies:                 380             78
Mean P/E:                         28.928        124.077
Median P/E:                       22.473         27.190
Standard deviation:               34.522        610.315
IQR:                              15.485         27.317

Mean difference (payers - nonpayers): -95.149
Welch t-test: t = -1.3764, p = 0.172672
Mann-Whitney: U = 11901.000, p = 0.00612574
Welch t-test on log(P/E): t = -2.6974, p = 0.00840847
Cohen's d = -0.376
Rank-biserial correlation = -0.197

Conclusions (alpha = 0.05):
Welch t-test: Fail to reject H0; no significant difference in mean P/E.
Mann-Whitney: Reject H0; Non-dividend payers tend to have higher P/E ratios.
Welch t-test on log(P/E): Reject H0; mean log(P/E) differs between groups.
Note: Both outlier-resistant methods (Mann-Whitney and the log-scale t-test) find a significant difference. The raw t-test does not, because a few extreme P/E values inflate the standard deviation of the non-dividend group.

Saved figures/q2_pe_boxplot.png
Saved figures/q2_log_pe_histogram.png
Conclusions

For Q2, among profitable S&P 500 companies, non-dividend-paying companies tend to have significantly higher P/E ratios than dividend-paying companies (Mann–Whitney p = 0.006; log-scale Welch t-test p = 0.008), although the effect is small (rank-biserial correlation = -0.197). The Welch t-test on the raw P/E values did not find a significant difference in means (p = 0.173) because a few extreme values in the non-dividend group greatly inflate its mean and standard deviation. Because the two outlier-resistant methods agree, we conclude that the groups do differ. These results show a relationship between dividend status and P/E ratios, but they do not show that paying a dividend causes a company's valuation to change. Another factor, such as industry sector, may explain part of the relationship: for example, growth-focused companies often do not pay dividends and tend to have higher P/E ratios.

We have completed one question/method pair for Phase II. Questions Q3 and Q4 are planned for the final project and have not yet been analyzed with the full proposed methods.

References / Source Files

[1] DataHub, "S&P 500 Companies with Financial Information," dataset and documentation, https://datahub.io/core/s-and-p-500-companies-financials (accessed Oct. 22, 2026).

[2] SciPy documentation, scipy.stats, https://docs.scipy.org/doc/scipy/reference/stats.html

[3] pandas documentation, https://pandas.pydata.org/docs/

[4] Matplotlib documentation, https://matplotlib.org/stable/

[5] statsmodels documentation, https://www.statsmodels.org/stable/

#Q3 and Q4 to be completed later