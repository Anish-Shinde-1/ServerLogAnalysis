from models import AnalysedReport, AggregateData
from collections import Counter


def analyse(stats) -> AnalysedReport:

    report = AnalysedReport()

    report.total_requests = stats.total_requests

    report.top_ips = stats.metrics["ip"].most_common(10)
    report.top_endpoints = stats.metrics["endpoint"].most_common(10)
    report.top_user_agents = stats.metrics["user_agent"].most_common(10)

    report.method_distribution = dict(stats.metrics["method"])
    report.status_distribution = dict(stats.metrics["status"])


    total_errors = 0

    for status, count in stats.metrics["status"].items():
        if status >= 400:
            total_errors += count

    if report.total_requests > 0:
        report.error_rate = total_errors / report.total_requests

    endpoint_errors = Counter()

    for (endpoint, status), count in stats.metrics["endpoint_status"].items():
        if status >= 400:
            endpoint_errors[endpoint] += count

    report.top_error_endpoints = endpoint_errors.most_common(10)

    endpoint_success = Counter()
    endpoint_total = Counter()

    for (endpoint, status), count in stats.metrics["endpoint_status"].items():

        endpoint_total[endpoint] += count

        if status < 400:
            endpoint_success[endpoint] += count

    for endpoint in endpoint_total:

        success = endpoint_success[endpoint]
        total = endpoint_total[endpoint]

        report.endpoint_success_rates[endpoint] = success / total

    failed_by_ip = Counter()

    for (ip, status), count in stats.metrics["ip_status"].items():
        if status >= 400:
            failed_by_ip[ip] += count

    report.failed_requests_by_ip = failed_by_ip.most_common(10)
    
    for ip, failures in report.failed_requests_by_ip:
        if failures > 100:
            report.suspicious_ips.append(ip)

    report.endpoint_usage = stats.metrics["endpoint"].most_common(10)

    report.endpoint_user_agent_usage = stats.metrics["endpoint_user_agent"].most_common(10)

    report.endpoint_referrer_sources = stats.metrics["endpoint_referrer"].most_common(10)
    
    
    report.requests_per_hour = stats.metrics["requests_per_hour"].most_common()

    peak_hour = stats.metrics["requests_per_hour"].most_common(1)
    if peak_hour:
        report.peak_hour = peak_hour[0]
    
    report.requests_per_minute = stats.metrics["requests_per_minute"].most_common(10)
    peak_minute = stats.metrics["requests_per_minute"].most_common(1)
    if peak_minute:
        report.peak_minute = peak_minute[0]
    
    errors_by_hour = Counter()

    for (status, hour), count in stats.metrics["status_hour"].items():
        if status >= 400:
            errors_by_hour[hour] += count
            
    report.error_spikes = errors_by_hour.most_common(10)
    
    attacks = []

    for (ip, endpoint, minute), count in stats.metrics["ip_endpoint_minute"].items():
        if count > 20:
            attacks.append((ip, endpoint, minute, count))

    report.attack_minutes = sorted(attacks, key=lambda x: x[3], reverse=True)[:10]

    return report