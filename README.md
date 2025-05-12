# A Better Bird of the Day

This project provides a dynamic dashboard for birdwatching enthusiasts, giving birdwatchers a recommended "bird of the day" to find during their next birdwatching trip. The bird of the day is recommended based on the most common birds in your area that you have not observed. For the given bird, the dashboard displays a snippet of information about the bird (sourced from Wikipedia), a list of at most 3 public hotspots where that bird has been observed, and a bar graph showing the trend of sightings for that species in the past 4 weeks.While the bird of the day autopopulates the bird dropdown bar, this information will be displayed for any bird inputted. The dashboard also provides some information about birds in the specified county, including the most common birds sighted and rare sightings. Lastly, the bottom plays a slideshow of images of the selected bird, also from Wikipedia.

This data is sourced using eBird's API, and for up to date information requires an API key, which can be obtained from their [website](https://ebird.org/data/download?_gl=1*7mjacs*_gcl_au*OTUxMTA4MzcxLjE3NDA0MjI3NTc.*_ga*NTQxNjQwMzEyLjE3NDA0MjI3NTc.*_ga_QR4NVXZ8BM*czE3NDcwNzE4NTgkbzc0JGcwJHQxNzQ3MDcxODYzJGo1NSRsMCRoMA..&_ga=2.89112600.280494711.1746969736-541640312.1740422757). Information on how to input your API key is included below. For test cases, some sample data has been uploaded for Williamsburg, Virginia, and can be accessed without an API key.

## Dashboard Features

- **State and County Dropdowns**: Filters sightings by county.
- **Bird Dropdown**: Select a bird. This will be autopopulated by the button below.
- **Generate Bird of the Day Button**: This will generate your bird of the day.
- **Bird Information**: Below the button, a section will display information about the bird, some local hotspots, as well as a bar chart showing how many of that species have been spotted in the past 4 weeks. Additionally, a link to that bird's eBird page is provided to find more information.
- **County Information**: The next section displays two tables. The first is the most commonly sighted birds in the past 14 days. The next is a list of rare sightings in the past 14 days.
- **Image Slideshow**: At the bottom, a slideshow of images of the selected bird plays. Images can include the bird itself, drawings, eggs, color variations, etc.
  
## Installation

To run this project locally, follow these steps:

### Steps

1. Download the repository from GitHub

2. Create a virtual environment:

    ```bash
    venv init

3. Initialize your API key (optional):

    ```bash
    uv run api_config.py
    Enter your API key: ##########

4. Run the dashboard:

    ```bash
    uv run main.py

Happy birdwatching!