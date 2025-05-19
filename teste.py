class Teste:
    def __init__(self):
        # Exemplo de lsdb (base de dados de estado de enlace)
        self.lsdb = {
            'router3': {'172.21.2.2': 1, '172.21.4.2': 1},
            'router1': {'router2': 1},
            '172.21.4.2': {'router3': 1, 'router5': 1},
            '172.21.2.2': {'router1': 1, 'router3': 1},
            'router5': {'172.21.4.2': 1},
            'router2': {}
        }
        # Exemplo de vizinhos: {nome: (porta, ip, custo)}
        self.neighbors = {
            'router1': (1, '172.21.1.1', 1),
            'router2': (2, '172.21.2.2', 1),
            'router3': (3, '172.21.3.3', 1),
            'router5': (5, '172.21.5.5', 1),
            '172.21.4.2': (4, '172.21.4.2', 1),
            '172.21.2.2': (6, '172.21.2.2', 1)
        }

    def process(self):
        host_to_ip = {}
        # Mapeia todos os nós conhecidos para seus IPs, se possível
        for node in self.lsdb:
            if node in self.neighbors:
                host_to_ip[node] = self.neighbors[node][1]
            else:
                # Procura nos vizinhos dos outros nós
                for n, (_, ip, _) in self.neighbors.items():
                    if node == n:
                        host_to_ip[node] = ip

        # Atualiza as chaves e valores da lsdb para usar IPs quando possível
        new_lsdb = {}
        for node, neighbors in self.lsdb.items():
            node_ip = host_to_ip.get(node, node)
            new_neighbors = {}
            for neighbor, cost in neighbors.items():
                neighbor_ip = host_to_ip.get(neighbor, neighbor)
                new_neighbors[neighbor_ip] = cost
            new_lsdb[node_ip] = new_neighbors
        self.lsdb = new_lsdb

        # Atualiza o grafo para usar IPs
        graph = {
            'router3': {'172.21.2.2': 1, '172.21.4.2': 1},
            'router1': {'router2': 1},
            '172.21.4.2': {'router3': 1, 'router5': 1},
            '172.21.2.2': {'router1': 1, 'router3': 1},
            'router5': {'172.21.4.2': 1},
            'router2': {}
        }
        graph_ip = {}
        for node, neighbors in graph.items():
            node_ip = host_to_ip.get(node, node)
            graph_ip[node_ip] = {}
            for neighbor, cost in neighbors.items():
                neighbor_ip = host_to_ip.get(neighbor, neighbor)
                graph_ip[node_ip][neighbor_ip] = cost

        print(graph_ip)

if __name__ == "__main__":
    t = Teste()
    t.process()

    # Formata a LSDB para exibição no formato desejado
    lsdb = {'router2': {'router1': {'ip': '172.21.1.2', 'custo': 1}, 'router3': {'ip': '172.21.3.2', 'custo': 1}}, 'router1': {'router2': {'ip': '172.21.2.2', 'custo': 1}}, 'router3': {'router2': {'ip': '172.21.2.2', 'custo': 1}, 'router4': {'ip': '172.21.4.2', 'custo': 1}}, 'router4': {'router3': {'ip': '172.21.3.2', 'custo': 1}, 'router5': {'ip': '172.21.5.2', 'custo': 1}}}
    
    
    # Exibe o LSDB formatado
    for router, neighbors in lsdb.items():
        print(f"[{router}] LSDB:")
        for neighbor, details in neighbors.items():
            print(f"  {neighbor}: IP = {details['ip']}, Custo = {details['custo']}")
    
    # [router3] Recebido pacote de router4: {'router3': {'ip': '172.21.3.2', 'custo': 1}, 'router5': {'ip': '172.21.5.2', 'custo': 1}}

    # [router3] Grafo atualizado: {'router3': {}, 'router2': {}, 'router4': {}, 'router5': {}, 'router1': {'router2': 1}}

    # [router3] LSDB: {'router3': {'router2': {'ip': '172.21.2.2', 'custo': 1}, 'router4': {'ip': '172.21.4.2', 'custo': 1}}, 'router2': {'router1': {'ip': '172.21.1.2', 'custo': 1}, 'router3': {'ip': '172.21.3.2', 'custo': 1}}, 'router4': {'router3': {'ip': '172.21.3.2', 'custo': 1}, 'router5': {'ip': '172.21.5.2', 'custo': 1}}, 'router5': {'router4': {'ip': '172.21.4.2', 'custo': 1}}, 'router1': {'router2': {'ip': '172.21.2.2', 'custo': 1}}}