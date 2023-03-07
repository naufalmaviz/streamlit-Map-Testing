# Basic libraries
import pandas as pd
import numpy as np
import os
import glob
from statistics import mean

# Map libraries
import folium
from folium import plugins, LinearColormap
from folium.plugins import Search, FloatImage
import geopandas as gpd
import branca

# Plotting libraries
import plotly.graph_objects as go
import plotly.express as px
import plotly.figure_factory as ff
from plotly.subplots import make_subplots

# Streamlit libraries
import streamlit as st
from streamlit_folium import folium_static
import streamlit_nested_layout


# Dataset
All_Blocks = gpd.read_file(r'GeoJSON Files/All_Blocks.geojson')
All_Boreholes = gpd.read_file(r'GeoJSON Files/All_Boreholes.geojson')
All_Well_Logs = pd.read_csv('CSV Files/well_all_log.csv', sep = ';')

# calculate the center of map
bounds = All_Blocks.total_bounds
x = mean([bounds[0], bounds[2]])
y = mean([bounds[1], bounds[3]])
location = (y, x)

# Initial customizations
st.set_page_config(
    page_title="Testing Map",
    layout="wide",
    initial_sidebar_state="auto"
)

# Styling
st.markdown("""
<style>
[data-testid=column]:nth-of-type(1) [data-testid=stVerticalBlock]{
    gap: 0rem;
}
</style>
""", unsafe_allow_html=True)


