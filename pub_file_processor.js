const { spawn } = require('child_process')
const path = require('path')
const express = require('express')
const app = express()

app.post('/convert/:file', ({ body, params: { file } }, res) => {
    const pub_processor = spawn('python3', [
        path.resolve(__dirname, 'process_file.py'),
        '-n',
        file
    ])

    let stdout = '';
    let stderr = '';
    pub_processor.stdout.on('data', data => { stdout += data.toString() });
    pub_processor.stderr.on('data', data => { stderr += data.toString() });

    pub_processor.on('exit', (code) => {
        if (code > 0) {
            res.status(500).send('Processing publication failed')
        } else {
            res.send(stdout)
        }
    })

    pub_processor.stdin.write(body)
    pub_processor.stdin.end()
})

module.exports = {
    app,
    message: `Running publication file processor...`
}
