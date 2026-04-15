# EGrid Charger Placement & Infrastructure Siting Guidelines

## Overview
These guidelines govern the selection and evaluation of new EV charging infrastructure locations based on demand data analysis, regional characteristics, and grid capacity constraints.

## 1. Demand-Driven Placement Criteria

### Primary Selection Factors
1. **Load_Score Threshold**: New charger deployment is triggered when any station consistently maintains Load_Score > 70 for more than 14 consecutive days.
2. **Vehicle_Count Growth**: Locations showing >20% month-over-month growth in Vehicle_Count require proactive capacity planning.
3. **Geographic Coverage Gap**: Any urban area with population density >5,000/sq.mi. lacking a charging station within 3 miles qualifies for new installation evaluation.

### Charger Type Selection Matrix
| Demand Pattern | Recommended Charger | Rationale |
|---------------|-------------------|-----------|
| Load_Score > 70, Avg Duration < 1hr | DC Fast Charger (Level 3) | High throughput needed, short dwell time |
| Load_Score 40-70, Avg Duration 1-4hrs | Level 2 (7.2-19.2 kW) | Moderate demand, workplace/retail setting |
| Load_Score < 40, Avg Duration > 4hrs | Level 2 (3.3-7.2 kW) | Overnight/residential use case |
| All patterns, Transit hub | DC Fast Charger + Level 2 mix | Mixed use requires flexible infrastructure |

## 2. Proximity & Spacing Rules

### Urban Dense Networks (New York, San Francisco)
- **Minimum Spacing**: 500 meters between high-output (>50kW) charging stations to prevent localized substation brownouts.
- **Maximum Spacing**: 2 kilometers between any charging points to ensure coverage density.
- **Substation Load Limit**: No single substation should serve more than 4 DC Fast Charging stations without a dedicated feeder.

### Suburban/Spread Networks (Houston, Los Angeles)
- **Minimum Spacing**: 1 kilometer between DC Fast Charger installations.
- **Maximum Spacing**: 5 kilometers between any charging points along major corridors.
- **Solar Co-location**: Prioritize sites with existing or planned solar canopy infrastructure for self-generation.

## 3. Site Evaluation Scoring

Each candidate site is evaluated on a 100-point scale:

| Factor | Weight | Scoring Criteria |
|--------|--------|-----------------|
| Demand Score | 30 pts | Based on nearest station Load_Score and growth trend |
| Grid Capacity | 25 pts | Available transformer capacity, feeder line rating |
| Accessibility | 20 pts | Proximity to major roads, ADA compliance, parking availability |
| Land/Lease Cost | 15 pts | Cost per kW of installed capacity relative to regional average |
| Future Growth | 10 pts | Projected EV adoption rate for the zip code (5-year forecast) |

**Minimum Viable Score: 65/100** for project approval.

## 4. Grid Interconnection Requirements

### Power Capacity by Charger Type
| Charger Type | Power per Unit | Typical Cluster Size | Total Site Demand |
|-------------|---------------|---------------------|-------------------|
| Level 2 (Standard) | 7.2 kW | 4-8 units | 29-58 kW |
| Level 2 (High) | 19.2 kW | 4-6 units | 77-115 kW |
| DC Fast Charger | 50-150 kW | 2-4 units | 100-600 kW |
| Ultra-Fast DC | 350 kW | 1-2 units | 350-700 kW |

### Requirements
1. Sites requiring >100 kW must have dedicated utility metering.
2. Sites requiring >250 kW should include on-site energy storage (minimum 100 kWh battery buffer).
3. All new installations must include smart load management systems capable of dynamic power sharing.

## 5. Regional Specific Siting Priorities

### Chicago
- Focus on covered/enclosed charging to mitigate extreme cold impact on user experience.
- Prioritize locations near CTA transit hubs for multimodal integration.

### Houston
- Solar canopy installations mandatory for new DC Fast Charger sites.
- Flood zone assessment required — all electrical infrastructure must be elevated per FEMA guidelines.

### San Francisco
- Space-constrained siting requires vertical/stacked charger configurations.
- Seismic compliance for all mounting and electrical infrastructure.

### New York
- Curbside charging integration with municipal parking infrastructure.
- Con Edison coordination required for any installation >50 kW. 

### Los Angeles
- Freeway corridor placement along I-10, I-405, I-110 for long-distance EV support.
- Air quality improvement zones receive priority permitting.
