import pandas as pd
import geopandas as gpd
import h3
import numpy as np
from shapely.geometry import Polygon, Point
from scipy.interpolate import griddata
from shiny import App, ui, render, reactive
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ============================================================================
# DATA LOADING AND PREPROCESSING
# ============================================================================

def load_and_prepare_data():
    """Load census data and tract shapefiles"""
    # Load population data
    pop_df = pd.read_csv('Population-2023-filtered.csv')
    
    # Load census tract shapefile
    tracts_gdf = gpd.read_file('tl_2023_48_tract/tl_2023_48_tract.shp')
    
    # Merge population data with geometries
    # Assuming Geography column matches GEOID in shapefile
    tracts_gdf = tracts_gdf.merge(pop_df, left_on='GEOID', right_on='Geography', how='inner')
    
    # Ensure CRS is WGS84 for H3 compatibility
    tracts_gdf = tracts_gdf.to_crs(epsg=4326)
    
    return tracts_gdf

def get_age_columns():
    """Define all age group columns to process"""
    age_columns = [
        'Estimate!!Total:!!Male:!!Under 5 years',
        'Estimate!!Total:!!Male:!!5 to 9 years',
        'Estimate!!Total:!!Male:!!10 to 14 years',
        'Estimate!!Total:!!Male:!!15 to 17 years',
        'Estimate!!Total:!!Male:!!18 and 19 years',
        'Estimate!!Total:!!Female:!!Under 5 years',
        'Estimate!!Total:!!Female:!!5 to 9 years',
        'Estimate!!Total:!!Female:!!10 to 14 years',
        'Estimate!!Total:!!Female:!!15 to 17 years',
        'Estimate!!Total:!!Female:!!18 and 19 years'
    ]
    return age_columns

# ============================================================================
# H3 HEXAGON GENERATION
# ============================================================================

def generate_texas_hexagons(tracts_gdf, resolution=7):
    """Generate H3 hexagons covering all Texas census tracts"""
    all_hexes = set()
    
    for idx, tract in tracts_gdf.iterrows():
        # Get hexagons that intersect with this tract
        geom = tract.geometry
        
        # Use polyfill to get hexagons covering the polygon
        if geom.geom_type == 'Polygon':
            hex_ids = h3.polyfill_geojson(geom.__geo_interface__, resolution)
        elif geom.geom_type == 'MultiPolygon':
            for poly in geom.geoms:
                hex_ids = h3.polyfill_geojson(poly.__geo_interface__, resolution)
                all_hexes.update(hex_ids)
            continue
        else:
            continue
            
        all_hexes.update(hex_ids)
    
    return list(all_hexes)

def hex_to_polygon(hex_id):
    """Convert H3 hex ID to Shapely polygon"""
    boundary = h3.h3_to_geo_boundary(hex_id, geo_json=True)
    return Polygon(boundary)

# ============================================================================
# POPULATION DISTRIBUTION WITH AREA WEIGHTING
# ============================================================================

def distribute_population_to_hexes(tracts_gdf, hex_ids, age_columns, resolution=7):
    """
    Distribute population from census tracts to hexes using area-weighted interpolation.
    
    For large tracts: Split population across multiple hexes proportionally
    For small tracts: Aggregate multiple tracts to single hex
    """
    
    # Create GeoDataFrame of hexagons
    hex_polygons = [hex_to_polygon(hid) for hid in hex_ids]
    hexes_gdf = gpd.GeoDataFrame({
        'hex_id': hex_ids,
        'geometry': hex_polygons
    }, crs='EPSG:4326')
    
    # Initialize population columns for hexes
    for col in age_columns:
        hexes_gdf[col] = 0.0
    
    # Calculate hex areas for normalization
    hexes_gdf['hex_area'] = hexes_gdf.geometry.area
    
    print("Distributing population to hexes...")
    
    # For each tract, distribute its population to overlapping hexes
    for idx, tract in tracts_gdf.iterrows():
        if idx % 100 == 0:
            print(f"Processing tract {idx}/{len(tracts_gdf)}")
        
        tract_geom = tract.geometry
        tract_area = tract_geom.area
        
        # Find hexes that intersect with this tract
        intersecting_hexes = hexes_gdf[hexes_gdf.intersects(tract_geom)]
        
        if len(intersecting_hexes) == 0:
            continue
        
        # Calculate intersection areas
        intersection_areas = []
        intersection_indices = []
        
        for hex_idx, hex_row in intersecting_hexes.iterrows():
            intersection = tract_geom.intersection(hex_row.geometry)
            intersection_area = intersection.area
            intersection_areas.append(intersection_area)
            intersection_indices.append(hex_idx)
        
        total_intersection_area = sum(intersection_areas)
        
        if total_intersection_area == 0:
            continue
        
        # Distribute population proportionally by intersection area
        for i, hex_idx in enumerate(intersection_indices):
            weight = intersection_areas[i] / total_intersection_area
            
            for col in age_columns:
                pop_value = tract[col]
                if pd.notna(pop_value):
                    hexes_gdf.at[hex_idx, col] += pop_value * weight
    
    print("Population distribution complete!")
    
    return hexes_gdf

