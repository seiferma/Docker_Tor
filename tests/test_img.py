from testcontainers.core.container import DockerContainer
from testcontainers.core.wait_strategies import LogMessageWaitStrategy, HealthcheckWaitStrategy
import requests
import socket
from dns.resolver import Resolver

checkip_url = 'http://checkip.amazonaws.com'

def test_anonymization(img_name):
    regular_ip = requests.get(checkip_url).text.strip()
    with DockerContainer(img_name).with_kwargs(privileged=True).waiting_for(LogMessageWaitStrategy(".*100%*")) as subject:
        result = subject.exec(f"curl --socks5-hostname 127.0.0.1:9050 {checkip_url}")
        assert result.exit_code == 0
        actual_ip = result.output.decode('utf-8').strip()
        assert regular_ip != actual_ip

def test_healthcheck(img_name):
    with DockerContainer(img_name).with_kwargs(privileged=True).waiting_for(HealthcheckWaitStrategy()) as subject:
        result = subject.exec(f"curl --socks5-hostname 127.0.0.1:9050 {checkip_url}")
        assert result.exit_code == 0

def test_exposed_dns(img_name):
    with DockerContainer(img_name).with_kwargs(privileged=True).with_exposed_ports("53/udp", "9053/udp").waiting_for(HealthcheckWaitStrategy()) as subject:
        ip = to_ip(subject.get_container_host_ip())
        for port in [53, 9053]:
            mapped_port = subject.get_exposed_port(port)
            resolver = Resolver()
            resolver.nameservers = [ip]
            resolver.nameserver_ports = {ip: mapped_port}
            answer = resolver.resolve("google.com")
            assert len(answer.response.errors) == 0

def test_exposed_socks(img_name):
    with DockerContainer(img_name).with_kwargs(privileged=True).with_exposed_ports("9050/tcp").waiting_for(HealthcheckWaitStrategy()) as subject:
        ip = to_ip(subject.get_container_host_ip())
        mapped_port = subject.get_exposed_port(9050)
        session = requests.session()
        session.proxies = {"http": f"socks5h://{ip}:{mapped_port}"}
        result = session.get(checkip_url)
        assert result.ok

def to_ip(hostname):
    return socket.gethostbyname(hostname)