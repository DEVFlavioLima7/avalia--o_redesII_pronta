import json

class LinkStatePacket:
    def __init__(self, router_id, neighbors, sequence_number):
        self.router_id = router_id
        self.neighbors = neighbors  # {vizinho: custo}
        self.sequence_number = sequence_number

    def serialize(self):
        return json.dumps({
            "router_id": self.router_id,
            "neighbors": self.neighbors,
            "sequence_number": self.sequence_number
        }).encode()

    @staticmethod
    def deserialize(data):
        content = json.loads(data.decode())
        return LinkStatePacket(content["router_id"], content["neighbors"], content["sequence_number"])
