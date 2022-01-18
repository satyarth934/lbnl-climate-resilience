import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
import leafmap  # Helps with the colorbar plot. Builds on top of ipyleaflet
from typing import List, Tuple

from ipyleaflet import (
    basemaps,
    Marker,
    FullScreenControl,
    AwesomeIcon,
    LayerGroup,
)

from tqdm import tqdm

tqdm.pandas()

# from climate_resilience import utils


def plot_site_on_map(
    site: pd.Series, icon_name: str, ipl_map: leafmap.Map, feature: str,
) -> None:
    """Plot a single site on the map.
    Also provides a tooltip at the markers showing the values and site ID.
    
    Args:
        site (pd.Series): Site to be plotted on the map.
        icon_name (str): Icon to be used as marker on the map.
        ipl_map (leafmap.Map): Map on which the site markers are added.
        feature (str): Feature based on which the markers are generated.
    """

    icon = AwesomeIcon(
        name=icon_name, marker_color=site.loc["color"], icon_color="black", spin=False,
    )
    loc = [site.loc["Latitude"], site.loc["Longitude"]]
    info = f"{feature}: {float(site[feature]):.5f}"
    marker = Marker(location=loc, draggable=False, icon=icon, title=info, alt=info)    # setting the title displays information when we hover over the markers.

    ipl_map.add_layer(marker)
    

def get_site_markers(
    site: pd.Series, icon_name: str, ipl_map: leafmap.Map, feature: str,
) -> None:
    """Same as plot_site_on_map() but returns the marker instead of plotting it 
    on the map. Also provides a tooltip at the markers showing the values and 
    site ID.
    
    Args:
        site (pd.Series): Site to be plotted on the map.
        icon_name (str): Icon to be used as marker on the map.
        ipl_map (leafmap.Map): Map on which the site markers are added.
        feature (str): Feature based on which the markers are generated.
    """

    icon = AwesomeIcon(
        name=icon_name, marker_color=site.loc["color"], icon_color="black", spin=False,
    )
    loc = [site.loc["Latitude"], site.loc["Longitude"]]
    info = f"{feature}: {float(site[feature]):.5f}"
    marker = Marker(location=loc, draggable=False, icon=icon, title=info, alt=info)    # setting the title displays information when we hover over the markers.

    return marker


def plot_map(
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
    
    The markers that are generated in white color either lie outside the range 
    specified in 'scale_range' OR have nan values.
    
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

    # Plot each site on the map (parallel function call. Ignoring because of inconsistencies.)
    # sites.progress_apply(
    #     lambda site: plot_site_on_map(site, icon_name, ipl_map, feature), axis=1
    # )
    
    # Plot each site on map
    site_markers = list()
    with tqdm(range(len(sites))) as tqdm_site_nos:
        tqdm_site_nos.set_description("Generating site markers")
        
        for site_i in tqdm_site_nos:
            site_marker = get_site_markers(sites.iloc[site_i], icon_name, ipl_map, feature)
            site_markers.append(site_marker)
    
    sites_lg = LayerGroup(layers=site_markers)
    ipl_map.add_layer(sites_lg)

    ipl_map.add_control(FullScreenControl())

    # Plot the colorbar on the map
    plot_colorbar_params = {
        "colors": colors,
        "label": colorbar_label,
        "discrete": True,
        "orientation": "horizontal",
        "vmin": colorbar_min,
        "vmax": colorbar_max,
    }
    
    if plot_colorbar:
        ipl_map.add_colormap(**plot_colorbar_params)

    # Saving output map as HTML
    if output_map_name is not None:
        # Saving the map
        ipl_map.to_html(output_map_name, title=output_map_name)
        print(f"Saved map as {output_map_name}.")
        
        # Saving the colorbar separately as PNG - only because the colorbar does
        # not show up in the HTML Map.
        output_colorbar_name = output_map_name.replace(".html", "_colorbar.png")
        colorbar_fig = leafmap.colormaps.create_colormap(**plot_colorbar_params)
        colorbar_fig.savefig(output_colorbar_name, bbox_inches='tight')
        print(f"Saved colorbar as {output_colorbar_name}.")
        
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
        bins (List[float]): Custom bins for the histogram. 
            Defaults to None. 'n_bins' argument is used in this case.
        plot_title (str): Title of the resulting plot.
        figsize (Tuple[int]): Size of the output plot. Format: (width, height).
        xlabels (List[str]): Custom labels in place of x-axis bin range values. 
            Defaults to None. Original bin values are used in this case.
        colors (List["str"]): List of colors for each data vector. 
            Must match the number features listed. 
            Defaults to None. Matplotlib default colors are used in this case.
            
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


def plot_boxplot(
    data: pd.DataFrame,
    x_feature: str,
    y_feature: str,
    hue_feature: str,
    hue_order: List[str] = None,
    colors: List[str] = None,
    x_label: str = None,
    y_label: str = None,
    plot_title: str = "Box Plot",
    figsize: Tuple[int] = (12, 6),
    output_filename: str = None,
) -> plt.axes:
    """Create boxplot using the provided data.
    
    Args:
        data (pd.DataFrame): Data that is used to plot the boxplots.
        x_feature (str): Feature within the data that is plotted on the x-axis.
        y_feature (str): Feature within the data that is plotted on the y-axis.
        hue_feature (str): Feature within the data that is used as the 
            third dimension categorical levels.
        hue_order (List[str]): The order in which the categorical levels are to 
            be plotted. 
            Defaults to None. Levels are infered from the data argument 
            automatically if this argument is None.
        colors (List[str]): List of colors to be used for each categorical 
            level. 
            Defaults to None. 
        x_label (str, optional): X-axis label. Defaults to None. The 'x_feature'
            argument is used if this argument is not provided.
        y_label (str, optional): Y-axis label. Defaults to None. The 'y_feature'
            argument is used if this argument is not provided.
        plot_title (str, optional): Title of the plot. Defaults to 'Box Plot'.
        figsize (Tuple[int], optional): Figure canvas size. Defaults to (12,6).
        output_filename (str, optional): Name of the output PNG file. 
            Defaults to None. The output file is not generated in this case.
    
    Returns:
        plt.axes: Return the plot object axes. This object can be used to 
            further add plot components if required by the user.
    """

    # Updating default values if None is passed as argument
    x_label = x_feature if x_label is None else x_label
    y_label = y_feature if y_label is None else y_label

    # Plotting the box plot
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot()
    ax = sns.boxplot(
        x=x_feature,
        y=y_feature,
        hue=hue_feature,
        data=data,
        hue_order=hue_order,
        palette=colors,
    )
    ax.legend(bbox_to_anchor=(1.0, 0.8))
    ax.set_title(plot_title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)

    # Generating the output file
    if output_filename is not None:
        fig.savefig(output_filename, bbox_inches="tight")

    return ax
