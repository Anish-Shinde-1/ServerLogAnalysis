from collections import Counter

class Event:
    def __init__(self, source_ip, date_time_zone, http_method, endpoint, version, status_code, result_size, source_domain, user_agent):
        self.source_ip = source_ip
        self.date_time_zone = date_time_zone
        self.http_method = http_method
        self.endpoint = endpoint
        self.version = version
        self.status_code = status_code
        self.result_size = result_size
        self.source_domain = source_domain
        self.user_agent = user_agent
        
from collections import Counter


class AggregateData:

    def __init__(self):


        self.metrics = {
            "ip": Counter(),
            "endpoint": Counter(),
            "method": Counter(),
            "status": Counter(),
            "user_agent": Counter(),
            "referrer": Counter(),
            
            "endpoint_status": Counter(),
            "endpoint_method": Counter(),
            "method_status": Counter(),
            "endpoint_method_status": Counter(),

            "ip_endpoint": Counter(),
            "ip_status": Counter(),
            "ip_method": Counter(),
            "ip_endpoint_status": Counter(),

            "endpoint_user_agent": Counter(),
            "endpoint_referrer": Counter(),
            "method_endpoint": Counter(),
            
            "requests_per_hour": Counter(),
            "requests_per_minute": Counter(),

            "endpoint_hour": Counter(),
            "status_hour": Counter(),
            "ip_hour": Counter(),

            "endpoint_status_hour": Counter(),
            "ip_endpoint_minute": Counter(),
        }
        
    def updateData(self, event):

        self.metrics["ip"][event.source_ip] += 1
        self.metrics["endpoint"][event.endpoint] += 1
        self.metrics["method"][event.http_method] += 1
        self.metrics["status"][event.status_code] += 1
        self.metrics["user_agent"][event.user_agent] += 1
        self.metrics["referrer"][event.source_domain] += 1

        self.metrics["endpoint_status"][
            (event.endpoint, event.status_code)
        ] += 1

        self.metrics["endpoint_method"][
            (event.endpoint, event.http_method)
        ] += 1

        self.metrics["method_status"][
            (event.http_method, event.status_code)
        ] += 1

        self.metrics["endpoint_method_status"][
            (event.endpoint, event.http_method, event.status_code)
        ] += 1

        self.metrics["ip_endpoint"][
            (event.source_ip, event.endpoint)
        ] += 1

        self.metrics["ip_status"][
            (event.source_ip, event.status_code)
        ] += 1

        self.metrics["ip_method"][
            (event.source_ip, event.http_method)
        ] += 1

        self.metrics["ip_endpoint_status"][
            (event.source_ip, event.endpoint, event.status_code)
        ] += 1

        self.metrics["endpoint_user_agent"][
            (event.endpoint, event.user_agent)
        ] += 1

        self.metrics["endpoint_referrer"][
            (event.endpoint, event.source_domain)
        ] += 1

        self.metrics["method_endpoint"][
            (event.http_method, event.endpoint)
        ] += 1

        hour = event.date_time_zone.hour
        minute = event.date_time_zone.replace(second=0)

        self.metrics["requests_per_hour"][hour] += 1
        self.metrics["requests_per_minute"][minute] += 1


        self.metrics["endpoint_hour"][
            (event.endpoint, hour)
        ] += 1

        self.metrics["status_hour"][
            (event.status_code, hour)
        ] += 1


        self.metrics["ip_hour"][
            (event.source_ip, hour)
        ] += 1


        self.metrics["endpoint_status_hour"][
            (event.endpoint, event.status_code, hour)
        ] += 1

        self.metrics["ip_endpoint_minute"][
            (event.source_ip, event.endpoint, minute)
        ] += 1

    @property
    def total_requests(self):
        return self.metrics["status"].total()

class AnalysedReport:

    def __init__(self):

        self.total_requests = 0
        self.top_ips = []
        self.top_endpoints = []
        self.top_user_agents = []

        self.method_distribution = {}
        self.status_distribution = {}

        self.error_rate = 0.0
        self.top_error_endpoints = []
        self.endpoint_success_rates = {}

        self.suspicious_ips = []
        self.failed_requests_by_ip = []

        self.endpoint_usage = []
        self.endpoint_user_agent_usage = []
        self.endpoint_referrer_sources = []
        
        self.requests_per_hour = []
        self.requests_per_minute = []

        self.peak_hour = None
        self.peak_minute = None

        self.error_spikes = []

        self.attack_minutes = []
                
    def __str__(self):

        lines = []

        lines.append("========== LOG ANALYSIS REPORT ==========\n")

        lines.append("---- Traffic Overview ----")
        lines.append(f"Total Requests: {self.total_requests}")
        lines.append(f"Top IPs: {self.top_ips}")
        lines.append(f"Top Endpoints: {self.top_endpoints}")
        lines.append(f"Top User Agents: {self.top_user_agents}")
        lines.append(f"HTTP Methods: {self.method_distribution}")
        lines.append(f"Status Distribution: {self.status_distribution}\n")

        lines.append("---- Performance ----")
        lines.append(f"Error Rate: {self.error_rate:.4f}")
        lines.append(f"Top Error Endpoints: {self.top_error_endpoints}")
        lines.append(f"Endpoint Success Rates: {self.endpoint_success_rates}\n")

        lines.append("---- Security ----")
        lines.append(f"Failed Requests by IP: {self.failed_requests_by_ip}")
        lines.append(f"Suspicious IPs: {self.suspicious_ips}\n")

        lines.append("---- Usage ----")
        lines.append(f"Top Endpoint Usage: {self.endpoint_usage}")
        lines.append(f"Endpoint × User Agent: {self.endpoint_user_agent_usage}")
        lines.append(f"Endpoint × Referrer: {self.endpoint_referrer_sources}")
        
        lines.append("\n---- Time Analysis ----")
        lines.append(f"Requests Per Hour: {self.requests_per_hour[:10]}")
        lines.append(f"Requests Per Minute: {self.requests_per_minute}")
        lines.append(f"Peak Hour: {self.peak_hour}")
        lines.append(f"Peak Minute: {self.peak_minute}")
        lines.append(f"Error Spikes: {self.error_spikes}")
        lines.append(f"Attack Minutes: {self.attack_minutes}")

        return "\n".join(lines)