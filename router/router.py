import threading
import socket
import time
import os

from link_state_packet import LinkStatePacket
from dijkstra import Dijkstra

class Router:
    def __init__(self, router_id, port, neighbors):
        self.router_id = router_id
        self.port = port
        self.neighbors = neighbors  # {vizinho: (ip, porta, custo)}
        self.lsdb = {self.router_id: {n: {"ip": ip,"custo":custo} for n, (ip, _, custo) in neighbors.items()}}
        self.routing_table = {}

    def send_link_state_packet(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while True:
            packet = LinkStatePacket(self.router_id, {n: {"ip": ip, "custo": custo} for n, (ip, _, custo) in self.neighbors.items()}, sequence_number=int(time.time()))
            data = packet.serialize()
            for neighbor, (ip, port, _) in self.neighbors.items():
                sock.sendto(data, (ip, port))
                print(f"[{self.router_id}] Enviado estado de enlace para {neighbor} ({ip}:{port})")
            # time.sleep(1)

    def receive_link_state_packet(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(("0.0.0.0", self.port))
        print(f"[{self.router_id}] Aguardando pacotes na porta {self.port}...")
        while True:
            data, _ = sock.recvfrom(4096)
            packet = LinkStatePacket.deserialize(data)
            print(f"[{self.router_id}] Recebido pacote de {packet.router_id}: {packet.neighbors}")
            
            # Atualiza a LSDB com o pacote recebido
            if packet.router_id not in self.lsdb or packet.sequence_number > self.lsdb[packet.router_id].get("sequence_number", 0):
                self.lsdb[packet.router_id] = packet.neighbors
                self.lsdb[packet.router_id]["sequence_number"] = packet.sequence_number
                self.update_routing_table()
                
                # Reencaminha o pacote para os vizinhos
                for neighbor, (ip, port, _) in self.neighbors.items():
                    if neighbor != packet.router_id:  # Evita enviar de volta para o remetente
                        sock.sendto(data, (ip, port))
                        print(f"[{self.router_id}] Reencaminhado pacote para {neighbor} ({ip}:{port})")

    def update_routing_table(self):
        graph = self.build_graph()
        
        print(f"[{self.router_id}] Grafo atualizado: {graph}")
        
        self.routing_table = Dijkstra(graph, self.router_id)

        # Extrai o mapeamento host->IP a partir da lsdb
        # Atualiza os nomes dos nós e vizinhos na lsdb e no grafo para usar IPs quando disponíveis
        host_to_ip = {}
        # Itera sobre todos os nós e seus vizinhos na LSDB para coletar os IPs
        for _, neighbors in self.lsdb.items():
            for neighbor, info in neighbors.items():
                if isinstance(info, dict) and "ip" in info:
                    host_to_ip[neighbor] = info["ip"]

        print(f"[{self.router_id}] Tabela de IPs:{host_to_ip}")

        # Tabela de Roteamento:{'router2': ['router2'], 'router3': ['router2', 'router3'], 'router4': ['router2', 'router3', 'router4']}
        print(f"[{self.router_id}] Tabela de Roteamento:{self.routing_table}")
        
        print(f"[{self.router_id}] LSDB:{self.lsdb}")
        
        # Atualiza as rotas do sistema usando 'ip route replace <destino>/<prefixo> via <ip_next_hop>'
        for destination, path in self.routing_table.items():
            if not path:
                continue

            # Não adiciona rota para si mesmo ou para vizinhos diretos
            if destination == self.router_id or destination in self.neighbors:
                continue

            next_hop = path[0]
            dest_ip = host_to_ip.get(destination, destination)

            # Formata o gateway como uma rede /24  172.21.2.0/24 somente se dest_ip for um IP válido
            dest_ip_str = str(dest_ip)
            if '.' in dest_ip_str and all(part.isdigit() and 0 <= int(part) <= 255 for part in dest_ip_str.split('.')):
                ip_parts = dest_ip_str.split('.')
                gateway = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.0/24"
            else:
                # Pula se não for um IP válido
                print(f"[{self.router_id}] Ignorando destino não-IP: {dest_ip}")
                continue

            ip_next_hop = host_to_ip.get(next_hop, next_hop)
            if not ('.' in ip_next_hop and all(part.isdigit() and 0 <= int(part) <= 255 for part in ip_next_hop.split('.'))):
                print(f"[{self.router_id}] Ignorando next_hop não-IP: {ip_next_hop}")
                continue

            cmd = f"ip route replace {gateway} via {ip_next_hop}"
            print(f"[{self.router_id}] Executando: {cmd}")
            os.system(cmd)
        
        # Agora graph_ip pode ser usado para algoritmos baseados em IPs
        output = []
        output.append(f"\n[{self.router_id}] Tabela de Roteamento Atualizada:")
        output.append(f"{'Destino':<10} | {'Caminho'}")
        output.append(f"{'-'*10}-+-{'-'*30}")

        for destination, path in self.routing_table.items():
            full_path = ' -> '.join([str(self.router_id)] + [str(node) for node in path]) if path else str(self.router_id)
            output.append(f"{destination:<10} | {full_path}")

        print("\n".join(output))
        with open(f"routing_table_{self.router_id}.txt", "w") as f:
            f.write("\n".join(output))

    def build_graph(self):
        # Constrói o grafo a partir da LSDB no formato {nó: {vizinho: custo}}
        graph = {}
        
        for node, neighbors in self.lsdb.items():
            graph[node] = {}
            for neighbor, info in neighbors.items():
                cost = info["custo"] if isinstance(info, dict) and "custo" in info else info
                graph[node][neighbor] = cost
        
        # Garante que todos os nós conhecidos estejam no grafo
        all_nodes = set(graph.keys())
        for neighbors in graph.values():
            all_nodes.update(neighbors.keys())
        for node in all_nodes:
            if node not in graph:
                graph[node] = {}
            else:
                # Remove nós que não têm vizinhos conhecidos
                graph[node] = {k: v for k, v in graph[node].items() if v is not None}
        return graph

def parse_neighbors(neighbor_string):
    neighbors = {}
    if neighbor_string:
        for entry in neighbor_string.split(','):
            parts = entry.strip().split(':')
            if len(parts) == 4:
                name, ip, port, cost = parts
                neighbors[name] = (ip, int(port), int(cost))
    return neighbors

if __name__ == "__main__":
    router_id = os.getenv("ROUTER_ID")
    port = int(os.getenv("ROUTER_PORT", 5000))
    neighbors = parse_neighbors(os.getenv("NEIGHBORS", ""))

    print(f"[{router_id}] Inicializando o roteador na porta {port} com vizinhos: {neighbors}")
    
    router = Router(router_id, port, neighbors)

    threading.Thread(target=router.send_link_state_packet, daemon=True).start()
    threading.Thread(target=router.receive_link_state_packet, daemon=True).start()
    threading.Thread(target=router.update_routing_table, daemon=True).start()
    
    while True:
        time.sleep(1)