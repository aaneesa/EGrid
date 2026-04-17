# EGrid Environmental Archetype Protocols

## Overview
The EGrid system classifies operational environments into distinct archetypes based on real-time telemetry data (temperature, humidity, location). Each archetype triggers specific infrastructure management mandates to ensure optimal charging performance and grid stability.

## [ARCH-COLD] Continental Cold Archetype
**Applicable Regions:** Chicago, New York (Winter), San Francisco (Winter)
**Trigger Condition:** Ambient Temperature < 10°C

### Mandates
1. **Thermal Management Priority**: All charging sessions must activate battery pre-conditioning protocols before initiating high-rate charging.
2. **Voltage Boost Authorization**: When Load_Score exceeds 45 at cold-climate stations (e.g., Station_104 Chicago with observed Load_Score of 47.16), a 10% voltage boost is authorized for battery thermal management.
3. **Charging Rate Reduction**: Level 2 chargers must reduce maximum output by 15% when temperature drops below 0°C to prevent lithium plating.
4. **Session Duration Extension**: Expected charging durations increase by 20-35% in sub-zero conditions. Scheduling algorithms must account for extended occupancy time.
5. **Infrastructure Impact**: Cold weather increases grid stress by approximately 18% due to heating demands. Station capacity calculations must include a 1.2x winter multiplier.

## [ARCH-HEAT] Humid/Arid Heat Archetype
**Applicable Regions:** Houston, Los Angeles, New York (Summer)
**Trigger Condition:** Ambient Temperature > 30°C

### Mandates
1. **Active Cooling Required**: High Load_Score stations in hot climates (e.g., Station_101 Houston at 38.9°C) must have active liquid cooling systems for charging equipment.
2. **Thermal Throttling**: Mandatory power throttling when Load_Score > 80 to prevent grid-side transformer fatigue. Reduce charging rate to 70% of rated capacity.
3. **Peak Heat Avoidance**: Between 12:00 PM and 4:00 PM during heat events (>35°C), DC Fast Chargers should implement dynamic queuing to prevent simultaneous high-draw sessions.
4. **Solar Integration Priority**: Heat archetype regions with solar availability (Houston, LA) should prioritize solar-to-EV direct buffering during peak solar hours (10 AM - 2 PM).
5. **Equipment Derating**: Charging infrastructure in sustained heat regions (>30°C average) must be derated by 10% for equipment longevity calculations.

## [ARCH-TEMPERATE] Temperate Archetype
**Applicable Regions:** San Francisco (Spring/Fall), Los Angeles (Winter), New York (Spring/Fall)
**Trigger Condition:** 10°C ≤ Ambient Temperature ≤ 30°C

### Mandates
1. **Standard Operations**: No special environmental adjustments required.
2. **Optimal Charging Window**: Temperate conditions represent ideal charging efficiency. Scheduling systems should maximize utilization during these periods.
3. **Baseline Metrics**: Performance measurements taken during temperate conditions serve as baseline for capacity planning calculations.
