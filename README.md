# qgis-geocodes
Plugin for [QGIS](https://github.com/qgis/QGIS) which provides tools for working with different types of geocodes.

## Features

- ___Zoom Tool___: Enter a geocode expression and zoom to the associated map location or area
- ___Capture Geocode___: Pick a map location and encode its latitude and longitude to a geocode 
- ___Processing Scripts___
    - _Append Geocode to Point Layer_: Add attribute with geocoded location to each feature of a point layer 
    - _Convert Table to Point Layer_: Create a map layer with point geometry from tables with a geocode column

## Supported Formats

- Plus Codes (Open Location Code)
- OSM Shortlink 
- Geohash

## Installation

1. Download the plugin `.zip` file from the [Release](https://github.com/CodeBardian/qgis-geocodes/releases) section 
2. Head to the QGIS-PluginManager (`Plugins` -> `Manage and Install Plugins`) and select the `Install from ZIP` tab. 
3. Select the filepath to the location of your download and click install.
