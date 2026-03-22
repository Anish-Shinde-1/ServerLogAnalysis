import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

def visualize(report):
    st.set_page_config(page_title="Log Analysis Dashboard", layout="wide")
    
    st.title("Web Server Log Analytics")
    st.markdown(f"**Report Generated at:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.divider()

    # --- TOP LEVEL METRICS ---
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Requests", f"{report.total_requests:,}")
    with col2:
        # Format error rate as percentage
        st.metric("Avg Error Rate", f"{report.error_rate:.2%}", delta_color="inverse")
    with col3:
        peak_val = report.peak_hour[1] if report.peak_hour else 0
        peak_time = report.peak_hour[0] if report.peak_hour else "N/A"
        st.metric("Peak Traffic Hour", f"{peak_time}:00", f"{peak_val} reqs")
    with col4:
        st.metric("Suspicious IPs", len(report.suspicious_ips))

    st.divider()

    # --- TRAFFIC ANALYSIS (TIME SERIES) ---
    st.subheader("Traffic Trends")
    # Convert requests_per_hour to DataFrame
    if report.requests_per_hour:
        df_hour = pd.DataFrame(report.requests_per_hour, columns=['Hour', 'Requests']).sort_values('Hour')
        fig_time = px.line(df_hour, x='Hour', y='Requests', title="Requests per Hour", markers=True)
        st.plotly_chart(fig_time, use_container_width=True)

    # --- CATEGORICAL BREAKDOWNS ---
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Top Endpoints")
        df_end = pd.DataFrame(report.top_endpoints, columns=['Endpoint', 'Hits'])
        fig_end = px.bar(df_end, x='Hits', y='Endpoint', orientation='h', color='Hits')
        st.plotly_chart(fig_end, use_container_width=True)

        st.subheader("Status Distribution")
        df_status = pd.DataFrame(list(report.status_distribution.items()), columns=['Status', 'Count'])
        df_status['Status'] = df_status['Status'].astype(str)
        fig_status = px.pie(df_status, names='Status', values='Count', hole=0.4, 
                            color_discrete_sequence=px.colors.qualitative.Safe)
        st.plotly_chart(fig_status, use_container_width=True)

    with col_right:
        st.subheader("Top User Agents")
        df_ua = pd.DataFrame(report.top_user_agents, columns=['User Agent', 'Hits'])
        # Shorten UA for display
        df_ua['User Agent'] = df_ua['User Agent'].str[:50] + "..."
        st.plotly_chart(px.bar(df_ua, x='Hits', y='User Agent', orientation='h'), use_container_width=True)

        st.subheader("HTTP Methods")
        df_method = pd.DataFrame(list(report.method_distribution.items()), columns=['Method', 'Count'])
        st.plotly_chart(px.bar(df_method, x='Method', y='Count', color='Method'), use_container_width=True)

    st.divider()

    # --- SECURITY SECTION ---
    st.subheader("Security & Anomalies")
    sec_col1, sec_col2 = st.columns(2)

    with sec_col1:
        st.error("Failed Requests by IP (4xx/5xx)")
        df_fail = pd.DataFrame(report.failed_requests_by_ip, columns=['IP Address', 'Failures'])
        st.table(df_fail)

    with sec_col2:
        st.warning("Potential Attack Bursts")
        if report.attack_minutes:
            df_attack = pd.DataFrame(report.attack_minutes, columns=['IP', 'Endpoint', 'Time', 'Burst Count'])
            st.dataframe(df_attack, use_container_width=True)
        else:
            st.write("No major spikes detected.")

    if report.suspicious_ips:
        st.info(f"**Action Required:** High-frequency failed requests detected from: {', '.join(report.suspicious_ips)}")

    # --- RAW DATA EXPANDER ---
    with st.expander("View Full Endpoint Success Rates"):
        df_success = pd.DataFrame(list(report.endpoint_success_rates.items()), columns=['Endpoint', 'Success Rate'])
        df_success['Success Rate'] = df_success['Success Rate'].map('{:.2%}'.format)
        st.dataframe(df_success, use_container_width=True)
        
    with open("report.txt", "w") as f:
        f.write(str(report))
    st.sidebar.success("Report saved to local directory!")