# ============================================================================
# COMPOSITE SCORING
# ============================================================================

def calculate_composite_scores(hexes_gdf, age_columns, method='total_density'):
    """
    Calculate composite score across all age groups for each hex.
    
    Methods:
    - 'total_density': Total population per unit area
    - 'normalized': Z-score normalization across all age groups
    - 'percentile': Percentile rank (0-100)
    """
    
    # Sum all age groups
    hexes_gdf['total_pop'] = hexes_gdf[age_columns].sum(axis=1)
    
    if method == 'total_density':
        hexes_gdf['composite_score'] = hexes_gdf['total_pop'] / hexes_gdf['hex_area']
        score_label = 'Population Density (per sq degree)'
        
    elif method == 'normalized':
        # Calculate mean and std across all age groups for normalization
        all_values = hexes_gdf[age_columns].values.flatten()
        mean_val = np.mean(all_values)
        std_val = np.std(all_values)
        
        # Z-score normalization
        hexes_gdf['composite_score'] = (hexes_gdf['total_pop'] - hexes_gdf['total_pop'].mean()) / hexes_gdf['total_pop'].std()
        score_label = 'Normalized Score (Z-score)'
        
    elif method == 'percentile':
        # Percentile rank
        hexes_gdf['composite_score'] = hexes_gdf['total_pop'].rank(pct=True) * 100
        score_label = 'Percentile Rank'
    
    return hexes_gdf, score_label

# ============================================================================
# KRIGING (OPTIONAL SMOOTHING)
# ============================================================================

def apply_kriging(hexes_gdf, grid_resolution=100):
    """
    Apply kriging interpolation to smooth the hex values.
    This is optional - can be toggled in the app.
    """
    from pykrige.ok import OrdinaryKriging
    
    # Get centroids
    hexes_gdf['centroid'] = hexes_gdf.geometry.centroid
    hexes_gdf['lon'] = hexes_gdf.centroid.x
    hexes_gdf['lat'] = hexes_gdf.centroid.y
    
    # Create grid
    lon_min, lon_max = hexes_gdf['lon'].min(), hexes_gdf['lon'].max()
    lat_min, lat_max = hexes_gdf['lat'].min(), hexes_gdf['lat'].max()
    
    grid_lon = np.linspace(lon_min, lon_max, grid_resolution)
    grid_lat = np.linspace(lat_min, lat_max, grid_resolution)
    
    # Ordinary Kriging
    OK = OrdinaryKriging(
        hexes_gdf['lon'].values,
        hexes_gdf['lat'].values,
        hexes_gdf['composite_score'].values,
        variogram_model='spherical',
        verbose=False,
        enable_plotting=False
    )
    
    z, ss = OK.execute('grid', grid_lon, grid_lat)
    
    return grid_lon, grid_lat, z

# ============================================================================
# VISUALIZATION
# ============================================================================

