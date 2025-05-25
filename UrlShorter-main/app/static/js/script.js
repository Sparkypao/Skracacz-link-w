async function getShortUrl(url, ttl) {
    try {
        const response = await fetch('/create_code', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                'url': url,
                'ttl': ttl,
            })
        });

        if (!response.ok) {
            throw new Error('Ошибка при создании короткой ссылки');
        }
        const link = response.json();

        return link;

    } catch (error) {
        console.error(error);
        return null;
    }
}

async function showUrl(url) {
    const shortUrl = document.getElementById('short-url');

    const qrContiner = document.getElementById('qr-container');
    qrContiner.style.display = 'none';

    if (!shortUrl) {
        
        console.log('shortUrl не найден ');
    }

    if (url) {
        shortUrl.textContent = url;
        shortUrl.href = url;
        shortUrl.style.display = 'block';
    } else {
        console.log('Ошибка получения короткого URL');
    }
}

async function showQr(url) {
    const qrCanvas = document.getElementById('qr-canvas');
    const qrContiner = document.getElementById('qr-container');
    
    const shortUrl = document.getElementById('short-url'); 

    shortUrl.style.display = 'none';

    qrContiner.style.display = 'block';

    QRCode.toCanvas(qrCanvas, url, {
        width: 256,
        margin: 2
    }, (error) => {
        if (error) {
            console.error('Ошибка генерации QR-кода:', error);
        }
    });
}


async function main() {
    const urlInputElement = document.getElementById('url-input');
    const ttlInputElement = document.getElementById('ttl-input');
    const linkButton = document.getElementById('link-button');
    const qrButton = document.getElementById('qr-button');
    const generateButton = document.getElementById('generate-button');

    let type = 'url' // url | qr

    generateButton.addEventListener('click', async () => {
        const url = urlInputElement.value.trim();
        const ttl = ttlInputElement.value.trim(); 
        if (!url) {
            return
        }

        if (type === 'url'){
            let result = undefined;
            if (!ttl) {
                result = await getShortUrl(url, 0);
            }
            else {
                result = await getShortUrl(url, ttl);
            }
            if (result) {
                await showUrl(result);
            }
            else {
                console.log(result);
            }
            linkButton.disabled = true
            
        }      
        else if (type === 'qr'){
            let result = await getShortUrl(url, ttl);
            if (result) {
                await showQr(result);
            }
            else {
                console.log(result);
            }
            qrButton.disabled = true
        }    
        else {
            alert('Incorect type!')
        }
    });

    linkButton.addEventListener('click', async () => {
        type = 'url';
    });

    qrButton.addEventListener('click', async () => {
        type = 'qr';
    });
}

document.addEventListener('DOMContentLoaded', main);
