"""Define the main module."""
import csv
from pathlib import Path

import geopandas
import pandas


def tweak_nw(df):
    """Prepare the neighborhood_ways dataset for further exploration."""
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


def process_neighborhood_ways_shapefile(shapefile):
    """Process neighborhood_ways shapefile."""
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

    return grouped_results


def tweak_scores(df):
    """Prepare the overall score dataset for further exploration."""
    return (
        df.drop(["id", "score_original", "human_explanation"], axis=1)
        .query(
            "score_id in ['core_services', 'opportunity', 'people', 'recreation', 'retail', 'transit']"
        )
        .set_index("score_id")
    )


def process_neighborhood_overall_scores(scorefile):
    """Process neighborhood_overall scorefile."""
    raw_df = pandas.read_csv(scorefile)
    df = tweak_scores(raw_df)
    return df.to_dict()["score_normalized"]


def collect_city_datasets(data_dir):
    """
    Collect the city datasets.

    If a city does not have *ALL* the datasets, it is discarded.
    """
    cities = {
        "-".join(city.stem.split("-")[0:-1])
        for city in list(data_dir.glob("*"))
        if not city.stem.startswith(".")
    }
    groups = []
    for city in cities:
        shapefile = data_dir / f"{city}-neighborhood_ways.zip"
        scorefile = data_dir / f"{city}-neighborhood_overall_scores.csv"
        if shapefile.exists() and scorefile.exists():
            groups.append((shapefile, scorefile))

    return groups


def main():
    """Define the program's main entrypoint."""

    # Collect the shape files to process.
    data_dir = Path("data")
    dataset_groups = collect_city_datasets(data_dir)
    results = []
    for dataset_group in dataset_groups:
        shapefile = dataset_group[0]
        scorefile = dataset_group[1]

        # Process them.
        nw_res = process_neighborhood_ways_shapefile(shapefile)
        scores = process_neighborhood_overall_scores(scorefile)
        results.append({**nw_res, **scores})

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