def create_hex_map(hexes_gdf, score_label, use_kriging=False):
    """Create interactive Plotly map of hexagons"""
    
    if use_kriging:
        # Apply kriging and create contour map
        grid_lon, grid_lat, z = apply_kriging(hexes_gdf)
        
        fig = go.Figure(data=go.Contour(
            x=grid_lon,
            y=grid_lat,
            z=z,
            colorscale='RdYlBu_r',
            colorbar=dict(title=score_label),
            contours=dict(
                coloring='heatmap',
                showlabels=True
            )
        ))
    else:
        # Create choropleth with hexagons
        hex_data = []
        
        for idx, row in hexes_gdf.iterrows():
            geom = row.geometry
            if geom.geom_type == 'Polygon':
                coords = list(geom.exterior.coords)
                lons = [c[0] for c in coords]
                lats = [c[1] for c in coords]
                
                hex_data.append({
                    'lons': lons,
                    'lats': lats,
                    'score': row['composite_score'],
                    'total_pop': row['total_pop'],
                    'hex_id': row['hex_id']
                })
        
        # Create figure
        fig = go.Figure()
        
        # Normalize scores for color scaling
        scores = [h['score'] for h in hex_data]
        min_score = min(scores)
        max_score = max(scores)
        
        for hex_info in hex_data:
            # Normalize score to 0-1 range for color
            normalized_score = (hex_info['score'] - min_score) / (max_score - min_score) if max_score > min_score else 0.5
            
            # Color: blue (low) to red (high)
            color_val = normalized_score
            color = f'rgb({int(255*color_val)}, {int(255*(1-color_val)*0.5)}, {int(255*(1-color_val))})'
            
            fig.add_trace(go.Scattergeo(
                lon=hex_info['lons'],
                lat=hex_info['lats'],
                mode='lines',
                fill='toself',
                fillcolor=color,
                line=dict(width=0.5, color='white'),
                hovertemplate=f"<b>Hex ID:</b> {hex_info['hex_id']}<br>" +
                              f"<b>Score:</b> {hex_info['score']:.2f}<br>" +
                              f"<b>Total Pop:</b> {hex_info['total_pop']:.0f}<extra></extra>",
                showlegend=False
            ))
    
    # Update layout
    fig.update_layout(
        title='Texas Population Density by H3 Hexagon (Resolution 7)',
        geo=dict(
            scope='usa',
            projection_type='albers usa',
            center=dict(lat=31.5, lon=-99.5),
            showland=True,
            landcolor='rgb(243, 243, 243)',
            coastlinecolor='rgb(204, 204, 204)',
            showlakes=True,
            lakecolor='rgb(230, 245, 255)',
        ),
        height=800,
        margin=dict(l=0, r=0, t=40, b=0)
    )
    
    return fig

# ============================================================================
# SHINY APP
# ============================================================================

app_ui = ui.page_fluid(
    ui.h2("Texas School-Age Population Hexbin Map"),
    ui.p("Visualizing population density for ages Under 5 through 18-19 years across Texas census tracts using H3 hexagons."),
    
    ui.layout_sidebar(
        ui.sidebar(
            ui.input_select(
                "scoring_method",
                "Composite Scoring Method:",
                choices={
                    "total_density": "Total Population Density",
                    "normalized": "Normalized Z-Score",
                    "percentile": "Percentile Rank"
                },
                selected="total_density"
            ),
            ui.input_checkbox("use_kriging", "Apply Kriging Smoothing", value=False),
            ui.input_action_button("refresh", "Refresh Map", class_="btn-primary"),
            ui.hr(),
            ui.h4("About the Scoring:"),
            ui.markdown("""
            - **Population Density**: Total population divided by hex area
            - **Normalized Z-Score**: How many standard deviations from the mean
            - **Percentile Rank**: Where the hex falls in the distribution (0-100%)
            
            **Color Scale**: 🔵 Blue = Low | 🔴 Red = High
            """),
            width=300
        ),
        ui.output_ui("map_plot"),
        ui.output_text("stats_text")
    )
)

def server(input, output, session):
    
    # Load data once at startup
    tracts_gdf = load_and_prepare_data()
    age_columns = get_age_columns()
    hex_ids = generate_texas_hexagons(tracts_gdf, resolution=7)
    hexes_gdf = distribute_population_to_hexes(tracts_gdf, hex_ids, age_columns, resolution=7)
    
    # Reactive: Calculate scores based on selected method
    @reactive.Calc
    def processed_hexes():
        hexes_with_scores, score_label = calculate_composite_scores(
            hexes_gdf.copy(),
            age_columns,
            method=input.scoring_method()
        )
        return hexes_with_scores, score_label
    
    # Render map
    @output
    @render.ui
    def map_plot():
        hexes_with_scores, score_label = processed_hexes()
        
        fig = create_hex_map(
            hexes_with_scores,
            score_label,
            use_kriging=input.use_kriging()
        )
        
        return ui.HTML(fig.to_html(include_plotlyjs="cdn"))
    
    # Render statistics
    @output
    @render.text
    def stats_text():
        hexes_with_scores, score_label = processed_hexes()
        
        total_pop = hexes_with_scores['total_pop'].sum()
        num_hexes = len(hexes_with_scores)
        avg_score = hexes_with_scores['composite_score'].mean()
        
        return f"Total Population: {total_pop:,.0f} | Number of Hexagons: {num_hexes:,} | Average Score: {avg_score:.2f}"

app = App(app_ui, server)
