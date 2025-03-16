import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import base64
import json
from streamlit_plotly_events import plotly_events
import numpy as np
from scipy.ndimage import gaussian_filter1d

st.set_page_config(page_title="Periodic Table Explorer", layout="wide")
MAX_GROUP = 18
MAX_PERIOD = 7 

@st.cache_data
def load_data(filepath):
    try:
        if not os.path.exists(filepath):
            st.error(f"File not found: {filepath}")
            st.stop()
        return pd.read_csv(filepath)
    except Exception as e:
        st.error(f"An error occurred while loading the dataset: {e}")
        st.stop()

DATA_PATH = "data/Periodic Table of Elements.csv"
df = load_data(DATA_PATH)

# Ensure 'Type' column has string values and handle NaN
df['Type'] = df['Type'].fillna('Unknown').astype(str)

st.markdown("""
<style>
body {
    background-color: #1a1a1a;
    color: white;
}

.periodic-table {
    overflow-x: auto;
    padding: 15px;
    background: #1a1a1a;
    border-radius: 10px;
}

.grid {
    display: grid;
    grid-template-columns: repeat(18, 70px);
    gap: 5px;
    padding: 10px;
    background: #1a1a1a;
}

.lanthanides, .actinides {
    display: grid;
    grid-template-columns: repeat(15, 70px);
    gap: 5px;
    margin-top: 20px;
    padding: 10px;
    background: #1a1a1a;
}

.element {
    position: relative;
    width: 70px;
    height: 70px;
    border-radius: 5px;
    cursor: pointer;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    font-family: Arial, sans-serif;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
}

.element:hover {
    transform: scale(1.1);
    z-index: 10;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.5);
}

.element-name {
    font-size: 10px;
    margin-top: 5px;
    color: white;
}

.element-symbol {
    font-size: 24px;
    font-weight: bold;
    color: white;
    margin-bottom: 5px;
}

.element-atomic {
    font-size: 12px;
    color: white;
}

.element-image {
    position: absolute;
    width: 100%;
    height: 100%;
    object-fit: cover;
    opacity: 0;
    transition: opacity 0.3s ease;
}

.element:hover .element-image {
    opacity: 1;
}

/* Element category colors */
.Alkali-Metal {
    background-color: #ff7f7f;
}

.Alkaline-Earth-Metal {
    background-color: #ffa57f;
}

.Transition-Metal {
    background-color: #e6e6fa;
}

.Post-Transition-Metal {
    background-color: #b3d9ff;
}

.Metalloid {
    background-color: #ffffb3;
}

.Nonmetal {
    background-color: #ffb3b3;
}

.Halogen {
    background-color: #ffb3ff;
}

.Noble-Gas {
    background-color: #b3ffb3;
}

.Lanthanide {
    background-color: #b3ffff;
}

.Actinide {
    background-color: #ffb3e6;
}

.Unknown {
    background-color: #d3d3d3;
}

/* Sidebar styles */
.stSidebar {
    background-color: #2d2d2d;
}

/* Button styles */
.stButton>button {
    min-height: 45px;
    font-size: 18px;
    border-radius: 8px;
    background: #4a90e2;
    color: white;
    transition: background 0.3s ease;
}

.stButton>button:hover {
    background: #357abd;
}

/* Input styles */
.stTextInput>input, .stSelectbox, .stMultiselect {
    font-size: 16px;
    border-radius: 8px;
    padding: 10px;
    background-color: #333;
    color: white;
}

/* Dataframe styles */
[data-bbox~="0, 0, 960, 780"] {
    background-color: #222;
}

/* Tab styles */
[data-testid="stTab"] {
    background-color: #222;
}

/* Expander styles */
[data-testid="stExpander"] {
    background-color: #222;
}
</style>
""", unsafe_allow_html=True)

st.title("⚛️ Periodic Table Explorer")
st.markdown("""
Dive into the fascinating world of elements with interactive visualizations, advanced filtering, and detailed analytics.
""")

