const { isMainThread, parentPort, workerData } = require('worker_threads');

const { Web3 } = require('web3')

var url = "wss://sly-attentive-lambo.quiknode.pro/701a96b9a9b95a0ad8bac7c49dc9ccbec618108e";
var options = {
    timeout: 30000,
    clientConfig: {
        maxReceivedFrameSize: 100000000,
        maxReceivedMessageSize: 100000000,
    },
    reconnect: {
        auto: true,
        delay: 5000,
        maxAttempts: 15,
        onTimeout: false,
    },
};

var web3 = new Web3(new Web3.providers.WebsocketProvider(url, options));

class WaitingTransaction {
    constructor(txHash) {
        this.txHash = txHash;
        this.timestamp = Date.now();
        this.timesTried = 1;
    }
}

const waitingTransactions = []
const droppedTransactions = []

parentPort.on('message', (message) => {
    if (message.type == 'status') {
        parentPort.postMessage({ type: 'status', payload: { waiting: waitingTransactions, dropped: droppedTransactions } });
    } else {
        let txHash = message.tx;
        // console.log(`Received tx hash ${txHash} from main thread`);
        waitingTransactions.push(new WaitingTransaction(txHash));
    }
});

setTimeout(async () => {
    await startSweeping();
}, 5000);

async function startSweeping() {
    console.log(`Starting sweeping...`);
    setInterval(async () => {
        if (waitingTransactions.length > 0) {
            const wTx = waitingTransactions.shift()
            // console.log(`Retrying tx ${wTx.txHash}`);
            try {
                let tx = await web3.eth.getTransaction(wTx.txHash);
                console.log(tx)
                parentPort.postMessage({ type: 'tx', payload: { timestamp: wTx.timestamp, tx: tx } });
            } catch (err) {
                console.error('Error getting', wTx.txHash);
                wTx.timesTried++;
                if (wTx.timesTried > 1) {
                    droppedTransactions.push(wTx)
                } else {
                    waitingTransactions.push(wTx);
                }
            }
        }
    }, 500);
}
