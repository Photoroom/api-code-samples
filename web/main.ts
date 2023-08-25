import { removeBackground } from './remove-background.js';

const fileInput = document.getElementById('fileInput') as HTMLInputElement;
const displayImage = document.getElementById('displayImage') as HTMLImageElement;

fileInput.addEventListener('change', async () => {
    const files = fileInput.files;
    if (files && files.length > 0) {
        try {
            const imageBlob = await removeBackground(files[0]);
            const objectURL = URL.createObjectURL(imageBlob);
            displayImage.src = objectURL;
        } catch (error) {
            console.error('Error:', error);
        }
    }
});
