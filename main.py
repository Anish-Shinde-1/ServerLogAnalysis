# In your main script (e.g., app.py)
import streamlit as st
from models import AggregateData
from parser import parse
from analyser import analyse
from visualizer import visualize

def run_pipeline():
    stats = AggregateData()
    with open("server2.log", "r") as logs:
        for line in logs:
            event = parse(line.strip())
            if event:
                stats.updateData(event)
    
    return analyse(stats)

# Streamlit execution
if __name__ == "__main__":
    # This triggers the analysis
    report = run_pipeline()
    # This triggers the dashboard
    visualize(report)