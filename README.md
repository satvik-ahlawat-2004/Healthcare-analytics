# Healthcare Analytics Dashboard 🏥

A comprehensive healthcare analytics dashboard built with Streamlit and Plotly that provides insights into patient data, billing patterns, and hospital performance metrics.

## Features

### 📊 Key Performance Indicators (KPIs)
- **Total Patients**: Overall patient count
- **Total Billing Amount**: Sum of all billing amounts
- **Average Length of Stay**: Mean hospital stay duration in days

### 📈 Interactive Charts
1. **Average Billing Amount by Medical Condition** - Horizontal bar chart showing billing patterns across different medical conditions
2. **Average Length of Stay by Condition** - Bar chart displaying hospital stay duration by medical condition
3. **Top 10 Hospitals by Average Billing Amount** - Horizontal bar chart of highest billing hospitals
4. **Total Billing by Insurance Provider** - Donut chart showing billing distribution across insurance providers
5. **Average Billing by Admission Type** - Bar chart comparing billing amounts by admission type (Emergency, Urgent, Elective)

### 🔍 Interactive Filters
- **Gender Filter**: Filter data by Male/Female
- **Age Range Filter**: Filter by age groups (0-18, 19-30, 31-45, 46-60, 61-75, 75+)
- **Insurance Provider Filter**: Filter by specific insurance companies

### 🎨 Professional Design
- Modern, clean interface with professional color schemes
- Responsive layout that works on different screen sizes
- Custom CSS styling for enhanced visual appeal
- Interactive tooltips and hover effects

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Verify Dataset
Ensure your `healthcare_dataset.csv` file is in the same directory as the dashboard script. The dataset should contain the following columns:
- Name, Age, Gender, Blood Type, Medical Condition
- Date of Admission, Doctor, Hospital, Insurance Provider
- Billing Amount, Room Number, Admission Type, Discharge Date
- Medication, Test Results

### Step 3: Run the Dashboard
```bash
streamlit run healthcare_dashboard.py
```

The dashboard will open in your default web browser at `http://localhost:8501`

## Usage Guide

### Navigation
1. **Sidebar Filters**: Use the left sidebar to filter data by Gender, Age Range, and Insurance Provider
2. **KPI Cards**: View key metrics at the top of the dashboard
3. **Charts**: Scroll down to explore various analytical charts
4. **Data Summary**: Expand the "Data Summary" section to view dataset overview and sample data

### Interacting with Charts
- **Hover**: Hover over chart elements to see detailed tooltips
- **Zoom**: Use mouse wheel or zoom controls to zoom into specific areas
- **Pan**: Click and drag to pan around zoomed charts
- **Legend**: Click on legend items to show/hide data series

### Filter Summary
The sidebar displays a real-time summary of applied filters and the number of records being displayed.

## Technical Details

### Data Processing
- **Date Parsing**: Automatically converts admission and discharge dates
- **Length of Stay Calculation**: Computes hospital stay duration in days
- **Age Grouping**: Creates age ranges for better analysis
- **Data Cleaning**: Handles missing values and standardizes text formatting

### Performance Optimization
- **Caching**: Uses Streamlit's `@st.cache_data` decorator for efficient data loading
- **Responsive Design**: Optimized for various screen sizes
- **Error Handling**: Graceful error handling for data loading issues

### Chart Specifications
- **Color Schemes**: Professional color palettes for each chart type
- **Formatting**: Currency formatting for billing amounts, proper date formatting
- **Responsiveness**: Charts automatically adjust to container width

## Customization

### Adding New Charts
To add new visualizations, create a new function following this pattern:
```python
def create_new_chart(df):
    # Your chart logic here
    fig = px.chart_type(...)
    return fig
```

### Modifying Filters
Add new filters by extending the `create_filters()` function:
```python
# Add new filter
new_filter = st.sidebar.selectbox("New Filter", options)
# Apply filter logic
if new_filter != 'All':
    filtered_df = filtered_df[filtered_df['Column'] == new_filter]
```

### Styling Changes
Modify the CSS in the `st.markdown()` section at the top of the file to change colors, fonts, or layout.

## Troubleshooting

### Common Issues
1. **File Not Found**: Ensure `healthcare_dataset.csv` is in the correct directory
2. **Import Errors**: Verify all required packages are installed using `pip install -r requirements.txt`
3. **Memory Issues**: For very large datasets, consider implementing data sampling or pagination

### Data Requirements
- CSV file with proper column headers
- Date columns in recognizable format (YYYY-MM-DD preferred)
- Numeric columns for Age and Billing Amount
- No completely empty rows

## Dependencies
- **streamlit**: Web app framework
- **pandas**: Data manipulation and analysis
- **plotly**: Interactive charting library
- **numpy**: Numerical computing support

## License
This project is open source and available under the MIT License.

## Support
For issues or questions, please check the troubleshooting section or create an issue in the project repository.
