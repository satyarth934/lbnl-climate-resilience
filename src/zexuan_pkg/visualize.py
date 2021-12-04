import os
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import leafmap  # Helps with the colorbar plot. Builds on top of ipyleaflet
from typing import List, Tuple

from ipyleaflet import (
    basemaps,
    Marker,
    FullScreenControl,
    AwesomeIcon,
)

from tqdm import tqdm

tqdm.pandas()

import utils


def plot_site_on_map(site: pd.Series, icon_name: str, ipl_map: leafmap.Map,) -> None:
    """Plot a single site on the map.
    
    Args:
        site (pd.Series): Site to be plotted on the map.
        icon_name (str): Icon to be used as marker on the map.
        ipl_map (leafmap.Map): Map on which the site markers are added.
    """

    icon = AwesomeIcon(
        name=icon_name, marker_color=site.loc["color"], icon_color="black", spin=False,
    )
    loc = [site.loc["Latitude"], site.loc["Longitude"]]
    marker = Marker(location=loc, draggable=False, icon=icon)
    ipl_map.add_layer(marker)


def plotmap(
    sites: pd.DataFrame,
    feature: str,
    colors: List[str],
    scale_range: List[float] = None,
    icon_name: str = "umbrella",
    map_center: List[float] = [39.0119, -98.4842],
    map_zoom: int = 4,
    plot_colorbar: bool = True,
    colorbar_label: str = "Colorbar",
    colorbar_min: float = None,
    colorbar_max: float = None,
    output_map_name: str = None,
) -> leafmap.Map:
    """Plot and mark each site on a map.
    
    Args:
        sites (pd.DataFrame): Data Frame containing all the site information. 
        feature (str): Feature of interest.
        colors (List[str]): List of colors to be used as markers. 
            The scale_range is divided into number of colors specified.
        scale_range (List[float], optional): Range of the scale. 
            Expects a min and max value to specify the range. Defaults to None.
            Min and Max value of the sites features are used in this case.
        icon_name (str, optional): Name of the Awesome icon that is used as 
            marker for the sites on the map. Defaults to 'umbrella'.
        map_center (List[float], optional): Marks the initial center coordinates
            of the map. Defaults to [39.0119, -98.4842].
        map_zoom (int, optional): Marks the intial zoom level in the map. 
            Defaults to 4.
        plot_colorbar (bool, optional): Boolean flag to spacify if the colorbar 
            is to be plotted in the map. Defaults to True.
        colorbar_label (str, optional): Caption for the colorbar. 
            Defaults to 'Colorbar'.
        colorbar_min (float, optional): Minimum value label in the color bar. 
            Defaults to None. Values are taken from scale_range in this case.
        colorbar_max (float, optional): Maximum value label in the color bar. 
            Defaults to None. Values are taken from scale_range in this case.
        output_map_name (str, optional): Name/Path of the output file. 
            Must be an HTML file. Defaults to None. The output file is not 
            generated in the default case.
        
    Returns:
        leafmap.Map: Returns the map that is generated using all the specified 
            configurations.
    """

    # Sanity check for the input params
    if scale_range is None:
        scale_range = [sites[feature].min(), sites[feature].max()]

    if colorbar_min is None:
        colorbar_min = scale_range[0]

    if colorbar_max is None:
        colorbar_max = scale_range[-1]

    # normalize values and decide colors based on threshold
    color = []
    x = np.array(
        [i / len(colors) for i in range(len(colors) + 1)]
    )  # [0, 0.25, 0.5, 0.75, 1]

    # Finding the color for each site
    for (i, value) in sites.iterrows():
        scaled = (value[feature] - scale_range[0]) / (scale_range[1] - scale_range[0])
        try:
            j = np.argwhere(x >= scaled)[0][0] - 1
            color.append(colors[j])
        except IndexError as ie:
            color.append("white")  # These are the invalid markers.

    sites["color"] = color

    # Initialize the ipyleaflet Map
    ipl_map = leafmap.Map(
        basemap=basemaps.Esri.WorldStreetMap, center=map_center, zoom=map_zoom
    )

    # Plot each site on the map
    sites.progress_apply(
        lambda site: plot_site_on_map(site, icon_name, ipl_map), axis=1
    )
    ipl_map.add_control(FullScreenControl())

    # Plot the colorbar on the map
    if plot_colorbar:
        ipl_map.add_colormap(
            colors=colors,
            label=colorbar_label,
            discrete=True,
            orientation="horizontal",
            vmin=colorbar_min,
            vmax=colorbar_max,
        )

    # Saving output map as HTML
    if output_map_name is not None:
        ipl_map.to_html(output_map_name, title=output_map_name)
        print(f"Saved map as {output_map_name}.")

    return ipl_map


