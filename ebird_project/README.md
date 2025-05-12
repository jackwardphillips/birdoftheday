# A Better Bird of the Day

This project provides a dynamic dashboard for birdwatching enthusiasts, giving birdwatchers a recommended "bird of the day" to find during their next birdwatching trip. The bird of the day is recommended based on the most common birds in your area that you have not observed. For the given bird, the dashboard displays a snippet of information about the bird (sourced from Wikipedia), a list of at most 3 public hotspots where that bird has been observed, and a bar graph showing the trend of sightings for that species in the past 4 weeks.While the bird of the day autopopulates the bird dropdown bar, this information will be displayed for any bird inputted. The dashboard also provides some information about birds in the specified county, including the most common birds sighted and rare sightings. Lastly, the bottom plays a slideshow of images of the selected bird, also from Wikipedia.

This data is sourced using eBird's API, and for up to date information requires an API key, which can be obtained from their [website](https://ebird.org/data/download?_gl=1*7mjacs*_gcl_au*OTUxMTA4MzcxLjE3NDA0MjI3NTc.*_ga*NTQxNjQwMzEyLjE3NDA0MjI3NTc.*_ga_QR4NVXZ8BM*czE3NDcwNzE4NTgkbzc0JGcwJHQxNzQ3MDcxODYzJGo1NSRsMCRoMA..&_ga=2.89112600.280494711.1746969736-541640312.1740422757). To enter your API key, simply run
    ```bash
    uv run api_config.py

where you'll be asked to input your API key which will be saved to a .txt file.

For test cases, some sample data has been uploaded for Williamsburg, Virginia, and can be accessed without an API key.

## Features

- **State and County Dropdowns**: Filters sightings by county.
  
## Installation

To run this project locally, follow these steps:

### Prerequisites

- Python 3.x
- `pip` (Python package manager)

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/birdwatching-dashboard.git
   cd birdwatching-dashboard

2. Create a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate

3. Install the necessary dependencies:

    ```bash
    pip install -r requirements.txt