with st.sidebar:
    st.header("🔍 Element Filters")
    with st.expander("Search & Filter Options", expanded=True):
        element_name = st.text_input("Search Element", "", placeholder="e.g., Hydrogen")
        group = st.multiselect("Filter by Group", df['Group'].dropna().unique())
        period = st.multiselect("Filter by Period", df['Period'].dropna().unique())
        is_metal = st.selectbox("Filter by Metal Type", ["All", "Metal", "Nonmetal", "Metalloid"], index=0)
        is_radioactive = st.selectbox("Filter by Radioactivity", ["All", "Radioactive", "Non-Radioactive"], index=0)

filtered_data = df.copy()
if element_name:
    filtered_data = filtered_data[filtered_data['Element'].str.contains(element_name, case=False, na=False)]
if group:
    filtered_data = filtered_data[filtered_data['Group'].isin(group)]
if period:
    filtered_data = filtered_data[filtered_data['Period'].isin(period)]
if is_metal != "All":
    filtered_data = filtered_data[filtered_data["Type"] == is_metal]
if is_radioactive != "All":
    filtered_data = filtered_data[filtered_data["Radioactive"] == ("yes" if is_radioactive == "Radioactive" else "no")]

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Interactive Periodic Table", "📊 Data Analysis", "📈 Trend Visualization", 
    "🔬 Analytics", "🖼️ Element Gallery", "🔍 Element Details"
])

element_colors = {
    "Alkali Metal": "#ff7f7f",
    "Alkaline Earth Metal": "#ffa57f",
    "Transition Metal": "#e6e6fa",
    "Post-Transition Metal": "#b3d9ff",
    "Metalloid": "#ffffb3",
    "Nonmetal": "#ffb3b3",
    "Halogen": "#ffb3ff",
    "Noble Gas": "#b3ffb3",
    "Lanthanide": "#b3ffff",
    "Actinide": "#ffb3e6",
    "Unknown": "#d3d3d3"
}


image_dir = 'images/elements/'
image_data = {}
for atomic_number in range(1, 119):
    image_path = os.path.join(image_dir, f"{atomic_number}.png")
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode('utf-8')
            image_data[atomic_number] = f"data:image/png;base64,{encoded}"
    else:
        image_data[atomic_number] = None

