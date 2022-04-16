const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');
const packageDefinition = protoLoader.loadSync('todo.proto', {});

const grpcObject = grpc.loadPackageDefinition(packageDefinition);
const todo = grpcObject.todoPackage;

const server = new grpc.Server();

function sleep(ms) {
    return new Promise((resolve) => {
      setTimeout(resolve, ms);
    });
  }
async function createTodo(call, callback) {
  const todo = call.request;
  console.log(`Creating todo: and sleep ${todo.text}`);
  await sleep(5000);
  console.log("Sleep done");
  callback(null, {text: "TO-DO created"});
}

async function getLogData(call) {
    console.log(`Getting log data`);
    for (i=0; i<1000; i++) {
        await sleep(500);
        call.write({text: "Log data"});
    }
}

server.addService(todo.Todo.service, {
    createTodo: createTodo,
    getLogData: getLogData
});

server.bindAsync("0.0.0.0:1234", grpc.ServerCredentials.createInsecure(), function() {
    server.start();
    console.log("Server started");
});