st.markdown("""
<style>
[data-testid=column]:nth-of-type(3) [data-testid=stVerticalBlock]{
    gap: 0rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
.big-font {
    font-size:7px !important;
}
.other-font {
    font-size:21px !important;
}
.spacing-font {
    font-size:5px !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    """
    <style>
        div[data-testid="column"]:nth-of-type(2)
        {
            border:1px;
            text-align: center;
        }
    """, unsafe_allow_html=True)

hide_menu_style = '''
<style>
#MainMenu {
    visibility:hidden;
}

footer{
    visibility:hidden;
}
</style>
'''
st.markdown(hide_menu_style, unsafe_allow_html=True)

hide_img_fs = '''
<style>
button[title="View fullscreen"]{
    visibility: hidden;}
</style>
'''
st.markdown(hide_img_fs, unsafe_allow_html=True)

# styling on tables pop up for Blocks
def make_popup(df):
    blockname = df["Block_Name"]
    status = df["Status"]
    operator = df["Operator"]
    kilos = df["Sq. Kilometers"]
    miles = df["Sq. Miles"]
        
    left_col_color = "#65b3d0"
    right_col_color = "#ebf2f7"
    
    html = """
    <!DOCTYPE html>
    <html>
    
    <head>
    <strong><h4 style="margin-bottom:30px; width:200px; font-size: 25px;">{}</strong></h4>""".format(blockname) + """

    
    </head>
        <table style="height: 126px; width: 300px;">
    <tbody>
    <tr>
    <td style="background-color: """ + left_col_color + """;"><span style="color: #151515;">Status</span></td>
    <td style="width: 200px;background-color: """ + right_col_color + """;">{}</td>""".format(status) + """
    </tr>
    <tr>
    <td style="background-color: """ + left_col_color + """;"><span style="color: #151515;">Operator</span></td>
    <td style="width: 200px;background-color: """ + right_col_color + """;">{}</td>""".format(operator) + """
    </tr>
    <tr>
    <td style="background-color: """ + left_col_color + """;"><span style="color: #151515;">Sq. Kilometers</span></td>
    <td style="width: 200px;background-color: """ + right_col_color + """;">{}</td>""".format(kilos) + """
    </tr>
    <tr>
    <td style="background-color: """ + left_col_color + """;"><span style="color: #151515;">Sq. Miles</span></td>
    <td style="width: 200px;background-color: """ + right_col_color + """;">{}</td>""".format(miles) + """
    </tr>
    </tbody>
    </table>
    </html>
    """
    return html

# styling on tables pop up for Boreholes
def make_popup_2(df):
    borehole = df["Borehole_I"]
    depth = df["Depth"]
    lithology = df["Lithology"]
    porosity = df["Porosity"]
    fluid_sat = df["Fluid_Satu"]
    oil_shows = df["Oil_shows"]
    gas_shows = df["Gas_shows"]
    blockname = df["Blocks"]

        
    left_col_color = "#65b3d0"
    right_col_color = "#ebf2f7"
    
    html = """
    <!DOCTYPE html>
    <html>
    
    <head>
    <strong><h4 style="margin-bottom:30px; width:200px; font-size: 25px;">{}</strong></h4>""".format(borehole) + """

    
    </head>
        <table style="height: 126px; width: 300px;">
    <tbody>
    <tr>
    <td style="background-color: """ + left_col_color + """;"><span style="color: #151515;">Depth (m)</span></td>
    <td style="width: 200px;background-color: """ + right_col_color + """;">{}</td>""".format(depth) + """
    </tr>
    <tr>
    <td style="background-color: """ + left_col_color + """;"><span style="color: #151515;">Lithology</span></td>
    <td style="width: 200px;background-color: """ + right_col_color + """;">{}</td>""".format(lithology) + """
    </tr>
    <tr>
    <td style="background-color: """ + left_col_color + """;"><span style="color: #151515;">Porosity</span></td>
    <td style="width: 200px;background-color: """ + right_col_color + """;">{}</td>""".format(porosity) + """
    </tr>
    <tr>
    <td style="background-color: """ + left_col_color + """;"><span style="color: #151515;">Fluid Saturation (%)</span></td>
    <td style="width: 200px;background-color: """ + right_col_color + """;">{}</td>""".format(fluid_sat) + """
    </tr>
    <tr>
    <td style="background-color: """ + left_col_color + """;"><span style="color: #151515;">Oil Shows (%)</span></td>
    <td style="width: 200px;background-color: """ + right_col_color + """;">{}</td>""".format(oil_shows) + """
    </tr>
    <tr>
    <td style="background-color: """ + left_col_color + """;"><span style="color: #151515;">Gas Shows (%)</span></td>
    <td style="width: 200px;background-color: """ + right_col_color + """;">{}</td>""".format(gas_shows) + """
    </tr>
    </tbody>
    </table>
    </html>
    """
    return html



# creating well logs dataframe and plotting to graphs

# logs = ['CALI', 'RDEP', 'GR', 'RHOB', 'NPHI', 'SP', 'DTC']
# colors = ['black', 'firebrick', 'green', 'mediumaquamarine', 'royalblue', 'goldenrod', 'lightcoral']

# def make_well_logs(df):
#     depth = df['Depth']
#     cali = df['CALI']
#     rdep = df['RDEP']
#     gr = df['GR']
#     rhob = df['RHOB']
#     nphi = df['NPHI']
#     sp = df['SP']
#     dtc = df['DTC']
#     lithology = df['Lithology']

text, display = st.columns([1,4])
with text:
    block_title = '<p style="color:#65b3d0; font-size: 45px;"><strong>Dummy Blocks </strong> </p>'
    st.markdown(block_title, unsafe_allow_html=True)
    
    st.markdown('<p class="spacing-font"> &nbsp; </p>',
                unsafe_allow_html=True)
    
    st.markdown('**Summary**')
    st.write('This block data are dummy, intended for testing purposes. All blocks are not representing the real conditions.')
    
    st.markdown('<p class="other-font"> &nbsp; </p>',
                unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(['Info', 'Blocks Filter', 'Wellhead Filter', 'Download'])

    with tab1:
        
        st.markdown('**Detail**')

        col1, mid, col2 = st.columns([1,1, 20])

        with col1:
            st.markdown('<p class="big-font"> &nbsp; </p>',
                        unsafe_allow_html=True)
            st.image(r'icon/data_icon.png', width=25)
            st.markdown('<p class="other-font"> &nbsp; </p>',
                        unsafe_allow_html=True)
            st.image(r'icon/info_icon.png', width=25)
            st.markdown('<p class="other-font"> &nbsp; </p>',
                        unsafe_allow_html=True)
            st.image(r'icon/date_icon.png', width=25)
            st.markdown('<p class="other-font"> &nbsp; </p>',
                        unsafe_allow_html=True)
            st.image(r'icon/world_icon.png', width=25)
            st.markdown('<p class="other-font"> &nbsp; </p>',
                        unsafe_allow_html=True)
            st.image(r'icon/lock_icon.png', width=27)
        
        with col2:
            # st.markdown('<p class="big-font"> </p>',
            #             unsafe_allow_html=True)
            st.caption('Feature Layer')
            st.markdown('**Dataset**')

            st.markdown('<p class="big-font"> &nbsp; </p>',
                        unsafe_allow_html=True)
            st.caption('Updated Info')
            st.markdown('**03 February 2023**')

            st.markdown('<p class="big-font"> &nbsp; </p>',
                        unsafe_allow_html=True)
            st.caption('Publication Date')
            st.markdown('**04 February 2023**')

            st.markdown('<p class="big-font"> &nbsp; </p>',
                        unsafe_allow_html=True)
            st.caption('Anyone can view this content')
            st.markdown('**Public**')

            st.markdown('<p class="big-font"> &nbsp; </p>',
                        unsafe_allow_html=True)
            st.caption('Request permission to use')
            st.markdown('**No License**')
            st.markdown('<p class="other-font"> &nbsp; </p>',
                        unsafe_allow_html=True)

        st.button('Get PDF files for more information')
        
    with tab2:
        
        #filter for blocks
        st.markdown('**Blocks**')
        
        with st.expander('Block name'):
            option_block = st.multiselect('Select the block name',   (All_Blocks['Block_Name']), default=All_Blocks['Block_Name'], label_visibility='collapsed')
            option_block_ = All_Blocks[All_Blocks['Block_Name'].isin(option_block)]
        
        st.markdown('<p class="big-font"> &nbsp; </p>',
        unsafe_allow_html=True)
        
        with st.expander('Status'):
            checkbox_stat_1 = st.checkbox('Exploration')
            checkbox_stat_2 = st.checkbox('Production')
            
            if checkbox_stat_1:
                option_block_ = option_block_[option_block_['Status'] == 'Exploration']
            elif checkbox_stat_2:
                option_block_ = option_block_[option_block_['Status'] == 'Production']
            elif checkbox_stat_1 and checkbox_stat_2:
                option_block_ = All_Blocks[All_Blocks['Status'].isin(['Exploration','Production'])]
            
        st.markdown('<p class="big-font"> &nbsp; </p>',
        unsafe_allow_html=True)
        
        with st.expander('Operator'):
            option_operator = st.multiselect(' ', (option_block_['Operator'].unique()), default = option_block_['Operator'].unique(), label_visibility='collapsed')
            option_block_ = option_block_[option_block_['Operator'].isin(option_operator)]
        
        st.markdown('<p class="big-font"> &nbsp; </p>',
        unsafe_allow_html=True)

        with st.expander('Shape area in Sq. Kilometers'):
            st.markdown('<p class="big-font"> &nbsp; </p>',
                        unsafe_allow_html=True)
            option_kilos = st.slider('Sq. Kilometers of block area', float(0.0), float(option_block_['Sq. Kilometers'].max() + 50), float(option_block_['Sq. Kilometers'].max()), 
                                    label_visibility='collapsed')
        
            option_block_ = option_block_[option_block_['Sq. Kilometers'] <= option_kilos]
        
        st.markdown('<p class="big-font"> &nbsp; </p>',
        unsafe_allow_html=True)
    
    with tab3:    
        #filter for boreholes
        
        #borehole = df["Borehole_I"]
        #depth = df["Depth"]
        #lithology = df["Lithology"]
        #porosity = df["Porosity"]
        #fluid_sat = df["Fluid_Satu"]
        #oil_shows = df["Oil_shows"]
        #gas_shows = df["Gas_shows"]
        #blockname = df["Blocks"]
        
        st.markdown('**Boreholes**')
        
        with st.expander('Boreholes'):
            option_bh = st.multiselect('Select the borehole',   (All_Boreholes['Borehole_I']), default=All_Boreholes['Borehole_I'], label_visibility='collapsed')
            option_bh_ = All_Boreholes[All_Boreholes['Borehole_I'].isin(option_bh)]
        
        st.markdown('<p class="big-font"> &nbsp; </p>',
        unsafe_allow_html=True)
        
        with st.expander('Depth in Meters'):
            st.markdown('<p class="big-font"> &nbsp; </p>',
                        unsafe_allow_html=True)
            option_depth = st.slider('Depth of borehole', float(0.0), float(option_bh_['Depth'].max() + 500), float(option_bh_['Depth'].max()), 
                                    label_visibility='collapsed')
        
            option_bh_ = option_bh_[option_bh_['Depth'] <= option_depth]
        
        st.markdown('<p class="big-font"> &nbsp; </p>',
        unsafe_allow_html=True)
            
        with st.expander('Lithology'):
            option_lith = st.multiselect('Lithology',   (option_bh_['Lithology']).unique(), default=option_bh_['Lithology'].unique(), label_visibility='collapsed')
            option_bh_ = option_bh_[option_bh_['Lithology'].isin(option_lith)]
        
        st.markdown('<p class="big-font"> &nbsp; </p>',
        unsafe_allow_html=True)
            
        with st.expander('Porosity in %'):
            st.markdown('<p class="big-font"> &nbsp; </p>',
                        unsafe_allow_html=True)
            option_poro = st.slider('Porosity in %', float(0.0), float(100), float(option_bh_['Porosity'].max()), 
                                    label_visibility='collapsed')
        
            option_bh_ = option_bh_[option_bh_['Porosity'] <= option_poro]
        
        st.markdown('<p class="big-font"> &nbsp; </p>',
        unsafe_allow_html=True)
        
        with st.expander('Fluid Saturation in %'):
            st.markdown('<p class="big-font"> &nbsp; </p>',
                        unsafe_allow_html=True)
            option_fluidst = st.slider('Fluid Saturation in %', float(0.0), float(option_bh_['Fluid_Satu'].max() + 10), float(option_bh_['Fluid_Satu'].max()), 
                                        label_visibility='collapsed')
        
            option_bh_ = option_bh_[option_bh_['Fluid_Satu'] <= option_fluidst]
        
        st.markdown('<p class="big-font"> &nbsp; </p>',
        unsafe_allow_html=True)
            
        with st.expander('Oil Shows'):
            option_oilsh = st.multiselect('Oil Shows',   (option_bh_['Oil_shows']).unique(), default=option_bh_['Oil_shows'].unique(), label_visibility='collapsed')
            option_bh_ = option_bh_[option_bh_['Oil_shows'].isin(option_oilsh)]
        
        st.markdown('<p class="big-font"> &nbsp; </p>',
        unsafe_allow_html=True)
        
        with st.expander('Gas Shows'):
            option_gassh = st.multiselect('Gas Shows',   (option_bh_['Gas_shows']).unique(), default=option_bh_['Gas_shows'].unique(), label_visibility='collapsed')
            option_bh_ = option_bh_[option_bh_['Gas_shows'].isin(option_gassh)]
        
        st.markdown('<p class="big-font"> &nbsp; </p>',
        unsafe_allow_html=True)
        
    with tab4:
        @st.cache
        def convert_csv(df):
            return df.to_csv().encode('utf-8')
        
        csv = convert_csv(option_block_)
        
        st.download_button(
            label='Download data as CSV',
            data=csv,
            file_name='Data_map.csv'
        )
               
with display:
    st.markdown('<p class="spacing-font"> &nbsp; </p>',
                unsafe_allow_html=True)
    # Initialize map (blank layer map with coordinate center in Aceh)
    map1 = folium.Map(location=location,
                    zoom_start=11, control_scale=300, tiles=None)

    # Put DEM for the layer map
    dem = folium.raster_layers.ImageOverlay(
                            "TIF Files/BATNAS_NORTH_ACEH.png",
                            name='BATNAS_NORTH_ACEH',
                            bounds=[[5, 95], [10, 100]],
                            opacity=0.7,
                            interactive=True,
                            cross_origin=False,
                            show=False
                            # colormap=lambda x: (1, 1, 1, x)
                            ).add_to(map1)

    dem2 = folium.raster_layers.ImageOverlay(
                            "TIF Files/BATNAS_SOUTH_ACEH.png",
                            bounds=[[0, 95], [5, 100]],
                            name='BATNAS_SOUTH_ACEH',
                            opacity=0.7,
                            interactive=True,
                            cross_origin=False,
                            show=False
                            # colormap=lambda x: (1, 1, 1, x)
                            ).add_to(map1)
    
    # adding legend for DEM
    color_map = LinearColormap(
                            ['blue', 'green', 'yellow', 'red'],  # List of colors in the color map
                            vmin=-3156,  # Minimum elevation value in your image
                            vmax=2277,  # Maximum elevation value in your image
                            )

    color_map.caption = 'Elevation'
    
    # Add the color map legend to the map
    legend = FloatImage(
                        color_map._repr_html_(), 
                        bottom=10, left=10
                        ).add_to(map1)
    
    # Put ESRI Satellite for the layer map
    tile = folium.TileLayer(
                            tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
                            attr='Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community',
                            name='Esri.WorldImagery',
                            overlay=False,
                            control=False,
                            show=True
                            ).add_to(map1)

    
    # Put Esri WorldTopoMap for the layer map

    tile2 = folium.TileLayer(
                            tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}',
                            attr='Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ, TomTom, Intermap, iPC, USGS, FAO, NPS, NRCAN, GeoBase, Kadaster NL, Ordnance Survey, Esri Japan, METI, Esri China (Hong Kong), and the GIS User Community',
                            name='Esri.WorldTopoMap',
                            overlay=False,
                            control=False,
                            show=False
                            ).add_to(map1)

    # Put openstreetmap for the layer map

    tile3 = folium.TileLayer(
                            tiles='https://tile.openstreetmap.org/{z}/{x}/{y}.png',
                            attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
                            name='OpenStreetMap.Mapnik',
                            overlay=False,
                            control=False,
                            show=False
                            ).add_to(map1)


    # Create a color bar legend and add it to the map
    legend = LinearColormap(
                            ['blue', 'cyan', 'yellow', 'red'],  # List of colors in the color map
                            vmin=-3156,  # Minimum elevation value in your image
                            vmax=2277,  # Maximum elevation value in your image
                            caption='Elevation',  # Label for the color bar
                            ).add_to(map1)

    legend.caption = 'Elevation'
        
    # put a minimap on bottom corner of the main map (optional, can be turned off) and other plugins such as szroll zoom toggler, fullscreen, etc
    minimap = plugins.MiniMap(toggle_display=True)
    map1.add_child(minimap)
    plugins.GroupedLayerControl({"BATNAS": [dem, dem2], "OpenStreetMap": [tile3], "Esri": [tile2] }, 
                                exclusive_groups=False,
                                hideSingleBase=True).add_to(map1)
    plugins.ScrollZoomToggler().add_to(map1)
    plugins.Fullscreen(position="topright").add_to(map1)
    plugins.Draw(position='topright').add_to(map1)
  
    # filter name blocks for showings
    def filter_by_name_blocks(df, parameter):
        return df[df['Block_Name'].isin(parameter)]

    # filter name boreholes for showings   
    def filter_by_name_boreholes(df, parameter):
        return df[df['Borehole_I'].isin(parameter)]

    # filter name well-log of boreholes for showings   
    def filter_by_name_well_log(df, parameter):
        return df[df['Borehole_I'].isin([parameter])]
    
    
    # option_block = st.multiselect('Select the block name', (All_Blocks['Block_Name']), default=All_Blocks['Block_Name'])
    df_filter_blocks = filter_by_name_blocks(option_block_, option_block)

    # Adding blocks to the main map
    for i, row in df_filter_blocks.iterrows():
        geo_json = folium.features.GeoJson(row.geometry.__geo_interface__, name=str(i), 
                                            style_function=
                                            lambda feature: {
                                            'fillColor':  '#65b3d0',
                                            #    'fillColor': '#F1D581' if 'x' in feature['properties']['Status'] == 'Exploration' else '#65b3d0',
                                            'color': 'black',
                                            'weight': 3,
                                            'fillOpacity': 0.2,
                                            'dashArray': '5,5'
                                        },

                                        highlight_function=lambda x: {
                                            'fillOpacity': 1},

                                        tooltip=folium.features.Tooltip(All_Blocks.iloc[i]['Block_Name'], sticky=False))
                                            # fields=All_Blocks.iloc[i]['Block_Name'], aliases=['Name']))
        
        geo_json.add_child(folium.Popup(make_popup(All_Blocks.iloc[i])))
        (geo_json.add_to(map1))

    # option_bh = st.multiselect('Select the borehole',   (All_Boreholes['Borehole_I'])
    df_filter_boreholes = filter_by_name_boreholes(option_bh_, option_bh)
    
    # Adding boreholes to the main map
    for j, row in df_filter_boreholes.iterrows():
        geo_json = folium.features.GeoJson(row.geometry.__geo_interface__, name=str(j), 
                                            # icon=folium.Icon( icon='glyphicon-pushpin'),

                                            tooltip=folium.features.Tooltip(All_Boreholes.iloc[j]['Borehole_I'], sticky=False))
                                            # fields=All_Boreholes.iloc[j]['Borehole_I'], aliases=['Name']))
        
        geo_json.add_child(folium.Popup(make_popup_2(All_Boreholes.iloc[j])))
        (geo_json.add_to(map1))
    
                                                   
    folium_static(map1, width=1500, height=700)
    
    st.markdown('<p class="big-font"> &nbsp; </p>',
        unsafe_allow_html=True)

# create container to contain well-log tables and graphs
with st.container():
    with st.expander('Well-log Data Display'):
        # create option for well-log
        option_well_log = st.selectbox('Select the well log', (All_Well_Logs['Borehole_I']).unique(), label_visibility='collapsed')
        option_well_log_ = All_Well_Logs[All_Well_Logs['Borehole_I'].isin([option_well_log])]
        
        #calling function to filter what well-log data should be shown
        df_filter_well_log = filter_by_name_well_log(option_well_log_, option_well_log)
        
        fig = make_subplots(rows=1, cols=7, shared_yaxes=True)

        # Add each well log parameter as a separate trace in its own subplot
        fig.add_trace(go.Scatter(x=df_filter_well_log['GR'], y=df_filter_well_log['Depth'],name='GR', line=dict(color='blue')), row=1, col=1)
        fig.add_trace(go.Scatter(x=df_filter_well_log['CALI'], y=df_filter_well_log['Depth'], name='CALI', line=dict(color='red')), row=1, col=2)
        fig.add_trace(go.Scatter(x=df_filter_well_log['RDEP'], y=df_filter_well_log['Depth'], name='RDEP', line=dict(color='green')), row=1, col=3)
        fig.add_trace(go.Scatter(x=df_filter_well_log['RHOB'], y=df_filter_well_log['Depth'], name='RHOB', line=dict(color='purple')), row=1, col=4)
        fig.add_trace(go.Scatter(x=df_filter_well_log['NPHI'], y=df_filter_well_log['Depth'], name='NPHI', line=dict(color='orange')), row=1, col=5)
        fig.add_trace(go.Scatter(x=df_filter_well_log['SP'], y=df_filter_well_log['Depth'], name='SP', line=dict(color='black')), row=1, col=6)
        fig.add_trace(go.Scatter(x=df_filter_well_log['DTC'], y=df_filter_well_log['Depth'], name='DTC', line=dict(color='pink')), row=1, col=7)

        # Set the layout of the subplots grid
        fig.update_layout(height=800, width=1200, title='Well Logs', xaxis=dict(title='Value'), yaxis=dict(title='Depth', autorange='reversed'))

        st.markdown('<p class="big-font"> &nbsp; </p>',
        unsafe_allow_html=True)

        # Show the figure
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)
        
        
        
            
        st.markdown('<p class="big-font"> &nbsp; </p>',
        unsafe_allow_html=True)
        
        
        
    
