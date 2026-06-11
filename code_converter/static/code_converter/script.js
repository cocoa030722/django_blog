document.getElementById('convertForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const inputLanguage = document.getElementById('inputLanguage').value;
    const cCode = document.getElementById('cCode').value;
    const outputLanguage = document.getElementById('outputLanguage').value;
    fetch('/code_converter/convert_code', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: new URLSearchParams({
            'inputLanguage': inputLanguage,
            'code': cCode,
            'outputLanguage': outputLanguage
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        document.getElementById('rustCode').value = data.extractedCode;
        document.getElementById('totalOutput').innerText = data.totalOutput;
    })
    .catch(error => {
        document.getElementById('rustCode').value = 'Error converting code: ' + error;
    });
});