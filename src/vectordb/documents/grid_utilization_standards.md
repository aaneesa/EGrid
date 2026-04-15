# EGrid Grid Utilization & Efficiency Standards

## Overview
These standards define operational thresholds and strategic actions for grid utilization management across the EGrid network. Each protocol is triggered by specific data patterns observed in station telemetry.

## Protocol GS-EFF-01: Phantom Load Detection
**Trigger:** Load_Score > 25 AND Energy Consumed = 0.0 kWh
**Severity:** Warning
**Example:** Station_101 New York — Load registered but no energy transfer recorded.

### Strategic Actions
1. Flag the station for immediate hardware diagnostic and reset.
2. Investigate potential connectivity failure between the charger and billing system.
3. Check for metering equipment malfunction (current transformer or energy meter drift).
4. If phantom load persists for more than 3 consecutive sessions, escalate to maintenance priority queue.
5. Cross-reference with Vehicle_Count data — if vehicles are present but energy is zero, the issue is likely charger-side.

## Protocol GS-CAP-02: Optimization Zone Management
**Trigger:** Load_Score between 40 and 70
**Severity:** Advisory
**Example:** Station_10 San Francisco — Moderate load indicating optimization opportunity.

### Strategic Actions
1. **Peak-Shifting via Dynamic Pricing**: Implement time-of-use pricing to redistribute demand from peak (8-10 AM, 5-8 PM) to off-peak hours.
2. **Load Balancing**: If multiple chargers exist at the station, distribute sessions across units to prevent single-unit overload.
3. **Demand Response Integration**: Enroll station in utility demand response programs for grid stabilization revenue.
4. **Predictive Alert**: When a station trends from <40 toward 60+ consistently over 7 days, issue a capacity expansion pre-alert.
5. **User Notification**: Push notifications to registered users suggesting optimal charging times based on historical load patterns.

## Protocol GS-CRIT-03: Critical Expansion Zone
**Trigger:** Load_Score > 70
**Severity:** Critical
**Example:** Station_1 Chicago — High sustained load indicating infrastructure at capacity.

### Strategic Actions
1. **Immediate**: Initiate Level 3 (DC) Fast Charger feasibility study for the location.
2. **Short-term (30 days)**: Deploy temporary mobile charging units to relieve pressure.
3. **Medium-term (90 days)**: Begin permitting process for additional permanent charging infrastructure.
4. **Capacity Target**: Expand to handle 150% of current peak Load_Score to provide headroom for growth.
5. **Grid Assessment**: Commission utility-side assessment for transformer capacity, feeder line ratings, and potential substation upgrades required.

## Protocol GS-MAINT-04: Preventive Maintenance Scheduling
**Trigger:** Any station with >500 cumulative charging sessions OR >180 days since last service
**Severity:** Routine

### Strategic Actions
1. Schedule non-peak maintenance windows (typically 11 PM - 5 AM).
2. Perform connector wear inspection, cable integrity check, and cooling system flush.
3. Update firmware and calibrate metering equipment.
4. Verify communication link integrity with central management system.

## Efficiency KPIs
| KPI | Target | Measurement |
|-----|--------|-------------|
| Average Utilization Rate | 60-75% | Sessions per charger per day |
| Uptime | >98% | Hours available / Total hours |
| Energy Efficiency | >92% | Energy delivered / Energy drawn from grid |
| Peak-to-Average Ratio | <1.8 | Peak hour load / Average daily load |
