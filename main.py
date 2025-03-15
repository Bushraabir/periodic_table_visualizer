import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# Set Page Configuration
st.set_page_config(page_title="Periodic Table Visualizer", layout="wide")


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

# Global CSS
st.markdown("""
<style>
/* Periodic Table Container */
.periodic-table {
    overflow-x: auto;
    padding: 10px;
}

/* Main Grid */
.grid {
    display: grid;
    grid-template-columns: repeat(18, 60px);
    grid-gap: 5px;
    min-width: 1080px;
}

/* Lanthanides and Actinides Grids */
.lanthanides, .actinides {
    display: grid;
    grid-template-columns: repeat(15, 60px);
    grid-gap: 5px;
    margin-top: 20px;
}

/* Element Styling */
.element {
    text-align: center;
    background-color: #f0f0f0;
    border-radius: 5px;
    padding: 5px;
    font-size: 12px;
    color: #000;
    cursor: pointer;
    transition: transform 0.2s;
}
.element:hover {
    transform: scale(1.1);
}

/* Responsive Adjustments */
@media (max-width: 768px) {
    .grid {
        grid-template-columns: repeat(18, 40px);
    }
    .lanthanides, .actinides {
        grid-template-columns: repeat(15, 40px);
    }
    .element {
        font-size: 10px;
        padding: 3px;
    }
}

/* Ensure Buttons and Inputs are Touch-Friendly */
.stButton>button {
    min-height: 40px;
    font-size: 16px;
}
.stTextInput>input, .stSelectbox, .stMultiselect {
    font-size: 16px;
}
</style>
""", unsafe_allow_html=True)


st.title("⚛️  Periodic Table Explorer")
st.markdown("""
Explore the periodic table using ** visualizations**, **statistical analysis**, and **customized filters**.  
Dive deep into the properties of elements and uncover trends, relationships, and insights.
""")

# Sidebar Filters
with st.sidebar:
    st.header("🔍 Filter Elements")
    with st.expander("Search and Filter", expanded=True):
        element_name = st.text_input("Search Element", "", placeholder="e.g., Hydrogen")
        group = st.multiselect("Filter by Group", df['Group'].dropna().unique())
        period = st.multiselect("Filter by Period", df['Period'].dropna().unique())
        is_metal = st.selectbox("Filter by Metal Type", ["All", "Metal", "Nonmetal", "Metalloid"], index=0)
        is_radioactive = st.selectbox("Filter by Radioactivity", ["All", "Radioactive", "Non-Radioactive"], index=0)

# Filters to Create Filtered Dataframe
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

# Define Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Periodic Table", "📋 Table View", "📊 Trends", "📈 3D Visualizations", "🧪 Radar Charts", "🔎 Element Details"
])

# Constants and Colors
MAX_GROUP = 18
MAX_PERIOD = 7
element_colors = {
    "Alkali Metal": "#FF5733",
    "Alkaline Earth Metal": "#FFBD33",
    "Transition Metal": "#FFC300",
    "Post-Transition Metal": "#33FFBD",
    "Metalloid": "#33FFF3",
    "Nonmetal": "#337BFF",
    "Halogen": "#8D33FF",
    "Noble Gas": "#C700FF",
    "Lanthanide": "#FF33A8",
    "Actinide": "#FF3333",
    "Unknown": "#D3D3D3"
}

