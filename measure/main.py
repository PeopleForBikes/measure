"""Define the main module."""
import csv
from pathlib import Path

import geopandas


def tweak_nw(df):
    """Prepare the dataset for further exploration."""
    return df.drop(
        [
            "FT_BIKE_01",
            "FT_CROSS_L",
            "FT_INT_STR",
            "FT_LANES",
            "FT_PARK",
            "FT_SEG_STR",
            "FUNCTIONAL",
            "INTERSECTI",
            "INTERSE_01",
            "JOB_ID",
            "ONE_WAY",
            "ONE_WAY_CA",
            "OSM_ID",
            "PATH_ID",
            "ROAD_ID",
            "SPEED_LIMI",
            "TDG_ID",
            "TF_BIKE_01",
            "TF_CROSS_L",
            "TF_INT_STR",
            "TF_LANES",
            "TF_PARK",
            "TF_SEG_STR",
            "TWLTL_CROS",
            "WIDTH_FT",
            "XWALK",
        ],
        axis=1,
    ).assign(distance=df.length)


def main():
    """Define the program's main entrypoint."""

    # Collect the shape files to process.
    p = Path(".")
    shapefiles = list(p.glob("data/*neighborhood_ways.zip"))

    # Process them.
    results = []
    for shapefile in shapefiles:
        # Load the shapefile.
        raw_gdf = geopandas.read_file(shapefile)

        # Clean up the dataset.
        gdf = tweak_nw(raw_gdf)

        # Sum the distances by type.
        grouped = gdf.groupby("FT_BIKE_IN", dropna=False).sum()

        # Get the distances in km.
        grouped["distance"] = grouped["distance"].astype(int) / 1000

        # Save the results.
        grouped_results = grouped.to_dict()["distance"]
        country, state, city, _ = shapefile.stem.split("-")
        grouped_results["country"] = country
        grouped_results["state"] = state
        grouped_results["city"] = city
        results.append(grouped_results)

    # Display the results as JSON.
    # print(json.dumps(results, indent=2))

    # Display the results as CSV.
    print(results)
    with open("results/measure.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)


if __name__ == "__main__":
    main()
