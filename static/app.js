let code = CodeMirror(document.querySelector('#code'), {
    tabSize: 2,
    value: 'print("Hello World")',
    mode: 'python'
});

function submit() {
    // send post request to server at /api
    fetch('/api', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            code: code.getValue()
        })
    }).then(res => res.json())
        .then(data => {
            document.getElementById('output').innerHTML = data.message
        })
}