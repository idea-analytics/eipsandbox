# Texas School-Age Population Hexbin Map

An interactive Shiny app for visualizing school-age population density (Under 5 through 18-19 years) across Texas using H3 hexagons and area-weighted distribution from census tracts.

## Features

- **H3 Hexagon Resolution 7**: Uniform spatial units for comparison
- **Area-Weighted Distribution**: Properly distributes population from variable-sized census tracts to hexes
- **Composite Scoring**: Three methods to visualize overall population density:
  - Total Population Density
  - Normalized Z-Score
  - Percentile Rank
- **Optional Kriging**: Smooth interpolation for visualization
- **Interactive Map**: Hover for hex-level details

## Project Structure

```
.
├── app.py                          # Main Shiny application
├── requirements.txt                # Python dependencies
├── Population-2023-filtered.csv    # Your census population data
└── tl_2023_48_tract/              # Census tract shapefiles folder
    └── tl_2023_48_tract.shp       # (and associated .dbf, .shx, etc.)
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Prepare Your Data

Ensure these files are in the same directory as `app.py`:
- `Population-2023-filtered.csv` (your census data)
- `tl_2023_48_tract/` folder with the shapefile

### 3. Run Locally

```bash
shiny run app.py
```

The app will open in your browser at `http://localhost:8000`

## Deployment to Posit Connect

### Option 1: Using rsconnect-python CLI

1. Install rsconnect-python:
```bash
pip install rsconnect-python
```

2. Configure your Posit Connect server:
```bash
rsconnect add \
    --server https://your-connect-server.com \
    --name myserver \
    --api-key YOUR_API_KEY
```

3. Deploy the app:
```bash
rsconnect deploy shiny . \
    --server myserver \
    --title "Texas Population Hexbin Map"
```

### Option 2: Using Posit Connect UI

1. Log into Posit Connect
2. Click "Publish" → "Upload"
3. Upload:
   - `app.py`
   - `requirements.txt`
   - `Population-2023-filtered.csv`
   - The entire `tl_2023_48_tract/` folder
4. Posit Connect will automatically detect it's a Shiny app and deploy it

### Option 3: Git-backed deployment

1. Create a Git repository with all files
2. In Posit Connect, create a new deployment and connect your Git repo
3. Set the content type to "Python Shiny Application"
4. Deploy from your branch

## How the Area-Weighted Distribution Works

### Large Census Tracts (Multiple Hexes)
When a census tract covers multiple hexagons:
1. Calculate the intersection area between the tract and each hex
2. Distribute the tract's population proportionally based on intersection areas
3. Result: Population sums correctly across all hexes within the tract

**Example**: 
- Tract has 1,000 people and covers 4 hexes
- Hex A intersects 40% of tract area → gets 400 people
- Hex B intersects 30% → gets 300 people
- Hex C intersects 20% → gets 200 people
- Hex D intersects 10% → gets 100 people
- Total: 1,000 people ✓

### Small Census Tracts (Within Hexes)
When multiple census tracts fit within a single hexagon:
1. Each tract contributes its population weighted by its intersection with the hex
2. The hex aggregates all contributing tracts
3. Result: Hex shows total population from all tracts within it

**Example**:
- Hex contains 3 small tracts with 50, 75, and 25 people
- Hex total: 150 people ✓

## Composite Scoring Methods

### 1. Total Population Density
- **Formula**: Total population ÷ Hex area
- **Use**: Shows absolute density per unit area
- **Color**: High density = Red, Low density = Blue

### 2. Normalized Z-Score
- **Formula**: (Hex population - Mean population) ÷ Standard deviation
- **Use**: Shows how many standard deviations from average
- **Color**: Above average = Red, Below average = Blue

### 3. Percentile Rank
- **Formula**: Rank(Hex population) as percentage
- **Use**: Shows relative position (0-100%)
- **Color**: Top percentiles = Red, Bottom percentiles = Blue

## Kriging Option

When enabled, applies Ordinary Kriging interpolation to smooth the hex values:
- Creates a continuous surface
- Useful for visualization and identifying trends
- Optional - can be toggled on/off in the app

## Age Groups Included

The app aggregates all these columns from your CSV:
- Male: Under 5 years, 5-9, 10-14, 15-17, 18-19
- Female: Under 5 years, 5-9, 10-14, 15-17, 18-19

This captures the school-age population relevant to STAAR testing (grades 3-8) plus younger and slightly older students.

## Troubleshooting

### "GEOID not found" error
Update line 26 in `app.py` to match your shapefile's ID column:
```python
tracts_gdf = tracts_gdf.merge(pop_df, left_on='YOUR_COLUMN_NAME', right_on='Geography', how='inner')
```

### Memory issues with large datasets
Reduce H3 resolution in line 78:
```python
hex_ids = generate_texas_hexagons(tracts_gdf, resolution=6)  # Lower resolution = fewer hexes
```

### Slow performance
- Disable kriging (uncheck in app)
- Use total_density scoring (fastest)
- Consider pre-computing and caching the hex distribution

## Customization

### Change H3 Resolution
In line 78 of `app.py`, modify the resolution parameter:
- Resolution 6: ~66 hexes across Texas (faster, less detail)
- Resolution 7: ~461 hexes (balanced)
- Resolution 8: ~3,221 hexes (slower, more detail)

### Modify Color Scheme
In the `create_hex_map` function (around line 260), change the colorscale:
```python
color = f'rgb({int(255*color_val)}, {int(255*(1-color_val)*0.5)}, {int(255*(1-color_val))})'
```

### Add More Scoring Methods
Add new methods in the `calculate_composite_scores` function (around line 140)

## Performance Notes

- Initial load time: 30-60 seconds (generating and distributing hexes)
- Subsequent interactions: <1 second (just recalculating scores)
- Memory usage: ~500MB-1GB depending on resolution

## License

MIT License - Feel free to modify and use as needed!

## Support

For issues with:
- **Census data**: https://www.census.gov/data/developers.html
- **H3 hexagons**: https://h3geo.org/
- **Posit Connect**: https://docs.posit.co/connect/
- **Shiny for Python**: https://shiny.posit.co/py/
