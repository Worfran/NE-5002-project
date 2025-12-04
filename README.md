# NE_5002 Project

## Overview
This application is designed to solve the 2D diffusion equation for a neutron transport problem. It is the final project for the NE_5002 course. It uses a modular architecture based on the Model-View-Controller (MVC) design pattern to ensure separation of concerns and maintainability. The recommended python version is 3.10.

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/Worfran/NE-5002-project.git
    ```
2. Navigate to the project directory:
    ```bash
    cd NE_5002_project
    ```
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
1. Run the application:
    ```bash
    python -m src.controller
    ```
2. Follow the on-screen instructions to introduce the necessary parameters. It will prompt you to enter the path to the input file containing the problem specifications. 

## Output
The output of the application can be found in the following location:
- **Directory**: `/path/to/repository/NE_5002_project/Output/`
- **File Format**: SVG for images and TXT for data files.

Ensure to check this directory after running the application for the results.
