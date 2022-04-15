import asyncio
import grpc.aio
import todo_pb2
import todo_pb2_grpc


async def hello():
    print("Hola")
    await asyncio.sleep(1)
    print("Adios")

async def myfuture():
    print("En myfuture")
    await asyncio.sleep(1)


def get_todo(stub):
    todo = stub.CreateTodo(todo_pb2.TodoText(text="Hello World"))
    print(todo)

async def aget_todo(stub):
    print("En aget_todo")
    todo = await stub.CreateTodo(todo_pb2.TodoText(text="Hello World"))
    print("Received response")
    return todo.text

async def main():
    #task1 = asyncio.create_task(hello())
    #task2 = asyncio.create_task(hello())

    #await myfuture()
    #await task1
    #await task2
    channel=grpc.aio.insecure_channel('localhost:1234')
    r = await channel.channel_ready()
    print(f"Ready={r}")
    st = channel.get_state(try_to_connect=True)
    print(f"St={st}")
    stub = todo_pb2_grpc.TodoStub(channel)
    tasks = []
    for x in range(10):
        tasks.append(aget_todo(stub))
    L = await asyncio.gather(*tasks)
    print(L)
asyncio.run(main())