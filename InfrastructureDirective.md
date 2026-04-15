# EGrid Universal Infrastructure Directive

> **Global Strategic Framework for Multi-City EV Grid Management**
>
> *Version 2.0 — April 2026 | Authorized for EGrid Agentic System*

---

## 1. Environmental Archetype Protocols

The system maps incoming telemetry (Temperature / Location) to the following regional mandates:

### `[ARCH-COLD]` Continental Archetype — Chicago, NY, SF (Winter)

| Parameter | Value |
|-----------|-------|
| **Trigger** | Ambient Temperature < 10°C |
| **Affected Stations** | Station_104 (Chicago), Station_1 (Chicago), Station_391 (NY Winter) |

**Mandates:**
- Thermal management must be prioritized across all charging sessions.
- If `Load_Score > 45` (as observed at Station_104 Chicago), a **10% voltage boost** is authorized for battery pre-conditioning and heating.
- Level 2 chargers must reduce max output by 15% below 0°C to mitigate lithium plating risk.
- Expected session durations increase by 20–35% under sub-zero conditions; scheduling algorithms must account for extended occupancy.

### `[ARCH-HEAT]` Humid / Arid Archetype — Houston, LA, NY (Summer)

| Parameter | Value |
|-----------|-------|
| **Trigger** | Ambient Temperature > 30°C |
| **Affected Stations** | Station_101 (Houston @ 38.9°C), Station_100 (Houston), Station_327 (Houston) |

**Mandates:**
- High `Load_Score` stations in hot climates require **active liquid cooling** for charging equipment.
- **Throttling is mandatory** when `Load_Score > 80` to prevent grid-side transformer fatigue — reduce to 70% of rated capacity.
- Between 12:00 PM and 4:00 PM during heat events (>35°C), DC Fast Chargers must implement dynamic queuing to prevent simultaneous high-draw sessions.
- Solar-to-EV direct buffering should be prioritized during peak solar hours (10 AM – 2 PM) in Sun Belt regions.

---

## 2. Grid Utilization & Efficiency Logic

| Protocol ID | Data Pattern | Strategic Action |
|:-----------:|:-------------|:-----------------|
| **GS-EFF-01** | `Load_Score > 25` & `Energy = 0.0` | **Phantom Load Alert:** (e.g., Station_101 NY). Flag for immediate hardware reset; investigate potential connectivity failure or metering malfunction. |
| **GS-CAP-02** | `Load_Score 40 – 70` | **Optimization Zone:** (e.g., Station_10 SF). Implement Peak-Shifting logic via dynamic pricing. Enroll station in utility demand response programs. |
| **GS-CRIT-03** | `Load_Score > 70` | **Expansion Zone:** (e.g., Station_1 Chicago @ 82.30). Initiate Level 3 (DC) Fast Charger feasibility study. Deploy temporary mobile units within 48 hours if service failures occur. |
| **GS-MAINT-04** | `Sessions > 500` or `180+ days since service` | **Preventive Maintenance:** Schedule non-peak maintenance window (11 PM – 5 AM). Perform connector inspection, cable integrity check, and cooling system flush. |

---

## 3. Capacity Expansion Trigger Matrix

| Trigger Level | Condition | Required Action | Timeline |
|:-------------:|:----------|:----------------|:---------|
| **Level 1 — Monitor** | `Load_Score 50–60` for 7+ days | Add to watchlist, increase monitoring frequency | Ongoing |
| **Level 2 — Evaluate** | `Load_Score 60–70` for 14+ days | Commission formal capacity assessment | 30 days |
| **Level 3 — Expand** | `Load_Score > 70` for 7+ days | Initiate expansion planning and procurement | 60–90 days |
| **Level 4 — Emergency** | `Load_Score > 85` or service failures | Deploy temporary mobile charging units immediately | 48 hours |

### Expansion Sizing Formula

```
Required_New_Capacity = Current_Peak_Load × Growth_Factor × Safety_Margin − Existing_Capacity

Where:
  Current_Peak_Load  = Max Load_Score (last 30 days), converted to kW
  Growth_Factor      = 1 + (Annual EV adoption rate / 100)  →  typically 1.15 to 1.35
  Safety_Margin      = 1.25  (25% headroom for demand spikes)
```

---

## 4. Regional Specific Logistics

### Houston / Los Angeles — Sun Belt
- Focus on **Solar-to-EV buffering** to handle high afternoon temperatures (Station_100 Houston @ 10:00 AM shows early peak onset).
- Solar canopy installations are **mandatory** for all new DC Fast Charger sites.
- Flood zone assessment required (Houston) — all electrical infrastructure must be elevated per FEMA guidelines.

### New York / San Francisco — Coastal Dense
- Strict **500m proximity rule** between high-output units (>50 kW) to prevent localized substation brownouts.
- Maximum 4 DC Fast Charging stations per single grid feeder without dedicated transformer.
- Space-constrained siting (SF) requires vertical/stacked charger configurations.

### Chicago — Continental
- Prioritize covered/enclosed charging infrastructure to mitigate extreme cold on user experience.
- Winter multiplier of **1.2×** must be applied to all capacity planning calculations.
- Locations near CTA transit hubs receive priority for multimodal integration.

---

## 5. Scheduling & Dynamic Pricing Policy

| Time Period | Price Multiplier | Target Effect |
|:------------|:----------------:|:--------------|
| **Off-Peak** (10 PM – 6 AM) | 0.6× base rate | Maximize overnight utilization |
| **Shoulder** (±2 hrs of peak) | 1.0× base rate | Maintain steady load |
| **Peak** (8–10 AM, 5–8 PM) | 1.5× base rate | Reduce demand to <60% capacity |
| **Critical Peak** (`Load_Score > 70`) | 2.0× base rate | Emergency demand reduction |

**Load Balancing Rules:**
- When Station A reaches `Load_Score > 70`, redirect users to Station B if `Load_Score < 50` and distance < 3 km.
- Use ML demand predictions to pre-allocate charging slots **2 hours ahead** based on forecasted `Load_Score`.
- Combined `Load_Score` across all stations on a single grid feeder must not exceed **200** without utility coordination.

---

## 6. Current Network Priority Assessment

Based on live EGrid telemetry analysis:

| Priority | City | Station | Max Load | Recommended Action |
|:--------:|:-----|:--------|:--------:|:-------------------|
| 🔴 1 | **Chicago** | Station_1 | 82.30 | DC Fast Charger deployment + transformer capacity assessment |
| 🔴 2 | **Houston** | Station_101 | 74.50 | Solar-integrated charging hub + active cooling retrofit |
| 🟡 3 | **San Francisco** | Station_10 | 58.20 | Level 2 expansion + peak-shifting via dynamic pricing |
| 🟡 4 | **New York** | Station_101 | 52.10 | Phantom load investigation (GS-EFF-01) → hardware fix first |
| 🟢 5 | **Los Angeles** | Station_88 | 41.30 | Freeway corridor deployment along I-10/I-405 |

---

> **End of Directive** — Authorized for EGrid Agentic Infrastructure Planning System
>
> This document serves as the primary knowledge source for RAG-augmented agent reasoning.
> All protocols, thresholds, and strategic actions defined herein are enforced by the agent workflow.