const removeBackground = require('./remove-background');

const imagePath = './test.jpg';
const savePath = './result.png';

removeBackground(imagePath, savePath)
    .then(message => {
        console.log(message);
    })
    .catch(error => {
        console.error('Error:', error);
    });
