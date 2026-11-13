"""ENGR 315 Group 30 - Q2: Dividends and P/E ratios."""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind, mannwhitneyu

# Load the same S&P 500 CSV used for our proposal.
data = pd.read_csv("data/constituents-financials.csv")
total_companies = len(data)

# Remove rows without a usable P/E ratio or dividend yield.
data["Price/Earnings"] = pd.to_numeric(data["Price/Earnings"], errors="coerce")
data["Dividend Yield"] = pd.to_numeric(data["Dividend Yield"], errors="coerce")
data = data.dropna(subset=["Price/Earnings", "Dividend Yield"])
data = data[(data["Price/Earnings"] > 0) & (data["Dividend Yield"] >= 0)]

# Compare companies that pay dividends to companies that do not.
payers = data[data["Dividend Yield"] > 0]["Price/Earnings"]
nonpayers = data[data["Dividend Yield"] == 0]["Price/Earnings"]

n1 = len(payers)
n2 = len(nonpayers)
if n1 < 2 or n2 < 2:
    raise ValueError("Both groups must have at least two companies.")

# Summary statistics for each group.
mean1, mean2 = payers.mean(), nonpayers.mean()
std1, std2 = payers.std(), nonpayers.std()
median1, median2 = payers.median(), nonpayers.median()
iqr1 = payers.quantile(0.75) - payers.quantile(0.25)
iqr2 = nonpayers.quantile(0.75) - nonpayers.quantile(0.25)

# Welch's t-test was the main comparison planned in our proposal.
t_stat, t_p = ttest_ind(payers, nonpayers, equal_var=False)

# Mann-Whitney is an extra check because P/E ratios can be skewed.
u_stat, u_p = mannwhitneyu(payers, nonpayers, alternative="two-sided")

# Effect sizes from our Phase I plan.
pooled_std = np.sqrt(((n1 - 1) * std1**2 + (n2 - 1) * std2**2) / (n1 + n2 - 2))
cohens_d = (mean1 - mean2) / pooled_std
rank_biserial = (2 * u_stat / (n1 * n2)) - 1

print("Q2: Dividend status compared with P/E ratio")
print("Total companies in CSV:", total_companies)
print("Companies used after filtering:", len(data))
print("\n                            Pays dividend    No dividend")
print(f"Number of companies:        {n1:12d}    {n2:11d}")
print(f"Mean P/E:                   {mean1:12.3f}    {mean2:11.3f}")
print(f"Median P/E:                 {median1:12.3f}    {median2:11.3f}")
print(f"Standard deviation:         {std1:12.3f}    {std2:11.3f}")
print(f"IQR:                        {iqr1:12.3f}    {iqr2:11.3f}")
print(f"\nMean difference (payers - nonpayers): {mean1 - mean2:.3f}")
print(f"Welch t-test: t = {t_stat:.4f}, p = {t_p:.6g}")
print(f"Mann-Whitney: U = {u_stat:.3f}, p = {u_p:.6g}")
print(f"Cohen's d = {cohens_d:.3f}")
print(f"Rank-biserial correlation = {rank_biserial:.3f}")

if t_p < 0.05:
    print("Welch conclusion: Reject H0; the mean P/E ratios differ.")
else:
    print("Welch conclusion: Fail to reject H0; no significant mean difference found.")

# Save the two plots described in our Phase I README.
os.makedirs("figures", exist_ok=True)

plt.figure(figsize=(7, 5))
plt.boxplot([payers, nonpayers])
plt.xticks([1, 2], ["Pays dividend", "No dividend"])
plt.yscale("log")
plt.ylabel("P/E ratio (log scale, unitless)")
plt.title("P/E Ratios by Dividend Status")
plt.tight_layout()
plt.savefig("figures/q2_pe_boxplot.png", dpi=150)
plt.close()

log_payers = np.log(payers)
log_nonpayers = np.log(nonpayers)
bins = np.linspace(np.log(data["Price/Earnings"].min()),
                   np.log(data["Price/Earnings"].max()), 21)

plt.figure(figsize=(7, 5))
plt.hist(log_payers, bins=bins, alpha=0.6, label="Pays dividend")
plt.hist(log_nonpayers, bins=bins, alpha=0.6, label="No dividend")
plt.xlabel("Natural log of P/E ratio (unitless)")
plt.ylabel("Number of companies")
plt.title("Distribution of Log(P/E) by Dividend Status")
plt.legend()
plt.tight_layout()
plt.savefig("figures/q2_log_pe_histogram.png", dpi=150)
plt.close()

print("\nSaved figures/q2_pe_boxplot.png")
print("Saved figures/q2_log_pe_histogram.png")