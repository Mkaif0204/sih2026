import pandas as pd

data = {
    "Job_Role": ["AI Engineer", "Full Stack Dev", "Cloud Architect", "Data Analyst", "Cybersecurity Analyst", "Blockchain Dev"],
    "Top_Skill": ["GenAI / PyTorch", "Next.js / React", "Kubernetes / AWS", "Pandas / SQL", "Zero Trust", "Solidity / Web3"],
    "Avg_Salary_LPA": [18.5, 12.0, 22.0, 8.5, 15.0, 16.0],
    "Open_Roles": [1240, 3500, 890, 2100, 1100, 450],
    "Growth_Projected_2026_Pct": [92, 85, 88, 75, 90, 82]
}

df = pd.DataFrame(data)
df.to_csv("industry_data.csv", index=False)
print("industry_data.csv created successfully!")