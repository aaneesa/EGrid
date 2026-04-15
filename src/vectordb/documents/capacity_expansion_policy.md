# EGrid Capacity Expansion & Infrastructure Investment Policy

## Overview
This policy defines when, where, and how EGrid infrastructure should be expanded based on demand analytics, grid capacity, and financial feasibility assessments. All expansion decisions must be data-driven and traceable to specific telemetry patterns.

## 1. Expansion Trigger Matrix

| Trigger Level | Condition | Required Action | Timeline |
|--------------|-----------|-----------------|----------|
| **Level 1 - Monitor** | Load_Score 50-60 for 7+ days | Add to watchlist, increase monitoring frequency | Ongoing |
| **Level 2 - Evaluate** | Load_Score 60-70 for 14+ days | Commission formal capacity assessment | 30 days |
| **Level 3 - Expand** | Load_Score > 70 for 7+ days | Initiate expansion planning and procurement | 60-90 days |
| **Level 4 - Emergency** | Load_Score > 85 OR service failures | Deploy temporary mobile units immediately | 48 hours |

## 2. Expansion Sizing Formula

### Capacity Calculation
```
Required_New_Capacity = Current_Peak_Load × Growth_Factor × Safety_Margin - Existing_Capacity

Where:
- Current_Peak_Load = Max Load_Score observed in last 30 days (converted to kW)
- Growth_Factor = 1 + (Annual EV adoption rate for region / 100) = typically 1.15 to 1.35
- Safety_Margin = 1.25 (25% headroom for demand spikes)
- Existing_Capacity = Sum of rated capacity of all operational chargers at site
```

### Example Calculation
Station_1 Chicago (Load_Score = 82.30):
- Current Peak Load: ~120 kW equivalent
- Growth Factor: 1.25 (Chicago metro EV growth rate ~25%/year)
- Safety Margin: 1.25
- Existing Capacity: 2 × Level 2 (19.2 kW) = 38.4 kW
- Required New Capacity: (120 × 1.25 × 1.25) - 38.4 = **149.1 kW**
- Recommendation: Install 1 × 150 kW DC Fast Charger

## 3. Financial Feasibility Thresholds

### Cost Benchmarks (2024 USD)
| Infrastructure Component | Cost Range | Lifetime |
|------------------------|-----------|----------|
| Level 2 Charger (installed) | $3,000 - $7,500 | 8-10 years |
| DC Fast Charger 50kW (installed) | $28,000 - $50,000 | 7-10 years |
| DC Fast Charger 150kW (installed) | $75,000 - $150,000 | 7-10 years |
| Transformer Upgrade | $25,000 - $100,000 | 20+ years |
| Battery Storage 100kWh | $40,000 - $60,000 | 10-15 years |
| Solar Canopy per parking space | $5,000 - $8,000 | 25 years |

### ROI Requirements
1. **Minimum Payback Period**: 7 years for Level 2, 5 years for DC Fast (higher utilization assumed).
2. **Minimum IRR**: 12% over equipment lifetime.
3. **Utilization Threshold for Approval**: Projected utilization must exceed 40% within 6 months of commissioning.

### Revenue Model
```
Annual_Revenue = Daily_Sessions × Avg_Energy_per_Session × Price_per_kWh × 365 × Utilization_Rate

Break-Even Point = Total_Installation_Cost / (Annual_Revenue - Annual_Operating_Cost)
```

## 4. Phased Expansion Strategy

### Phase 1: Quick Wins (0-30 days)
- Software optimization: Implement dynamic pricing and load balancing at existing stations.
- Expected result: 15-20% reduction in peak Load_Scores without any hardware.

### Phase 2: Incremental Hardware (31-90 days)
- Add Level 2 chargers at stations in GS-CAP-02 (Optimization Zone, Load_Score 40-70).
- Deploy smart load management controllers for power sharing.

### Phase 3: Major Infrastructure (91-180 days)
- Install DC Fast Chargers at GS-CRIT-03 stations (Load_Score > 70).
- Commission transformer upgrades where required.
- Install battery energy storage at sites with constrained grid capacity.

### Phase 4: Network Growth (181-365 days)
- Open new station locations based on geographic coverage gap analysis.
- Integrate solar generation at suitable sites (Houston, LA priority).
- Deploy vehicle-to-grid (V2G) capability at fleet charging locations.

## 5. Regional Expansion Priorities

Based on current EGrid telemetry data analysis:

| Priority | City | Justification | Recommended Action |
|----------|------|---------------|-------------------|
| 1 | **Chicago** | Station_1 Load_Score 82.30 (Critical) | DC Fast Charger deployment + transformer assessment |
| 2 | **Houston** | Station_101 high temp stress + growing demand | Solar-integrated charging hub |
| 3 | **San Francisco** | Station_10 in Optimization Zone | Level 2 expansion + peak-shifting |
| 4 | **New York** | Phantom load issues at Station_101 | Hardware fix first, then capacity review |
| 5 | **Los Angeles** | Moderate load, freeway corridor gaps | Corridor charging deployment along I-10/I-405 |

## 6. Approval Workflow
1. **Data Trigger** → Automated alert from monitoring system.
2. **Analyst Review** → Validate data, confirm trends, estimate costs.
3. **Feasibility Report** → Generate structured expansion recommendation.
4. **Stakeholder Approval** → City/utility/property owner coordination.
5. **Procurement** → Equipment ordering and contractor selection.
6. **Deployment** → Installation, testing, and commissioning.
7. **Validation** → 30-day post-deployment Load_Score monitoring to confirm improvement.