# Tab 1: Periodic Table
with tab1:
    # Define Static Content
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

    # Function to Create Responsive Periodic Table
    def create_periodic_table(df):
        lanthanides = df[(df['AtomicNumber'] >= 57) & (df['AtomicNumber'] <= 71)]
        actinides = df[(df['AtomicNumber'] >= 89) & (df['AtomicNumber'] <= 103)]
        
        # Main Grid HTML
        main_grid_html = '<div class="periodic-table"><div class="grid">'
        for period in range(1, 8):
            for group in range(1, 19):
                element = df[(df['Period'] == period) & (df['Group'] == group) & 
                             (~df['AtomicNumber'].between(57, 71)) & (~df['AtomicNumber'].between(89, 103))]
                if not element.empty:
                    element = element.iloc[0]
                    symbol = element['Symbol']
                    atomic_number = element['AtomicNumber']
                    name = element['Element']
                    element_type = element['Type']
                    color = element_colors.get(element_type, "#FFFFFF")
                    main_grid_html += f'<div class="element" style="background-color: {color};">'
                    main_grid_html += f'<strong>{symbol}</strong><br><small>{atomic_number}</small><br><small>{name}</small>'
                    main_grid_html += '</div>'
                else:
                    main_grid_html += '<div class="element" style="background-color: transparent;"></div>'
        main_grid_html += '</div></div>'

        # Lanthanides HTML
        lanth_html = '<div class="lanthanides">'
        for _, element in lanthanides.iterrows():
            symbol = element['Symbol']
            atomic_number = element['AtomicNumber']
            name = element['Element']
            color = element_colors['Lanthanide']
            lanth_html += f'<div class="element" style="background-color: {color};">'
            lanth_html += f'<strong>{symbol}</strong><br><small>{atomic_number}</small><br><small>{name}</small>'
            lanth_html += '</div>'
        lanth_html += '</div>'

        # Actinides HTML
        act_html = '<div class="actinides">'
        for _, element in actinides.iterrows():
            symbol = element['Symbol']
            atomic_number = element['AtomicNumber']
            name = element['Element']
            color = element_colors['Actinide']
            act_html += f'<div class="element" style="background-color: {color};">'
            act_html += f'<strong>{symbol}</strong><br><small>{atomic_number}</small><br><small>{name}</small>'
            act_html += '</div>'
        act_html += '</div>'

        # Combine and Display
        full_html = main_grid_html + '<h3>Lanthanides</h3>' + lanth_html + '<h3>Actinides</h3>' + act_html
        st.markdown(full_html, unsafe_allow_html=True)

    # Display Content
    st.markdown(history_of_periodic_table)
    st.markdown(basic_info_periodic_table)
    create_periodic_table(df)
    st.markdown(fun_facts_about_periodic_table)
    st.markdown(features_modern_chemistry)
    st.markdown(periodic_table_in_everyday_life)

# Tab 2: Table View
with tab2:
    st.subheader("📋 Filtered Periodic Table")
    st.markdown("""
    **Welcome to the Periodic Table Filter Tool!**  
    Customize your table view, search for elements, apply filters, and explore statistical summaries.  
    """)

    st.markdown("### 1️⃣ Select Columns to Display")
    available_columns = df.columns.tolist()
    selected_columns = st.multiselect(
        "Choose Columns to Display:",
        options=available_columns,
        default=available_columns[:5],
        help="Choose which columns you want to display in the table."
    )

    if len(selected_columns) == 0:
        st.warning("⚠️ Please select at least one column to display.")
    else:
        st.markdown("### 2️⃣ Search and Filter Table")
        search_query = st.text_input(
            "🔍 Search for Specific Values:",
            placeholder="Type an element name, symbol, or value...",
            help="Search for elements across all displayed columns."
        )

        filtered_table = filtered_data.copy()
        st.markdown("**Filter by Column Values:**")
        for column in selected_columns:
            if filtered_table[column].dtype in ['float64', 'int64']:
                min_val, max_val = float(filtered_table[column].min()), float(filtered_table[column].max())
                filter_range = st.slider(
                    f"{column} Range:",
                    min_value=min_val,
                    max_value=max_val,
                    value=(min_val, max_val),
                    help=f"Filter rows where {column} is within this range."
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
                    help=f"Choose specific {column} values to include in the table."
                )
                filtered_table = filtered_table[filtered_table[column].isin(selected_values)]

        if search_query:
            filtered_table = filtered_table[
                filtered_table.apply(lambda row: search_query.lower() in row.to_string().lower(), axis=1)
            ]

        st.markdown(f"### 3️⃣ Filtered Table ({len(filtered_table)} Rows)")
        styled_table = filtered_table[selected_columns]

        def highlight_radioactive(row):
            if 'Radioactive' in row and row['Radioactive'] == 'yes':
                return ['background-color: #FFB6C1; color: black;'] * len(row)
            return [''] * len(row)

        st.dataframe(
            styled_table.style.apply(highlight_radioactive, axis=1),
            use_container_width=True,
            height=400
        )

        st.markdown("### 4️⃣ Download Filtered Table")
        csv = styled_table.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Download as CSV",
            data=csv,
            file_name="filtered_periodic_table.csv",
            mime="text/csv",
            help="Download the filtered table as a CSV file."
        )

