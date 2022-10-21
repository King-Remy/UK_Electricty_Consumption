# UK Electricty Consumption
 This project analyzes and presents the electricity consumption data to users on a postcode level for the UK using Python and Jupyter Notebook.

 ## Task List
- [x] Data Collection from the UK government website [here](https://www.gov.uk/government/uploads/system/uploads/attachment_data/file/1050244/Postcode_Level_Standard_Electricity_2020_A_to_K.csv/preview) and geographical postcode location data from Ordinance Survey [here](https://osdatahub.os.uk/downloads/open/CodePointOpen).
- [x] Create web API with Python and Flask.
- [x] Visualize total anual electrcity consumption per postcode from areacode selection using Plotly.
- [ ] Deploy API to server.

### API for Collected data from Gov UK and Ordinance Survey websites
![data_collection](/Asset/data_collection.gif)
![data_collection2](/Asset/data_collection2.gif)

### Visualization of selected areacodes
![visualization](/Asset/visualization.gif)
![home_feature](/Asset/home_feature.gif)

# Development

## Environment Setup
**Note:**
The datasets are available to be downloaded at UK government website [here](https://www.gov.uk/government/uploads/system/uploads/attachment_data/file/1050244/Postcode_Level_Standard_Electricity_2020_A_to_K.csv/preview) and and geographical postcode location data from Ordinance Survey [here](https://osdatahub.os.uk/downloads/open/CodePointOpen). These are the 2 datasets required for this project.

* **Create the virtual environment and install packages**
  ```
  python3 -m venv venv
  source venv/bin/activate
  pip3 install -r requirements.txt
  ```

* **Set up .env and .yaml file**
  * Create .env and .yaml files:

  ![envsetup](/Asset/envsetup.JPG)
  ![yamlareacodes](/Asset/yamlareacodes.JPG)



* **Download and extract**
* Download UK postcode level data:  
  ```
  curl -O https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/1050244/Postcode_Level_Standard_Electricity_2020_A_to_K.csv
  ```
* Download UK geographic postcode data:
  ```
  https://api.os.uk/downloads/v1/products/CodePointOpen/downloads?area=GB&format=GeoPackage&redirect
  ```


  