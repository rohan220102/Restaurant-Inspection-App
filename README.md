# 🍽️ Restaurant Inspection Management App

A full-stack, interactive web application designed to streamline the management, exploration, and analysis of restaurant health inspection data.

## 🚀 Live App

Access the deployed application here:  
👉 [https://restaurantinspectionsapp-plkfmq6tbmg8scpyyodcmy.streamlit.app/](https://restaurantinspectionsapp-plkfmq6tbmg8scpyyodcmy.streamlit.app/)
Username - Neilb;
Password - qwerty123

---

## 📌 Project Overview

The goal of this project is to create a comprehensive restaurant inspection management system that allows public health departments, analysts, and restaurant owners to interact with structured inspection data. The app provides full CRUD capabilities, visual analytics, and a user-friendly interface for managing records of establishments, inspectors, and violations.

---

## 🧱 Features

- **User Authentication** – Sign up and login system with SHA256 password hashing.
- **CRUD Operations** – Create, Read, Update, and Delete entries across five key tables:
  - `establishment`
  - `employee`
  - `inspection`
  - `violation`
  
- **Interactive Visualizations**
  - Monthly inspection trends
  - Top 10 violation types
  - Most active inspectors
  - Top fined establishments
  - Risk level distribution
- **Streamlit UI** – Lightweight, browser-based interface with dynamic form handling.
- **SQLite Integration** – Local relational database support with robust schema and constraints.

---

## 📊 Tech Stack

- **Frontend/UI**: Streamlit
- **Backend/Logic**: Python
- **Database**: SQLite
- **Data Handling**: pandas
- **Visualization**: Streamlit charts, matplotlib

---

## 🏗️ Database Schema

The application uses a normalized relational schema consisting of the following entities:
- **establishment**: Restaurant metadata and location
- **employee**: Inspector details
- **inspection**: Inspection events and results
- **violation**: Violations linked to inspections

Each table is created with primary/foreign key constraints to maintain referential integrity.
![Database Schema](https://raw.githubusercontent.com/rohan220102/Restaurant-Inspection-App/main/ADT_proj_schema.png)



---