# Tab 3: Trends
with tab3:
    st.subheader("📊 Comparative Trends Across Atomic Numbers")
    st.markdown("""
    Explore how various properties of elements change with their atomic numbers.  
    Customize the trends by selecting properties, adding smoothing, and adjusting visualization styles.
    """)

    available_properties = filtered_data.select_dtypes(include=['number']).columns.tolist()[4:]
    if not available_properties:
        st.warning("⚠️ No numeric properties found for comparison.")
    else:
        trend_properties = st.multiselect(
            "Select Properties to Compare:",
            options=available_properties,
            default=available_properties[:2] if len(available_properties) > 1 else available_properties,
            help="Select the properties you want to compare across atomic numbers."
        )

        st.markdown("### 🔧 Customize Chart Appearance")
        show_markers = st.checkbox("Show Markers", value=True, help="Display markers for each data point.")
        use_smoothing = st.checkbox("Smooth the Line", value=False, help="Apply smoothing to the trends.")
        line_style = st.selectbox(
            "Line Style",
            options=["solid", "dash", "dot", "dashdot"],
            index=0,
            help="Choose the style of the trend lines."
        )

        if len(trend_properties) > 0:
            data_to_plot = filtered_data.copy()
            if use_smoothing:
                import scipy.ndimage
                for prop in trend_properties:
                    if prop in data_to_plot:
                        data_to_plot[prop] = scipy.ndimage.gaussian_filter1d(data_to_plot[prop].fillna(0), sigma=2)

            fig_trends = px.line(
                data_to_plot,
                x="AtomicNumber",
                y=trend_properties,
                title="Comparative Trends of Selected Properties",
                markers=show_markers,
                line_dash_sequence=[line_style],
                labels={"AtomicNumber": "Atomic Number", "value": "Property Value", "variable": "Properties"},
                color_discrete_sequence=px.colors.qualitative.Set1
            )

            fig_trends.update_layout(
                title=dict(text="Comparative Trends of Properties Across Atomic Numbers", font=dict(size=20, color="#4CAF50"), x=0.5),
                xaxis_title="Atomic Number",
                yaxis_title="Property Value",
                legend=dict(title="Properties", orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                template="plotly_white"
            )
            fig_trends.update_traces(mode="lines+markers" if show_markers else "lines", hoverinfo="all")
            st.plotly_chart(fig_trends, use_container_width=True)

            st.markdown("### 🔍 Insights")
            st.markdown("""
            - **Hover over the chart** to view detailed information about each property.  
            - Use the **legend** to toggle the visibility of specific properties.  
            - Enable **smoothing** to identify general trends without noise.  
            """)
        else:
            st.warning("⚠️ Please select at least one property to visualize.")

# Tab 4: 3D Visualizations
with tab4:
    st.subheader("📈 3D Visualizations")
    st.sidebar.header("Filter Data")
    atomic_number_range = st.sidebar.slider(
        "Select Atomic Number Range",
        min_value=int(filtered_data['AtomicNumber'].min()),
        max_value=int(filtered_data['AtomicNumber'].max()),
        value=(int(filtered_data['AtomicNumber'].min()), int(filtered_data['AtomicNumber'].max()))
    )

    plot_data = filtered_data[(filtered_data['AtomicNumber'] >= atomic_number_range[0]) & 
                              (filtered_data['AtomicNumber'] <= atomic_number_range[1])]
    numeric_columns = plot_data.select_dtypes(include=['number']).columns.tolist()

    if len(numeric_columns) < 5:
        st.error("Not enough numeric columns in the dataset for 3D plotting. Please check your data.")
    else:
        x_property = st.selectbox("X-Axis Property", numeric_columns, index=0)
        y_property = st.selectbox("Y-Axis Property", numeric_columns, index=1)
        z_property = st.selectbox("Z-Axis Property", numeric_columns, index=2)
        size_property = st.selectbox("Bubble Size Property", numeric_columns, index=3)
        color_property = st.selectbox("Bubble Color Property", numeric_columns, index=4)

        plot_data = plot_data.dropna(subset=[x_property, y_property, z_property, size_property, color_property])
        for col in [x_property, y_property, z_property, size_property, color_property]:
            plot_data[col] = pd.to_numeric(plot_data[col], errors='coerce')
        plot_data = plot_data.dropna()

        if plot_data.empty:
            st.warning("No data available for the selected filters or properties.")
        else:
            try:
                fig_3d = px.scatter_3d(
                    plot_data,
                    x=x_property,
                    y=y_property,
                    z=z_property,
                    size=size_property,
                    color=color_property,
                    hover_data=["Element", "Symbol", "AtomicNumber", "AtomicMass", "Density", "IonizationEnergy"],
                    title="3D Bubble Plot of Atomic Properties"
                )

                log_scale = st.checkbox("Apply Logarithmic Scale to Axes", value=False)
                if log_scale:
                    fig_3d.update_layout(scene=dict(xaxis=dict(type="log"), yaxis=dict(type="log"), zaxis=dict(type="log")))

                marker_size = st.slider("Bubble Size Adjustment", min_value=5, max_value=30, value=10)
                fig_3d.update_traces(marker=dict(size=plot_data[size_property] * marker_size))
                st.plotly_chart(fig_3d, use_container_width=True)
            except Exception as e:
                st.error(f"An error occurred while creating the 3D scatter plot: {e}")

# Tab 5: Radar Charts
with tab5:
    st.subheader("🧪 Radar Chart for Atomic Properties")
    selected_elements = st.multiselect(
        "Select Elements for Comparison",
        filtered_data["Element"].unique(),
        default=filtered_data["Element"].unique()[:2]
    )
    numeric_properties = filtered_data.select_dtypes(include=['int64', 'float64']).columns[4:]
    selected_properties = st.multiselect(
        "Select Properties to Visualize",
        numeric_properties,
        default=numeric_properties[:5]
    )

    if selected_elements and selected_properties:
        fig_radar = go.Figure()
        for selected_element in selected_elements:
            element_data = filtered_data[filtered_data["Element"] == selected_element].iloc[0]
            values = [element_data[prop] for prop in selected_properties if pd.notnull(element_data.get(prop, None))]
            if len(values) > 0:
                color = px.colors.qualitative.Set1[len(fig_radar.data) % len(px.colors.qualitative.Set1)]
                hover_text = [f"<b>{prop}</b>: {value}" for prop, value in zip(selected_properties, values)]
                fig_radar.add_trace(go.Scatterpolar(
                    r=values,
                    theta=selected_properties,
                    fill='toself',
                    name=f"{element_data['Element']} ({element_data['Symbol']})",
                    marker=dict(color=color, line=dict(color='rgba(0, 0, 0, 0.8)', width=2)),
                    hoverinfo='text',
                    text=hover_text,
                    hoverlabel=dict(bgcolor='rgba(255, 255, 255, 0.8)', font_size=12, font_family='Arial')
                ))

        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, ticks='outside', tickwidth=2, tickcolor='rgba(54, 162, 235, 1)', 
                                showticklabels=True, tickangle=0, tickfont=dict(size=14)),
                angularaxis=dict(tickfont=dict(size=14), linecolor='rgba(200, 200, 200, 1)')
            ),
            title="Radar Chart Comparison of Selected Elements",
            title_font=dict(size=26, family='Arial, sans-serif', color='rgba(0, 0, 0, 0.85)'),
            showlegend=True,
            legend=dict(title="Elements", x=1.05, y=1, font=dict(family="Arial", size=14), bgcolor="rgba(255, 255, 255, 0.7)"),
            margin=dict(t=40, b=40, l=40, r=40),
            paper_bgcolor="rgba(255, 255, 255, 1)",
            font=dict(size=16),
            hovermode='closest'
        )
        st.plotly_chart(fig_radar, use_container_width=True)

        st.markdown("### Element-Level Details")
        for selected_element in selected_elements:
            element_data = filtered_data[filtered_data["Element"] == selected_element].iloc[0]
            st.markdown(f"""
            #### {element_data['Element']} ({element_data['Symbol']})
            - **Atomic Number**: {element_data['AtomicNumber']}
            - **Atomic Mass**: {element_data['AtomicMass']} g/mol
            - **Density**: {element_data['Density']} g/cm³
            - **Boiling Point**: {element_data['BoilingPoint']} °C
            - **Melting Point**: {element_data['MeltingPoint']} °C
            - **Ionization Energy**: {element_data.get('IonizationEnergy', 'N/A')} eV
            - **Electron Affinity**: {element_data.get('ElectronAffinity', 'N/A')} eV
            - **Number of Shells**: {element_data['NumberofShells']}
            - **Valence Electrons**: {element_data['NumberofValence']}
            """)
    else:
        st.warning("Please select at least one element and one property for comparison.")

# Tab 6: Element Details
with tab6:
    st.subheader("🔎 Element-Level Details")
    selected_element = st.selectbox(
        "Choose an Element for Details",
        filtered_data["Element"].unique(),
        key="element_details"
    )
    element_data = filtered_data[filtered_data["Element"] == selected_element].iloc[0]

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

# Footer
st.markdown("---")
st.write("✨ Created with ❤️ to Explore the Beauty of the Periodic Table!")