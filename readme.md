# ⚛️ Periodic Table Visualizer

An interactive and visually appealing web application for exploring the periodic table of elements, built with [Streamlit](https://streamlit.io/) and [Plotly](https://plotly.com/). This project lets you filter elements, visualize trends, and dive into detailed element analytics with a modern, intuitive interface.

## 🌟 Features

- **Interactive Periodic Table:**  
  - 🔍 Explore elements in a grid with tooltips and hover effects.  
  - 🎨 Color-coded differentiation for element types (e.g., metals, nonmetals, lanthanides, actinides).

- **Data Analysis & Filtering:**  
  - 🔎 Filter elements by name, group, period, metal type, and radioactivity.  
  - 📊 Select columns, search for values, and download filtered data as CSV.

- **Trend Visualization:**  
  - 📈 Compare element properties across atomic numbers with interactive line charts.  
  - ✨ Options for smoothing, markers, and customizable line styles.

- **3D Analytics:**  
  - 🌐 Analyze 3D relationships between properties using customizable scatter plots.  
  - 📏 Dynamic selection for axes, bubble size, and color mapping.

- **Element Gallery:**  
  - 🖼️ Browse visual representations and images of elements.  
  - 🖥️ Enjoy a clean, responsive layout with adjustable elements per row.

- **Element-Level Details:**  
  - 🔬 Detailed view of each element including atomic number, mass, density, boiling/melting points, ionization energy, and more.  
  - 📚 Comprehensive definitions and explanations for key chemical properties.

## 🚀 Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Bushraabir/periodic_table_visualizer.git
   cd periodic_table_visualizer
Set up a virtual environment (optional but recommended):

bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
Install required packages:

bash
Copy
Edit
pip install -r requirements.txt
If a requirements.txt file is not available, install the libraries manually:

bash
Copy
Edit
pip install streamlit pandas plotly numpy scipy streamlit-plotly-events
Verify required files/directories:

data/Periodic Table of Elements.csv – CSV file with periodic table data.
images/elements/ – Directory with element images (e.g., 1.png, 2.png, etc.).
(Optional) images/banner.png – Banner image for the repository.
💻 Running the Application
Launch the Streamlit app with:

bash
Copy
Edit
streamlit run app.py
Replace app.py with your Python script's filename if different. The app will open in your default web browser, letting you interact with the periodic table, apply filters, visualize trends, and explore element details.

🗂️ Project Structure
bash
Copy
Edit
periodic_table_visualizer/
│
├── app.py                      # Main Streamlit application script
├── data/
│   └── Periodic Table of Elements.csv   # CSV file with element data
├── images/
│   ├── banner.png              # Optional banner image for the repo
│   └── elements/               # Directory containing element images (1.png, 2.png, ..., 118.png)
├── requirements.txt            # Python dependencies
└── README.md                   # This file
🤝 Contributing
Contributions are welcome! To contribute:

Fork the repository.

Create a new branch:

bash
Copy
Edit
git checkout -b feature/your-feature
Make your changes and commit them:

bash
Copy
Edit
git commit -m 'Add new feature'
Push to your branch:

bash
Copy
Edit
git push origin feature/your-feature
Open a Pull Request describing your changes.

🙏 Acknowledgments
Streamlit: For providing an easy-to-use platform for building interactive web applications.
Plotly: For their powerful visualization tools.
Open Source Community: For countless resources and inspiration in data visualization.
