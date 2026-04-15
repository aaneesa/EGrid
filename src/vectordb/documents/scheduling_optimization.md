# EGrid Scheduling & Load Optimization Protocols

## Overview
These protocols define the strategies for optimizing EV charging schedules across the EGrid network to maximize infrastructure utilization, minimize grid stress, and reduce operational costs.

## 1. Peak-Shifting Strategy

### Peak Hours Definition
| Region | Morning Peak | Evening Peak | Off-Peak Window |
|--------|-------------|--------------|-----------------|
| Chicago | 7:00-9:30 AM | 5:00-8:00 PM | 10:00 PM - 6:00 AM |
| Houston | 7:30-9:30 AM | 4:30-7:30 PM | 9:00 PM - 6:00 AM |
| New York | 7:00-10:00 AM | 5:00-8:30 PM | 10:30 PM - 6:00 AM |
| San Francisco | 7:30-9:30 AM | 5:00-8:00 PM | 10:00 PM - 6:00 AM |
| Los Angeles | 7:00-9:00 AM | 4:00-7:00 PM | 9:00 PM - 5:30 AM |

### Dynamic Pricing Tiers
| Time Period | Price Multiplier | Load_Score Target |
|-------------|-----------------|-------------------|
| Off-Peak | 0.6x base rate | Maximize utilization |
| Shoulder (±2hrs of peak) | 1.0x base rate | Maintain steady load |
| Peak | 1.5x base rate | Reduce to <60% capacity |
| Critical Peak (Load_Score > 70) | 2.0x base rate | Emergency demand reduction |

### Implementation Rules
1. Price signals must be communicated to users at least 1 hour before session start.
2. Users with active reservations are grandfathered at the rate at booking time.
3. Fleet/commercial accounts can negotiate fixed off-peak rates for guaranteed overnight charging windows.

## 2. Load Balancing Algorithms

### Station-Level Balancing
When multiple chargers exist at a single station:
1. **Round-Robin Assignment**: New sessions assigned to the charger with lowest cumulative daily energy delivery.
2. **Power Sharing**: When total station demand exceeds 80% of transformer capacity, implement proportional power reduction across all active sessions.
3. **Priority Queue**: Emergency vehicles and low-battery (<10% SoC) vehicles get priority access at full power.

### Network-Level Balancing
Across multiple stations in the same grid zone:
1. **Redirect Protocol**: When Station A reaches Load_Score > 70, the app should suggest Station B (if Load_Score < 50 and distance < 3 km).
2. **Predictive Pre-positioning**: Use ML demand predictions to pre-allocate charging slots 2 hours ahead based on forecasted Load_Score.
3. **Grid Zone Cap**: Total combined Load_Score across all stations on a single grid feeder must not exceed 200 without utility coordination.

## 3. Smart Scheduling Protocols

### Automated Session Management
1. **Flexible Start Windows**: Users can request "charge by" time instead of immediate start. System optimizes actual start within the window for grid benefit.
2. **Session Interruption**: Non-critical sessions (SoC > 50%) may be paused for up to 15 minutes during grid emergency events. Users must opt-in.
3. **Completion Notification**: Push alert when target SoC reached to minimize charger occupancy by fully charged vehicles.

### Fleet Scheduling
For commercial/fleet operators:
1. **Staggered Departure**: Schedule overnight fleet charging in 30-minute staggered groups to prevent simultaneous full-power draw.
2. **Priority Matrix**: Vehicles with earliest departure get charged first to highest SoC. Later departures charge to minimum required SoC first, then top up.
3. **Vehicle-to-Grid (V2G)**: Fleet vehicles with V2G capability scheduled to discharge during peak grid demand (5-8 PM) if not needed for operations.

## 4. Seasonal Adjustment Protocols

### Winter Adjustments (November - March, Cold Archetype Regions)
- Extend expected session durations by 25% in scheduling algorithms.
- Reduce available capacity per charger by 15% for battery pre-conditioning power.
- Increase scheduling buffer between sessions from 5 to 15 minutes for connector and cable management in cold conditions.

### Summer Adjustments (June - September, Heat Archetype Regions)
- Implement thermal throttling schedules: reduce DC Fast Charger max power by 20% between 12-4 PM.
- Increase maintenance windows frequency by 50%.
- Activate demand response programs with utility partners during heat wave events (>38°C for 3+ consecutive days).

## 5. Optimization KPIs
| Metric | Target | Formula |
|--------|--------|---------|
| Utilization Efficiency | >70% | Active charging hours / Available hours |
| Peak Reduction | >25% | (Unmanaged peak - Managed peak) / Unmanaged peak |
| Average Wait Time | <10 min | Sum of queue wait times / Total sessions |
| Grid Stress Index | <0.75 | Actual peak load / Transformer rated capacity |
| Revenue per kW | >$0.15 | Total revenue / Total energy delivered |
