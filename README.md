# Manufacturing Operations Data Platform

A production-style Data Engineering project that simulates a manufacturing company data platform. This system ingests raw operational CSV files, loads them into PostgreSQL, transforms them into warehouse and reporting marts, runs data quality checks, orchestrates the pipeline with Prefect, and exposes dashboard-ready analytics through Streamlit.

---

## Project Overview

Manufacturing companies generate data from many departments such as:

- production
- machines
- quality inspection
- inventory
- suppliers
- shipments
- sales

In many organizations, this data is messy, separated across files or systems, and difficult to trust.

This project solves that problem by building an internal data platform that:

- collects raw CSV files
- loads them into PostgreSQL staging tables
- transforms them into warehouse tables
- validates data quality
- creates reporting marts
- orchestrates the full pipeline
- displays business metrics in a Streamlit dashboard

This is an internal analytics platform, not a customer-facing website.

---

## Business Problem

Manufacturing teams often face these problems:

- reports are slow to create
- data is spread across departments
- metrics are inconsistent
- teams do not trust the numbers
- there is no single source of truth

This project addresses those problems by building a clean end-to-end data pipeline for operational reporting.

---

## Project Goals

The main goals of this project are:

- build a realistic ETL/ELT pipeline
- model manufacturing operations data in PostgreSQL
- separate staging, warehouse, and marts layers
- add data quality checks for reliability
- automate the pipeline with orchestration
- provide dashboard-ready business metrics

---

## Architecture / Pipeline Flow

```text
Raw CSV Files
→ Staging Tables
→ Warehouse Tables
→ Data Quality Checks
→ Reporting Marts
→ Prefect Orchestration
→ Streamlit Dashboard