const fs = require('node:fs/promises');
const { Worker, MessageChannel, MessagePort, isMainThread, parentPort } = require('worker_threads');
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

BigInt.prototype["toJSON"] = function() {
    return this.toString();
};

async function writeCapturedTransactions() {
    try {
        const content = JSON.stringify(capturedTransactions);
        await fs.writeFile('./mempool.txt', content);
    } catch (err) {
        console.log(err);
    }
}

const capturedTransactions = []
var web3 = new Web3(new Web3.providers.WebsocketProvider(url, options));

const worker = new Worker('./worker.js',
    options = {});

let revivedTransactions = 0;
worker.on('message', (message) => {
    if (message.type == 'status') {
        console.log(`Number of waiting txs: ${message.payload.waiting.length}`);
        console.log(`Number of dropped txs: ${message.payload.dropped.length}`);
        // console.log(message.payload.dropped.map((tx) => tx.txHash));
    } else {
        console.log(`Successful transaction from worker`);
        revivedTransactions++;
        console.log(`Number of revived txs: ${revivedTransactions}`);
        capturedTransactions.push(message.payload);
    }
    console.log(`Number of captured txs: ${capturedTransactions.length}`);
});

worker.on('error', (err) => {
    console.error(err);
});

var init = async function() {
    const subscription = await web3.eth.subscribe("pendingTransactions", (err, res) => {
        if (err) console.error(err);
    });
    setInterval(async () => {
        console.log(`Getting status...`);
        worker.postMessage({ type: 'status', tx: '' });
        console.log(`Writing captured transactions...`);
        await writeCapturedTransactions();
    }, 5000);
    subscription.on("data", (txHash) => {
        setTimeout(async () => {
            try {
                let tx = await web3.eth.getTransaction(txHash);
                capturedTransactions.push(
                    {
                        timestamp: Date.now(),
                        tx: tx
                    }
                );
            } catch (err) {
                worker.postMessage({ type: 'tx', tx: txHash });
            }
        });
    });
};

init();