def plot_histogram(
    sites: pd.DataFrame,
    features: List[str],
    n_bins: int = 10,
    bins: List[float] = None,
    plot_title: str = "Histogram",
    figsize: Tuple[int] = (12, 6),
    xlabels: List[str] = None,
    colors: List["str"] = None,
) -> Tuple[plt.figure, plt.axes]:
    """Plot histogram between specified bins for the select features of 
    the sites data frame.
    
    Args:
        sites (pd.DataFrame): Data Frame containing all the site information. 
        features (List[str]): Features of interest.
        n_bins (int): Number of histogram bins. Will be ignored if 
            'bins' argument is passed. Defaults to 10.
        bins (List[float]): Custom bins for the histogram. Defaults to None. 
            'n_bins' argument is used in this case.
        plot_title (str): Title of the resulting plot.
        figsize (Tuple[int]): Size of the output plot. Format: (width, height).
        xlabels (List[str]): Custom labels in place of x-axis bin range values. 
            Defaults to None. Original bin values are used in this case.
        colors (List["str"]): List of colors for each data vector. 
            Must match the number features listed. Defaults to None. 
            Matplotlib default colors are used in this case.
            
    Returns:
        Tuple[plt.figure, plt.axes]: Returns the figure and axes for the 
            generated plot.
    """

    # Get data to plot
    x = np.array(sites[features])

    # Creat plot
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=figsize)

    if bins is None:
        hist_data, hist_bins, hist_patches = ax.hist(
            x, n_bins, histtype="bar", label=features, color=colors
        )
    else:
        hist_data, hist_bins, hist_patches = ax.hist(
            x, bins=bins, histtype="bar", label=features, color=colors
        )

    ax.legend()
    ax.set_title(plot_title)
    ax.set_xticks(hist_bins)

    if xlabels is not None:
        ax.set_xticklabels(xlabels, rotation=45)

    fig.tight_layout()

    return fig, ax


# ONLY USED FOR DEBUGGING
if __name__ == "__main__":
    datadir = "/global/scratch/satyarth/Projects/lbnl-zexuan-code/data"
    sites_csv_path = os.path.join(datadir, "LMsites.csv")
    sites = pd.read_csv(sites_csv_path)

    pr_csv_path = os.path.join(datadir, "LMsites_pr1.csv")
    df_pr = pd.read_csv(pr_csv_path)
    df_pr = df_pr.dropna(subset=["historical"])

    df_pr["rcp26_diff"] = df_pr["rcp26"] - df_pr["historical"]
    df_pr["rcp45_diff"] = df_pr["rcp45"] - df_pr["historical"]
    df_pr["rcp60_diff"] = df_pr["rcp60"] - df_pr["historical"]
    df_pr["rcp85_diff"] = df_pr["rcp85"] - df_pr["historical"]

    df_pr["rcp26_ratio"] = df_pr["rcp26_diff"] / df_pr["historical"]
    df_pr["rcp45_ratio"] = df_pr["rcp45_diff"] / df_pr["historical"]
    df_pr["rcp60_ratio"] = df_pr["rcp60_diff"] / df_pr["historical"]
    df_pr["rcp85_ratio"] = df_pr["rcp85_diff"] / df_pr["historical"]

    col_pr = ["red", "lightblue", "cadetblue", "blue", "darkblue"]
    ipl_map = plotmap(
        sites=df_pr,
        feature="rcp45_diff",
        icon_name="umbrella",
        scale_range=np.array([-0.05, 0.35]),
        col=col_pr,
        plot_colorbar=True,
        output_map_name="Test_map_4.html",
    )
