# Core

Core is a FastAPI-based project that provides a simple RESTful API for managing products. It demonstrates basic CRUD (Create, Read, Update, Delete) operations using FastAPI and Beanie ODM with MongoDB.

## Table of Contents

- [Project Description](#project-description)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
  - [Installation](#installation)

## Project Description

Core is a simple FastAPI project for managing product data. It provides endpoints to perform CRUD operations on product entities, including creating, reading, updating, and deleting products. The project is built using FastAPI for API development, Beanie as the ODM for MongoDB interaction, and Motor as the MongoDB driver.

## Features

- Create new products with a name, price, and description.
- Retrieve a list of all products.
- Retrieve a specific product by its ID.
- Update an existing product by its ID.
- Delete a product by its ID.

## Prerequisites

Before running the Core project, ensure you have the following prerequisites:

- Python 3.7 or higher installed.
- MongoDB installed and running (adjust database connection settings in `app/db/database.py` if needed).

### Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/itsgemmara/SimpleFastAPIChallenge
   cd core

2. Install Dependencies:

  ```bash
   pip install -r requirements.txt

3. Running the Application

  ```bash 
   uvicorn main:app --reload


