from concurrent import futures
import grpc
from db_service import db_pb2_grpc
import time
from datetime import datetime
from dateutil.parser import parse
from google.protobuf.json_format import MessageToDict
from google.protobuf.timestamp_pb2 import Timestamp
from db.db_connection import collection
from db_service.db_pb2 import (
    Box,
    GetBoxRequest,
    GetBoxResponse,
    GetAllBoxesRequest,
    GetBoxesResponse,
    CreateBoxRequest,
    CreateBoxResponse,
    UpdateBoxRequest,
    UpdateBoxResponse,
    DeleteBoxRequest,
    DeleteBoxResponse,
    GetBoxesInCategoryRequest,
    GetBoxesInTimeRangeRequest
)

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class DatabaseServiceCRUD(db_pb2_grpc.DatabaseServiceServicer):
    def GetBox(self, request: GetBoxRequest, context):
        id = MessageToDict(request)["id"]
        data = collection.find_one({"_id": id})
        date_time = parse(data["created_at"])
        float_seconds = date_time.timestamp()
        seconds = int(float_seconds)
        nanos = int((float_seconds - seconds) * 10 ** 9)
        timestamp = Timestamp(seconds=seconds, nanos=nanos)
        response = Box(
            name=data["name"],
            id=data["_id"],
            price=data["price"],
            description=data["description"],
            category=data["category"],
            quantity=data["quantity"],
            created_at=timestamp
        )
        return GetBoxResponse(box=response, status=0)

    def GetBoxes(self, request: GetAllBoxesRequest, context):
        results = collection.find()
        boxes = []
        for result in results:
            if result is not None:
                date_time = parse(result["created_at"])
                float_seconds = date_time.timestamp()
                seconds = int(float_seconds)
                nanos = int((float_seconds - seconds) * 10 ** 9)
                timestamp = Timestamp(seconds=seconds, nanos=nanos)
                box_item = Box(
                    name=result["name"],
                    id=result["_id"],
                    price=result["price"],
                    description=result["description"],
                    category=result["category"],
                    quantity=result["quantity"],
                    created_at=timestamp
                )
                boxes.append(box_item)
        return GetBoxesResponse(box=boxes, status=0)

    def CreateBox(self, request: CreateBoxRequest, context):
        data = MessageToDict(request)["box"]
        collection.insert_one({
            "_id": data["id"],
            "name": data["name"],
            "price": data["price"],
            "description": data["description"],
            "category": data["category"],
            "quantity": data["quantity"],
            "created_at": data["createdAt"]
        })
        return CreateBoxResponse(status=0)

    def UpdateBox(self, request: UpdateBoxRequest, context):
        data = MessageToDict(request)["box"]
        id = data.pop("id")
        collection.update_one(
            {
                "_id": id
            },
            {
                "$set":
                    {
                        "name": data["name"],
                        "price": data["price"],
                        "description": data["description"],
                        "category": data["category"],
                        "quantity": data["quantity"]
                    }
            }
        )
        return UpdateBoxResponse(status=0)

    def DeleteBox(self, request: DeleteBoxRequest, context):
        id = MessageToDict(request)["id"]
        collection.delete_one({"_id": id})
        return DeleteBoxResponse(status=0)

    def GetBoxesInCategory(self, request: GetBoxesInCategoryRequest, context):
        cat = MessageToDict(request)["category"]
        results = collection.find({"category": cat})
        boxes = []
        for result in results:
            if result is not None:
                date_time = parse(result["created_at"])
                float_seconds = date_time.timestamp()
                seconds = int(float_seconds)
                nanos = int((float_seconds - seconds) * 10 ** 9)
                timestamp = Timestamp(seconds=seconds, nanos=nanos)
                box_item = Box(
                    name=result["name"],
                    id=result["_id"],
                    price=result["price"],
                    description=result["description"],
                    category=result["category"],
                    quantity=result["quantity"],
                    created_at=timestamp
                )
                boxes.append(box_item)
        return GetBoxesResponse(box=boxes, status=0)

    def GetBoxesInTimeRange(self, request: GetBoxesInTimeRangeRequest, context):
        start = request.start_time
        end = request.end_time
        start_obj = datetime.fromtimestamp(start.seconds + start.nanos / 1e9)
        end_obj = datetime.fromtimestamp(end.seconds + end.nanos / 1e9)
        results = collection.find({"created_at": {"$gte": start_obj, "$lte": end_obj}})
        boxes = []
        for result in results:
            if result is not None:
                box_item = Box(
                    name=result["name"],
                    id=result["_id"],
                    price=result["price"],
                    description=result["description"],
                    category=result["category"],
                    quantity=result["quantity"],
                    created_at=result["created_at"]
                )
                boxes.append(box_item)
        return GetBoxesResponse(box=boxes, status=0)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    db_pb2_grpc.add_DatabaseServiceServicer_to_server(DatabaseServiceCRUD(), server)
    server.add_insecure_port('localhost:50051')
    server.start()
    server.wait_for_termination(timeout=15)

    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)

    except KeyboardInterrupt:
        print("Keyboard Interrupt")
        server.stop(0)


if __name__ == '__main__':
    serve()
