import grpc
import db_pb2
import db_pb2_grpc
import time
from google.protobuf.json_format import MessageToDict
from google.protobuf.timestamp_pb2 import Timestamp


class DatabaseClient(object):
    """
    Client(stub) for database microservice
    """
    def __init__(self):
        self.host = "localhost"
        self.port = 50051
        self.channel = grpc.insecure_channel(f"{self.host}:{self.port}")
        self.client = db_pb2_grpc.DatabaseServiceStub(self.channel)

    def get_box(self, id):
        box_pb = db_pb2.GetBoxRequest(id=id)
        box_data = self.client.GetBox(box_pb)
        return MessageToDict(box_data)

    def get_boxes(self):
        box_list = self.client.GetBoxes(db_pb2.GetAllBoxesRequest())
        return MessageToDict(box_list)

    def create_box(self, data):
        now = time.time()
        seconds = int(now)
        nanos = int((now - seconds) * 10 ** 9)
        timestamp = Timestamp(seconds=seconds, nanos=nanos)
        box = db_pb2.Box(
            id=data["id"],
            name=data["name"],
            price=data["price"],
            description=data["description"],
            category=data["category"],
            quantity=data["quantity"],
            created_at=timestamp
        )
        box_pb = db_pb2.CreateBoxRequest(box=box)
        created_box = self.client.CreateBox(box_pb)
        return MessageToDict(created_box)

    def update_box(self, data):
        box_pb = db_pb2.UpdateBoxRequest(box=data)
        updated_box = self.client.UpdateBox(box_pb)
        return MessageToDict(updated_box)

    def delete_box(self, id):
        box_pb = db_pb2.DeleteBoxRequest(id=id)
        deleted_box = self.client.DeleteBox(box_pb)
        return MessageToDict(deleted_box)

    def getboxes_incategory(self, category):
        box_pb = db_pb2.GetBoxesInCategoryRequest(category=category)
        data = self.client.GetBoxesInCategory(box_pb)
        return MessageToDict(data)

    def getboxes_intimerange(self, start_time, end_time):
        box_pb = db_pb2.GetBoxesInTimeRangeRequest(start_time=start_time, end_time=end_time)
        data = self.client.GetBoxesInTimeRange(box_pb)
        return MessageToDict(data)

if __name__ == '__main__':
    DatabaseClient()