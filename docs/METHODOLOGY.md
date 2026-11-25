# SolAI screening methodology — v0.1

## Purpose

This first implementation is a transparent, explainable screening prototype. It ranks candidate sites for further investigation; it does not certify a site as solar-ready.

## Five screening dimensions

Each dimension is represented as a normalized 0–100 suitability score, where higher is better:

| Dimension | Default weight | Meaning |
|---|---:|---|
| Land availability | 30% | Indicative usable-land suitability |
| Shading | 20% | Higher score means lower shading |
| Slope | 15% | Higher score means more suitable slope |
| Flood safety | 20% | Higher score means lower flood risk |
| Grid proximity | 15% | Indicative proximity to substation/grid |

Weighted score = sum(feature score × normalized weight).

Weights are defaults for prototype demonstration only. They must be agreed with the utility and calibrated to the problem statement before operational use.

## Indicative solar estimate

- DC capacity (MW) = usable area (m²) × installed density (W/m²) / 1,000,000
- Annual generation (MWh) = DC capacity (MW) × specific yield (MWh/MW/year)
- Avoided emissions (tCO₂e/year) = annual generation × documented grid emission factor (tCO₂e/MWh)

Defaults in the API are illustrative assumptions. The caller must provide a documented grid emission factor. The estimate does not account for detailed panel layout, setbacks, DC/AC ratio, degradation, curtailment, shading losses, inverter losses, or interconnection constraints.

## Required second-stage utility checks

Before a site is described as technically feasible, obtain and assess:
- land title, ownership, access and permitted use;
- transformer capacity and loading;
- feeder loading, voltage and protection constraints;
- interconnection scope, cost and approvals;
- site survey, geotechnical and flood assessment;
- detailed engineering design and yield study.

## Evidence and uncertainty

Every production assessment should retain data source, acquisition date, spatial resolution, coordinate reference system, processing version, assumptions, score, calculation version, emission factor source, uncertainty and validation status.

A cryptographic hash can show that a stored record has not changed; it does not establish the truth or quality of its source data.
