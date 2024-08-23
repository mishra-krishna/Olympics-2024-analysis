
# Paris Olympics Analysis Dashboard

## Overview

The **Paris Olympics Analysis Dashboard** is an interactive web application that offers comprehensive insights into the Paris 2024 Olympic Games. Leveraging Streamlit for the user interface and Plotly for advanced visualizations, this dashboard enables users to explore detailed data on athletes, medals, and events dynamically. The application is containerized using Docker and deployed on Azure App Services, ensuring seamless scalability and accessibility.

## Features

- **Interactive Visualizations**: Visualize medal counts, athlete performance, and event statistics through dynamic charts and graphs.
- **User-Friendly Interface**: Intuitive navigation with filters and tabs for customized data exploration.
- **Real-Time Data Handling**: Updated to reflect real-time results and statistics during the Olympics.

## Technologies Used

- **Frontend**: Streamlit for building the user interface.
- **Data Visualization**: Plotly for interactive and visually appealing plots.
- **Backend**: Python for data processing and application logic.
- **Containerization**: Docker for creating consistent deployment environments.
- **Cloud Deployment**: Azure App Services for hosting the application, with Azure Container Registry for managing Docker containers.

## Getting Started

### Prerequisites

- Docker installed on your machine.
- An Azure account for deployment (if deploying to Azure).

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/mishra-krishna/Olympics-2024-analysis.git
   cd Olympics-2024-analysis
   ```

2. **Build the Docker image:**

   ```bash
   docker build -t olympics-dashboard .
   ```

3. **Run the Docker container:**

   ```bash
   docker run -p 8501:8501 olympics-dashboard
   ```

4. **Access the dashboard:**

   Open your browser and go to `http://localhost:8501` to view the dashboard.

### Deployment on Azure

1. **Push Docker Image to Azure Container Registry:**

   ```bash
   docker tag olympics-dashboard:latest <your-registry-name>.azurecr.io/olympics-dashboard:latest
   docker push <your-registry-name>.azurecr.io/olympics-dashboard:latest
   ```

2. **Deploy to Azure App Services:**

   - Create an Azure App Service via the Azure Portal or Azure CLI.
   - Configure the App Service to pull the Docker image from Azure Container Registry and start the application.

## Usage

- **Medal Analysis**: Explore and visualize the medal distribution by country and event.
- **Athlete Insights**: Analyze athlete data, including performance metrics and demographic information.
- **Overall Analysis**: Review and track the number of events and sports with interactive charts.

## Contributing

Contributions to enhance the dashboard are welcome! Feel free to submit pull requests or open issues if you have suggestions or find any bugs.

## Contact

For any inquiries or feedback, please contact [Krishna Misra](mailto:mishhra.krishhna@gmail.com).

## Repository

Visit the repository on GitHub: [Paris Olympics Analysis Dashboard](https://github.com/mishra-krishna/Olympics-2024-analysis)
