# Codebook

The variables in the analysis-ready datasets in `data/clean/`. One section per dataset, one row per variable.
Update a row in the same commit that creates, renames or changes the variable.

## [county_panel.dta]

One row per [county × census year], [1860–1920]. Built by [`code/01_build/02_merge_counties.do`].

| Variable | Label | Type and unit | Definition and notes |
|:--|:--|:--|:--|
| [fips] | [County FIPS code] | [string, 5 digits] | [Unique together with year] |
| [year] | [Census year] | [integer] | |
| [fb_share] | [Foreign-born share of population] | [share, 0–1] | [Foreign-born / total population, from the full-count census] |
