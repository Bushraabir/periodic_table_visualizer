# Advanced Periodic Table Visualizer

An interactive Streamlit application to explore the periodic table through advanced visualizations, filtering, and statistical analysis. This project leverages **Streamlit**, **Pandas**, and **Plotly** to provide an immersive and educational experience for users interested in chemical elements and their properties.

## Overview

The Advanced Periodic Table Visualizer transforms a static periodic table into a dynamic, interactive data app. Users can:
- **Explore a custom-built periodic table layout** with historical context, fun facts, and detailed explanations about modern chemistry.
- **Apply advanced filters** (by element name, group, period, metal type, and radioactivity) and view a customized table of element data.
- **Visualize trends** across atomic numbers using interactive line charts with smoothing options.
- **Dive into 3D visualizations** with an adjustable bubble scatter plot that maps various atomic properties.
- **Compare elements with radar charts** that display multiple atomic attributes side by side.
- **View element-level details** presented in a styled card format, including definitions for key chemical properties.

## Features

### Sidebar Filters
- **Search by Element:** Quickly locate elements by name.
- **Group & Period Filters:** Narrow down elements based on their group (column) or period (row).
- **Metal and Radioactivity Options:** Filter by metal type (Metal, Nonmetal, Metalloid) and radioactivity (Radioactive, Non-Radioactive).

### Tabbed Navigation
The app is organized into six tabs, each focusing on a unique aspect of the periodic table:
1. **Periodic Table:**  
   - Displays historical information, basic facts, fun facts, and advanced features of modern chemistry.
   - Renders a custom grid layout that includes special sections for Lanthanides and Actinides.
2. **Table View:**  
   - An advanced, filterable table where users can select columns, search for values, and apply numeric or categorical filters.
   - Includes a download button to export the filtered table as a CSV file.
3. **Trends:**  
   - Comparative line charts that visualize trends across atomic numbers.
   - Options to display markers, smooth lines, and adjust line styles.
4. **3D Visualizations:**  
   - An interactive 3D bubble plot that maps selected atomic properties on the X, Y, and Z axes.
   - Features adjustable bubble sizes and an optional logarithmic scale for enhanced data exploration.
5. **Radar Charts:**  
   - Compare selected elements across multiple numeric properties using dynamic radar charts.
   - Displays additional element-level details and custom hover text for deeper insights.
6. **Element Details:**  
   - A detailed, card-style view for individual elements.
   - Includes definitions for key chemical properties like atomic number, atomic mass, density, boiling point, and more.

### Data Management
- **Optimized Data Loading:**  
  Uses `st.cache_data` to efficiently load and cache data from the CSV file (`data/Periodic Table of Elements.csv`).
- **CSV Dataset:**  
  Ensure that the dataset is placed in the `data/` directory. The app dynamically adapts to changes in the dataset.

### Visualizations and Interactivity
- **Custom HTML/CSS Styling:**  
  The periodic table grid and element cards use inline HTML styling for clear visualization.
- **Interactive Plotly Charts:**  
  All charts (line, 3D scatter, and radar) are built with Plotly for interactivity, responsiveness, and a polished look.

## Installation

### Prerequisites
- **Python 3.7+**
- **pip** package manager

### Setup Instructions

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/advanced-periodic-table-visualizer.git
   cd advanced-periodic-table-visualizer