with tab1:

    history_of_periodic_table = """
    ## History of the Periodic Table

    The periodic table of elements is one of the most significant scientific achievements in history. It organizes all known elements based on their atomic number, electron configurations, and recurring chemical properties. The table was first proposed by **Dmitri Mendeleev** in 1869, who arranged the elements by atomic mass and noticed periodic trends in their properties.
    
    ### **Key Milestones:**
    - **1669:** Hennig Brand discovers phosphorus, marking the beginning of systematic chemical research into the elements.
    - **1789:** Antoine Lavoisier publishes the first extensive list of elements, distinguishing between metals and non-metals.
    - **1869:** Dmitri Mendeleev publishes the first version of the periodic table, predicting undiscovered elements based on gaps in the table.
    - **1913:** Henry Moseley refines the table by arranging elements based on atomic number rather than atomic mass.
    - **1940s–Present:** Synthetic elements, such as plutonium and seaborgium, are created in laboratories, expanding the periodic table.

    Mendeleev’s original periodic table was remarkable for its predictive power. He left gaps in his table for elements that were not yet discovered but accurately predicted their properties. For example, his prediction of **eka-aluminum** corresponded almost exactly to the properties of gallium, which was discovered later.

    The periodic table continues to evolve as new elements are discovered and as the atomic model becomes more refined. Today, the periodic table not only serves as a tool for chemists but also represents the culmination of centuries of scientific inquiry into the building blocks of matter.
    """

    basic_info_periodic_table = """
    ## Basic Information About the Periodic Table

    The periodic table is a tabular arrangement of all known chemical elements. The elements are ordered by their atomic number (the number of protons in the nucleus of an atom), with each element also having a specific electron configuration. It is widely used in chemistry, physics, biology, and engineering.

    ### **Structure of the Periodic Table:**
    1. **Groups (Columns):** The vertical columns of the periodic table. There are 18 groups, and elements in the same group often have similar chemical properties.
        - **Group 1:** Alkali metals (e.g., Lithium, Sodium)
        - **Group 2:** Alkaline Earth metals (e.g., Magnesium, Calcium)
        - **Groups 3–12:** Transition metals (e.g., Iron, Copper, Zinc)
        - **Group 17:** Halogens (e.g., Fluorine, Chlorine)
        - **Group 18:** Noble gases (e.g., Helium, Neon)

    2. **Periods (Rows):** The horizontal rows of the periodic table. There are 7 periods. As you move across a period from left to right, elements transition from metals to nonmetals, and their properties gradually change.

    3. **Blocks of the Periodic Table:**
        - **s-block:** Includes Groups 1 and 2, along with Helium.
        - **p-block:** Includes Groups 13 to 18.
        - **d-block:** Transition metals, which occupy the center of the table.
        - **f-block:** Lanthanides and Actinides, often displayed separately at the bottom.

    4. **Categories of Elements:**
        - **Metals:** Found on the left and center of the table, metals are generally shiny, conductive, malleable, and ductile.
        - **Nonmetals:** Found on the right side of the table, nonmetals are often brittle and are insulators of electricity.
        - **Metalloids:** Elements with properties intermediate between metals and nonmetals. Examples include boron and silicon.

    5. **Periodic Trends:**
        - **Atomic Radius:** Decreases across a period and increases down a group.
        - **Ionization Energy:** Increases across a period and decreases down a group.
        - **Electronegativity:** Increases across a period and decreases down a group.
    """

    fun_facts_about_periodic_table = """
    ## Fun Facts About the Periodic Table
    1. **Ununseptium to Oganesson:** The most recently discovered elements, including **Oganesson (Og)**, are synthetic and only exist momentarily in laboratories.
    2. **Gold and Platinum:** These metals are so unreactive that they are often found in their pure forms in nature, unlike most elements.
    3. **Carbon:** Known as the "King of Elements," carbon forms the backbone of organic chemistry and is the basis for all known life.
    4. **Helium:** The second most abundant element in the universe is used in everything from party balloons to cooling superconducting magnets in MRI machines.
    5. **Periodic Table Song:** There is a famous song by Tom Lehrer that lists all the known elements at the time, set to the tune of "The Major General's Song" from Gilbert and Sullivan's *The Pirates of Penzance*.
    """

    features_modern_chemistry = """
    ##  Features of Modern Chemistry
    1. **Synthetic Elements:** As of today, there are 118 elements in the periodic table, with elements beyond uranium (92) being man-made in particle accelerators. These include **plutonium**, **americium**, and **seaborgium**.
    2. **Isotopes:** Many elements have isotopes, which are atoms of the same element with different numbers of neutrons. Some isotopes, like **Carbon-14**, are used in radiocarbon dating to estimate the age of fossils and artifacts.
    3. **Superheavy Elements:** Scientists are working to create and study "island of stability" elements, hypothesized to be more stable than other synthetic elements.
    4. **Element Naming:** The naming of new elements is governed by the International Union of Pure and Applied Chemistry (IUPAC). Names often honor scientists or places, such as **Einsteinium (Es)** or **Moscovium (Mc)**.
    """

    periodic_table_in_everyday_life = """
    ## The Periodic Table in Everyday Life
    1. **In Medicine:** Elements like **Iodine** and **Technetium** are used in medical imaging and treatments.
    2. **In Technology:** Elements like **Silicon** power the semiconductor industry, while **Lithium** is essential for rechargeable batteries.
    3. **In Environment:** Noble gases like **Argon** are used in energy-efficient windows, and **Oxygen** is critical for life and industrial processes.
    4. **In Food and Health:** Trace elements like **Zinc** and **Iron** are crucial for human health, supporting functions like enzyme activity and oxygen transport.
    """



    def create_periodic_table(df):
       
      
        grid = [[None for _ in range(MAX_GROUP)] for _ in range(MAX_PERIOD)]

        
        lanthanides = df[(df['AtomicNumber'] >= 57) & (df['AtomicNumber'] <= 71)]
        actinides = df[(df['AtomicNumber'] >= 89) & (df['AtomicNumber'] <= 103)]

  
        for _, row in df.iterrows():
            if 57 <= row['AtomicNumber'] <= 71 or 89 <= row['AtomicNumber'] <= 103:
              
                continue
            try:
                group = int(row['Group']) - 1 if not pd.isnull(row['Group']) else None
                period = int(row['Period']) - 1 if not pd.isnull(row['Period']) else None

                if group is not None and period is not None:
                    grid[period][group] = row
            except (ValueError, KeyError):
                continue  


        for period in range(MAX_PERIOD):
            cols = st.columns(MAX_GROUP)
            for group in range(MAX_GROUP):
                if grid[period][group] is not None:
                    element = grid[period][group]
                    symbol = element['Symbol']
                    atomic_number = element['AtomicNumber']
                    name = element['Element']
                    element_type = element['Type']
                    color = element_colors.get(element_type, "#FFFFFF")  # Default to white if type not found

           
                    with cols[group]:
                        st.markdown(
                            f"""
                            <div style="text-align: center; background-color: {color}; 
                                        border-radius: 5px; padding: 10px; margin: 5px; color: #000000;">
                                <strong>{symbol}</strong><br>
                                <small>{atomic_number}</small><br>
                                <small>{name}</small>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                else:
                    with cols[group]:
                        st.markdown("<div style='padding: 10px; margin: 5px;'>&nbsp;</div>", unsafe_allow_html=True)


        if len(lanthanides) > 0:
            st.subheader("Lanthanides")
            lan_cols = st.columns(len(lanthanides))
            for i, (_, element) in enumerate(lanthanides.iterrows()):
                with lan_cols[i]:
                    symbol = element['Symbol']
                    atomic_number = element['AtomicNumber']
                    name = element['Element']
                    color = element_colors['Lanthanide']
                    st.markdown(
                        f"""
                        <div style="text-align: center; background-color: {color}; 
                                    border-radius: 5px; padding: 10px; margin: 5px; color: #000000;">
                            <strong>{symbol}</strong><br>
                            <small>{atomic_number}</small><br>
                            <small>{name}</small>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
        else:
            st.subheader("Lanthanides")
            st.write("No lanthanides data available.")

        # Render Actinides
        if len(actinides) > 0:
            st.subheader("Actinides")
            act_cols = st.columns(len(actinides))
            for i, (_, element) in enumerate(actinides.iterrows()):
                with act_cols[i]:
                    symbol = element['Symbol']
                    atomic_number = element['AtomicNumber']
                    name = element['Element']
                    color = element_colors['Actinide']
                    st.markdown(
                        f"""
                        <div style="text-align: center; background-color: {color}; 
                                    border-radius: 5px; padding: 10px; margin: 5px; color: #000000;">
                            <strong>{symbol}</strong><br>
                            <small>{atomic_number}</small><br>
                            <small>{name}</small>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
        else:
            st.subheader("Actinides")
            st.write("No actinides data available.")


    st.markdown(history_of_periodic_table)
    st.markdown(basic_info_periodic_table)
    
    create_periodic_table(df)    
    st.markdown(fun_facts_about_periodic_table)
    st.markdown(features_modern_chemistry)
    st.markdown(periodic_table_in_everyday_life)

with tab2:
    st.subheader("📊 Data Analysis")
    st.markdown("Explore the periodic table data with filtering and statistical analysis.")

    st.markdown("### Column Selection")
    available_columns = df.columns.tolist()
    selected_columns = st.multiselect(
        "Choose Columns to Display",
        options=available_columns,
        default=available_columns[:5],
        help="Select which columns you want to display in the table."
    )

    if not selected_columns:
        st.warning("Please select at least one column to display.")
    else:
        st.markdown("### Search and Filter")
        search_query = st.text_input(
            "🔍 Search for Specific Values",
            placeholder="Type an element name, symbol, or value...",
            help="Search for elements across all displayed columns."
        )

        filtered_table = filtered_data.copy()
        for column in selected_columns:
            if filtered_table[column].dtype in ['float64', 'int64']:
                min_val, max_val = float(filtered_table[column].min()), float(filtered_table[column].max())
                filter_range = st.slider(
                    f"Filter {column}:",
                    min_value=min_val,
                    max_value=max_val,
                    value=(min_val, max_val),
                    key=f"slider_{column}"
                )
                filtered_table = filtered_table[
                    (filtered_table[column] >= filter_range[0]) & (filtered_table[column] <= filter_range[1])
                ]
            elif filtered_table[column].nunique() <= 10:
                unique_values = filtered_table[column].dropna().unique()
                selected_values = st.multiselect(
                    f"Select {column}:",
                    options=unique_values,
                    default=unique_values,
                    key=f"multiselect_{column}"
                )
                filtered_table = filtered_table[filtered_table[column].isin(selected_values)]

        if search_query:
            filtered_table = filtered_table[
                filtered_table.apply(lambda row: search_query.lower() in row.to_string().lower(), axis=1)
            ]

        st.markdown(f"### Filtered Table ({len(filtered_table)} Rows)")
        styled_table = filtered_table[selected_columns].style.set_properties(**{
            'background-color': 'rgba(255, 255, 255, 0.1)',
            'color': 'white',
            'border': '1px solid rgba(255, 255, 255, 0.2)',
            'border-radius': '5px',
            'padding': '8px',
            'font-family': 'Arial, sans-serif'
        })

        def highlight_radioactive(row):
            if 'Radioactive' in row and row['Radioactive'] == 'yes':
                return ['background-color: rgba(255, 0, 0, 0.2); color: white;'] * len(row)
            return [''] * len(row)

        styled_table = styled_table.apply(highlight_radioactive, axis=1)
        st.dataframe(styled_table, use_container_width=True, height=400)

        st.markdown("### Data Download")
        csv = styled_table.data.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download Filtered Data",
            data=csv,
            file_name="filtered_periodic_table.csv",
            mime="text/csv",
            help="Download the filtered table as a CSV file."
        )

with tab3:
    st.subheader("📈 Trend Visualization")
    st.markdown("Explore how element properties change across the periodic table.")

    numeric_properties = filtered_data.select_dtypes(include=['number']).columns.tolist()
    if not numeric_properties:
        st.warning("No numeric properties found for comparison.")
    else:
        trend_properties = st.multiselect(
            "Select Properties to Compare",
            options=numeric_properties,
            default=numeric_properties[:2],
            help="Select the properties you want to compare across atomic numbers."
        )

        st.markdown("### Chart Customization")
        show_markers = st.checkbox("Show Data Points", value=True)
        use_smoothing = st.checkbox("Apply Smoothing")
        line_style = st.selectbox(
            "Line Style",
            ["solid", "dash", "dot", "dashdot"],
            index=0
        )

        if trend_properties:
            data_to_plot = filtered_data.copy()
            if use_smoothing:
                for prop in trend_properties:
                    data_to_plot[prop] = gaussian_filter1d(data_to_plot[prop].fillna(0), sigma=2)

            fig = px.line(
                data_to_plot,
                x="AtomicNumber",
                y=trend_properties,
                title="Property Trends Across Elements",
                markers=show_markers,
                line_dash_sequence=[line_style],
                color_discrete_sequence=px.colors.qualitative.Bold
            )

            fig.update_layout(
                title=dict(
                    text="Property Trends Across Elements",
                    font=dict(size=24, color="white"),
                    x=0.5,
                    y=0.95
                ),
                xaxis_title="Atomic Number",
                yaxis_title="Property Value",
                legend=dict(
                    title="Properties",
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                ),
                hovermode="x unified",
                template="plotly_dark",
                margin=dict(l=0, r=0, b=0, t=50),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )

            fig.update_traces(mode="lines+markers" if show_markers else "lines")
            st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.subheader("🔬 Analytics")
    st.markdown("Explore 3D relationships between element properties.")

    atomic_number_range = st.slider(
        "Select Atomic Number Range",
        min_value=int(filtered_data['AtomicNumber'].min()),
        max_value=int(filtered_data['AtomicNumber'].max()),
        value=(int(filtered_data['AtomicNumber'].min()), int(filtered_data['AtomicNumber'].max()))
    )

    plot_data = filtered_data[
        (filtered_data['AtomicNumber'] >= atomic_number_range[0]) & 
        (filtered_data['AtomicNumber'] <= atomic_number_range[1])
    ]
    numeric_columns = plot_data.select_dtypes(include=['number']).columns.tolist()

    if len(numeric_columns) < 5:
        st.error("Not enough numeric columns for 3D analysis.")
    else:
        x_property = st.selectbox("X-Axis Property", numeric_columns, index=0)
        y_property = st.selectbox("Y-Axis Property", numeric_columns, index=1)
        z_property = st.selectbox("Z-Axis Property", numeric_columns, index=2)
        size_property = st.selectbox("Bubble Size Property", numeric_columns, index=3)
        color_property = st.selectbox("Bubble Color Property", numeric_columns, index=4)

        plot_data = plot_data.dropna(subset=[x_property, y_property, z_property, size_property, color_property])
        plot_data = plot_data.fillna(0)

        if plot_data.empty:
            st.warning("No data available for the selected filters or properties.")
        else:
            fig = px.scatter_3d(
                plot_data,
                x=x_property,
                y=y_property,
                z=z_property,
                size=size_property,
                color=color_property,
                hover_name="Element",
                hover_data=["Symbol", "AtomicNumber", "AtomicMass", "Density", "IonizationEnergy"],
                title="3D Property Relationships"
            )

            log_scale = st.checkbox("Apply Logarithmic Scale")
            if log_scale:
                fig.update_layout(scene=dict(
                    xaxis=dict(type="log"),
                    yaxis=dict(type="log"),
                    zaxis=dict(type="log")
                ))

            marker_size = st.slider("Bubble Size", min_value=5, max_value=30, value=10)
            fig.update_traces(marker=dict(size=plot_data[size_property] * marker_size))

            fig.update_layout(
                title=dict(
                    text="3D Property Relationships",
                    font=dict(size=24, color="white"),
                    x=0.5
                ),
                scene=dict(
                    xaxis_title=x_property,
                    yaxis_title=y_property,
                    zaxis_title=z_property,
                    bgcolor="rgba(0,0,0,0)"
                ),
                margin=dict(l=0, r=0, b=0, t=50),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )

            st.plotly_chart(fig, use_container_width=True)

with tab5:
    st.subheader("🖼️ Element Gallery")
    st.markdown("Browse visual representations of elements with their properties.")

    elements_per_row = st.selectbox("Elements per row", [10, 15, 20], index=0)
    elements = filtered_data.sort_values("AtomicNumber")["Element"].unique()
    num_rows = int(np.ceil(len(elements) / elements_per_row))

    for row in range(num_rows):
        cols = st.columns(elements_per_row)
        for idx in range(elements_per_row):
            element_idx = row * elements_per_row + idx
            if element_idx < len(elements):
                element_name = elements[element_idx]
                element_data = filtered_data[filtered_data["Element"] == element_name].iloc[0]
                with cols[idx]:
                    if image_data[element_data["AtomicNumber"]]:
                        st.image(image_data[element_data["AtomicNumber"]], use_container_width=True)
                    else:
                        st.write("No image available")
                    st.markdown(f"""
                    <div style="background: rgba(255, 255, 255, 0.1); padding: 10px; border-radius: 8px; text-align: center;">
                        <p><strong>{element_data['Symbol']}</strong></p>
                        <p style="font-size: 12px; color: white;">{element_data['Element']}</p>
                        <p style="font-size: 12px; color: white;">{element_data['AtomicNumber']}</p>
                    </div>
                    """, unsafe_allow_html=True)




with tab6:
    st.subheader("🔎 Element-Level Details")

    selected_element = st.selectbox(
        "Choose an Element for Details", 
        df["Element"].unique(), 
        key="element_details"
    )

 
    element_data = df[df["Element"] == selected_element].iloc[0]


    st.markdown(f"""
    <div style="background-color:#f1f1f1; padding: 20px; border-radius: 10px; border: 2px solid #ddd;">
        <h3 style='color: #2a7d8e; font-weight: bold; text-align: center;'>Element: {element_data['Element']}</h3>
        <div style="display: flex; flex-wrap: wrap; justify-content: space-between;">
            <div style="flex-basis: 45%; margin-bottom: 10px;">
                <p style='font-size: 16px; color: #333;'><strong>Symbol:</strong> {element_data['Symbol']}</p>
                <p style='font-size: 16px; color: #333;'><strong>Atomic Number:</strong> {element_data['AtomicNumber']}</p>
                <p style='font-size: 16px; color: #333;'><strong>Atomic Mass:</strong> {element_data['AtomicMass']} g/mol</p>
                <p style='font-size: 16px; color: #333;'><strong>Density:</strong> {element_data['Density']} g/cm³</p>
                <p style='font-size: 16px; color: #333;'><strong>Boiling Point:</strong> {element_data['BoilingPoint']} °C</p>
            </div>
            <div style="flex-basis: 45%; margin-bottom: 10px;">
                <p style='font-size: 16px; color: #333;'><strong>Melting Point:</strong> {element_data['MeltingPoint']} °C</p>
                <p style='font-size: 16px; color: #333;'><strong>Ionization Energy:</strong> {element_data.get('IonizationEnergy', 'N/A')} eV</p>
                <p style='font-size: 16px; color: #333;'><strong>Electron Affinity:</strong> {element_data.get('ElectronAffinity', 'N/A')} eV</p>
                <p style='font-size: 16px; color: #333;'><strong>Number of Shells:</strong> {element_data['NumberofShells']}</p>
                <p style='font-size: 16px; color: #333;'><strong>Valence Electrons:</strong> {element_data['NumberofValence']}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <hr style='border: 1px solid #ddd;' />
        <h4 style='color: #2a7d8e;'>Definitions:</h4>
        <ul>
            <li><strong>Atomic Number</strong>: The number of protons in the nucleus of an atom, determines the element.</li>
            <li><strong>Atomic Mass</strong>: The weighted average mass of the atoms in an element.</li>
            <li><strong>Density</strong>: The mass per unit volume of a substance.</li>
            <li><strong>Boiling Point</strong>: The temperature at which a substance changes from liquid to gas.</li>
            <li><strong>Melting Point</strong>: The temperature at which a solid turns into a liquid.</li>
            <li><strong>Ionization Energy</strong>: The energy required to remove an electron from an atom.</li>
            <li><strong>Electron Affinity</strong>: The amount of energy released when an electron is added to a neutral atom.</li>
            <li><strong>Number of Shells</strong>: The number of electron energy levels in an atom.</li>
            <li><strong>Valence Electrons</strong>: Electrons in the outermost shell of an atom, crucial for chemical bonding.</li>
        </ul>
    """, unsafe_allow_html=True)


    

st.markdown("---")
st.write("✨ Discover the wonders of chemistry with interactive exploration!")